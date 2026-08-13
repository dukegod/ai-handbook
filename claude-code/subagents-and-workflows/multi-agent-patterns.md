---
title: 多 Agent 常见模式
description: 'Claude Code 多 agent 协作 7 种模式速查——Fan-out/Map-Reduce、判官团、对抗验证、流水线、循环到收敛、分治、协调者-worker，附 workflow 脚本骨架'
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  workflowsDocs: 'https://code.claude.com/docs/en/workflows'
  subagentsDocs: 'https://code.claude.com/docs/en/sub-agents'
  accessedAt: 2026-08-04
---

# 多 Agent 常见模式

> **TL;DR**：多 agent 不是乱生成——有 7 种成熟模式可套。本页给每种模式一句话本质 + 何时用 + workflow 脚本骨架，让你遇到任务能快速对号入座。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- 7 种多 agent 模式：Fan-out/Map-Reduce / 判官团 / 对抗验证 / 流水线 / 循环到收敛 / 分治 / 协调者-worker
- 每种模式的适用场景与陷阱
- 对应的 workflow 脚本骨架

## 前置

- 读过 [什么是 Subagent](./what-is-a-subagent) 和 [Workflow 编排](./workflow-orchestration)
- 会写基础 workflow 脚本

## 一、7 种模式速查

| 模式 | 一句话 | 何时用 |
| --- | --- | --- |
| **Fan-out / Map-Reduce** | 并发 N 个、合并 1 个 | 对很多 item 做同样操作 |
| **判官团（Judge Panel）** | N 个独立尝试 + 评分择优 | 解空间宽、单次迭代易次优 |
| **对抗验证（Adversarial Verify）** | 生成 → 独立反驳者质疑 | 挤掉似是而非的发现 |
| **流水线（Pipeline）** | 每 item 串过多 stage | 批量多步处理 |
| **循环到收敛（Loop-until-dry）** | 重复直到 K 轮无新发现 | 未知规模发现任务 |
| **分治（Divide & Conquer）** | 拆子任务 → 合并 | 任务可自然切分 |
| **协调者-worker（Coordinator）** | 主 agent 调度专职 worker | 多角色协作 |

---

## 二、Fan-out / Map-Reduce

**本质**：N 个 worker 并发处理 N 个 item → 1 个 synthesizer 合并。

```javascript
const files = await agent('列出 src/routes/ 下所有 .ts', { schema: FILES })

const audits = await parallel(files.map(f => () =>
  agent(`审计 ${f} 缺失的 auth 检查`, { label: f, schema: AUDIT })
))

const summary = await agent(
  `合并这些审计结果，去重排序：${JSON.stringify(audits)}`,
  { schema: SUMMARY }
)
```

**何时用**：对同质 item 重复操作（每文件审计、每端点测试、每模块文档）。

**陷阱**：item 间有依赖时别用——worker 彼此看不到。

## 三、判官团（Judge Panel）

**本质**：N 个 agent 从不同角度独立解 → 评分 → 从胜者综合。

```javascript
const drafts = await parallel([
  () => agent('从 MVP 优先角度起草方案'),
  () => agent('从风险优先角度起草方案'),
  () => agent('从用户体验角度起草方案'),
])

const scored = await parallel(drafts.map((d, i) => () =>
  agent(`给方案 ${i} 打分（0-10），评创新性/可行性/风险`, { schema: SCORE })
))

const winner = await agent(
  `从评分择优并融合其它方案亮点：${JSON.stringify({drafts, scored})}`
)
```

**何时用**：解空间宽（架构设计、方案选型）——单次迭代易陷次优。

**陷阱**：judge 与 drafter 用同一 prompt 会趋同；给 judge 明确评分维度。

## 四、对抗验证（Adversarial Verify）

**本质**：生成者产出 → 独立反驳者尝试证伪 → 多数表决存活。

```javascript
const findings = await pipeline(
  files,
  f => agent(`审计 ${f} 找 bug`, { label: `find:${f}` }),
)

const verified = await parallel(findings.flatMap(f => [
  () => agent(`从 correctness 角度反驳：${f.title}`),
  () => agent(`从 security 角度反驳：${f.title}`),
  () => agent(`从可复现性反驳：${f.title}`),
]))

// 多数反驳成立则丢弃
const confirmed = findings.filter((f, i) => {
  const votes = verified.slice(i*3, i*3+3)
  return votes.filter(v => !v.refuted).length >= 2
})
```

**何时用**：审计、安全 review——怕 plausible-but-wrong 的发现混过去。

**陷阱**：反驳者默认倾向「不反驳」会失效；prompt 里写「默认 refuted=true 如果不确定」。

## 五、流水线（Pipeline）

**本质**：每 item 独立串过所有 stage，无 barrier——item A 在 stage 3 时 item B 还在 stage 1。

```javascript
const results = await pipeline(
  files,
  f => agent(`读取 ${f}`),
  content => agent(`提取 ${content} 的 API 签名`, { schema: SIGS }),
  sigs => agent(`为 ${JSON.stringify(sigs)} 生成文档`, { schema: DOC })
)
```

**何时用**：批量多步处理、stage 间无跨 item 依赖。

**陷阱**：stage N 真需要全部 stage N-1 结果时别用 pipeline，用 `parallel` barrier。

## 六、循环到收敛（Loop-until-dry）

**本质**：重复生成直到连续 K 轮无新发现。

```javascript
const seen = new Set(), all = []
let dry = 0
while (dry < 2) {
  const found = await parallel(FINDERS.map(f => () =>
    agent(f.prompt, { schema: BUGS })))
  const fresh = found.flat().filter(b => !seen.has(key(b)))
  if (!fresh.length) { dry++; continue }
  dry = 0
  fresh.forEach(b => seen.add(key(b)))
  all.push(...fresh)
  log(`${all.length} 个，${dry}/2 轮无新发现`)
}
```

**何时用**：bug 扫描、issue 发现——不知道总量、要扫到穷尽。

**陷阱**：用 `seen` 去重而非 `confirmed`，否则被否的发现每轮复现、永不收敛。

## 七、分治（Divide & Conquer）

**本质**：拆成互斥子任务 → 各自完成 → 合并。

```javascript
const areas = ['auth', 'db', 'api', 'frontend', 'infra']
const reports = await parallel(areas.map(a => () =>
  agent(`只审 ${a} 模块的安全问题，不碰其它`, { label: a, schema: REPORT })
))
const merged = await agent(`合并 5 份模块报告为统一安全报告`, {
  schema: FINAL })
```

**何时用**：任务可沿自然边界切分（模块、目录、功能域）。

**陷阱**：子任务边界要互斥，否则重复劳动或遗漏。

## 八、协调者-worker（Coordinator）

**本质**：主 agent 当协调者，用 `Agent(worker, researcher)` 限制只能生成特定类型 worker。

```yaml
# .claude/agents/coordinator.md
---
name: coordinator
description: 协调多专职 agent 完成复杂任务
tools: Agent(researcher, implementer, reviewer), Read, Bash
---
你是协调者：拆任务 → 派 researcher 调研 → 派 implementer 实现
→ 派 reviewer 审查。不要自己写代码。
```

```javascript
// workflow 里
await agent('作为协调者，拆解并调度 researcher/implementer/reviewer 完成任务')
```

**何时用**：多角色协作（调研 / 实现 / 审查分离）、想固定流程。

**陷阱**：协调者 `tools` 漏写 `Agent(worker类型)` 就生成不了对应 worker。

---

## 模式选择决策

```text
任务有 N 个同质 item？
  ├─ 是 → Fan-out/Map-Reduce（要合并）或 Pipeline（多 stage）
  └─ 否 → 任务解空间宽？
            ├─ 是 → 判官团（择优）或 对抗验证（挤水分）
            └─ 否 → 未知规模发现？
                      ├─ 是 → 循环到收敛
                      └─ 否 → 可沿边界切分？
                                ├─ 是 → 分治
                                └─ 否 → 多角色协作？→ 协调者-worker
```

## 常见坑

**模式混用不清**——一个 workflow 里既 fan-out 又对抗验证又循环，难调试。一次用一个主模式，验证用独立 stage。

**worker 间隐式依赖**——fan-out 假设 item 独立；若 worker B 需要 worker A 的结果，改用 pipeline 或分治。

**对抗验证的反驳者太宽容**——默认 prompt 倾向「不反驳」。写「默认 refuted=true，除非有确凿证据」。

**循环不设 dry 上限**——无限循环到 1000 agent 上限。用 `dry < K`（通常 2）退出。

**判官团 judge 与 drafter 同 prompt**——趋同无意义。给 judge 明确评分维度 + 不同视角。

## 参考

- [Anthropic · Workflows](https://code.claude.com/docs/en/workflows)（访问于 2026-08-04）—— 模式来源
- [Anthropic · Create custom subagents](https://code.claude.com/docs/en/sub-agents)（访问于 2026-08-04）—— `Agent(type)` 限制

## 下一步

- 回顾 workflow 脚本机制 → [Workflow 编排](./workflow-orchestration)
- 看 subagent 配置 → [Agent 类型清单](./agent-types)

## 如果你想

- 看这些模式在真实场景的应用 → [Cookbook 实战案例](/cookbook/) 🚧
- 理解 workflow 限制 → [Workflow 编排 · 限制](./workflow-orchestration#六、限制)
- 回到章导读看全貌 → [Claude Code 章导读](../)

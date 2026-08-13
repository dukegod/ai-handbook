---
title: Workflow 编排
description: 'Claude Code 动态 Workflow——用 JavaScript 脚本确定性编排几十到上百个 subagent，meta 块 + agent/parallel/pipeline 三大 hook，适合代码审计、大规模迁移、交叉验证研究'
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  workflowsDocs: 'https://code.claude.com/docs/en/workflows'
  accessedAt: 2026-08-04
---

# Workflow 编排

> **TL;DR**：Workflow 是 Claude 写的一段 JavaScript 脚本——用 `agent()` / `parallel()` / `pipeline()` 编排几十到上百个 subagent，**确定性**控制流程（loop / branch / fan-out），中间结果存在脚本变量里不污染主 context。适合代码审计、大规模迁移、交叉验证研究。触发：prompt 里带 `ultracode` 关键词，或 `/effort ultracode` 让 Claude 自动规划。

⏱ 预计阅读时间：10 分钟

## 你能在这里学到

- Workflow 与 subagent / skill / agent team 的本质区别（谁持有计划）
- 三个脚本 hook：`agent()` / `parallel()` / `pipeline()`
- `meta` 块 + schema 结构化输出
- 5 种触发方式与审批机制
- 限制：16 并发 / 1000 agent 上限 / 无文件系统直接访问
- 何时该用 workflow、何时不该用

## 前置

- 读过 [什么是 Subagent](./what-is-a-subagent) 和 [Agent 类型清单](./agent-types)
- Claude Code v2.1.154+

## 一、Workflow 是什么

普通 subagent 委派：Claude **逐轮决定**下一步生成什么 agent，每个结果都进 context。

Workflow：把计划写进**代码**——脚本持有 loop / branch / fan-out，中间结果存在变量里，Claude context 只装最终答案。

| | Subagent | Skill | Agent Team | **Workflow** |
| --- | --- | --- | --- | --- |
| **谁决定下一步** | Claude 逐轮 | Claude 跟着 prompt | lead agent 逐轮 | **脚本** |
| **中间结果** | Claude context | Claude context | 共享 task list | **脚本变量** |
| **可复用** | worker 定义 | 指令 | team 定义 | **编排本身** |
| **规模** | 几个/轮 | 同 subagent | 几个长期 peer | **几十到几百/次** |
| **中断** | 重启轮次 | 重启轮次 | peer 继续跑 | **session 内可恢复** |

**核心价值**：把计划从 Claude 脑子挪到代码里——可读、可 rerun、可施加质量模式（如对抗式验证）。

## 二、三大脚本 Hook

```javascript
// 1. agent()：生成单个 subagent，返回其结果
const result = await agent('审读 auth.ts 的安全问题', {
  schema: { type: 'object', required: ['issues'], ... }
})

// 2. parallel()：并发跑多个 thunk，barrier 等全部完成
const all = await parallel([
  () => agent('研究 auth 模块'),
  () => agent('研究 db 模块'),
  () => agent('研究 api 模块'),
])

// 3. pipeline()：每个 item 串过所有 stage，无 barrier
const audited = await pipeline(
  files,
  file => agent(`审计 ${file}`),
  audit => agent(`验证 ${audit.findings}`)
)
```

| Hook | 语义 | 何时用 |
| --- | --- | --- |
| `agent()` | 单个 subagent | 一步任务 |
| `parallel()` | 并发 + barrier | 需要全部结果再合并 |
| `pipeline()` | 每 item 独立串 stages | 批量处理、无 barrier 更省时 |

**默认用 `pipeline()`**——只有真需要跨 item 合并时才用 `parallel()` 的 barrier。

## 三、`meta` 块

每个脚本必须以 `meta` 开头（纯字面量）：

```javascript
export const meta = {
  name: 'audit-routes',
  description: '审计所有 route handler 缺失的 auth 检查',
  phases: [
    { title: 'Scan', detail: '列出 src/routes/ 下所有 .ts' },
    { title: 'Audit', detail: '每文件一个 agent 审计' },
    { title: 'Verify', detail: '对抗式验证每个发现' },
  ],
}
```

`phases` 的 title 与 `phase('xxx')` 调用一一对应，决定进度视图分组。

## 四、Schema 结构化输出

`agent()` 加 `schema`（JSON Schema）→ 强制 subagent 调 StructuredOutput 工具，返回验证过的对象，无需解析：

```javascript
const found = await agent('列出 src/routes/ 下所有 .ts 文件', {
  schema: {
    type: 'object',
    required: ['files'],
    properties: {
      files: { type: 'array', items: { type: 'string' } }
    }
  }
})
// found.files 是 string[]
```

## 五、触发方式

| 方式 | 说明 |
| --- | --- |
| **`ultracode` 关键词** | prompt 里带 `ultracode`，Claude 为该任务写 workflow |
| **自然语言请求** | 「use a workflow」「run a workflow」同样触发 |
| **`/effort ultracode`** | session 级开启，每个实质任务都自动规划 workflow |
| **`/deep-research <问题>`** | 内置 workflow，多源交叉验证研究 |
| **保存的 workflow** | `/workflows` 选运行 → `s` 保存为 `/<name>` 命令 |

**`ultracode` = xhigh effort + 自动 workflow 编排**。session 内有效，新 session 重置。用 `/effort high` 退回常规。

**审批**：default / acceptEdits 模式每次运行都问；auto 模式首次问；bypass / `-p` / SDK 不问。workflow 内 subagent **始终跑 acceptEdits 模式** + 继承你的工具白名单。

## 六、限制

| 限制 | 值 | 原因 |
| --- | --- | --- |
| 并发 agent | 16（CPU 少则更少） | 本地资源 |
| 单次运行总 agent | 1000 | 防失控循环 |
| 运行中用户输入 | ❌ | 只有权限提示能暂停 |
| 脚本直接文件系统/shell | ❌ | agent 读写跑命令，脚本只协调 |
| 大 workflow 警告 | >25 agent 或 >150 万 token | v2.1.203+，advisory |

**无 mid-run 用户输入**：需要阶段间签字就拆成多个 workflow。

## 七、何时用 Workflow

✅ **适合**：

- 任务规模超出单 agent context 容量（如 500 文件迁移）
- 同一步骤要对很多 item 重复跑（每文件一个审计 agent）
- 需要对抗式验证（独立 agent 互相反驳后再报告）
- 多角度独立起草方案再择优
- 计划要可读、可 rerun、可 diff

❌ **不适合**：

- 单步任务（直接让 Claude 干更快）
- 需要频繁人工签字中断
- 任务规模小（几个 agent 就能搞定，用普通 subagent 委派）

## 八、典型 prompt 模板

```text
use a workflow to audit every route handler under src/routes/
for missing authentication checks, and adversarially verify
each finding before reporting it
```

```text
use a workflow to run npx tsc --noEmit and keep fixing the
reported errors until the type check passes or two rounds in
a row make no progress
```

```text
use a workflow to migrate every component under src/components/
from styled-components to Tailwind, working on each file in
its own isolated copy
```

## 九、管理与成本

- `/workflows` 看运行中 / 已完成的 workflow，可暂停 / 恢复 / 停止
- **恢复**：session 内可恢复，已完成 agent 走缓存；退出 Claude Code 后下次重新跑
- **成本**：多 agent = 多 token。大任务前先跑小切片估花费
- **size guideline**（`/config` 里设）：`small`(<5) / `medium`(<15，默认) / `large`(<50) / `unrestricted`
- **关掉**：`/config` 关 Dynamic workflows / `disableWorkflows: true` / `CLAUDE_CODE_DISABLE_WORKFLOWS=1`

## 常见坑

**fan-out 中途停止代价高**——恢复时未完成的 agent 及其后启动的 agent 全部重跑。扇出小 agent 比一个长 agent 更能保留进度。

**workflow 内 subagent 不继承你的 permissionMode**——始终 `acceptEdits`。想限制能力用 subagent 定义的 `tools` / `disallowedTools`。

**`ultracode` 关键词在非交互输入不触发**——`-p` / SDK / 定时任务 / webhook 里不生效（v2.1.210+）。只在交互式 prompt / IDE / Remote Control / 标记 `human` origin 的 SDK 输入里有效。

**把 workflow 当普通 subagent 用**——几个 agent 就能搞定的任务别上 workflow，写脚本 + 审批的额外开销不划算。

## 参考

- [Anthropic · Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)（访问于 2026-08-04）

## 下一步

- 常见多 agent 协作模式速查 → [多 Agent 常见模式](./multi-agent-patterns) 🚧
- 回顾 subagent 基础 → [什么是 Subagent](./what-is-a-subagent)

## 如果你想

- 看内置 workflow 实战 → 跑 `/deep-research <问题>` 体验完整 fan-out + 交叉验证
- 保存常用 workflow → `/workflows` 选运行 → 按 `s` 存到 `.claude/workflows/`
- 理解 effort 等级 → [模型选择 · effort](../basics/model-selection)

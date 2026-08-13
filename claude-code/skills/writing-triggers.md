---
title: 写好触发描述
description: 让 Claude 恰好在该用你 Skill 的时候用它——description 字段的写法、字符预算、命中率验证与三类失败模式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-29
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  bestPracticesDocs: 'https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices'
  officialDocs: 'https://code.claude.com/docs/en/skills'
  accessedAt: 2026-07-29
---

# 写好触发描述

> **TL;DR**：Claude 决定何时用你的 Skill **只看 `description`**（可选加 `when_to_use`）。写好这一栏就是 Skill 命中率的全部。四条铁律：**第三人称 + 说清做什么 + 说清何时用 + 塞关键触发词**。

⏱ 预计阅读时间：10 分钟

## 你能在这里学到

- 为什么 `description` 是触发的唯一开关（body 里内容再详尽也救不了它）
- 一个可以直接照抄的三段式模板
- 三类典型失败：太模糊 / 太具体 / 关键触发词缺失
- Anthropic 与 Claude Code 两层字符预算差异（1,024 vs 1,536）
- 用 should-trigger / should-not-trigger 清单验证命中率

## 前置

- 读过 [什么是 Skill](./what-is-a-skill) — 知道 description 常驻 / body 按需的两阶段加载
- 读过 [SKILL.md 规范](./skill-md-spec) — 熟悉完整 frontmatter 字段
- Claude Code v2.1.196+（`/context` 命令能看到 Skills 行截断后大小）

## 一、为什么只有 description 起作用

Claude Code 会话启动时**只把每个 skill 的 `description`**（可选加 `when_to_use`）**拼进 system prompt**。SKILL.md 的 body 只有在 Claude 真的决定「用这个 skill」之后才作为一条消息进入对话。

一个直接推论：**description 判 Claude 该不该来，body 决定来了之后做什么**。如果 description 让 Claude 认定「这题不归我管」，body 写得再详尽都没用——它根本读不到。

## 二、可以直接照抄的三段式

```yaml
description: <做什么>。用户 <什么场景 / 什么触发短语 / 什么文件类型> 时用。<可选：加更多关键词扩大命中面>
```

具体到 [什么是 Skill](./what-is-a-skill) 开头的 git diff 例子：

```yaml
description: 分析当前 git diff，用 2-3 条 bullet 概括改动并列出风险。用户说"这次改了啥"、"帮我写 commit message"、"diff 里有什么问题"时用。
```

三段的分工：

- **做什么**（动词 + 宾语）：Claude 一眼看清能力
- **何时用**：**这里最容易出错**——必须用**读者实际会说的话**（"这次改了啥"），而不是你脑子里的抽象类别（"版本控制辅助"）
- **可选关键词**：把用户可能提到的文件类型、专有名词、命令名塞进去

Anthropic Best Practices 强制要求**第三人称**：description 被注入 system prompt，第一 / 第二人称会让触发判定混乱。

```yaml
description: 分析 Excel 表格并生成图表  # 对
description: 我可以帮你分析 Excel        # 错
description: 你可以用这个分析 Excel      # 错
```

## 三、三个正例

**PDF 处理**：

```yaml
description: 从 PDF 提取文本与表格、填写表单、合并文档。用户提到 PDF / pdf 文件 / 表单 / 文档提取时用。
```

**Excel 分析**：

```yaml
description: 分析 Excel 表格、创建透视表、生成图表。用户处理 .xlsx / spreadsheet / 表格数据 / 数据透视时用。
```

**Commit 助手**：

```yaml
description: 分析 git diff 生成规范化 commit message（type(scope): subject 格式）。用户请求"帮我写提交信息 / commit message / 提交注释"或 review staged changes 时用。
```

三个都遵循：动词开头、明确边界、堆入用户会敲的原话。

## 四、三种反例

### 反例 1：太模糊

```yaml
description: 处理文档
description: 帮助数据分析
description: 做一些文件相关的事
```

问题：项目里可能有 30 个 skill 都是「处理文档 / 分析数据 / 文件操作」——Claude 一个都不会准确选中。**description 是让你从 100 个 skill 里被选中的门票**，越通用越选不中。

### 反例 2：太具体

```yaml
description: 分析 2026-07-25 之前提交的、位于 src/ 且不含 .test.tsx 后缀的 diff
```

问题：只在极窄场景才触发。用户说"看看最近改了啥"——静默错过。

**平衡点**：**触发场景写宽**（"任何 diff 分析请求"）**+ 内部约束写窄**（body 里再讲筛选规则）。

### 反例 3：缺关键触发词

```yaml
description: 生成变更摘要
```

问题：用户会说 "diff"、"改了啥"、"commit"、"提交信息"——一个都没写，Claude 抓不到关键词信号。

修正：**把用户可能敲的原话堆进去**：diff / commit / 改动 / staged changes / PR 描述……

## 五、字符预算：1,024 vs 1,536

两个数字都是真的，只是层不同。

| 层 | 限制 | 语义 |
| --- | --- | --- |
| Anthropic Skills 规范 | `description` 单字段 ≤ **1,024** | **硬校验**：超过被拒 |
| Claude Code 触发预算 | `description + when_to_use` 合计 ≤ **1,536** | **软预算**：超过被截断 |

实操建议：

- **≤ 200 字符**：随便写
- **200–1,024**：合规区间，主要信息全塞 `description`
- **1,024–1,536**：想再多加触发短语，用 `when_to_use` 独立字段
- **> 1,536**：一定被截断——**最重要的关键词放最前面**

Claude Code 里 `/context` 的 Skills 行显示的是**截断后**大小（v2.1.196+）。想给关键 skill 保留完整描述，可以在 `.claude/settings.local.json` 把不常用 skill 设 `"name-only"`，或调大 `skillListingBudgetFraction`（默认 `0.01` = context window 1%）。

## 六、验证：should-trigger / should-not-trigger

Anthropic 官方推荐**评估驱动开发**——先建测试样本，再回来调 description。建议在 skill 目录里维护 `TRIGGERS.md`：

```markdown
## should-trigger（这些提问必须触发）

- 帮我看看这次 diff 有啥问题
- 写个 commit message
- review 一下我 staged 的改动
- 这次改动风险在哪

## should-not-trigger（这些提问不该触发）

- 帮我改 bug（太泛，不属于 diff 分析）
- 看看 README（不是 diff）
- 跑测试（另有 skill）
```

用法：`claude -p '<提问>' --verbose` 起一个纯净会话（不污染当前上下文），观察 Claude 是否加载你这个 skill。命中率 < 80% 就回来加更多关键触发短语或收窄 `when_to_use`。

Anthropic 建议的迭代节奏：**用 Claude A 帮你改 description，用 Claude B（新会话）在真实任务里测**，观察 B 是否命中，把偏差带回 A。

## 七、常见坑

**description 写完就不管**——description 决定命中率，但**只有实际用过才知道命中率**。每周复盘该触发时没触发 / 不该触发时触发的案例，回来改这一栏。

**description 完全一致的两个 skill**——Claude 会随机挑一个。用 `when_to_use` 明确边界（"当仓库有未提交改动" vs "当有 staged 但未 commit"）。

**指望 description 里放执行步骤**：

```yaml
description: 分析 diff。步骤：1) 读文件 2) 归类 3) 输出 markdown ...  # 错
```

Claude 只用 description 判断"要不要用"，**不用它执行**。步骤放 body（触发后会加载）——把 description 里塞满步骤既超预算，又降低触发命中率。

**中英文触发短语只写一种**——如果你的用户既说中文也用英文，两种都写：

```yaml
description: 分析 diff … 用户说"改了啥" / "what changed" / "review diff" 时用。
```

**忘了 `disable-model-invocation` 场景**——设了 `disable-model-invocation: true` 的 skill，description 不常驻、也不参与自动触发判定。这时 description 只影响 `/skill` 补全列表——写清楚"做什么"够用。

## 参考

- [Anthropic · Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（访问于 2026-07-29）
- [Anthropic · Writing effective descriptions](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions)（访问于 2026-07-29）
- [Anthropic · Evaluation-driven Skill development](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#build-evaluations-first)（访问于 2026-07-29）
- [Claude Code · Skills 文档](https://code.claude.com/docs/en/skills)（访问于 2026-07-29）
- [SKILL.md 规范 · 字符预算](./skill-md-spec#六yaml-解析细节与常见坑) — 本站 description 截断与 skillListingBudgetFraction 详解

## 下一步

- 拿这些原则做出你自己的 skill → [写你的第一个 Skill](./custom-skill) 🚧
- 对比 skill / command / agent 各自的适用边界 → [Skill vs Command vs Agent](./skills-vs-commands-vs-agents) 🚧

## 如果你想

- 从原理层理解为什么 description 是唯一开关 → [什么是 Skill · 两阶段加载](./what-is-a-skill#两阶段加载为什么-skill-便宜)
- 看别人写的 description → [内置 Skills 一览](./built-in-skills) 🚧
- 深挖 frontmatter 全字段 → [SKILL.md 规范](./skill-md-spec)

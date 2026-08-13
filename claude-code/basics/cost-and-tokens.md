---
title: 成本与 Token 管理
description: 'Claude Code 的计费模型、`/usage` 命令、Prompt Caching TTL、9 条降本策略与长会话成本爬升的 5 大原因'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/costs'
  accessedAt: 2026-07-28
---

# 成本与 Token 管理

> **TL;DR**：Claude Code 按 API token 计费——一次 turn 会**重发完整历史**，所以长会话贵。**Prompt Caching 自动生效**（订阅计划 1 小时 TTL，API 5 分钟），命中的 token 成本降到约 10%。省钱三板斧：**选对模型 + 定期 `/clear` + Plan Mode**。

⏱ 预计阅读时间：10 分钟

## 你能在这里学到

- Claude Code 的计费模型与实际成本量级
- `/usage` 命令的输出与解读
- Prompt Caching 的 TTL 差异（订阅 vs API）
- 9 条具体降本策略
- 长会话 token 爬升的 5 大原因

## 前置

- 装好 Claude Code、跑过 [第一次对话](/getting-started/first-conversation)
- 理解 [心智模型 · 上下文里有什么](/getting-started/mental-model#三上下文里有什么)（每 turn 重发全上下文）

## 一、计费模型

Claude Code 按 **API token 消费**计费。三种付费路径：

| 路径 | 计费方式 | 参考 |
| --- | --- | --- |
| **订阅计划**（Pro / Max / Team / Enterprise） | Seat allowance（滚动 5 小时窗 + 每周窗） | [claude.com/pricing](https://claude.com/pricing) |
| **Anthropic Console（API）** | 按 token，workspace 级 spend limit | [Console usage](https://platform.claude.com/usage) |
| **Cloud provider**（Bedrock / Vertex / Foundry） | 按 token，你的 cloud 账单 | Cloud 计费控制台 |

**成本量级参考**（Anthropic 官方数据）：企业平均约 **$13/开发者/活跃日**，**$150–250/月**；90% 用户 < $30/活跃日。个人差异大，取决于模型选择、代码库大小、使用模式。

## 二、`/usage`：观测成本

会话内输入：

```text
/usage
```

Session block 输出示例：

```
Total cost:            $0.55
Total duration (API):  6m 20s
Total duration (wall): 6h 33m 10s
Total code changes:    0 lines added, 0 lines removed
Usage by model:
   claude-sonnet-4-6:  1.2k input, 5.3k output, 940.0k cache read, 50.0k cache write ($0.55)
```

**注意**：

- **`/usage` 是新的官方命令**——不是 `/cost`（后者是老版本）
- 订阅计划用户看到的美元是**本地按 list price 计算**的估算，可能与实际账单不同
- 每次 `/clear` 后 total 重置（v2.1.211+ 行为）
- 订阅计划的 `/usage` 还显示 skills / subagents / plugins / MCP 各自占比，按 `d` / `w` 切 24 小时 / 7 天视图

**`/usage-credits`**：订阅计划里超出 seat allowance 后请求额外用量（`/login` 用 claude.ai 订阅登录才可用）。

## 三、Prompt Caching 自动生效

Claude Code 每 turn 自动打 cache breakpoint——同样的上下文（system prompt / CLAUDE.md / 历史）第二次读**命中缓存的 token 成本降到约 10%**。

**Cache TTL 差异**（重要）：

| 场景 | TTL |
| --- | --- |
| **订阅计划**（Pro / Max / Team / Enterprise） | **1 小时** |
| **订阅计划 + 已启用 usage credits** | 5 分钟 |
| **API key / cloud provider** | **5 分钟**（默认） |

超过 TTL 后第一次消息就 **cache miss** ——长上下文会被完整重跑。所以**歇了半天再回来问一句话可能很贵**（下一节展开）。深入 API 层机制见 [Prompt Caching](/claude-capabilities/api/prompt-caching)。

## 四、9 条降本策略

按官方建议顺序：

### 1. 选对模型

- **Sonnet**：日常代码、80%+ 场景，性价比最好
- **Opus**：复杂架构决策、多步推理
- **Haiku**：简单 subagent 任务、快速批量

`/model` 会话内切换，`/config` 设默认。Subagent 单独指定：`model: haiku`。

### 2. 定期 `/clear`

切换到不相关任务时 `/clear` 开新对话——**旧上下文继续占每次 token**。想保留会话文件用 `/rename` 命名后再 clear，之后 `/resume <name>` 回来。

### 3. 自定义 `/compact`

```text
/compact focus on code samples and API usage
```

告诉 Claude compact 时**保留什么**。CLAUDE.md 里加一段 `# Compact instructions` 长期生效。

### 4. Plan Mode 先出方案

`Shift+Tab` 切到 Plan Mode，Claude 只读探索、出方案，避免「走错方向白跑」浪费。见 [Plan Mode](./plan-mode)。

### 5. 减少 MCP server 开销

- **优先 CLI 工具**（`gh` / `aws` / `gcloud` / `sentry-cli`）而非 MCP——CLI 不加 per-tool listing
- `/mcp` 看每个 server 的 token 花销，关掉不用的
- `/context` 看什么在占空间

### 6. Hook 预处理 / Skill 承载知识

- **Hook 过滤日志**：PreToolUse hook 把测试输出过滤到只有 `FAIL/ERROR` 行——上下文从数万 token 降到几百
- **Skill 承载领域知识**：让 Claude 按需加载 skill 里的架构说明，而不是探索代码库

### 7. CLAUDE.md 精简到 < 200 行

超长 CLAUDE.md 每次会话开头都消耗 token。把详细的 workflow 挪进 skills（按需加载）。见 [CLAUDE.md · 写作建议](./claude-md#七写作建议)。

### 8. 调整 Extended Thinking

**Thinking token 也是 output token**——默认启用时每次请求可能消耗**数万** token。降低方式：

- `/effort` 或 `/model` 里的 effort level 调低
- `/config` 里禁用 thinking（Fable 5 除外，它总是启用）
- 环境变量 `MAX_THINKING_TOKENS=8000`（对 fixed budget 模型）

简单任务不需要深度推理，可以关。

### 9. 派 Subagent 处理 verbose 输出

跑测试、抓文档、处理日志——这些 verbose 操作用 Subagent 隔离：输出留在 subagent 上下文，**只有摘要返回主会话**。见 [什么是 Subagent](/claude-code/subagents-and-workflows/what-is-a-subagent)。

## 五、长会话 token 爬升的 5 大原因

会话开了一天却发现 token 用量惊人？官方点名的 5 个原因：

1. **Long context**：每次消息 Claude Code 都发**完整对话历史**。开了一天后的「一句话」其实带着整天的历史
2. **Cache miss**：超过 [cache TTL](#三prompt-caching-自动生效) 后第一次消息就 miss，整个上下文重跑
3. **Scheduled tasks**：定时任务按 interval 触发，每次也发完整上下文
4. **Agent teammates**：每个活跃 teammate 都在独立消耗 token 直到退出。**agent team 大约用 7x 于标准会话**
5. **`/compact` 本身也贵**：compact 要读完当前上下文才能摘要——**大 context 的 compact 本身就是大请求**。想彻底重开用 `/clear`（0 成本）

**订阅计划**的 `/usage` 会自动标记占比 ≥ 10% 的行为（long context / cache miss 等），每条附具体缓解建议。

## 六、后台 token 消耗

即使空闲，Claude Code 也可能消耗少量 token：

- **对话摘要**：为 `claude --resume` 准备的后台摘要
- **命令处理**：如 `/usage` 会发请求查状态

通常单会话 **< $0.04**——不用特别在意。

## 常见坑

**忘了切模型，Opus 跑全天**

`/model` 或 `/config` 里设默认。Sonnet 应付 80%+ 场景。

**`--continue` 一直往上叠会话**

每次都在旧会话上继续，token 指数上升。切任务时果断 `/clear`。

**大文件让 Claude 全读**

Claude 遇陌生大文件容易 `Read` 全文——用 Grep / Glob **先定位再读**，或明确要求读文件片段。

**Batch API 在 Claude Code 里不适用**

[Batch API](/claude-capabilities/api/message-batches) 是 API 侧的**异步**折扣（50% off，24h 窗口）。Claude Code 是交互式，不适用——想批量降本走 API 层。

## 参考

- [Anthropic Docs · Manage costs effectively](https://code.claude.com/docs/en/costs)（访问于 2026-07-28）
- [Anthropic Docs · Prompt caching](https://code.claude.com/docs/en/prompt-caching)（访问于 2026-07-28）
- [Anthropic Docs · Analytics](https://code.claude.com/docs/en/analytics)（访问于 2026-07-28）
- [Anthropic Docs · Model configuration](https://code.claude.com/docs/en/model-config)（访问于 2026-07-28）

## 下一步

- 选对模型是省钱头号杠杆 → [模型选择](./model-selection)

## 如果你想

- 深入 Plan Mode → [Plan Mode](./plan-mode)
- 学 API 层 Prompt Caching → [Prompt Caching](/claude-capabilities/api/prompt-caching)
- 学 Batch API 批量降本 → [Message Batches](/claude-capabilities/api/message-batches)
- 派 Subagent 隔离 verbose 操作 → [什么是 Subagent](/claude-code/subagents-and-workflows/what-is-a-subagent)

---
title: Claude in Slack
description: Slack 集成——DM / Channel 调用 Claude / @claude / 4 实战模式 + 4 坑
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  slackApp: 'https://slack.com/apps/A04KGS7N95S-claude'
  accessedAt: 2026-08-07
---

# Claude in Slack

> **TL;DR**：Claude 官方 Slack App——在 Slack DM 或 Channel 里**@claude 提问**或**私聊**。**适合团队协作 / 实时问答 / 知识库接入**。Workspace admin 安装后全员可用。

⏱ 预计阅读时间：3 分钟

## 一、安装

Workspace admin 在 [Slack App Directory](https://slack.com/apps/A04KGS7N95S-claude) 安装 → 授权。

## 二、4 个核心能力

### 1. 私聊（DM）

```text
在 Slack 左侧找到 "Claude" → 私聊
→ 跟普通 Claude.ai 一样
```

### 2. Channel 内 @claude

```text
#engineering channel:
"@claude 这个 PR 有什么问题？"
"@claude 总结下这个 thread"
"@claude 帮我写 Slack 消息回复客户"
```

### 3. Thread 内回复

```text
thread 内 @claude
→ Claude 看整个 thread context
→ 给出综合回复
```

### 4. 文件 + 链接理解

```text
上传 PDF / 代码到 Slack
@claude 总结
@claude 解释这段代码
```

## 三、3 个实战模式

### 模式 1：实时技术问答

```text
#engineering channel:
"@claude 这段报错什么意思？"
[粘贴 stack trace]
→ Claude 解读 + 给建议
```

### 模式 2：会议纪要

```text
thread 里有 30 条讨论
"@claude 总结 thread 决策点"
→ 3 段总结 + 待办
```

### 模式 3：客户支持

```text
#support channel:
"@claude 给客户写回复：订单 #1234 延迟原因..."
→ 草稿（人审后发）
```

## 四、4 个常见坑

**1. 数据进 Slack = 数据进 Anthropic**

```text
# Slack 频道内容 = Anthropic 看到的内容
# 敏感信息别在公开频道 @claude
```

**2. 长 context 受限**

```text
# Slack thread 50+ 条消息
# Claude context 有限 → 早期消息可能丢
```

**3. 多轮对话断裂**

```text
# Channel 消息流被刷掉 → Claude 看不到之前对话
# 复杂任务用 DM 或 Claude.ai
```

**4. 权限混乱**

```text
# Workspace admin 能看所有 @claude 记录
# 敏感内部讨论 → 用 DM（private）
```

## 五、与 claude.ai 对比

| 维度 | Claude in Slack | claude.ai |
| --- | --- | --- |
| 入口 | Slack | 浏览器 |
| 团队协作 | ✅（频道共享） | ❌（个人 / project） |
| 实时问答 | ✅ | ❌ |
| 长对话 | ❌ | ✅ |
| Project + KB | ❌ | ✅ |
| 数据安全 | ⚠️（Slack 第三方） | ✅ |

**何时用 Claude in Slack**：
- 团队频道（#eng / #support）
- 实时技术问答
- Slack workflow 集成

**何时用 claude.ai**：
- 个人 / 长对话
- Project + Knowledge base
- 敏感数据

## 参考

- [Claude in Slack](https://slack.com/apps/A04KGS7N95S-claude)
- [Claude.ai](/claude-capabilities/surfaces/claude-ai)
- [安全](/claude-capabilities/agentic/safety)

## 下一步

- 切到桌面 → [Desktop](/claude-capabilities/surfaces/desktop-app)
- 切到 API → [Messages API](/claude-capabilities/api/messages)
- v0.3.3 收官 → [Claude.ai](/claude-capabilities/surfaces/claude-ai)

## 如果你想

- 数据安全 → [安全 · 数据外泄](/claude-capabilities/agentic/safety#风险-3数据外泄)
- 切到 Claude Code → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

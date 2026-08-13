---
title: Managed Agents
description: Anthropic 完全托管的 agent 服务；不自建部署、关注业务逻辑即可
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  managedAgents: 'https://docs.claude.com/en/docs/build-with-claude/managed-agents'
  accessedAt: 2026-08-07
---

# Managed Agents

> **TL;DR**：Managed Agents 是 Anthropic **完全托管的 agent 服务**——你不部署 agent 服务，只调 API；agent runtime / 调度 / 扩缩容 / 监控全由 Anthropic 管。**适合不想自建运维的团队**。

⏱ 预计阅读时间：3 分钟

## 一、与 Agent SDK 的区别

| 维度 | [Agent SDK](/claude-capabilities/sdk/agent-sdk) | **Managed Agents** |
| --- | --- | --- |
| **部署** | 你部署 | Anthropic 部署 |
| **runtime** | 你管 | Anthropic 管 |
| **扩缩容** | 你配 | 自动 |
| **监控** | 自己接 | 内置 |
| **成本模型** | pay-per-token | pay-per-run |
| **可控性** | 高 | 中（抽象更多） |
| **适合** | 自建 SaaS / 数据敏感 | 快速上线 / 不想运维 |

**何时用 Managed Agents**：
- 快速 MVP / 不自建运维
- 流量波动大（扩缩容省心）
- 团队 < 3 人没运维

**何时用 Agent SDK**：
- 数据敏感（必须自建）
- 需深度定制 agent 行为
- 已有 K8s 平台

## 二、Managed Agents 实战

```python
from anthropic_managed_agents import ManagedAgent

# 1. 定义 agent（上传代码 / 配置 tools）
agent = ManagedAgent.create(
    name="support-bot",
    model="claude-sonnet-5-...",
    system="你是客服助手。",
    tools=["jira_search", "slack_notify"],
    code_source="./support_bot/",   # 上传代码
)

# 2. 调用（HTTP / Webhook / 定时任务）
result = agent.run(
    input={"ticket_id": "TICKET-1234"},
    webhook="https://my-app.com/callback",
)
print(result.output)
```

## 三、3 个实战场景

### 1. 客服自动化工单

```python
agent = ManagedAgent.create(
    name="support-bot",
    model="claude-sonnet-5-...",
    tools=["jira_search", "slack_notify", "kb_search"],
)

# 新工单触发（Jira webhook）
agent.run(input={"ticket_id": "TICKET-1234"})
# → agent 查 JIRA、查知识库、Slack 通知
```

### 2. 定时数据 ETL

```python
# 每天 02:00 跑
agent = ManagedAgent.create(
    name="daily-etl",
    schedule="0 2 * * *",
    tools=["s3_read", "bigquery_write", "transform"],
)
```

### 3. 长链异步任务

```python
# 提交后 30 分钟再查结果
run = agent.run_async(input={"task": "..."})
# 30 分钟后
result = agent.get_run(run.id)
```

## 四、4 个常见坑

**1. 数据出域**

```python
# ❌ agent 跑在 Anthropic 服务端——你的数据离开你的服务器
# ✅ 敏感数据用 Agent SDK 自建
```

**2. 工具不兼容**

```python
# Managed Agents 的 tools 列表是**白名单**——不是所有 Python 包都能用
# ✅ 用前查 supported tools
```

**3. 调试难**

```python
# 抽象多，调试 trace 难
# ✅ 用 Managed Agents 自带 observability + 日志导出
```

**4. pay-per-run 成本不可控**

```python
# 单次 run 可能跑 100 步 → 账单爆炸
# ✅ 设置 max_steps + cost_alert
agent = ManagedAgent.create(max_steps=20, cost_alert=10.0, ...)
```

## 参考

- [Anthropic Docs · Managed Agents](https://docs.claude.com/en/docs/build-with-claude/managed-agents)（访问于 2026-08-07）
- [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- [Tool Runner](/claude-capabilities/sdk/tool-runner)
- [SDK 概览](/claude-capabilities/sdk/overview)

## 下一步

- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
- Sub-agent 编排 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

## 如果你想

- 数据敏感 → [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- 扩缩容模式 → [Managed Agents · 实战场景](#三3-个实战场景)

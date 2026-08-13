---
title: Agent SDK
description: 状态化多步 agent 高层封装；memory / tool 调度 / sub-agent 实战
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  agentSdk: 'https://github.com/anthropics/claude-agent-sdk-python'
  accessedAt: 2026-08-07
---

# Agent SDK

> **TL;DR**：`claude-agent-sdk` 是**状态化多步 agent 的高层封装**——相比 [Python SDK](/claude-capabilities/sdk/python-sdk) 手写循环，它内置 memory / tool 调度 / sub-agent 管理。**适合 10+ tool call 的长链任务**。

⏱ 预计阅读时间：5 分钟

## 一、安装

```bash
pip install claude-agent-sdk
```

> 注意：包名是 `claude-agent-sdk`（不是 `claude-agent`）。

## 二、与 Python SDK 的关系

```
Python SDK
  ↓ client.messages.create() 一次调用
  ↓ 你手写 50 行循环代码（messages / tools / stop_reason）
  
Agent SDK
  ↓ agent.run("...") 一次调用
  ↓ 内部封装：memory / tool 调度 / sub-agent / retry / checkpoint
```

**何时用 Agent SDK vs Python SDK**：

| 场景 | 用 | 原因 |
| --- | :---: | --- |
| 简单 API 调用 | **Python SDK** | Agent SDK 太重 |
| **10+ tool call 长链** | **Agent SDK** | 内置 memory / sub-agent |
| 需 sub-agent 编排 | **Agent SDK** | 内置 sub-agent 调度 |
| 需 checkpoint / retry | **Agent SDK** | 内置 |
| 完全自管流程 | **Python SDK** | Agent SDK 抽象太多 |

## 三、3 个实战模式

### 模式 1：单 agent 跑多步任务

```python
from claude_agent_sdk import Agent

agent = Agent(
    model="claude-sonnet-5-...",
    system="你是研究助手，能查 Wikipedia / 算数学 / 写报告。",
    tools=["wikipedia", "calculator", "file_write"],
)

result = agent.run("研究一下 transformer 架构的演进，写一份 500 字总结到 /tmp/report.md")
print(result.final_text)
```

### 模式 2：多 agent 编排

```python
from claude_agent_sdk import Agent, Team

researcher = Agent(
    name="researcher",
    model="claude-sonnet-5-...",
    system="你专做研究。",
    tools=["wikipedia", "web_search"],
)

writer = Agent(
    name="writer",
    model="claude-opus-5-...",
    system="你专做写作。",
    tools=["file_write"],
)

team = Team(
    agents=[researcher, writer],
    workflow="researcher 调研 → writer 写报告",
)

result = team.run("研究 transformer 架构，写报告")
```

### 模式 3：带 memory 的对话

```python
agent = Agent(
    model="claude-sonnet-5-...",
    system="你是个人助理，记住用户偏好。",
    tools=["user_memory"],
    memory_path="/tmp/agent_memory.json",   # 跨 session 持久化
)

# 第 1 轮
agent.run("我喜欢简洁的 Python 代码")

# 第 2 轮（新 session）— 仍记得
agent.run("写个 list comprehension 示例")
```

## 四、5 个常见坑

**1. 简单任务用 Agent SDK**

```python
# ❌ Agent SDK 做 1 步调用
agent = Agent(model="claude-sonnet-5-...")
result = agent.run("Hello")    # 太重

# ✅ Python SDK
client.messages.create(model="claude-sonnet-5-...", max_tokens=1024, messages=[...])
```

**2. memory 路径冲突**

```python
# ❌ 多个 agent 共享同一 memory 路径
agent_a = Agent(memory_path="/tmp/mem.json", ...)
agent_b = Agent(memory_path="/tmp/mem.json", ...)   # 互相覆盖

# ✅ 各自独立
agent_a = Agent(memory_path="/tmp/mem_a.json", ...)
agent_b = Agent(memory_path="/tmp/mem_b.json", ...)
```

**3. sub-agent 无限递归**

```python
# ❌ agent_a 调度 agent_b，agent_b 又调度 agent_a
# → 无限循环

# ✅ 明确 workflow（无环 DAG）
workflow = "a → b → c"
```

**4. 工具列表太大（> 20）**

Claude 注意力分散——**精简到 5-10 个最常用**。

**5. 没用 checkpoint**

```python
# ❌ 50 步 agent 跑到 49 步崩了——全部重来

# ✅ 启用 checkpoint
agent = Agent(checkpoint_interval=10, ...)
```

## 参考

- [Anthropic Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)（访问于 2026-08-07）
- [Python SDK](/claude-capabilities/sdk/python-sdk)
- [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)
- [Tool Use API](/claude-capabilities/api/tool-use)
- [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- [SDK 概览](/claude-capabilities/sdk/overview)

## 下一步

- 隔离 tool → [Tool Runner](/claude-capabilities/sdk/tool-runner)
- 托管 agent → [Managed Agents](/claude-capabilities/sdk/managed-agents)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

## 如果你想

- 多 agent 编排模式 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- 长链 agent 实战 → [Opus 5 vs Sonnet 5 · 选型](/claude-capabilities/models/opus#四opus-5-vs-sonnet-5实测选型)

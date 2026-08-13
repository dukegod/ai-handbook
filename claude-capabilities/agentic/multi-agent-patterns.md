---
title: 多 Agent 模式
description: 5 种多 agent 协作模式——supervisor / peer / pipeline / debate / cast；3 维决策表
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  multiAgent: 'https://docs.claude.com/en/docs/agents-and-tools/multi-agent-systems'
  accessedAt: 2026-08-07
---

# 多 Agent 模式

> **TL;DR**：多 agent 系统 = **多个 Claude 实例协作**完成复杂任务。**5 种模式**：supervisor（主从）/ peer（对等）/ pipeline（流水线）/ debate（辩论）/ cast（角色扮演）。选型核心是"任务是否可分解 + 是否需要协商"。

⏱ 预计阅读时间：5 分钟

## 一、为什么需要多 Agent

```
单 agent 问题：
  - 1 个 context 装不下 100 步任务
  - 1 个 prompt 装不下 10 个角色
  - 1 个 model 跑所有任务 = 慢 + 贵

多 agent 解决：
  - 每个 agent 独立的 context
  - 每个 agent 专注自己的角色
  - 主 agent 用 Sonnet 5、sub agent 用 Haiku 4.5 = 省钱
```

## 二、5 种模式

### 模式 1：Supervisor（主从）⭐⭐⭐⭐⭐

```
        Supervisor
       /    |    \
    A1    A2    A3    ← sub agents
```

**特点**：
- 1 个主 agent + N 个 sub agent
- 主 agent 决策、调度、汇总
- sub agent 各自执行任务

**实战**：
```python
# Claude Code 内置 sub agent
subagent_type="general-purpose"  # / Explore / Plan subagents
```

详见 [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)。

**适用**：90% 场景（**默认模式**）。

### 模式 2：Peer（对等）⭐⭐

```
   A1 ↔ A2
    ↓    ↓
   A3 ↔ A4
```

**特点**：
- 所有 agent 对等
- 互相通信、协商
- 没有明确"主"

**实战**：研究 / 调研场景——多个 agent 各自探索，共享发现。

**适用**：协作型任务（不常见、调试难）。

### 模式 3：Pipeline（流水线）⭐⭐⭐

```
A1 → A2 → A3 → A4 → output
```

**特点**：
- 串行：每个 agent 处理后传给下一个
- 适合**有明确步骤**的任务

**实战**：代码审查流水线
```
A1: 读 diff → 静态分析
A2: 找 bug
A3: 找安全问题
A4: 综合写报告
```

**适用**：多步处理（review、ETL、build pipeline）。

### 模式 4：Debate（辩论）⭐⭐

```
   A1 (支持) ↔ A2 (反对)
        ↓
    最终答案
```

**特点**：
- 多个 agent 给不同观点
- 互相挑战 / 反方观点
- 取一致或多数

**实战**：
```python
# 决策时：pro agent vs con agent → 取平衡
pro = Agent(system="支持这个方案，给 3 个理由")
con = Agent(system="反对这个方案，给 3 个理由")
final = Agent(system="综合 pro / con 给最终建议")
```

**适用**：高价值决策（架构选型、方案 review）。

**成本**：3x 起步（多个 agent 各跑一次）。

### 模式 5：Cast（角色扮演）⭐⭐⭐

```
   PM    Dev    QA    Designer    ← 4 个角色
   ↓      ↓     ↓       ↓
   共同推进一个项目
```

**特点**：
- 每个 agent 模拟一个角色
- 角色之间对话
- 模拟真实团队

**实战**：模拟用户访谈、code review 委员会、设计评审。

**适用**：模拟 / 演练 / 培训场景。

## 三、3 维选型表

| 维度 | Supervisor | Peer | Pipeline | Debate | Cast |
| --- | :---: | :---: | :---: | :---: | :---: |
| **可分解性** | 高 | 中 | 高 | 中 | 中 |
| **需要协商** | 否 | 是 | 否 | 是 | 是 |
| **成本倍数** | 1.5-2x | 2-3x | 1.5-2x | 2-3x | 2-4x |
| **调试难度** | 中 | 高 | 中 | 高 | 高 |
| **实战常用度** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

## 四、Supervisor 实战模板

```python
# 主 agent
supervisor = Agent(
    model="claude-sonnet-5-...",
    system="你是 supervisor。决定下一步调哪个 sub agent。",
    tools=["task"],
)

# Sub agent A
researcher = Agent(
    model="claude-sonnet-5-...",
    system="你是研究员。查资料 + 总结。",
    tools=["web_search", "wikipedia"],
)

# Sub agent B
coder = Agent(
    model="claude-sonnet-5-...",
    system="你是工程师。写代码 + 跑测试。",
    tools=["file_read", "file_write", "bash"],
)

# Sub agent C
reviewer = Agent(
    model="claude-opus-5-...",
    system="你是审查员。审查代码 + 给改进建议。",
)

# 主 agent 通过 task 工具调 sub agents
# （Agent SDK 自动管理）
```

## 五、4 个常见坑

**1. Sub agent 太泛**

```python
# ❌ 1 个 sub agent 做所有事
sub = Agent(tools="*")

# ✅ 每个 sub agent 专一
researcher = Agent(tools=["web_search", "wikipedia"])
coder = Agent(tools=["file_read", "file_write"])
```

**2. 无循环检测**

```python
# ❌ A1 → A2 → A1 → A2 ... 死循环
# ✅ 限 max_turns + 检测重复状态
```

**3. Context 不共享**

```python
# sub agent 不知道主 agent 的状态
# ✅ 显式传 context（sub.agent_run(context=...))
```

**4. 成本失控**

```python
# 1 个 supervisor + 5 个 sub + 50 步 = 50*5 = 250 个 messages
# 成本 = 单 agent 50 倍
# ✅ 关键决策用 Opus、Sprint 任务用 Haiku
```

## 参考

- [Anthropic Docs · Multi-Agent Systems](https://docs.claude.com/en/docs/agents-and-tools/multi-agent-systems)（访问于 2026-08-07）
- [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- [Computer Use](/claude-capabilities/agentic/computer-use)

## 下一步

- 安全实践 → [安全](/claude-capabilities/agentic/safety)
- 切到 SDK → [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- 切到 Claude Code → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

## 如果你想

- Computer Use 协同 → [Computer Use](/claude-capabilities/agentic/computer-use)
- Prompt 优化 → [深度提示工程](/claude-capabilities/prompting/best-practices)

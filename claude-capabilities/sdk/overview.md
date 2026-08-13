---
title: SDK 概览
description: API/SDK 视角的 7 个 Claude 客户端封装总览；选型决策表 + examples/ 仓库骨架规划
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  pythonSdk: 'https://github.com/anthropics/anthropic-sdk-python'
  typescriptSdk: 'https://github.com/anthropics/anthropic-sdk-typescript'
  agentSdk: 'https://github.com/anthropics/claude-agent-sdk-python'
  accessedAt: 2026-08-07
---

# SDK 概览

> **TL;DR**：Anthropic 提供 **7 个 SDK**——3 个官方（Python / TypeScript / Agent SDK）+ 4 个高层封装（Tool Runner / Managed Agents / Claude Code SDK / overview）。SDK 是 [Messages API](/claude-capabilities/api/messages) 的**客户端封装**——选型核心是"你建什么 + 团队用什么语言"。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 7 个 SDK 的定位、适用场景、依赖关系
- 按"你要建什么"和"团队技术栈"双维度选型决策表
- examples/ 仓库骨架规划
- 与 [Messages API](/claude-capabilities/api/messages) 的关系

## 一、SDK 全景图

```
┌─────────────────────────────────────────────────────┐
│ 你的应用                                            │
├─────────────────────────────────────────────────────┤
│ 高层封装：构建 agent / workflow                     │
│   ├─ Agent SDK          ← 状态化多步 agent          │
│   ├─ Tool Runner        ← 单 tool 执行沙箱          │
│   ├─ Managed Agents     ← 完全托管（无需部署）      │
│   └─ Claude Code SDK    ← 把 Claude Code 嵌入应用    │
├─────────────────────────────────────────────────────┤
│ 基础 SDK：HTTP 客户端                                │
│   ├─ Python SDK         ← 同步 + async + streaming  │
│   └─ TypeScript SDK     ← Node + Deno + 浏览器      │
├─────────────────────────────────────────────────────┤
│ Messages API（HTTP 协议层）                          │
└─────────────────────────────────────────────────────┘
```

## 二、3 个官方 SDK

### 1. Python SDK（`anthropic`）

```bash
pip install anthropic
```

**核心特性**：
- 同步 + async 双接口
- Streaming、Tool Use、Prompt Caching 全支持
- 与 Pydantic 集成（structured outputs）
- 类型注解完整

详见 [Python SDK](/claude-capabilities/sdk/python-sdk)。

### 2. TypeScript SDK（`@anthropic-ai/sdk`）

```bash
npm install @anthropic-ai/sdk
```

**核心特性**：
- Node / Deno / 现代浏览器（带 polyfill）
- Streaming、Tool Use、Prompt Caching 全支持
- 类型安全（TypeScript 5+）

详见 [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)。

### 3. Agent SDK（`claude-agent-sdk-python`）

```bash
pip install claude-agent-sdk
```

**核心特性**：
- **状态化多步 agent**（高层抽象）
- 内置 memory / tool 调度 / sub-agent
- 与 Python SDK 共享底层（messages.create）

详见 [Agent SDK](/claude-capabilities/sdk/agent-sdk)。

## 三、4 个高层封装

| 封装 | 何时用 | 状态 |
| --- | --- | --- |
| [Tool Runner](/claude-capabilities/sdk/tool-runner) | 单一 tool 的隔离执行沙箱 | 实验性 |
| [Managed Agents](/claude-capabilities/sdk/managed-agents) | 不自建部署的 agent 托管服务 | 公开 beta |
| [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk) | 把 Claude Code 作为库嵌入应用 | GA |

## 四、按"你要建什么"选型

| 你要建什么 | 首选 | 备选 |
| --- | --- | --- |
| **简单 API 调用**（脚本 / 工具） | [Python SDK](/claude-capabilities/sdk/python-sdk) 或 [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk) | 直接 HTTP（curl） |
| **多步 agent**（10+ tool calls） | [Agent SDK](/claude-capabilities/sdk/agent-sdk) | Python SDK + 手写循环 |
| **生成应用 + Claude Code 内置能力** | [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk) | Agent SDK + 自建子 agent |
| **托管 agent**（不想自建部署） | [Managed Agents](/claude-capabilities/sdk/managed-agents) | Agent SDK + 自建服务 |
| **隔离 tool 执行**（不可信 code） | [Tool Runner](/claude-capabilities/sdk/tool-runner) | 容器 + 自管沙箱 |
| **流式 UI**（聊天 / typing） | [Python SDK streaming](/claude-capabilities/sdk/python-sdk#streaming) | [TypeScript SDK streaming](/claude-capabilities/sdk/typescript-sdk#streaming) |
| **结构化输出**（JSON） | [Python SDK tool_use](/claude-capabilities/sdk/python-sdk#structured-outputs) | [TypeScript SDK tool_use](/claude-capabilities/sdk/typescript-sdk#structured-outputs) |

## 五、按"团队技术栈"选型

| 团队 | 首选 |
| --- | --- |
| **后端 Python**（FastAPI / Django） | [Python SDK](/claude-capabilities/sdk/python-sdk) |
| **前端 / Node**（Next.js / Express） | [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk) |
| **数据科学 / ML** | [Python SDK](/claude-capabilities/sdk/python-sdk) |
| **CLI 工具** | TypeScript SDK（Node 生态分发容易） |
| **混合栈** | 各自选 + 共用 Messages API |

## 六、SDK 与 Messages API 的关系

```
SDK 内部都调 Messages API
  ├─ Python SDK: client.messages.create() → POST /v1/messages
  ├─ TypeScript SDK: client.messages.create() → POST /v1/messages
  └─ Agent SDK: 内部多次 client.messages.create() 形成多步循环
```

**学完 Messages API 再看 SDK 就像看"魔术揭秘"**——SDK 内部都是 messages.create()。

详见 [Messages API](/claude-capabilities/api/messages) + [Tool Use API](/claude-capabilities/api/tool-use)。

## 七、examples/ 仓库骨架

v0.3.2 段需要在 `examples/` 目录起最小可复现仓库：

| 仓库 | 用途 | 状态 |
| --- | --- | --- |
| `examples/check-page/` | Skill 模板（v0.2.1 已 published） | ✅ |
| `examples/glossary-mcp-server/` | MCP Server 模板（v0.2.1 已 published） | ✅ |
| `examples/anthropic-sdk-python-minimal/` | Python SDK 最小复现 | ⏳ v0.3.2.3 |
| `examples/anthropic-sdk-typescript-minimal/` | TypeScript SDK 最小复现 | ⏳ v0.3.2.3 |
| `examples/agent-sdk-minimal/` | Agent SDK 最小复现 | ⏳ v0.3.2.3 |

每个仓库结构（参考 [v0.2 glossary-mcp-server](/examples/glossary-mcp-server/README)）：

```
<repo>/
├── README.md        # 装依赖 / 跑测试 / 接入命令 / 已知限制
├── main.py          # 主入口
├── <lib>.py         # 业务逻辑
├── test_<lib>.py    # 自测
├── pyproject.toml   # uv 锁依赖
└── uv.lock
```

## 八、何时不用 SDK

| 场景 | 不用 SDK 的原因 |
| --- | --- |
| **纯 HTTP / 跨语言胶水** | 直接调 Messages API（curl / fetch）更轻 |
| **极简嵌入式**（单图 OCR） | SDK 引入的依赖可能过重 |
| **跑在 Web Worker** | TypeScript SDK 主线程 + worker 通信复杂，可直接 fetch |
| **Serverless 冷启动敏感** | SDK 初始化开销大（v0.3.2.3 末会补 FAQ） |

详见 [Messages API · curl 实战](/claude-capabilities/api/messages#二3-段完整可运行代码)。

## 九、5 个常见坑

**1. 跨 SDK 共享 API key**

```bash
# ✅ 用 env var
export ANTHROPIC_API_KEY=sk-ant-...
# 所有 SDK 都自动读
```

**2. SDK 版本不一致**

Python SDK 0.4x → 1.x 有 breaking change（response 结构变化）——**团队统一升级**。

**3. Agent SDK 误用为 Python SDK**

```python
# ❌ Agent SDK 做简单调用（杀鸡用牛刀）
from claude_agent_sdk import Agent
agent = Agent(model="claude-sonnet-5-...")
agent.run("...")   # 慢

# ✅ 简单调用用 Python SDK
import anthropic
client = anthropic.Anthropic()
client.messages.create(...)
```

**4. Managed Agents 当自建 agent 用**

Managed Agents 是**完全托管**——你想要"自建可定制 agent"用 Agent SDK + 自己部署。

**5. 跨 region API key 不通用**

`us-east-1` 的 key 在 `eu-west-1` 不能用（部分 plan 限制）。

## 参考

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)（访问于 2026-08-07）
- [Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)（访问于 2026-08-07）
- [Anthropic Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)（访问于 2026-08-07）
- [Messages API](/claude-capabilities/api/messages)
- [Tool Use API](/claude-capabilities/api/tool-use)
- [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 下一步

- Python 实战 → [Python SDK](/claude-capabilities/sdk/python-sdk)
- TypeScript 实战 → [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)
- 多步 agent → [Agent SDK](/claude-capabilities/sdk/agent-sdk)

## 如果你想

- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)
- 托管 agent → [Managed Agents](/claude-capabilities/sdk/managed-agents)
- 切到 v0.3.2.3 完成标志 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

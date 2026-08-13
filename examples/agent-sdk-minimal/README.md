# agent-sdk-minimal

Agent SDK 模式的**最小可复现示例**——3 个核心模式（单 agent / Supervisor 调度 / 带 memory），基于 `anthropic` SDK 自实现，零额外依赖。

> **配套教程**：[Agent SDK](/claude-capabilities/sdk/agent-sdk)（主 wiki）
> **多 agent 模式选型**：[多 Agent 模式](/claude-capabilities/agentic/multi-agent-patterns)

## 它做了什么

提供 3 个独立函数，对应 Agent SDK 文档的 3 个核心模式：

| Mode | 用途 | 是否需 API key |
| --- | --- | :---: |
| `single` | 单 agent + 简单 system prompt + Tool Use 循环 | ✅ |
| `supervisor` | 主 agent 调 sub-agent（researcher + writer） | ✅ |
| `memory` | 跨 session 持久化 memory（JSON 文件） | ✅ |

**与 anthropic-sdk-python-minimal 区别**：那个仓库是**单步调用**的 5 模式（最小调用 / Streaming / Tool Use / Structured / Cache）；本仓库是**多步 agent** 的 3 模式。

## 为什么"基于 anthropic SDK 自实现"而不是 `claude-agent-sdk`

- `claude-agent-sdk` 还在早期，API 可能变
- 自实现版本**完全可控**、**零额外依赖**、**行为透明**——你看 main.py 就懂 agent 怎么工作
- 核心模式（tool use 循环 / 主从调度 / memory 持久化）是**通用 agent 模式**，换 SDK 也能用

如果你想用官方 `claude-agent-sdk`——见 [Agent SDK 文档](/claude-capabilities/sdk/agent-sdk)。

## 目录结构

```
agent-sdk-minimal/
├── README.md
├── main.py          # 3 模式综合示例
├── test_main.py     # 5 静态自测
├── pyproject.toml
└── .python-version  # 3.12
```

## 装依赖

需要 [uv](https://docs.astral.sh/uv/)（推荐）或 pip：

```bash
# uv（推荐）
uv sync

# pip（备选）
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 设置 API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## 跑测试

```bash
uv run test_main.py
# 期望：5/5 通过

uv run pytest
```

## 3 模式实战

```bash
# 模式 1：单 agent 跑多步任务
uv run python3 main.py single
# 输出：Claude 调 web_search + 总结

# 模式 2：Supervisor 调度 sub-agent
uv run python3 main.py supervisor
# 输出：主 agent 调 researcher → writer → 200 字报告

# 模式 3：带 memory 的多轮对话
uv run python3 main.py memory
# 输出：第 1 轮偏好 + 第 2 轮"基于偏好"的回复
#       memory 存到 /tmp/agent_memory.json
```

## 关键设计点

1. **3 模式拆 3 函数**——独立可复制，不依赖 main.py 其他部分
2. **Sub-agent = 普通 Python function**——用 `client.messages.create()` 模拟独立 agent 行为（**比真 sub-agent 简单**但足够演示模式）
3. **Memory 用 JSON 文件**——跨 session 持久化（生产可换 Redis / SQLite）
4. **Mock web_search**——避免外部依赖；生产用真 API
5. **MAX_TURNS = 20**——防死循环

## 实战模式选择

| 你的场景 | 用 |
| --- | --- |
| 简单 Q&A | [anthropic-sdk-python-minimal](../anthropic-sdk-python-minimal/README) `minimal` |
| 多步 agent（5-10 步） | 本仓库 `single` |
| 多 agent 协作 | 本仓库 `supervisor` |
| 跨 session 记忆 | 本仓库 `memory` |
| 真 sub-agent SDK | [Agent SDK](/claude-capabilities/sdk/agent-sdk) |
| 商业级 agent 框架 | [LangGraph](https://langchain-ai.github.io/langgraph/) / [CrewAI](https://www.crewai.com/) |

## 已知限制

- **需真 API key**——3 模式都调真 API（mock web_search 是 mock，但 client.messages.create 仍需真 key）
- **Sub-agent = function**——不是真并发 agent。生产用真 multi-agent 框架（LangGraph / CrewAI）
- **Memory = 本地 JSON**——多用户 / 分布式场景换 Redis / DB
- **测试不覆盖真 API**——结构正确 ≠ 业务正确

## 进阶

| 需求 | 路径 |
| --- | --- |
| 多 agent 并发 | 用 [asyncio.gather](https://docs.python.org/3/library/asyncio.html) 并发 client.messages.create |
| 真 sub-agent | 换 [Agent SDK](/claude-capabilities/sdk/agent-sdk) 或 LangGraph |
| Memory 持久化 | 换 Redis / SQLite / Pinecone |
| 监控 | 加 LangSmith / Helicone |

## 参考

- [Agent SDK 详解](/claude-capabilities/sdk/agent-sdk)
- [多 Agent 模式](/claude-capabilities/agentic/multi-agent-patterns)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Tool Use API](/claude-capabilities/api/tool-use)
- [Python SDK 仓库](/examples/anthropic-sdk-python-minimal/README)
- [TypeScript SDK 仓库](/examples/anthropic-sdk-typescript-minimal/README)
- [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 下一步

- 切到商业级 agent 框架 → LangGraph / CrewAI
- 多 agent 选型 → [多 Agent 模式](/claude-capabilities/agentic/multi-agent-patterns)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

## 如果你想

- Tool Use 循环模板 → [anthropic-sdk-python-minimal · mode_tool_loop](/examples/anthropic-sdk-python-minimal/README#模式-2tool-use-循环--让-claude-调-bash-工具)
- 实战 Cookbook → [Cookbook · 第一个真实任务](/cookbook/first-real-task)

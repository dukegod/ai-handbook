---
title: 工具使用
description: API 视角的 tool_use 协议；tool block 结构、input_schema、多步循环、tool choice 与流式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  toolUse: 'https://platform.claude.com/docs/en/build-with-claude/tool-use'
  accessedAt: 2026-08-06
---

# 工具使用

> **TL;DR**：tool_use 是 Claude 调用外部工具的**原语**——你定义工具 schema，Claude 决定何时调、调哪个、回什么。**多步 tool call 循环**是 agent 系统的核心。本页是 **API 视角的 tool_use 协议**；Claude Code 怎么用 MCP 接外部系统见 [v0.2 · MCP 使用层](/claude-code/mcp/what-is-mcp)；MCP 协议本身见 [MCP 协议层](/claude-capabilities/mcp-protocol/protocol-spec)。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- tool_use block 结构（`type` / `id` / `name` / `input`）
- input_schema 怎么写（JSON Schema 子集）
- 多步 tool call 循环（最常见的 agent 模式）
- tool_choice 控制（auto / any / tool / none）
- 流式 tool use（streaming + tool calls）
- 错误处理（tool_result is_error、retry 策略）
- 4 模型 tool use 能力对比
- 5 个常见坑（schema 错、循环失控、错误处理、token 爆炸）

## 一、Tool Use Block 结构

Claude 调用工具时返回的 `tool_use` block：

```python
{
    "type": "tool_use",
    "id": "toolu_01ABC...",        # 唯一 ID，用于对应 tool_result
    "name": "read_file",            # 工具名（与你定义的一致）
    "input": {                      # 实际参数（按 input_schema 验证）
        "path": "/Users/you/auth.ts"
    }
}
```

**对应的 tool_result**（你回给 Claude）：

```python
{
    "type": "tool_result",
    "tool_use_id": "toolu_01ABC...",   # ← 对应上面的 id
    "content": "export function ...",  # 工具执行结果（str 或 list of blocks）
    "is_error": False                   # 可选，标记是否执行失败
}
```

## 二、定义工具 Schema

**input_schema 用 JSON Schema 子集**：

```python
tools = [
    {
        "name": "search_issues",
        "description": "在 GitHub 仓库里搜索 issue",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo": {
                    "type": "string",
                    "description": "owner/repo 格式，如 'anthropics/anthropic-sdk-python'",
                },
                "query": {
                    "type": "string",
                    "description": "搜索关键词",
                },
                "max_results": {
                    "type": "integer",
                    "description": "最多返回多少条",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50,
                },
            },
            "required": ["repo", "query"],
        },
    }
]
```

**`description` 至关重要**——Claude 决定调哪个工具**全靠 description**。模糊的 description 会让 Claude 永不调用或乱调。

**JSON Schema 支持的字段**（子集）：
- 类型：`string` / `integer` / `number` / `boolean` / `array` / `object` / `null`
- 修饰：`enum` / `default` / `minimum` / `maximum` / `minLength` / `maxLength` / `pattern`
- 数组：`items` / `minItems` / `maxItems`
- 对象：`properties` / `required` / `additionalProperties`
- 组合：`anyOf` / `oneOf` / `allOf`

**不支持**：`$ref` / `$defs` / `if/then/else` 等高级 JSON Schema 特性。

## 三、多步 Tool Call 循环（Agent 核心）

```python
import anthropic

client = anthropic.Anthropic()

TOOLS = [...]  # 见上
MAX_TURNS = 50

def execute_tool(name: str, tool_input: dict) -> str:
    """执行工具，返回字符串结果。"""
    if name == "search_issues":
        # 实际调 GitHub API
        return json.dumps(github_search(**tool_input))
    elif name == "read_file":
        return Path(tool_input["path"]).read_text()
    # ... 其他工具
    return "Unknown tool"

def run_agent(user_query: str) -> str:
    messages = [{"role": "user", "content": user_query}]

    for turn in range(MAX_TURNS):
        msg = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )

        if msg.stop_reason == "end_turn":
            # Claude 完成，返回 text
            return next(b.text for b in msg.content if b.type == "text")

        if msg.stop_reason == "tool_use":
            # Claude 要调工具
            messages.append({"role": "assistant", "content": msg.content})
            tool_results = []
            for block in msg.content:
                if block.type == "tool_use":
                    try:
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })
                    except Exception as e:
                        # 错误处理
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(e),
                            "is_error": True,
                        })
            messages.append({"role": "user", "content": tool_results})
        else:
            # 其他 stop_reason（max_tokens / refusal）
            return next((b.text for b in msg.content if b.type == "text"), "")

    return "Max turns exceeded"
```

**关键点**：
- **MAX_TURNS 必设**——避免 Claude 死循环
- **`stop_reason` 三态**：`end_turn`（完成）/ `tool_use`（要调工具）/ 其他（异常）
- **每轮 messages append 两条**（assistant 的 tool_use 请求 + user 的 tool_result 回包）

## 四、Tool Choice 控制

`tool_choice` 控制 Claude 调工具的策略：

| 值 | 行为 | 适用 |
| --- | --- | --- |
| `auto`（默认） | Claude 自己决定调不调、调哪个 | 一般 agent |
| `any` | **必须**调一个工具（但 Claude 选哪个） | 强制走工具 |
| `tool` + `{name: "X"}` | **必须**调指定工具 X | 已知只调一个 |
| `none` | **禁止**调工具 | 纯对话 |

```python
# 强制 Claude 调 search_issues
msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    tools=TOOLS,
    tool_choice={"type": "tool", "name": "search_issues"},   # 强制
    messages=[{"role": "user", "content": "查最近 5 个 open issue"}],
)
```

**实战用法**：
- `auto`：默认
- `any`：路由层（先调分类器、再调专门 agent）
- `tool`：UI 强制流程（点"查 JIRA"按钮一定走 search_issues）

## 五、流式 Tool Use

```python
with client.messages.stream(
    model="claude-sonnet-5",
    max_tokens=4096,
    tools=TOOLS,
    messages=[...],
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                # 工具开始调用
                tool_name = event.content_block.name
                tool_id = event.content_block.id
                tool_input_json = ""
        elif event.type == "content_block_delta":
            if event.delta.type == "input_json_delta":
                # 流式接收 input JSON
                tool_input_json += event.delta.partial_json
        elif event.type == "content_block_stop":
            # tool_use 完整
            tool_input = json.loads(tool_input_json)
            # 执行
            ...
```

**流式的价值**：长 tool_input 不用等完整生成——可以提前开始解析执行（适合 input 很大的工具如"读取大文件"）。

## 六、4 模型 Tool Use 能力

| 模型 | tool_use 支持 | max tools | input_schema 严格度 |
| --- | :---: | :---: | --- |
| **Opus 5** | ✅ | 100+ | 严格 |
| **Sonnet 5** | ✅ | 100+ | 严格 |
| **Fable 5** | ✅ | 100+ | 严格 |
| **Haiku 4.5** | ✅ | 50 | 较严格（少量边界宽松） |

**实战**：4 模型在 tool use 上能力**接近**——但 Opus 5 / Sonnet 5 在**多步 tool 编排**上更稳（不会循环、不会忘 schema）。

## 七、错误处理

```python
# 工具执行失败时
tool_results.append({
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": f"Error: {str(e)}",
    "is_error": True,
})

# Claude 看到 is_error=True 会自动调整策略（重试 / 改用其他工具 / 告诉用户）
```

**3 个层次**：

1. **工具级错误**（`is_error=True`）：Claude 自动处理
2. **Schema 错**（输入参数类型不对）：API 端报错 → 你 catch 后重发
3. **循环失控**（> MAX_TURNS）：你硬中断

**实战建议**：
- 工具实现里**永远** try/except——别让异常逃出
- 把异常信息**清楚传给 Claude**（别只传 "Error"）
- 提供 fallback 路径——文件读不到就 grep 别处

## 八、与 MCP 协议的关系

```
┌─────────────────────────────────┐
│ 应用层：Claude Code / 你的产品   │
├─────────────────────────────────┤
│ 协议层：MCP（标准化工具/资源）   │  ← v0.2 mcp/* + v0.3 mcp-protocol/*
├─────────────────────────────────┤
│ 原语层：tool_use / tool_result  │  ← 本页
├─────────────────────────────────┤
│ 模型层：Opus 5 / Sonnet 5 ...   │
└─────────────────────────────────┘
```

- **tool_use 是 API 原语**——直接调 Claude API 时的工具调用方式
- **MCP 是上层协议**——标准化"工具如何暴露、调用、授权"
- **MCP server 内部仍用 tool_use 实现**——MCP 是把 tool_use 包装成可插拔的服务

详见：
- [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp)
- [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)

## 九、常见坑

**1. description 写太模糊**

```python
# ❌ 模糊 → Claude 永远不调
{"name": "search", "description": "搜索东西"}

# ✅ 明确 + 关键词
{"name": "search_github_issues", "description": "在指定 GitHub 仓库按关键词搜索 issue（含标题、标签、状态）；用户问「XX 项目有没相关 issue」「查一下 bug 报告」时用"}
```

**2. 多步循环无 MAX_TURNS 上限**

```python
# ❌ Claude 可能死循环
while True:
    msg = client.messages.create(...)
    if msg.stop_reason == "end_turn": break

# ✅ 必设 MAX_TURNS
for turn in range(MAX_TURNS):
    ...
```

**3. tool_result 不带 is_error**

工具失败时仍传 `is_error=False` → Claude 以为成功了，继续用错的数据。**永远标记错误**。

**4. 工具 schema 用 `$ref`**

Claude API 不支持 JSON Schema 高级特性：

```python
# ❌ 不支持
"properties": {
    "user": {"$ref": "#/definitions/User"}
}

# ✅ 展开定义
"properties": {
    "user": {"type": "object", "properties": {...}}
}
```

**5. 一个工具塞太多功能**

```python
# ❌ 一个工具做 5 件事
{"name": "do_everything", ...}

# ✅ 拆成多个
[{"name": "search_issues"}, {"name": "read_issue"}, {"name": "close_issue"}]
```

**经验**：**1 个工具 = 1 个原子操作**——拆细让 Claude 调度。

## 参考

- [Anthropic Docs · Tool use](https://platform.claude.com/docs/en/build-with-claude/tool-use)（访问于 2026-08-06）
- [Anthropic Docs · Messages API](https://platform.claude.com/docs/en/api/messages)（访问于 2026-08-06）
- [Claude Code · 工具总览](/claude-code/tools/overview)
- [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp)
- [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- [代码能力 · 工具使用模式](/claude-capabilities/core/coding#二api-视角的工具使用模式)

## 下一步

- MCP 协议层（v0.3.2/3 写） → [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- 代码生成 → [代码能力](/claude-capabilities/core/coding)
- Sub-agent 编排 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

## 如果你想

- 实战 Agent 框架 → [Anthropic Cookbook · Building effective agents](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)
- Token 与成本 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 工具安全 → [MCP 协议层 · Server 安全](/claude-capabilities/mcp-protocol/server-authoring)

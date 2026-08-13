---
title: Tool Use API
description: HTTP 协议层的 tool_use / tool_result 协议；tool_choice 控制、完整可运行多步循环代码
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  toolUseApi: 'https://platform.claude.com/docs/en/api/messages#tool-use'
  accessedAt: 2026-08-07
---

# Tool Use API

> **TL;DR**：Tool Use API 让 Claude 在响应中**返回 `tool_use` block**（要调哪个工具、传什么参数），你执行后用 `tool_result` 回包——多步循环形成 Agent。本页是 **HTTP 协议层**（与 [core/tool-use](/claude-capabilities/core/tool-use) 视角分工：那里讲 agent 模式，这里讲协议字段）。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 完整可运行多步循环代码（Python）
- 协议层请求 / 响应字段（tools / tool_choice / tool_use block / tool_result）
- tool_choice 4 档控制（auto / any / tool / none）
- 4 个常见坑

## 一、协议概览

```
请求：
  messages + tools 定义
  ↓
响应：
  stop_reason = "tool_use"
  content[0] = {type: "tool_use", name, input, id}
  ↓
你执行工具 → 回包：
  messages.append({role: "user", content: [{type: "tool_result", tool_use_id, content}]})
  ↓
继续请求 → Claude 看 tool_result 决定下一步
```

详见 [core/tool-use · 多步循环](/claude-capabilities/core/tool-use#三多步-tool-call-循环agent-核心)。

## 二、完整可运行多步循环

```python
import anthropic
import json
from pathlib import Path

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "read_file",
        "description": "读取文件内容",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "list_dir",
        "description": "列出目录下文件",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]

def execute_tool(name, tool_input):
    if name == "read_file":
        return Path(tool_input["path"]).read_text()
    elif name == "list_dir":
        return "\n".join(p.name for p in Path(tool_input["path"]).iterdir())
    return f"Unknown tool: {name}"

def run_agent(user_query):
    messages = [{"role": "user", "content": user_query}]
    for _ in range(20):
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )
        if msg.stop_reason == "end_turn":
            return next(b.text for b in msg.content if b.type == "text")
        if msg.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": msg.content})
            results = []
            for block in msg.content:
                if block.type == "tool_use":
                    try:
                        result = execute_tool(block.name, block.input)
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })
                    except Exception as e:
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(e),
                            "is_error": True,
                        })
            messages.append({"role": "user", "content": results})

result = run_agent("列出 src/ 目录下的所有 .py 文件，然后读 auth.py")
print(result)
```

## 三、协议字段详解

### 请求：`tools` 数组

```json
{
  "tools": [
    {
      "name": "search_issues",
      "description": "在 GitHub 仓库搜索 issue",
      "input_schema": {
        "type": "object",
        "properties": {
          "repo": {"type": "string"},
          "query": {"type": "string"},
          "max_results": {"type": "integer", "default": 10}
        },
        "required": ["repo", "query"]
      }
    }
  ]
}
```

### 响应：`tool_use` block

```json
{
  "content": [{
    "type": "tool_use",
    "id": "toolu_01ABC...",
    "name": "search_issues",
    "input": {"repo": "anthropics/anthropic-sdk-python", "query": "streaming"}
  }]
}
```

### 回包：`tool_result`

```json
{
  "role": "user",
  "content": [{
    "type": "tool_result",
    "tool_use_id": "toolu_01ABC...",
    "content": "Found 3 issues...",
    "is_error": false
  }]
}
```

## 四、tool_choice 控制

| 值 | 行为 |
| --- | --- |
| `auto`（默认） | Claude 自己决定调不调 |
| `any` | 必须调一个（Claude 选哪个） |
| `{"type": "tool", "name": "X"}` | 必须调 X |
| `none` | 禁止调 |

```python
# 强制调 search_issues
msg = client.messages.create(
    model="claude-sonnet-5-...",
    tools=TOOLS,
    tool_choice={"type": "tool", "name": "search_issues"},
    messages=[...],
)
```

## 五、4 个常见坑

**1. `tools` 定义里 `description` 太模糊**

Claude 决定调哪个工具**全靠 description**。

**2. 多步循环无上限**

必设 `MAX_TURNS`（示例里 20 步）——避免死循环。

**3. `tool_result` 不带 `is_error`**

工具失败时仍传 `is_error=False` → Claude 以为成功。

**4. JSON Schema 用 `$ref`**

不支持——`input_schema` 用 JSON Schema 子集（详见 [core/tool-use · 4 常见坑](/claude-capabilities/core/tool-use#九常见坑)）。

## 参考

- [Anthropic Docs · Messages API · Tool use](https://platform.claude.com/docs/en/api/messages#tool-use)（访问于 2026-08-07）
- [Tool Use 协议 · 多步循环模板](/claude-capabilities/core/tool-use#三多步-tool-call-循环agent-核心)
- [Messages API](/claude-capabilities/api/messages)

## 下一步

- 流式响应 → [流式响应](/claude-capabilities/api/streaming)
- 强制 JSON 输出 → [结构化输出](/claude-capabilities/api/structured-outputs)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- 完整 tool_use 实战 → [Tool Use 协议](/claude-capabilities/core/tool-use)
- 多 agent 编排 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

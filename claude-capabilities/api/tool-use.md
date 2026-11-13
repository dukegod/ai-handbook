---
title: Tool Use API
description: HTTP 协议层的 tool_use / tool_result 协议；tool_choice 控制、完整可运行多步循环代码
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核了模型 ID、tool_choice 四档语义、tool_use / tool_result 字段与 stop_reason 取值；强制调用的型号限制取自官方 Define tools 页；本轮订正 JSON Schema 支持范围——local $ref / $defs / definitions 在 strict tool use 与结构化输出下均支持，external $ref、allOf 带 $ref、递归 schema 不支持；本页代码示例未在本机重跑'
  claudeCode: 2.1.319
  model: claude-opus-5-5
  toolUseApi: 'https://platform.claude.com/docs/en/api/messages#tool-use'
  defineTools: 'https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools'
  structuredOutputs: 'https://platform.claude.com/docs/en/build-with-claude/structured-outputs'
  accessedAt: 2026-11-13
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

详见 [core/tool-use · 多步循环](/claude-capabilities/core/tool-use#三、多步-tool-call-循环-agent-核心)。

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
            model="claude-sonnet-5-5",
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

> ⚠️ **型号限制**：`any` 和 `tool` 返回 **400** 的只有 **Fable 5.2 / Mythos 5.2 / Opus 5.5 / Sonnet 5.5 / Fable 5.1 / Mythos 5.1** 这 6 个型号（[官方 Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)）。**Haiku 5.5 与上一代 Opus 5 仍然支持强制调用**——官方强制调用的示例用的正是 `claude-opus-5`。受限型号上只有 `auto` / `none` 可用；改用 `auto` + prompt 指令，或上 strict tool use 保证入参合法。
>
> 另外两点：**手动开 extended thinking（`thinking: {type: "enabled"}`）时强制调用不可用**（但 adaptive thinking 本身不挡强制调用——只是被强制调用时响应直接以 `tool_use` 开头、**没有 thinking 块**）；改 `tool_choice` 会让**已缓存的 message block 失效**（tool 定义与 system prompt 仍命中缓存）。

```python
# 强制调 search_issues：需用支持强制调用的型号（如 claude-opus-5）
msg = client.messages.create(
    model="claude-opus-5",
    tools=TOOLS,
    tool_choice={"type": "tool", "name": "search_issues"},
    messages=[...],
)

# 当前主力型号的替代写法：auto + prompt 指令
msg = client.messages.create(
    model="claude-sonnet-5-5",
    tools=TOOLS,
    tool_choice={"type": "auto"},
    messages=[{"role": "user", "content": "必须调用 search_issues 工具来查 issue"}],
)
```

想在主力型号上**保证**入参合法，给工具定义加 `strict: true`（同时写 `additionalProperties: false`）——见 [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)（访问于 2026-11-13）。strict 与结构化输出共用同一套 JSON Schema 限制（含 `$ref` 的三条边界），见下面第 4 个坑。

## 五、4 个常见坑

**1. `tools` 定义里 `description` 太模糊**

Claude 决定调哪个工具**全靠 description**。

**2. 多步循环无上限**

必设 `MAX_TURNS`（示例里 20 步）——避免死循环。

**3. `tool_result` 不带 `is_error`**

工具失败时仍传 `is_error=False` → Claude 以为成功。

**4. strict 模式下 `$ref` 的三条边界**

**本地 `$ref` 是支持的**（`$defs` / `definitions` 都能引，不必展开重写定义）。但有三条硬边界：**external `$ref` 不支持**、**递归 schema 不支持**、**`allOf` 里带 `$ref` 不支持**。

```json
// ❌ external $ref：引用外部文件，不支持
{"$ref": "https://example.com/user.json"}

// ✅ 本地 $ref + $defs：官方示例的结构
{
  "type": "object",
  "properties": {"contact": {"$ref": "#/$defs/contact"}},
  "required": ["contact"],
  "additionalProperties": false,
  "$defs": {
    "contact": {
      "type": "object",
      "properties": {"email": {"type": "string", "format": "email"}},
      "required": ["email"],
      "additionalProperties": false
    }
  }
}
```

strict 与结构化输出共用的完整支持 / 不支持清单见 [core/tool-use · 9 常见坑](/claude-capabilities/core/tool-use#九、常见坑)。

## 参考

- [Anthropic Docs · Messages API · Tool use](https://platform.claude.com/docs/en/api/messages#tool-use)（访问于 2026-11-13）
- [Anthropic Docs · Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)（访问于 2026-11-13）
- [Anthropic Docs · Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（访问于 2026-11-13）
- [Tool Use 协议 · 多步循环模板](/claude-capabilities/core/tool-use#三、多步-tool-call-循环-agent-核心)
- [Messages API](/claude-capabilities/api/messages)

## 下一步

- 流式响应 → [流式响应](/claude-capabilities/api/streaming)
- 强制 JSON 输出 → [结构化输出](/claude-capabilities/api/structured-outputs)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- 完整 tool_use 实战 → [Tool Use 协议](/claude-capabilities/core/tool-use)
- 多 agent 编排 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

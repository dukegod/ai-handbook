---
title: 结构化输出
description: 强制 JSON / JSON Schema 输出的 3 种方式；tool_use 实现 vs response_format vs Prefill
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  structuredOutputs: 'https://platform.claude.com/docs/en/build-with-claude/structured-outputs'
  accessedAt: 2026-08-07
---

# 结构化输出

> **TL;DR**：强制 Claude 输出**结构化数据**（JSON / 字段化）有 3 种方式：**tool_use 实现**（最稳，推荐）/ **Prefill**（最简，prompt 层）/ 手动 prompt 引导（最不可靠）。生产**一律用 tool_use**。

⏱ 预计阅读时间：4 分钟

## 一、3 种方式对比

| 方式 | 可靠性 | 复杂度 | 适用 |
| --- | :---: | :---: | --- |
| **tool_use + JSON Schema** | ⭐⭐⭐⭐⭐ | 中 | 生产 / API 集成 |
| **Prefill `{`** | ⭐⭐⭐⭐ | 低 | 简单 prompt 拼接 |
| **手动 prompt "请输出 JSON"** | ⭐⭐ | 低 | 临时 demo |

## 二、tool_use 实现（推荐）

```python
import anthropic
import json

client = anthropic.Anthropic()

TOOL = {
    "name": "extract_invoice",
    "description": "从发票文本提取结构化字段",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_no": {"type": "string", "description": "发票号"},
            "amount": {"type": "string", "description": "金额（字符串保留原始格式）"},
            "date": {"type": "string", "description": "日期 YYYY-MM-DD"},
            "merchant": {"type": "string", "description": "商家名称"},
        },
        "required": ["invoice_no", "amount", "date", "merchant"],
    },
}

msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=512,
    tools=[TOOL],
    tool_choice={"type": "tool", "name": "extract_invoice"},   # 强制
    messages=[{"role": "user", "content": "提取：发票号 INV-001，金额 ¥1000，日期 2024-01-15，商家 ACME"}],
)

# 解析 tool_use block
for block in msg.content:
    if block.type == "tool_use":
        data = block.input
        # data = {"invoice_no": "INV-001", "amount": "1000", "date": "2024-01-15", "merchant": "ACME"}
        print(json.dumps(data, ensure_ascii=False, indent=2))
```

**实战优势**：
- **Schema 强制**——Claude 不能瞎填字段
- **字段类型校验**——SDK 帮你验证
- **重试友好**——字段缺失 / 类型错时再请求一次

## 三、Prefill `{`

```python
msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=512,
    messages=[
        {"role": "user", "content": "提取：发票号 INV-001，金额 ¥1000"},
        {"role": "assistant", "content": "{"},   # Prefill
    ],
)
# Claude 从 { 开始输出 JSON
```

详见 [Prefill 与 XML 标签 · 场景 1](/claude-capabilities/prompting/prefill-and-xml#场景-1强制-json-输出)。

## 四、手动 prompt 引导（不推荐）

```python
msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=512,
    system="你必须输出严格 JSON 格式，不要包含其他文字。",
    messages=[{"role": "user", "content": "提取：INV-001，¥1000"}],
)

# 仍可能输出：
# "好的，以下是 JSON：\n{\"invoice_no\": ...}"
# 还要手动剥离前缀
```

**风险**：Claude 经常"客套"——"好的！这是你要的 JSON..."，**JSON 之外多出文字**让你解析失败。

## 五、3 个实战技巧

### 1. 字段类型灵活选

```python
# amount 选 string 而非 number —— 保留 "¥1,000" / "$500" 原始格式
"amount": {"type": "string"}

# 严格要求数字才用 number
"score": {"type": "number", "minimum": 0, "maximum": 100}
```

### 2. 必填 vs 可选

```python
"required": ["invoice_no"],   # 这 1 个必填
# amount / date / merchant 可选（缺时返回 null）
```

### 3. 枚举值

```python
"status": {"type": "string", "enum": ["draft", "paid", "overdue"]}
# Claude 不会瞎填
```

## 六、4 个常见坑

**1. 用 `tool_choice: "any"`**

`any` 让 Claude 选工具，但**不保证是想要的**——必须用 `{"type": "tool", "name": "X"}` 强制。

**2. 字段太多（> 10）**

Schema 太复杂 → Claude 漏字段 / 填错类型。**拆成多个 tool**（"extract_basic" + "extract_detail"）。

**3. 不验证响应**

```python
# ❌ 信任 Claude 输出
data = block.input
do_something(data["amount"])    # 假设是数字

# ✅ 验证
try:
    amount = float(data["amount"])
except (ValueError, KeyError):
    raise ExtractionError("amount 字段格式错误")
```

**4. 嵌套对象没声明**

```python
# ❌ 期望 Claude 自动嵌套
"items": {"type": "array"}  # 元素类型没说

# ✅ 显式
"items": {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "qty": {"type": "integer"},
        },
    },
}
```

## 参考

- [Anthropic Docs · Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)（访问于 2026-08-07）
- [Tool Use API](/claude-capabilities/api/tool-use)
- [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)
- [Messages API](/claude-capabilities/api/messages)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)

## 下一步

- Prompt 缓存 → [Prompt Caching](/claude-capabilities/api/prompt-caching)
- 批处理 → [Message Batches](/claude-capabilities/api/message-batches)
- 文件引用 → [Files API](/claude-capabilities/api/files)

## 如果你想

- JSON Schema 速查 → [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)
- 流式 + 结构化 → [流式响应](/claude-capabilities/api/streaming)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

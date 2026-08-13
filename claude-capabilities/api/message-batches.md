---
title: Message Batches
description: 50% 价格折扣的离线批处理 API；24h SLA、提交 / 轮询 / 取消完整实战
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-haiku-4-5-...
  messageBatches: 'https://platform.claude.com/docs/en/api/messages/batches'
  accessedAt: 2026-08-07
---

# Message Batches

> **TL;DR**：Message Batches API 让你**一次性提交最多 10 万条请求**，24h 内处理完，**价格 50% 折扣**。适合离线批处理（分类、提取、初审、ETL）。**不能用于实时**。

⏱ 预计阅读时间：4 分钟

## 一、API 概览

```
1. 提交 batch
   POST /v1/messages/batches
   body: {requests: [{custom_id, params: {model, messages, ...}}, ...]}
   ↓
2. 拿到 batch_id
   ↓
3. 轮询 batch 状态（每秒 1 次足够）
   GET /v1/messages/batches/{batch_id}
   status: in_progress → ended
   ↓
4. 拉取结果
   GET /v1/messages/batches/{batch_id}/results
```

## 二、完整可运行代码

```python
import anthropic

client = anthropic.Anthropic()

# 1. 准备 1000 条评论分类请求
requests = [
    {
        "custom_id": f"comment-{i}",
        "params": {
            "model": "claude-haiku-4-5-...",
            "max_tokens": 64,
            "messages": [{
                "role": "user",
                "content": f"分类为「投诉」/「建议」/「表扬」：{comment}"
            }],
        },
    }
    for i, comment in enumerate(comments)   # 你的 1000 条评论
]

# 2. 提交 batch
batch = client.messages.batches.create(requests=requests)
print(f"batch id: {batch.id}")

# 3. 轮询状态
import time
while True:
    status = client.messages.batches.retrieve(batch.id)
    print(f"status: {status.processing_status}, succeeded: {status.request_counts.succeeded}")
    if status.processing_status == "ended":
        break
    time.sleep(60)   # 1 分钟轮询

# 4. 拉取结果
results = []
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        text = result.result.message.content[0].text
        results.append({"id": result.custom_id, "text": text})
    else:
        results.append({"id": result.custom_id, "error": str(result.result.error)})

print(f"处理 {len(results)} 条")
```

## 三、限制

| 项 | 上限 |
| --- | --- |
| 单 batch 请求数 | 100,000 |
| 单 batch 大小 | 256 MB |
| 处理 SLA | 24h（多数情况 1-2h） |
| 重试 | 失败请求自动重试 1 次 |

## 四、4 个实战场景

### 1. 离线分类

```python
# 100 万条评论情感分类
# Online: $1.5 / 1M input
# Batch: $0.75 / 1M input → 节省 50%
```

### 2. 数据提取（文档 → 结构化）

```python
# 10 万份发票 OCR + 字段提取
requests = [
    {"custom_id": f"invoice-{i}", "params": {
        "model": "claude-sonnet-5-...",
        "tools": [EXTRACT_INVOICE_TOOL],   # 用 tool_use 强制 JSON
        "tool_choice": {"type": "tool", "name": "extract_invoice"},
        "messages": [{"role": "user", "content": pdf_text}],
    }}
    for i, pdf_text in enumerate(invoices)
]
```

详见 [结构化输出](/claude-capabilities/api/structured-outputs)。

### 3. 批量翻译

```python
# 5 万条用户评论翻译为英文
```

### 4. 跨小时 ETL 流水线

```python
# 每天 02:00 跑批：昨天积累的工单做初筛
import schedule
schedule.every().day.at("02:00").do(submit_daily_batch)
```

## 五、Batch vs Online 决策

| 场景 | 用 | 原因 |
| --- | :---: | --- |
| 实时对话 | **Online** | 24h SLA 不能用 |
| 用户提交后等结果（< 30s） | **Online** | 用户等 |
| **离线批处理（万级以上）** | **Batch** | 50% 折扣 |
| 跨小时 ETL | **Batch** | 50% 折扣 |
| 紧急重要但量大 | Online + parallel | Batch 太慢 |

详见 [Haiku 4.5 · 批量任务实战](/claude-capabilities/models/haiku#四批量任务实战)。

## 六、4 个常见坑

**1. 用 batch 跑实时**

24h SLA → 用户等一天。**实时必用 online**。

**2. 单 batch 太大（> 10 万）**

超出会 400。**拆成多个 batch**。

**3. 不读 `request_counts`**

```python
# ❌ 只看 status
if status.processing_status == "ended":
    break

# ✅ 看 succeeded / errored / expired
if (status.request_counts.succeeded + 
    status.request_counts.errored + 
    status.request_counts.expired) == total:
    break
```

**4. 失败请求没重试**

`errored` 计数 > 0 → **拉出来后**手动重发（API 自动重试 1 次，但不够）。

## 参考

- [Anthropic Docs · Message Batches API](https://platform.claude.com/docs/en/api/messages/batches)（访问于 2026-08-07）
- [Haiku 4.5 · 批量任务实战](/claude-capabilities/models/haiku#四批量任务实战)
- [结构化输出](/claude-capabilities/api/structured-outputs)
- [Messages API](/claude-capabilities/api/messages)
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 下一步

- 文件引用 → [Files API](/claude-capabilities/api/files)
- Token 计算 → [Token Counting](/claude-capabilities/api/token-counting)
- Admin API → [Admin & Usage](/claude-capabilities/api/admin-usage)

## 如果你想

- 并发 + online vs batch 决策 → [Haiku 4.5 · 实战模式](/claude-capabilities/models/haiku#四批量任务实战)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
- Agent SDK → [Agent SDK](/claude-capabilities/sdk/agent-sdk)

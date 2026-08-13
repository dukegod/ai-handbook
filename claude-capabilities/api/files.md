---
title: Files API
description: 上传 / 引用 / 删除文件的端点；与 PDF / 图片 / base64 引用对比
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5-...
  filesApi: 'https://platform.claude.com/docs/en/api/files'
  accessedAt: 2026-08-07
---

# Files API

> **TL;DR**：Files API 让你**上传文件**到 Anthropic 服务端（最大 500 MB），拿到 `file_id` 后在请求中**用 `{"type": "file", "file_id": "..."}` 引用**——比 base64 内嵌省 token、比 URL 引用更稳定。

⏱ 预计阅读时间：4 分钟

## 一、3 种文件引用方式

| 方式 | 限制 | 适用 |
| --- | --- | --- |
| **base64 内嵌** | 单图 ≤ 5 MB | 临时小图 |
| **URL 引用** | 必须公网可达 | 公网静态图 |
| **Files API 上传** | 单文件 ≤ 500 MB | 反复用的大文件 / 私密图 |

## 二、Files API 实战

### 1. 上传

```python
import anthropic

client = anthropic.Anthropic()

# 上传文件
with open("report.pdf", "rb") as f:
    file_obj = client.files.create(
        file=f,
        purpose="user_data",   # 必填
    )
print(f"file_id: {file_obj.id}")
# file_id = "file_01ABC..."
```

### 2. 引用

```python
msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {"type": "file", "file_id": file_obj.id},
            {"type": "text", "text": "总结这份报告"},
        ],
    }],
)
print(msg.content[0].text)
```

### 3. 列出 / 删除

```python
# 列出所有文件
files = client.files.list()
for f in files.data:
    print(f"{f.id}: {f.filename} ({f.size_bytes} bytes)")

# 删除单个
client.files.delete(file_obj.id)
```

## 三、限制

| 项 | 上限 |
| --- | --- |
| 单文件大小 | 500 MB |
| 单 org 总存储 | 100 GB |
| 文件保留 | 30 天（**到期自动删除**） |
| 支持类型 | PDF / 图片 / 文本 |

## 四、与 vision 的关系

**Vision（图片）**和 **Files API** 是两个层级：

```
base64 内嵌  →  Vision image block
URL 引用    →  Vision image source: url
Files API  →  content: {type: "file", file_id: ...}   ← Vision 也支持
```

```python
# 同一张图：3 种写法
content = [
    {"type": "image", "source": {"type": "base64", "data": "..."}},   # ① base64
    {"type": "image", "source": {"type": "url", "url": "..."}},       # ② URL
    {"type": "file", "file_id": "file_01ABC..."},                     # ③ Files API
]
```

详见 [Vision · 3 种传图方式](/claude-capabilities/core/vision#二最小调用示例)。

## 五、3 个实战场景

### 1. 反复用的大文件

```python
# 上传一次
file_id = upload("huge_manual.pdf")

# 多次请求引用（token 不重复计）
for question in user_questions:
    answer = ask_claude(file_id, question)
```

### 2. 私密图片

```python
# 不想走公网 URL（隐私）→ 用 Files API
file_id = upload("private_screenshot.png")
# 仅 Anthropic 内部存储
```

### 3. 批量文档

```python
# 100 份合同 OCR + 提取
for contract_pdf in contracts:
    file_id = upload(contract_pdf)
    extract_invoice(file_id)
    # 30 天后自动清理
```

## 六、5 个常见坑

**1. 30 天自动删除**

上传后**30 天自动删**——长保留需求自己备份。

**2. 500 MB 单文件上限**

```python
# ❌ 上传 600 MB
with open("huge.bin", "rb") as f:
    client.files.create(file=f, ...)   # 400

# ✅ 切片
```

**3. PDF 超过 Pages 上限**

PDF 解析按页计费，**1M context 装不下 → 用 RAG 切片**（详见 [长上下文 · RAG 模式](/claude-capabilities/core/long-context#模式-4rag超-1m-走-rag)）。

**4. `purpose` 写错**

```python
# ❌ 漏 purpose
client.files.create(file=f)   # 400

# ✅ 必填 purpose
client.files.create(file=f, purpose="user_data")
```

**5. 删除后还能引用**

```python
client.files.delete(file_id)
# file_id 仍可引用到失效那一刻
msg = client.messages.create(...content=[{"type": "file", "file_id": file_id}]...)
# → 可能 404
```

**解决**：删除前确认没有 in-flight 请求。

## 参考

- [Anthropic Docs · Files API](https://platform.claude.com/docs/en/api/files)（访问于 2026-08-07）
- [Vision · 3 种传图方式](/claude-capabilities/core/vision#二最小调用示例)
- [Messages API](/claude-capabilities/api/messages)
- [长上下文 · RAG](/claude-capabilities/core/long-context)

## 下一步

- Token 用量 → [Token Counting](/claude-capabilities/api/token-counting)
- Admin 报告 → [Admin & Usage](/claude-capabilities/api/admin-usage)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- PDF 处理 → [Vision · PDF 实战](/claude-capabilities/core/vision#四多图实战)
- 长 context 文档处理 → [长上下文](/claude-capabilities/core/long-context)

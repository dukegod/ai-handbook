---
title: Admin & Usage
description: org / workspace 管理端点；用量报告、成本追踪、成员管理实战
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  adminApi: 'https://platform.claude.com/docs/en/api/administration'
  usageApi: 'https://platform.claude.com/docs/en/api/usage'
  accessedAt: 2026-08-07
---

# Admin & Usage

> **TL;DR**：Admin API 用于 **org / workspace 管理**（成员、密钥、用量、计费）——**必须 Admin Key 才能调**（普通 API key 调 403）。Usage API 拉取**详细用量数据**（按模型 / 用户 / 时间拆分），是成本监控 / 报销 / 配额管理的核心。

⏱ 预计阅读时间：4 分钟

## 一、两类端点

| 端点 | 用途 | 鉴权 |
| --- | --- | --- |
| **Admin API** | 成员管理 / 邀请 / 角色 / 工作空间 | Admin Key |
| **Usage API** | 用量报告 / 成本数据 | Admin Key |

**关键**：**普通 `ANTHROPIC_API_KEY` 调 Admin / Usage 端点会 403**——必须用 Admin Key（在 Console 里单独生成）。

```python
import anthropic

# 普通 client（调 Messages / Batch / Files）
client = anthropic.Anthropic()    # 用 ANTHROPIC_API_KEY

# Admin client
admin = anthropic.AnthropicAdmin()  # 用 ANTHROPIC_ADMIN_KEY
```

## 二、Usage 实战

### 1. 拉取月度用量

```python
from datetime import datetime, timedelta

now = datetime.utcnow()
start = (now - timedelta(days=30)).isoformat() + "Z"
end = now.isoformat() + "Z"

usage = admin.usage.reports(
    start_time=start,
    end_time=end,
    bucket_width="1d",       # 按天分组
    models=["claude-sonnet-5-...", "claude-opus-5-..."],   # 可选过滤
)

for bucket in usage.data:
    print(f"{bucket.start_time}: {bucket.input_tokens + bucket.output_tokens} tokens")
```

### 2. 按用户拆分

```python
usage = admin.usage.reports(
    start_time=start,
    end_time=end,
    group_by=["user_id", "model"],   # 多维分组
)
```

### 3. 输出 JSON 到 BI 工具

```python
import json
report = [
    {
        "time": b.start_time,
        "model": b.model,
        "input": b.input_tokens,
        "output": b.output_tokens,
        "cache_read": b.cache_read_input_tokens,
    }
    for b in usage.data
]
with open("usage_report.json", "w") as f:
    json.dump(report, f, indent=2)
```

## 三、Admin 实战

### 1. 邀请成员

```python
invite = admin.organization.invites.create(
    email="alice@company.com",
    role="developer",     # developer / admin / billing
)
print(f"invite id: {invite.id}")
```

### 2. 列出成员

```python
members = admin.organization.members.list()
for m in members.data:
    print(f"{m.email}: {m.role}")
```

### 3. 创建 API key（子用户）

```python
key = admin.organization.api_keys.create(
    name="production-bot",
    workspace_id="ws_01ABC...",
)
print(f"key: {key.id}, secret: {key.secret[:10]}...")
```

## 四、4 个常见坑

**1. 用普通 key 调 Admin**

```python
client = anthropic.Anthropic()    # ANTHROPIC_API_KEY
client.usage.reports(...)         # ❌ 403

# ✅ 用 Admin client
admin = anthropic.AnthropicAdmin()  # ANTHROPIC_ADMIN_KEY
admin.usage.reports(...)
```

**2. `bucket_width` 选错**

```
"1m"  → 按分钟（细粒度，适合实时监控）
"1h"  → 按小时
"1d"  → 按天（默认）
"1mo" → 按月（适合月度账单）
```

**3. 时间窗太大**

```python
# ❌ 拉一年数据（100 万条）
usage = admin.usage.reports(start_time="2025-01-01", end_time="2026-01-01")

# ✅ 按月分次拉
for month_start in month_starts:
    usage = admin.usage.reports(start_time=month_start, end_time=month_end)
```

**4. 不存用量数据**

```python
# ❌ 只看实时
print(usage.data[0].input_tokens)

# ✅ 持久化到 DB / BI 工具（成本趋势分析）
db.insert("usage_reports", report)
```

## 参考

- [Anthropic Docs · Admin API](https://platform.claude.com/docs/en/api/administration)（访问于 2026-08-07）
- [Anthropic Docs · Usage API](https://platform.claude.com/docs/en/api/usage)（访问于 2026-08-07）
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- [Messages API](/claude-capabilities/api/messages)

## 下一步

- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
- v0.3.2.2 收官 → [Messages API](/claude-capabilities/api/messages) 链回首页
- v0.3.2.3 SDK 7 篇规划

## 如果你想

- 成本拆分到 BI 工具 → [成本与 Token 管理 · 月度拆分](/claude-code/basics/cost-and-tokens)
- 用量告警 → [Admin · 配额管理](#)
- 切到 SDK 实战 → [Python SDK](/claude-capabilities/sdk/python-sdk)

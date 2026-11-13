---
title: Admin & Usage
description: org / workspace 管理端点；用量报告、成本追踪、成员管理实战
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核模型 ID、Admin / Usage 端点与参数、鉴权口径；示例按官方文档改写，未在本机实跑（需 Admin Key 与真实 org）'
  claudeCode: 2.1.319
  model: claude-opus-5-5
  adminApi: 'https://platform.claude.com/docs/en/manage-claude/admin-api'
  usageApi: 'https://platform.claude.com/docs/en/manage-claude/usage-cost-api'
  accessedAt: 2026-11-13
---

# Admin & Usage

> **TL;DR**：Admin API 用于 **org / workspace 管理**（成员、密钥、用量、计费）——**必须 Admin Key 才能调**（普通 API key 调 403）。Usage API 拉取**详细用量数据**（按模型 / 用户 / 时间拆分），是成本监控 / 报销 / 配额管理的核心。

⏱ 预计阅读时间：4 分钟

## 一、两类端点

| 端点 | 用途 | 鉴权 |
| --- | --- | --- |
| **Admin API** | 成员管理 / 邀请 / 角色 / 工作空间 | Admin Key |
| **Usage API** | 用量报告 / 成本数据 | Admin Key |

**关键**：**普通 API key（`sk-ant-api...`）调 Admin / Usage 端点会被拒（403）**——必须用 Admin API key（`sk-ant-admin...`）或带 `org:admin` scope 的 OAuth token；反过来 Admin 凭据也不能调 Messages API。

> **2026-11-13 复核**：Admin 端点在 SDK 里挂 **`client.organization.*`**（不是 `client.beta.organization`）；**用量 / 成本报告不在 Admin SDK 里**，得直接打 `GET /v1/organizations/usage_report/messages`。Usage and Cost API 已标 **legacy**——新集成建议直接上 [Usage and Cost Analytics API](https://platform.claude.com/docs/en/manage-claude/usage-cost-analytics-api)。

```python
import anthropic

# 普通 client（调 Messages / Batch / Files）
client = anthropic.Anthropic()    # 用 ANTHROPIC_API_KEY

# Admin 端点：client.organization.*（需 Admin API key）
org = client.organization.retrieve()
print(org.name)
```

## 二、Usage 实战

### 1. 拉取月度用量

用量报告不在 SDK 里，用裸 HTTP 打 `/v1/organizations/usage_report/messages`：

```python
import httpx
from datetime import datetime, timedelta, timezone

ADMIN_KEY = "sk-ant-admin..."     # 或 org:admin scope 的 OAuth token

def usage_report(**params):
    return httpx.get(
        "https://api.anthropic.com/v1/organizations/usage_report/messages",
        params=params,
        headers={"x-api-key": ADMIN_KEY, "anthropic-version": "2026-10-21"},
    ).json()

now = datetime.now(timezone.utc)
start = (now - timedelta(days=30)).isoformat()
end = now.isoformat()

report = usage_report(
    starting_at=start,
    ending_at=end,
    bucket_width="1d",                    # 按天分组
    models=["claude-sonnet-5-5", "claude-opus-5-5"],   # 可选过滤
)

for bucket in report["data"]:
    for item in bucket["results"]:
        tokens = item["uncached_input_tokens"] + item["output_tokens"]
        print(bucket["starting_at"], item["model"], tokens)
```

### 2. 按用户拆分

`group_by[]` 的合法维度：`account_id` / `api_key_id` / `workspace_id` / `model` / `service_tier` / `context_window` / `inference_geo` / `speed` / `service_account_id`。

```python
report = usage_report(
    starting_at=start,
    ending_at=end,
    group_by=["account_id", "model"],   # 多维分组
)
```

### 3. 输出 JSON 到 BI 工具

```python
import json
rows = [
    {
        "time": bucket["starting_at"],
        "model": item["model"],
        "input": item["uncached_input_tokens"],
        "output": item["output_tokens"],
        "cache_read": item["cache_read_input_tokens"],
    }
    for bucket in report["data"]
    for item in bucket["results"]
]
with open("usage_report.json", "w") as f:
    json.dump(rows, f, indent=2)
```

## 三、Admin 实战

### 1. 邀请成员

```python
invite = client.organization.invites.create(
    email="alice@company.com",
    role="developer",     # developer / admin / billing
)
print(f"invite id: {invite.id}")
```

### 2. 列出成员

```python
# limit 是分页大小，不是总数——SDK 会自动翻页
for user in client.organization.users.list(limit=10):
    print(f"{user.email}: {user.role}")
```

### 3. API key：Console 建，API 管

⚠ **Admin API 不能创建 API key**——key 在 Claude Console 里建，API 只能读、改名、改状态。

```python
for key in client.organization.api_keys.list():
    print(key.id, key.name, key.status)

client.organization.api_keys.update("apikey_01...", status="inactive", name="旧机器人")
```

## 四、4 个常见坑

**1. 用普通 key 调 Admin**

```python
client = anthropic.Anthropic()           # 普通 API key
client.organization.users.list()         # ❌ 403

# ✅ 用 Admin API key
admin = anthropic.Anthropic(api_key="sk-ant-admin...")
admin.organization.users.list()
```

**2. `bucket_width` 选错**

只有 `1m` / `1h` / `1d` 三档，**没有 `1mo`**——按月出账请用 `1d` 拉 31 天。

```
"1m"  → 按分钟（默认 60 分钟，最多 1440）
"1h"  → 按小时（默认 24 小时，最多 168）
"1d"  → 按天（默认 7 天，最多 31）
```

**3. 时间窗太大**

桶数超上限会被截断或报错——按月分次拉，别一次要一年。

```python
# ❌ 1d 粒度最多 31 个桶
usage_report(starting_at="2025-01-01", ending_at="2026-01-01", bucket_width="1d")

# ✅ 按月分次拉
for month_start in month_starts:
    usage_report(starting_at=month_start, ending_at=month_end, bucket_width="1d")
```

响应里有 `has_more` / `next_page`，翻页把 `next_page` 传回 `page` 参数继续拉。

**4. 不存用量数据**

```python
# ❌ 只看实时
print(report["data"][0]["results"][0]["uncached_input_tokens"])

# ✅ 持久化到 DB / BI 工具（成本趋势分析）
db.insert("usage_reports", rows)
```

## 参考

- [Anthropic Docs · Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api)（访问于 2026-11-13）
- [Anthropic Docs · Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api)（访问于 2026-11-13）
- [Anthropic Docs · Get Messages Usage Report](https://platform.claude.com/docs/en/api/beta/organization/usage_report/retrieve_messages)（访问于 2026-11-13）
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

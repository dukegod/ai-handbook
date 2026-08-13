---
title: Claude Code SDK
description: 把 Claude Code 作为库嵌入你的应用；子 agent / 工作流自动化实战
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  claudeCodeSdk: 'https://docs.claude.com/en/docs/claude-code/sdk'
  accessedAt: 2026-08-07
---

# Claude Code SDK

> **TL;DR**：Claude Code SDK 让你**把 Claude Code 作为库嵌入应用**——调用 `claude_code.run(prompt)` 就能启动一个 Claude Code 子进程跑任务。**适合 CI 自动化、PR 批量处理、自建 coding agent**。

⏱ 预计阅读时间：4 分钟

## 一、核心能力

```python
from claude_code_sdk import ClaudeCode

cc = ClaudeCode(working_dir="/path/to/project")

# 跑任务
result = cc.run(
    "审查 src/auth/ 下的所有文件，按严重性排序安全问题",
    allowed_tools=["Read", "Grep", "Glob"],   # 限定权限
)
print(result.text)
```

**本质**：SDK 启动 `claude` CLI 子进程，传入 prompt + 权限，等结果。

## 二、3 个实战场景

### 1. CI 自动 PR 审查

```python
# .github/workflows/pr-review.yml
from claude_code_sdk import ClaudeCode

def review_pr(diff: str) -> str:
    cc = ClaudeCode(working_dir=".")
    return cc.run(
        f"审查这个 diff，找安全问题：\n\n{diff}",
        allowed_tools=["Read", "Grep"],
    ).text
```

```yaml
# GitHub Actions
- name: Claude Code Review
  run: python review.py
```

### 2. 批量代码迁移

```python
# 100 个老旧文件从 Flask 迁到 FastAPI
import os
for f in flask_files:
    cc = ClaudeCode(working_dir="/path/to/repo")
    result = cc.run(
        f"把 {f} 从 Flask 迁到 FastAPI，保持 API 兼容",
        allowed_tools=["Read", "Write", "Bash"],
    )
    print(f"{f}: {result.summary}")
```

### 3. 自建 coding agent UI

```python
# Web 应用接 Claude Code SDK
@app.post("/api/code")
def code_endpoint(prompt: str):
    cc = ClaudeCode(working_dir=USER_REPO)
    result = cc.run(prompt)
    return {"text": result.text, "diff": result.diff}
```

## 三、权限控制

```python
cc.run(
    prompt="修这个 bug",
    allowed_tools=["Read", "Edit"],      # 只读 + 编辑，不能跑 Bash
    disallowed_tools=["WebFetch"],       # 禁外网
    auto_approve=False,                  # 每次 Edit 弹权限（默认）
)
```

详见 [权限系统](/claude-code/basics/permissions)。

## 四、3 个实战模式

### 模式 1：headless 跑 Claude Code

```python
# 等同于 `claude -p "..."`
result = cc.run("分析这个项目用什么框架")
print(result.text)
```

详见 [Headless 模式](/claude-code/advanced/headless)。

### 模式 2：sub-agent 编排

```python
# 主 agent 调 sub-agent
result = cc.run(
    "用 general-purpose subagent 找 src/ 下所有 hardcoded secret",
    subagent_type="general-purpose",
)
```

详见 [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)。

### 模式 3：持久化 session

```python
# 多轮对话（保留 context）
session = cc.create_session()
session.run("先看 src/auth.ts")
session.run("重构为 async + Result 类型")
```

## 五、4 个常见坑

**1. 子进程成本失控**

```python
# ❌ 跑长任务不设超时
cc.run("...")   # 跑到 1 小时

# ✅ 设 max_duration
cc.run("...", max_duration=600)   # 10 分钟超时
```

**2. 权限过大**

```python
# ❌ 给所有权限
allowed_tools="*"
# ✅ 最小权限（按任务限定）
allowed_tools=["Read", "Grep", "Edit"]
```

**3. working_dir 错了**

```python
# ❌ working_dir 没设
cc.run("分析 src/")   # 找不到 src/

# ✅ 显式设
cc = ClaudeCode(working_dir="/path/to/repo")
```

**4. 同步阻塞 event loop**

SDK 同步调用——**async 上下文里用 `asyncio.to_thread`**：

```python
import asyncio
result = await asyncio.to_thread(cc.run, "...")
```

## 参考

- [Anthropic Docs · Claude Code SDK](https://docs.claude.com/en/docs/claude-code/sdk)（访问于 2026-08-07）
- [Headless 模式](/claude-code/advanced/headless)
- [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- [权限系统](/claude-code/basics/permissions)
- [Python SDK](/claude-capabilities/sdk/python-sdk)
- [SDK 概览](/claude-capabilities/sdk/overview)

## 下一步

- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
- Headless 深入 → [Headless 模式](/claude-code/advanced/headless)
- v0.3.2.3 收官 → [SDK 概览](/claude-capabilities/sdk/overview)

## 如果你想

- CI 自动化 → [自动化与 CI](/claude-code/advanced/automation)
- Git workflow → [Git Workflow](/claude-code/advanced/git-workflow)
- worktree 多分支 → [Worktree](/claude-code/advanced/worktree)

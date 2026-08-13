---
title: Tool Runner
description: 单 tool 隔离执行沙箱；不可信 code / 外部输入的安全执行实战
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  toolRunner: 'https://docs.claude.com/en/docs/build-with-claude/tool-runner'
  accessedAt: 2026-08-07
---

# Tool Runner

> **TL;DR**：Tool Runner 是 Anthropic 提供的**单 tool 隔离执行沙箱**——Claude 生成的 code 或外部输入**在沙箱里跑**，不污染主进程。**适合不可信 code**（用户输入 LLM 生成的、第三方插件 code）。

⏱ 预计阅读时间：3 分钟

## 一、核心问题

Claude tool use 时，**Claude 生成的 code 你敢直接跑吗**？

```python
# Claude 生成的 tool input
tool_input = {"command": "rm -rf /tmp/important_data"}

# ❌ 直接执行
subprocess.run(tool_input["command"], shell=True)   # 删你数据

# ✅ Tool Runner 沙箱
runner.execute(tool_input)   # 沙箱内运行，权限受控
```

## 二、Tool Runner 实战

```python
from claude_tool_runner import ToolRunner, SandboxConfig

config = SandboxConfig(
    allowed_commands=["ls", "cat", "grep"],   # 白名单
    timeout=10,                                # 10s 超时
    max_memory_mb=128,                         # 内存上限
    network="none",                            # 禁止网络
)

runner = ToolRunner(config)

# 工具实现
def execute_bash(command: str) -> str:
    result = runner.execute(command)
    return result.stdout

# 配到 Tool Use
TOOLS = [{
    "name": "bash",
    "description": "执行 shell 命令",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]

# Claude 调工具时，runner 拦截执行
```

## 三、3 个实战场景

### 1. 用户上传 code 让你跑

```python
# 用户上传的 Python 脚本
user_code = "print('hello')"

# ✅ 沙箱跑
result = runner.execute(f"python3 -c '{user_code}'")
print(result.stdout)   # "hello\n"
# 不会污染主进程
```

### 2. LLM 生成 SQL 查数据库

```python
# Claude 生成的 SQL
sql = "SELECT * FROM users; DROP TABLE users;"   # 注入！

# ✅ 沙箱用 read-only 用户跑
runner_db = ToolRunner(SandboxConfig(
    db_user="readonly",
    allowed_tables=["users", "orders"],
))
runner_db.execute_sql(sql)   # DROP 失败，只读返回
```

### 3. 多租户隔离

```python
# 租户 A 的工具实例
runner_a = ToolRunner(SandboxConfig(workspace="/tmp/tenant_a/"))

# 租户 B 的工具实例（独立文件系统）
runner_b = ToolRunner(SandboxConfig(workspace="/tmp/tenant_b/"))
# 互不干扰
```

## 四、4 个常见坑

**1. 沙箱配置过松**

```python
# ❌ 几乎没限制
SandboxConfig(allowed_commands="*", network="*")

# ✅ 最小权限
SandboxConfig(allowed_commands=["ls", "cat", "grep"], network="none")
```

**2. 超时设太大**

```python
# ❌ timeout=3600（1 小时）—— 资源滥用
# ✅ timeout=10-30
```

**3. 内存无上限**

```python
# ❌ 内存炸弹
SandboxConfig(max_memory_mb=999999)
# ✅ max_memory_mb=128
```

**4. 沙箱逃逸漏洞**

Tool Runner 是**缓解层**，不是**绝对安全**——定期更新 SDK，修最新漏洞。

## 参考

- [Anthropic Docs · Tool Runner](https://docs.claude.com/en/docs/build-with-claude/tool-runner)（访问于 2026-08-07）
- [Tool Use API](/claude-capabilities/api/tool-use)
- [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- [SDK 概览](/claude-capabilities/sdk/overview)

## 下一步

- 托管 agent → [Managed Agents](/claude-capabilities/sdk/managed-agents)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- Claude Code 内置权限系统 → [权限系统](/claude-code/basics/permissions)
- 危险操作拦截 → [Permissions · 实战模式](/claude-code/basics/permissions)

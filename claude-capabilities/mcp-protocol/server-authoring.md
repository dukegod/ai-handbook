---
title: Server 作者指南
description: 写高质量 MCP Server 的 8 条准则——工具设计 / 错误处理 / 性能 / 安全 / 文档
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  serverAuthoring: 'https://modelcontextprotocol.io/specification/2025-06-18/server'
  examples: 'https://github.com/modelcontextprotocol/servers'
  accessedAt: 2026-08-07
---

# Server 作者指南

> **TL;DR**：写高质量 MCP Server 的 **8 条准则**——工具原子化、JSON Schema 严格、错误信息具体、并发安全、权限白名单、资源受限、文档化描述、版本兼容。与 [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec) 配套使用：协议告诉你"消息怎么走"，本文告诉你"工具怎么写好"。

⏱ 预计阅读时间：5 分钟

## 一、为什么需要准则

```python
# ❌ 烂 Server：1 个工具做 5 件事
{"name": "do_everything", "description": "工具"}


# ✅ 好 Server：5 个工具各做 1 件事
{"name": "search_issues"}
{"name": "read_issue"}
{"name": "create_issue"}
{"name": "update_issue"}
{"name": "close_issue"}
```

**坏 Server 的代价**：
- Claude 不知道何时调哪个
- 用户无法预测结果
- 错误处理混乱
- 难测试

## 二、8 条准则

### 准则 1：工具原子化

```python
# ❌ 1 个工具 = 1 团
{"name": "manage_user", "description": "管理用户"}

# ✅ 1 个工具 = 1 个原子操作
{"name": "create_user"}
{"name": "read_user"}
{"name": "update_user"}
{"name": "delete_user"}
```

详见 [MCP 协议规范 · 5 个常见坑](/claude-capabilities/mcp-protocol/protocol-spec#七4-个常见坑)。

### 准则 2：JSON Schema 严格

```python
# ❌ 模糊
{"name": "search", "inputSchema": {"type": "object"}}

# ✅ 严格
{
    "name": "search_jira_issues",
    "inputSchema": {
        "type": "object",
        "properties": {
            "project_key": {"type": "string", "pattern": "^[A-Z]{2,10}$"},
            "query": {"type": "string", "minLength": 1, "maxLength": 200},
            "max_results": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
            "status": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
        },
        "required": ["project_key", "query"],
        "additionalProperties": False,    # 禁额外字段
    },
}
```

### 准则 3：description 写具体

```python
# ❌ 模糊 → Claude 永不调
{"description": "搜索"}

# ✅ 具体 + 关键词
{"description": "在指定 GitHub 仓库按关键词搜索 issue（含标题、标签、状态、作者）。用户问「XX 项目有没相关 bug」「查 issue 列表」时用。"}
```

详见 [Cookbook · 写你的第一个 MCP Server](/cookbook/build-first-mcp-server)。

### 准则 4：错误信息具体

```python
# ❌ 模糊错误
raise Exception("Failed")

# ✅ 具体错误 + 建议
raise ToolError(
    f"未找到项目 {project_key}。"
    f"现有项目：{[p.key for p in projects]}。"
    f"如需创建新项目，联系管理员。"
)
```

**实战**：
- 错误信息要**让 Claude 能 self-correct**
- 包含**已尝试的状态** + **下一步建议**

### 准则 5：并发安全

```python
# ❌ 全局可变状态
state = {}

@mcp.tool()
def read_state():
    return state["key"]   # 并发不安全

# ✅ 每次调用独立 / 锁保护
import threading
state_lock = threading.Lock()

@mcp.tool()
def update_state(key: str, value: str):
    with state_lock:
        state[key] = value
    return "ok"
```

### 准则 6：权限白名单

```python
# ❌ 默认全权限
@mcp.tool()
def run_command(command: str):
    return subprocess.run(command, shell=True)   # rm -rf /

# ✅ 白名单
ALLOWED = {"ls", "cat", "grep", "find"}

@mcp.tool()
def run_command(command: str):
    cmd = command.split()[0]
    if cmd not in ALLOWED:
        raise ToolError(f"不允许命令：{cmd}。允许：{ALLOWED}")
    return subprocess.run(command, shell=True, capture_output=True, text=True)
```

详见 [Tool Runner · 沙箱](/claude-capabilities/sdk/tool-runner)。

### 准则 7：资源受限

```python
# ❌ 无限大输出
@mcp.tool()
def read_file(path: str):
    return Path(path).read_text()    # 读 1GB 文件炸

# ✅ 限大小
MAX_SIZE = 10 * 1024 * 1024   # 10 MB

@mcp.tool()
def read_file(path: str, max_lines: int = 1000):
    p = Path(path)
    if p.stat().st_size > MAX_SIZE:
        raise ToolError(f"文件过大（>{MAX_SIZE} bytes），请指定 max_lines")
    lines = p.read_text().splitlines()[:max_lines]
    return "\n".join(lines)
```

### 准则 8：版本兼容

```python
# 协议版本协商
@mcp.tool()
def list_data(version: str = "latest"):
    if version == "v1":
        return get_v1_data()    # 老格式
    elif version == "v2":
        return get_v2_data()    # 新格式
    else:
        raise ToolError(f"未知 version: {version}")
```

详见 [MCP 协议规范 · 版本协商](/claude-capabilities/mcp-protocol/protocol-spec#六协议版本)。

## 三、测试

```python
# test_server.py —— 不依赖 Claude 直接测
import asyncio
from server import mcp

async def test_list_terms():
    result = await mcp.call_tool("list_terms", {"path": "contributing/glossary.md"})
    assert len(result) > 0
    assert "Anthropic" in [t["term"] for t in result]

asyncio.run(test_list_terms())
```

详见 [examples/glossary-mcp-server · 自测](/examples/glossary-mcp-server/README#为什么-parser-和-server-分层)。

## 四、4 个常见坑

**1. 工具太多（> 20）**

Claude 注意力分散——**精简到 5-10 个最常用**。

**2. 同步阻塞**

```python
# ❌ 同步阻塞 stdio
@mcp.tool()
def slow_tool():
    time.sleep(60)    # Claude 卡 60s

# ✅ async
@mcp.tool()
async def slow_tool():
    await asyncio.sleep(60)
```

**3. 资源泄漏**

```python
# ❌ 每次调用打开文件不关
@mcp.tool()
def read_file(path):
    return open(path).read()    # file handle 泄漏

# ✅ context manager
@mcp.tool()
def read_file(path):
    with open(path) as f:
        return f.read()
```

**4. 没日志**

```python
# ❌ 静默失败
@mcp.tool()
def fetch_data():
    return requests.get(url).json()    # 失败时不知道

# ✅ 记日志
import logging
logger = logging.getLogger(__name__)

@mcp.tool()
def fetch_data():
    try:
        result = requests.get(url, timeout=10).json()
        logger.info(f"fetched {len(result)} items")
        return result
    except Exception as e:
        logger.error(f"fetch failed: {e}")
        raise ToolError(f"网络请求失败：{e}")
```

## 参考

- [MCP Spec · Server 规范](https://modelcontextprotocol.io/specification/2025-06-18/server)（访问于 2026-08-07）
- [MCP 官方 Servers 列表](https://github.com/modelcontextprotocol/servers)
- [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- [Cookbook · 写你的第一个 MCP Server](/cookbook/build-first-mcp-server)
- [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 下一步

- Client 实现 → [Client 实现要点](/claude-capabilities/mcp-protocol/client-implementation)
- 实战 → [Cookbook · 写你的第一个 MCP Server](/cookbook/build-first-mcp-server)
- Tool Runner 沙箱 → [Tool Runner](/claude-capabilities/sdk/tool-runner)

## 如果你想

- Claude Code 接入 MCP → [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp)
- 切到协议层 → [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- 工具使用安全 → [Tool Runner 沙箱](/claude-capabilities/sdk/tool-runner)

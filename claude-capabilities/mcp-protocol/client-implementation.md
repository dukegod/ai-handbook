---
title: Client 实现要点
description: 实现 MCP Client 的 6 个坑——握手 / capabilities / transport 选择 / 资源管理 / 错误处理
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  clientSpec: 'https://modelcontextprotocol.io/specification/2025-06-18/client'
  accessedAt: 2026-08-07
---

# Client 实现要点

> **TL;DR**：实现 MCP Client 的 **6 个坑**——握手顺序、capabilities 协商、transport 选择、资源管理、错误处理、版本兼容。Claude Code 本身就是一个 MCP Client，**但你可以自己实现**（如自定义 host / IDE 集成）。

⏱ 预计阅读时间：4 分钟

## 一、Claude Code 已经是 Client

`claude mcp add xxx -- command` 时，Claude Code 自动作为 MCP Client 启动。**多数场景你不需要自己实现**——除非：

- 自建 IDE / Editor 集成
- 自建 host（Claude Code 替代品）
- 自建自动化测试框架
- 研究 MCP 协议本身

## 二、最小 Client 实战（Python）

```python
import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    # 启动 server 子进程
    server_params = StdioServerParameters(
        command="python3",
        args=["/path/to/glossary_mcp_server/main.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. 握手
            await session.initialize()

            # 2. 列工具
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            # 3. 调工具
            result = await session.call_tool("list_terms", {"path": "contributing/glossary.md"})
            for content in result.content:
                if content.type == "text":
                    data = json.loads(content.text)
                    print(f"Found {len(data)} terms")

asyncio.run(main())
```

## 三、6 个常见坑

### 坑 1：握手顺序错

```python
# ❌ initialize 后没等响应
await session.initialize()
await session.list_tools()    # server 还没收到 notifications/initialized

# ✅ SDK 帮你处理：initialize() 内部已发 notifications/initialized
await session.initialize()
await session.list_tools()    # 正常
```

详见 [MCP 协议规范 · 握手协议](/claude-capabilities/mcp-protocol/protocol-spec#三握手协议)。

### 坑 2：capabilities 没声明

```python
# Client 端 initialize 时
{
    "capabilities": {
        "sampling": {},    # 如果要用 sampling（让 server 让 client 调 LLM），必须声明
        "roots": {"listChanged": False},
    }
}
```

**capabilities 决定能调什么**——不声明的能力可能 server 拒绝。

### 坑 3：transport 选错

| 场景 | 选 |
| --- | --- |
| **本地进程** | **stdio**（最简单） |
| 远程服务（HTTP API） | HTTP + SSE |
| 远程服务（普通 HTTP） | HTTP（无 SSE，polling） |

详见 [Claude Code · MCP 传输方式](/claude-code/mcp/transports)。

### 坑 4：资源泄漏

```python
# ❌ 不关 session
session = ClientSession(...)
await session.initialize()
# ... 用完忘关

# ✅ context manager
async with ClientSession(read, write) as session:
    await session.initialize()
    # ... 用
# 自动关
```

### 坑 5：错误处理

```python
# ❌ 失败直接 raise
result = await session.call_tool(...)

# ✅ 处理 MCP 错误
try:
    result = await session.call_tool("read_file", {"path": "/bad"})
except McpError as e:
    if e.code == -32602:    # Invalid params
        print(f"参数错：{e.message}")
    elif e.code == -32000:  # Server-defined
        print(f"Server 错：{e.message}")
    else:
        raise
```

### 坑 6：版本不兼容

```python
# Server 只支持 2025-03-26，client 用 2025-06-18
# → 失败
# ✅ 协商：从最新到最旧，client 决定降级
```

详见 [MCP 协议规范 · 版本](/claude-capabilities/mcp-protocol/protocol-spec#六协议版本)。

## 四、3 个实战场景

### 1. 集成到 IDE

```python
# VSCode 扩展里启动 MCP Client
class MCPClientProvider:
    def __init__(self, server_command):
        self.session = None
        self.server_params = StdioServerParameters(command=server_command)

    async def start(self):
        self.transport = stdio_client(self.server_params)
        read, write = await self.transport.__aenter__()
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()

    async def get_tools(self):
        result = await self.session.list_tools()
        return result.tools
```

### 2. 自动化测试 MCP Server

```python
# 测试 server 实现的正确性
import pytest

@pytest.mark.asyncio
async def test_server_list_tools():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert "list_terms" in [t.name for t in tools.tools]
```

### 3. 自建 Host

```python
# 自建聊天 UI 后端，前端发请求 → 你的 host → MCP server → Claude
class HostServer:
    def __init__(self):
        self.mcp_client = MCPClientProvider(...)

    async def handle_user_query(self, query):
        await self.mcp_client.start()
        tools = await self.mcp_client.get_tools()
        # 调 Anthropic API + 工具循环
        ...
```

## 五、4 个常见坑

**1. async 上下文混 sync**

```python
# ❌ sync 函数里 await
def get_tools():
    return await session.list_tools()    # TypeError

# ✅ async 函数
async def get_tools():
    return await session.list_tools()
```

**2. 不超时**

```python
# ❌ 死等
result = await session.call_tool(...)

# ✅ 设超时
import asyncio
try:
    result = await asyncio.wait_for(
        session.call_tool("read_file", {"path": "/huge"}),
        timeout=10,
    )
except asyncio.TimeoutError:
    print("Tool 10s 未响应")
```

**3. 跨进程通信无错误日志**

```python
# server 端日志
import logging
logger = logging.getLogger("mcp-server")
logger.setLevel(logging.INFO)
# 输出到 stderr —— client 端能看到
```

**4. 资源能力没声明**

```python
# Client 想用 resources（读 server 端文件）必须声明
{"capabilities": {"resources": {"subscribe": True}}}
```

## 参考

- [MCP Spec · Client 规范](https://modelcontextprotocol.io/specification/2025-06-18/client)（访问于 2026-08-07）
- [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- [Server 作者指南](/claude-capabilities/mcp-protocol/server-authoring)
- [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp)
- [Claude Code · MCP 传输方式](/claude-code/mcp/transports)

## 下一步

- Server 端 → [Server 作者指南](/claude-capabilities/mcp-protocol/server-authoring)
- 实战示例 → [Cookbook · 写你的第一个 MCP Server](/cookbook/build-first-mcp-server)
- Claude Code 集成 → [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp)

## 如果你想

- 协议层细节 → [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- 切到工具使用 → [Tool Use 协议](/claude-capabilities/core/tool-use)

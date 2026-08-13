# glossary-mcp-server

一个最小可复现的 MCP Server 示例——把仓库内 `contributing/glossary.md`（写作术语表）暴露成 3 个 tool，让 Claude Code 在对话中能直接查术语 / 查易错对照。

> **配套教程**：[写你的第一个 MCP Server](../../cookbook/build-first-mcp-server)（位于主 wiki 的 `cookbook/`）

## 它做了什么

提供 3 个 tool（均通过 stdio 与 Claude Code 通信）：

| Tool | 用途 |
| --- | --- |
| `list_terms` | 列出术语表所有条目 `{term, category, definition, note}` |
| `list_common_mistakes` | 列出「常见易错」一节的 ❌ → ✅ 对照清单 |
| `find_term` | 按关键词查术语：先精确匹配（大小写不敏感），没有再退化到子串匹配 |

## 目录结构

```
glossary-mcp-server/
├── main.py                    # MCP Server 入口（mcp.server.mcpserver.MCPServer）
├── glossary_parser.py         # 纯函数解析器（标准库，无 MCP 依赖）
├── test_glossary_parser.py    # 解析器自测（标准库，5 个 test case）
├── pyproject.toml             # uv 项目元数据
├── uv.lock                    # 锁定的依赖图（Python 3.14 / mcp[cli]>=2.0.0）
└── .python-version            # 3.14
```

## 为什么 parser 和 server 分两层

- `glossary_parser.py` 只做字符串处理，标准库之外无依赖，**不用装 MCP 也能单测**
- `main.py` 只做 MCP 包装（`@mcp.tool()` 装饰器 + `mcp.run()`），**协议层改了不动解析逻辑**
- 解析器的边界条件靠 `test_glossary_parser.py` 锁定；MCP 层只负责"传对收对"

## 装依赖

需要 [uv](https://docs.astral.sh/uv/)（一次性装好后所有命令都从这里走）：

```bash
uv sync
```

> Python 3.14 由 `.python-version` 锁版本，uv 会自动下载并建 `.venv/`。

## 跑测试（不需要 MCP 知识）

```bash
uv run test_glossary_parser.py
# 预期：5/5 通过
```

## 起 server

```bash
uv run main.py
# 进程会挂起等 stdio——这是正常的，MCP server 永远以客户端主动连接为生
# 用 Ctrl+C 退出
```

## 接入 Claude Code

在项目根目录执行（路径改成你本机绝对路径）：

```bash
claude mcp add glossary -- uv --directory /Users/you/path/to/glossary-mcp-server run main.py
```

或者最简形式（cd 到 examples/glossary-mcp-server 后）：

```bash
claude mcp add glossary -- $(pwd)/.venv/bin/python3 $(pwd)/main.py
```

接好以后 `claude` 起一个新对话，验证：

```text
请用 glossary 的 list_terms 列一下术语表。
```

应该返回一份术语清单；返回即说明握手 + tool 调度都通。

## 关键设计点

1. **path 默认值是相对 CWD**——`contributing/glossary.md` 假设 Claude Code 在仓库根启子进程；如果在别处连，请传绝对路径。
2. **instructions 字段给客户端提示**——Claude Code 看到 `instructions` 才知道"什么场景下优先用本服务"，比纯 tool 列表更主动。
3. **返回值是 `list[dict]`**——MCP 协议会自动 JSON 序列化；dict 的 key 顺序与 parser 一致（term / category / definition / note），客户端按 key 取值即可。
4. **stdio 而不是 SSE / HTTP**——Claude Code 默认走 stdio；改成 HTTP 需要 `mcp.run(transport="streamable-http")` 并配端口。

## 已知限制

- **依赖 Python 3.14**：mcp 2.0 的依赖树要求 3.14。如果团队用 3.11/3.12，pin `mcp<2.0` 走 1.x 兼容分支（API 略有差异）。
- **不带 OAuth / 鉴权**：本地 stdio 不需要；如果改成远程 HTTP 部署，要补 `auth_server_provider`。
- **一次只解析一个文件**：`path` 是单文件路径，glossary 拆成多文件的话 parser 也要升级。

## 参考

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

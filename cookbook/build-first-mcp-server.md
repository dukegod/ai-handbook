---
title: 写你的第一个 MCP Server
description: Python + mcp[cli]>=2.0，stdio 接入 Claude Code；以仓库内 glossary-mcp-server 为实例，30 分钟
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  mcpSdk: 'mcp[cli]>=2.0.0'
  python: '3.14'
  officialDocs: 'https://modelcontextprotocol.io/'
  accessedAt: 2026-08-06
---

# 写你的第一个 MCP Server

> **目标**：跟着做完，你会从零写一个最小的 MCP Server（含解析器、测试、MCP 包装），并通过 `claude mcp add` 接入 Claude Code，在对话里调通至少 1 个 tool——全程约 30 分钟。

⏱ 预计阅读时间：8 分钟 · 动手 30 分钟

## 你将做到

- ✅ 用 `uv` 起一个 Python 项目（独立可复现，跟主项目隔离）
- ✅ 写**先于 MCP 的纯函数解析器**——不装 mcp 包也能单测
- ✅ 用 `mcp.server.mcpserver.MCPServer` 把纯函数包成 tool
- ✅ `claude mcp add` 接进去，对话里验证一次

## 前置检查清单

- [ ] 装好 [uv](https://docs.astral.sh/uv/)（一次性装好后所有命令都从这里走）
- [ ] Python 3.14 已经在 PATH（mcp[cli]>=2.0 当前锁 3.14）——`python3 --version`
- [ ] 装好 Claude Code v2.1.x：`claude --version`

## 第 1 步：起 uv 项目

```bash
mkdir quote-mcp-server && cd quote-mcp-server
uv init --python 3.14
uv add 'mcp[cli]>=2.0.0'
```

这条建出 `pyproject.toml` / `.python-version` / `.venv/` / `uv.lock`。**锁文件一起入库**——下次 `uv sync` 能完整复现。

## 第 2 步：写纯函数解析器

**关键设计：把"解析"和"MCP 包装"分两层**——前者纯字符串处理、零 MCP 依赖、跑测试不需要 mcp 包；后者只做协议层包装。

新建 `quote_parser.py`：

```python
"""quote_parser.py —— 解析本地 quotes.txt 的纯函数，标准库之外无依赖。"""
from pathlib import Path

def parse_quotes(path: str) -> list[dict]:
    """每行一句；空行 / `#` 开头跳过。返回 [{text, author}]。"""
    items = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if " — " in line:
            text, author = line.split(" — ", 1)
        else:
            text, author = line, ""
        items.append({"text": text.strip(), "author": author.strip()})
    return items

def random_quote(path: str) -> dict:
    import random
    items = parse_quotes(path)
    return random.choice(items) if items else {"text": "", "author": ""}
```

再建一个最小 `quotes.txt`：

```text
Stay hungry, stay foolish. — Steve Jobs
知而不行，等于不知。 — 王阳明
The only way to do great work is to love what you do. — Steve Jobs
```

## 第 3 步：写测试（不需要 MCP）

新建 `test_quote_parser.py`——纯标准库，能不装 mcp 跑：

```bash
cat > test_quote_parser.py <<'EOF'
import tempfile, json
from pathlib import Path
import quote_parser as qp

SAMPLE = """\
# 这条是注释
Stay hungry, stay foolish. — Steve Jobs

知而不行，等于不知。 — 王阳明
"""

def test_parse_skips_comments_and_blank():
    f = Path(tempfile.mkstemp(suffix=".txt")[1])
    f.write_text(SAMPLE, encoding="utf-8")
    items = qp.parse_quotes(str(f))
    assert len(items) == 2
    assert items[0]["author"] == "Steve Jobs"
    assert items[1]["text"] == "知而不行，等于不知。"

def test_random_quote_in_set():
    f = Path(tempfile.mkstemp(suffix=".txt")[1])
    f.write_text(SAMPLE, encoding="utf-8")
    q = qp.random_quote(str(f))
    assert q["text"] in ("Stay hungry, stay foolish.", "知而不行，等于不知。")
EOF
```

跑：

```bash
uv run test_quote_parser.py
# 预期：2/2 通过
```

> 这步**不是可选项**——MCP tool 把内部状态暴露给客户端后，回归测试的成本就上去了。**先把纯函数锁住**，MCP 层只做传参接参。

## 第 4 步：用 MCPServer 包装

新建 `main.py`：

```python
"""main.py —— MCP Server 入口（stdio 模式）。"""
import quote_parser as qp
from mcp.server.mcpserver import MCPServer

DEFAULT_QUOTES = "quotes.txt"

mcp = MCPServer(
    name="quote",
    instructions="查询本地 quotes.txt 的工具集。用户要「来一句鸡汤/格言」时用。",
)

@mcp.tool(description="列出 quotes.txt 所有句子；返回 list[dict]，每条 {text, author}。")
def list_quotes(path: str = DEFAULT_QUOTES) -> list[dict]:
    return qp.parse_quotes(path)

@mcp.tool(description="随机抽一条。")
def random_quote(path: str = DEFAULT_QUOTES) -> dict:
    return qp.random_quote(path)

if __name__ == "__main__":
    mcp.run()  # 默认 stdio
```

注意 3 件事：

- **`name="quote"`** 是给 Claude Code 看到的标识——`claude mcp add quote ...` 的 `quote` 对应这里
- **`instructions`** 告诉客户端"什么场景下优先用本服务"，比单给 tool 列表更主动
- **`mcp.run()`** 默认 stdio——Claude Code 默认走 stdio，**不要改 SSE / HTTP 除非你知道在做什么**

## 第 5 步：手动起一次（验证握手）

```bash
uv run main.py
# 进程挂起等 stdio——这是正常的
# 用 Ctrl+C 退出
```

进程没崩 = import 全通、MCPServer 构造 OK。想看协议层握手是否对，可以模拟 initialize（参考 [glossary-mcp-server README 的验证段](/examples/glossary-mcp-server/README)）。

## 第 6 步：接入 Claude Code

```bash
claude mcp add quote -- uv --directory "$(pwd)" run main.py
```

> 路径写**绝对路径**，别用相对——Claude Code 启子进程时 CWD 不一定是项目根。

接好以后**重启 Claude Code**（`/exit` 再 `claude`），让 mcp 客户端重读配置。

## 第 7 步：对话里验证

新开一个 `claude` 会话：

```text
用 quote 服务给我来一句格言
```

预期：

1. Claude 主动调 `random_quote` tool
2. 你看到工具返回的内容（如 "Stay hungry, stay foolish. — Steve Jobs"）
3. Claude 用自然语言把结果说一遍

**如果没触发**：

- 用 `/mcp list` 看 quote 是不是已注册
- 没注册：检查 `claude mcp add` 命令的 `--` 后那段在 shell 里能不能独立跑（用 `uv --directory "$(pwd)" run main.py` 自己试一次）
- 注册了没触发：看 `instructions` 里是不是有用户会说的关键词（如 "格言"/"鸡汤"）

## 常见错误

**Parser 和 MCP 写在一起**

MCP 协议层一改（SDK 升级、改 transport），业务逻辑也跟着重测。把纯字符串解析拆出来，**业务测试零依赖、跑得快**。

**path 写死绝对路径**

`quotes.txt` 相对 CWD 是对的（Claude Code 在项目根起子进程）；但你写 `Path("/Users/you/quotes.txt")` 换机器就崩。**让 caller 传，default 给相对**。

**忘了锁 Python 版本**

mcp 2.0 依赖 Python 3.14；不在 `.python-version` 锁住，团队另一人 `uv sync` 可能在 3.11 上装不上。**第一步 `uv init --python 3.14` 就把版本锁死**。

**`mcp.run()` 忘了 `if __name__ == "__main__"` 保护**

模块被别的代码 `import main` 时会自动起 server，**会 hang 死调试器**。所有 `mcp.run()` 都包 `if __name__ == "__main__":` 守卫。

**`claude mcp add` 之后没重启 Claude Code**

mcp 客户端在启动时读配置；不重启，新的 server 不会出现在 `/mcp list` 里。

## 参考

- [MCP 协议是什么](/claude-code/mcp/what-is-mcp)
- [MCP 传输方式选型](/claude-code/mcp/transports)
- [Claude Code 接入 MCP Server](/claude-code/mcp/mcp-json-config)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)（访问于 2026-08-06）
- 实战示例：[`examples/glossary-mcp-server`](/examples/glossary-mcp-server/README)

## 下一步

- 学写第一个 Skill → [写你的第一个 Skill](./build-first-skill)
- 想把 MCP server 做成可分发包 → [MCP 调试与鉴权](/claude-code/mcp/auth-and-debug)

## 如果你想

- 写自己的第一个 MCP server 但还没想好工具集 → [官方 Servers 列表](/claude-code/mcp/official-servers) 看成熟形态再裁剪
- 想把多个 MCP server 组合用 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

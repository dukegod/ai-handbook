"""main.py —— glossary-mcp-server 的 MCP Server 入口。

把 glossary_parser.py 的三个纯函数包成 MCP tool，让 Claude Code 在对话中
可以直接查术语、查易错对照。

和 parser 分两层是为了能「不装 MCP / 不起 server」单独跑测试：
    python3 test_glossary_parser.py   # 纯字符串解析逻辑的自测
    python3 main.py                   # stdio 模式起 MCP server

Claude Code 接入：
    claude mcp add glossary -- python3 /绝对路径/main.py

注意：tool 的 `path` 参数默认 `contributing/glossary.md`，是相对**调用方的工作目录**
——Claude Code 启动子进程时 CWD 是仓库根，所以默认能解析；如果在别处用 MCP 客户端
连，建议传绝对路径。
"""
import glossary_parser as gp
from mcp.server.mcpserver import MCPServer

mcp = MCPServer(
    name="glossary",
    instructions=(
        "查询 Claude Handbook 写作术语表（contributing/glossary.md）的工具集。"
        "用户问「XX 怎么写 / 哪个术语是首选 / 这个错在哪」时优先用本服务的 3 个 tool。"
    ),
)

DEFAULT_GLOSSARY_PATH = "contributing/glossary.md"


@mcp.tool(
    description=(
        "列出 contributing/glossary.md 里所有术语，含分类、定义、备注。"
        "返回 list[dict]，每条形如 {term, category, definition, note}。"
    )
)
def list_terms(path: str = DEFAULT_GLOSSARY_PATH) -> list[dict]:
    return gp.parse_glossary(path)


@mcp.tool(
    description=(
        "列出「常见易错」一节里的 ❌→✅ 对照清单。"
        "返回 list[dict]，每条形如 {wrong, right, note}。"
    )
)
def list_common_mistakes(path: str = DEFAULT_GLOSSARY_PATH) -> list[dict]:
    return gp.parse_common_mistakes(path)


@mcp.tool(
    description=(
        "按关键词查术语：先精确匹配（大小写不敏感），没有再退化到术语本体或定义里的子串匹配。"
        "空 query 或全空白返回空列表。"
    )
)
def find_term(query: str, path: str = DEFAULT_GLOSSARY_PATH) -> list[dict]:
    terms = gp.parse_glossary(path)
    return gp.find_term(terms, query)


if __name__ == "__main__":
    mcp.run()  # 默认 stdio，Claude Code 接入直接用

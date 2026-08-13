"""glossary_parser.py —— 纯函数解析 contributing/glossary.md。

和 server.py 分开是为了能不装 mcp 包、不起 server 就单独测试——
纯字符串处理，标准库之外无依赖。server.py 只做 MCP 包装，调用这里的函数。
"""
import re
from pathlib import Path

BACKTICK = re.compile(r"`([^`]*)`")
BOLD = re.compile(r"\*\*(.+?)\*\*")


def _clean_cell(cell):
    """去掉表格单元格里的 markdown 粗体包装，留纯文本用于展示与匹配。"""
    cell = cell.strip()
    m = BOLD.search(cell)
    return m.group(1).strip() if m else cell


def _split_row(line):
    """按 `|` 切一行表格，去掉首尾空 cell。"""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_glossary(path):
    """解析「常见易错」之前的所有 `## 分类` 表格小节，返回术语列表。

    每条：{term, category, definition, note}（note 无第三列时为空字符串）。
    表格之外的小节（如「## 阅读方式」的项目符号列表）没有以 `|` 开头的行，
    自然被跳过，不需要单独判断标题文字。
    """
    text = Path(path).read_text(encoding="utf-8")
    stop = text.find("## 常见易错")
    if stop != -1:
        text = text[:stop]

    terms = []
    category = None
    in_table = False
    header_seen = False
    for line in text.splitlines():
        h2 = re.match(r"^##\s+(.+)$", line)
        if h2:
            category = h2.group(1).strip()
            in_table = False
            header_seen = False
            continue
        if category is None or not line.strip().startswith("|"):
            in_table = False
            header_seen = False
            continue

        cells = _split_row(line)
        if not header_seen:
            header_seen = True  # 这一行是表头（首选写法 | 说明 | ...），跳过
            continue
        if re.match(r"^:?-+:?$", cells[0]):
            in_table = True  # 分隔行 | --- | --- |，之后才是真正数据行
            continue
        if not in_table:
            continue

        term = _clean_cell(cells[0])
        if not term:
            continue
        terms.append(
            {
                "term": term,
                "category": category,
                "definition": cells[1] if len(cells) > 1 else "",
                "note": cells[2] if len(cells) > 2 else "",
            }
        )
    return terms


MISTAKE_LINE = re.compile(r"[❌✘]\s*(.+?)\s*→\s*✅\s*(.+?)\s*$")
TRAILING_NOTE = re.compile(r"[（(](.*)[）)]\s*$")


def parse_common_mistakes(path):
    """解析「## 常见易错」一节的 `- ❌ X → ✅ Y（说明）` 列表。

    每条：{wrong, right, note}。说明括注是可选的，跟在 ✅ 那部分后面。

    已知边界：这份清单里第七条是「中英不加空格」这类整句示范，不是单个
    术语对齐，wrong 字段会带上前面的说明文字——这是本解析器的简化取舍，
    没有为这一种特例再加规则。
    """
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"^## 常见易错\s*$(.*?)(?:\n## |\Z)", text, re.M | re.S)
    if not m:
        return []

    mistakes = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        mm = MISTAKE_LINE.search(line)
        if not mm:
            continue
        wrong_raw, right_raw = mm.group(1), mm.group(2)
        note = ""
        paren = TRAILING_NOTE.search(right_raw)
        if paren:
            note = paren.group(1).strip()
            right_raw = right_raw[: paren.start()]

        def _plain(s):
            return BACKTICK.sub(lambda bm: bm.group(1), s).strip()

        mistakes.append({"wrong": _plain(wrong_raw), "right": _plain(right_raw), "note": note})
    return mistakes


def find_term(terms, query):
    """按 query 查术语——先精确匹配（大小写不敏感），没有再退化到子串匹配
    （匹配术语本身或一句话定义）。空 query 直接返回空列表。"""
    q = query.strip().lower()
    if not q:
        return []
    exact = [t for t in terms if t["term"].lower() == q]
    if exact:
        return exact
    return [t for t in terms if q in t["term"].lower() or q in t["definition"].lower()]

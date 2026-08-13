#!/usr/bin/env python3
"""check_page.py —— 按 Claude Handbook 写作规范给一篇 md 做体检。

依据 contributing/style-guide.md 第十节「PR 前自检 checklist」，
覆盖脚本能自动判断的部分：frontmatter 必填字段、汉字数上限、
术语易错（对齐 contributing/glossary.md「常见易错」）、中英间距、
结尾双组引导（下一步 / 如果你想）。

用法：
    python3 check_page.py <file.md> [file2.md ...]

无第三方依赖，纯标准库——跑在系统自带 Python 3.8+ 即可。

本脚本的规则都是"体检提示"而非"死板判决"——见配套 Cookbook 页
《写你的第一个 Skill》的「踩坑」一节：正则天然分不清"用错术语"和
"举例说明什么是错的"，报告需要人工过一遍再决定改不改。
"""
import re
import sys

REQUIRED_FIELDS = ["title", "description", "audience", "difficulty", "status", "lastUpdated"]
HANZI_LIMIT = 1500

# 章导读（index.md）与 contributing/ 下的元文档不是"某个 Claude Code 行为"的教程，
# 天然没有 verifiedWith 概念——这是本项目已经在用的实际约定，而非本脚本编造。
VERIFIED_WITH_EXEMPT = re.compile(r"(^|/)index\.md$|(^|/)contributing/")

# 术语易错对照，来自 contributing/glossary.md 「常见易错」一节
TERM_RULES = [
    (re.compile(r"Claude\s*公司"), "「Claude 公司」→ 用「Anthropic」"),
    (re.compile(r"ClaudeCode(?!\w)"), "「ClaudeCode」→ 加空格「Claude Code」"),
    (re.compile(r"MCP\s*服务器"), "「MCP 服务器」→ 用「MCP Server」"),
    (re.compile(r"[Cc]luade"), "拼写错误「cluade」→「claude」"),
    (re.compile(r"Opus4\.8|Sonnet5|Haiku4\.5"), "型号名缺空格，如「Opus4.8」→「Opus 4.8」"),
]

ZH = r"[一-鿿]"
EN_NUM = r"[A-Za-z0-9]"
# 中文紧贴英文/数字（任一方向）且中间无空格
SPACING_RULES = [
    re.compile(f"({ZH})({EN_NUM})"),
    re.compile(f"({EN_NUM})({ZH})"),
]

# 命中即视为"合法紧贴"、不报的白名单模式
SPACING_ALLOW = [
    re.compile(r"[⏱🟢🟡🔴✅✘✔📌]"),  # emoji 前缀，紧跟中文是排版惯例
    re.compile(r"第\d"),  # 「第1步」这类序数不强制加空格
]

# 本项目「反例举证」的固定写法：- ❌ 错误写法 → ✅ 正确写法
# 这类行是在**教读者什么是错的**，术语检查应该跳过，否则永远误报。
ANTI_PATTERN_LINE = re.compile(r"[❌✘]")


def _in_corner_quotes(line, start, end):
    """判断 [start, end) 这段是否被同一行内最近的一对「…」包住。

    glossary.md 这类术语表会写「不用『Claude 公司』」来举例什么是错的写法——
    这是在**引用**一个说法，不是在**使用**它，术语检查不该报。
    只看 ❌/✘ 符号覆盖不了这种没有符号、纯引号提及的写法。"""
    open_before = line.rfind("「", 0, start)
    if open_before == -1:
        return False
    if line.rfind("」", 0, start) > open_before:
        return False  # 上一个「已经在到达 start 前闭合，不算包住
    close_after = line.find("」", end)
    if close_after == -1:
        return False
    if "「" in line[end:close_after]:
        return False  # 中间还夹了个新「，边界不清晰，保守起见不跳过
    return True


def split_frontmatter(text):
    """返回 (frontmatter 原文, frontmatter 行数, 正文)。

    行数用来把"正文里第几行"换算回"文件里第几行"——
    第一版脚本忘了这一步，报出来的行号全部偏移了 frontmatter 的长度，
    对照原文件时全对不上。
    """
    m = re.match(r"^---\n(.*?\n)---\n(.*)$", text, re.S)
    if not m:
        return "", 0, text
    fm = m.group(1)
    fm_lines = fm.count("\n") + 2  # + 两行 "---" 分隔符
    return fm, fm_lines, m.group(2)


def _blank(m):
    """把匹配内容替换成等长空白，只留换行符。

    直接删掉代码块会导致后面所有内容的行号往前移——
    第一版就是这么错的：只补偿了 frontmatter 的行数，
    没想到 fenced code block 一删，正文行号跟着全错位。
    挖空而不是删除，行号和汉字计数都不受影响。"""
    return re.sub(r"[^\n]", " ", m.group(0))


def strip_code(body):
    body = re.sub(r"```.*?```", _blank, body, flags=re.S)
    body = re.sub(r"`[^`]*`", _blank, body)
    return body


def strip_anchors(body):
    """去掉 `(...#anchor-slug)` 形式的链接目标——同页锚点 `(#foo)`，
    也包括更常见的跨页锚点 `(./page#foo)` / `(/abs/page#foo)`。

    VitePress 把标题编译成锚点 id 时会拼接多个词（如 `#三session-picker`），
    这类机器生成的复合 token 不是"中英文紧贴的病句"。第一版只摘了裸
    `(#foo)`，漏掉了本站更常用的带路径前缀写法，全部误报。"""
    return re.sub(r"\([^)\n]*#[^)\n]*\)", "()", body)


def count_hanzi(body):
    return len(re.findall(ZH, strip_code(body)))


def check_frontmatter(fm, path):
    problems = []
    for field in REQUIRED_FIELDS:
        if not re.search(rf"^{field}:", fm, re.M):
            problems.append(f"缺少 frontmatter 字段：{field}")
    status_m = re.search(r"^status:\s*(\S+)", fm, re.M)
    status = status_m.group(1) if status_m else None
    if status == "published" and "verifiedWith:" not in fm and not VERIFIED_WITH_EXEMPT.search(path):
        problems.append("status: published 但缺 verifiedWith 块")
    return problems, status


def line_of(text, pos, offset):
    return text.count("\n", 0, pos) + 1 + offset


def check_terms(body, offset):
    hits = []
    lines = strip_code(body).split("\n")
    for line_no, line in enumerate(lines):
        if ANTI_PATTERN_LINE.search(line):
            continue  # 反例举证行（- ❌ … → ✅ …）——跳过，见模块顶部说明
        for pattern, msg in TERM_RULES:
            for m in pattern.finditer(line):
                if _in_corner_quotes(line, m.start(), m.end()):
                    continue  # 「引用式」提及——跳过，见 _in_corner_quotes 说明
                hits.append(f"第 {line_no + 1 + offset} 行：{msg}")
    return hits


def check_spacing(body, offset):
    hits = []
    text = strip_anchors(strip_code(body))
    for pattern in SPACING_RULES:
        for m in pattern.finditer(text):
            window = text[max(0, m.start() - 2) : m.end() + 2]
            if any(p.search(window) for p in SPACING_ALLOW):
                continue
            hits.append(f"第 {line_of(text, m.start(), offset)} 行疑似缺中英半角空格：…{m.group(0)}…")
    seen, uniq = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    return uniq[:10]  # 避免刷屏，只报前 10 条


def check_endings(body):
    problems = []
    if not re.search(r"^##\s*下一步", body, re.M):
        problems.append("缺少「## 下一步」章节")
    if not re.search(r"^##\s*如果你想", body, re.M):
        problems.append("缺少「## 如果你想」章节")
    return problems


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm, fm_lines, body = split_frontmatter(text)

    fm_problems, status = check_frontmatter(fm, path)
    hanzi = count_hanzi(body)
    problems = list(fm_problems)
    if hanzi > HANZI_LIMIT:
        problems.append(f"汉字数 {hanzi} 超过 {HANZI_LIMIT} 上限")
    problems += check_terms(body, fm_lines)
    problems += check_spacing(body, fm_lines)
    problems += check_endings(body)

    return {"file": path, "status": status, "hanzi": hanzi, "problems": problems}


def main(argv):
    if not argv:
        print("用法：check_page.py <file.md> [file2.md ...]", file=sys.stderr)
        return 2
    exit_code = 0
    for path in argv:
        r = check_file(path)
        print(f"\n=== {r['file']} ===")
        print(f"status: {r['status']} · 汉字数: {r['hanzi']}")
        if r["problems"]:
            exit_code = 1
            for p in r["problems"]:
                print(f"  ✘ {p}")
        else:
            print("  ✔ 未发现问题")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

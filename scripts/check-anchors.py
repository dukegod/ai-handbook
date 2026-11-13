#!/usr/bin/env python3
"""scripts/check-anchors.py —— 站内锚点（fragment）死链检查

为什么需要它
------------
lychee 的 `include_fragments` 在 lychee.toml 里是**关闭**的——因为当时把
VitePress 与 GFM 的 slug 算法当成了一回事。实测二者并不一致：

  - GFM / github-slugger 会丢掉「、」这类 CJK 标点
  - VitePress 的 slugify 先做 NFKD 规范化，再按 `rSpecial` 字符类替换

结果就是：正文里按 GFM 习惯写的锚点（`#二最小调用示例`）在 VitePress 生成的
真实 id（`二、最小调用示例`）里找不到 —— 浏览器能跳到页面，但**不会滚动到对应小节**。

本脚本直接从 .md 源码算 slug（不依赖 `pnpm build`），因此可以直接进 CI。

用法
----
    python3 scripts/check-anchors.py            # 检查，有错 exit 1
    python3 scripts/check-anchors.py --fix     # 自动修（仅唯一候选时），其余只报告

判定依据
--------
锚点写成什么，取决于 VitePress 生成的真实 id。唯一可靠的 ground truth 是
构建产物，所以 `--fix` 只在「去掉标点后与某个标题完全一致」时才动手；
标题被改过名的（找不到候选）一律报告，留给人判断。
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# VitePress 的 slugify（从 vitepress/dist/node/*.js 逐字提取后等价实现）
# --------------------------------------------------------------------------
_SPECIAL_CHARS = "".join(
    sorted(set("~`!@#$%^&*()-_+=|\\;:\"'“”‘’<>,.?/"))
)

_R_CONTROL = re.compile("[\u0000-\u001f]")
_R_COMBINING = re.compile("[\u0300-\u036f]")
_R_SPECIAL = re.compile("[\\s" + re.escape(_SPECIAL_CHARS) + "]+")
_R_MULTI_DASH = re.compile("-{2,}")
_R_TRIM_DASH = re.compile("^-+|-+$")
_R_LEADING_DIGIT = re.compile(r"^(\d)")

_INLINE_CODE = re.compile(r"`([^`]*)`")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_BOLD = re.compile(r"(\*\*|__)(.*?)\1")
_ITAL = re.compile(r"(\*|_)([^*_]+)\1")
_HTML = re.compile(r"<[^>]+>")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = _R_COMBINING.sub("", text)
    text = _R_CONTROL.sub("", text)
    text = _R_SPECIAL.sub("-", text)
    text = _R_MULTI_DASH.sub("-", text)
    text = _R_TRIM_DASH.sub("", text)
    text = _R_LEADING_DIGIT.sub(r"_\1", text)
    return text.lower()


def heading_title(raw: str) -> str:
    """把 markdown 标题行还原成 VitePress 的 title（去掉行内标记）"""
    t = raw.strip()
    t = _LINK.sub(r"\1", t)
    t = _INLINE_CODE.sub(r"\1", t)
    t = _BOLD.sub(r"\2", t)
    t = _ITAL.sub(r"\2", t)
    t = _HTML.sub("", t)
    return t.strip()


# --------------------------------------------------------------------------
# 收集每页的标题 slug
# --------------------------------------------------------------------------
SKIP_DIRS = {"node_modules", ".vitepress", ".obsidian", "dist", ".git"}
SKIP_FILES = {"AGENTS.md", "CLAUDE.md", "README.md"}


def iter_markdown():
    for md in sorted(ROOT.rglob("*.md")):
        parts = md.relative_to(ROOT).parts
        if parts[0] in SKIP_DIRS:
            continue
        if md.name in SKIP_FILES:
            continue
        yield md


def page_key(md: Path) -> str:
    key = "/" + str(md.relative_to(ROOT))[:-3]
    if key.endswith("/index"):
        key = key[: -len("/index")]
    return key


def heading_slugs(md: Path) -> list:
    slugs, in_fence = [], False
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            slugs.append(slugify(heading_title(m.group(2))))
    return slugs


def resolve(md: Path, base: str):
    """把链接里的路径部分解析成站点内的页面 key；解析不出来返回 None

    同时返回 (key, needs_trailing_slash)：目标页是 index.md 时，URL 必须带尾斜杠，
    否则 VitePress 的死链检查会判定为 dead（其它目录型链接都带尾斜杠）。
    """
    if base.startswith("/"):
        key = base
        needs_slash = False
    else:
        needs_slash = False
        target = (md.parent / base).resolve()
        candidates = [target]
        if target.suffix == "":
            candidates.append(target.with_suffix(".md"))
        rel = None
        for c in candidates:
            if c.exists() and c.is_file():
                try:
                    rel = "/" + str(c.relative_to(ROOT))
                except ValueError:
                    return None, False
                break
        if rel is None:
            return None, False
        key = rel[:-3] if rel.endswith(".md") else rel
    if key.endswith("/index"):
        key = key[: -len("/index")]
        needs_slash = True
    return key, needs_slash


def norm(s: str) -> str:
    """忽略标点后的比较键，用于判断「只是 slug 写法不同」还是「标题已改名」"""
    return re.sub(r"[^0-9A-Za-z㐀-䶿一-鿿]", "", s.lower())


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------
def main() -> int:
    fix = "--fix" in sys.argv

    pages = {}          # key -> Path
    slugs = {}          # key -> [slug]
    for md in iter_markdown():
        key = page_key(md)
        pages[key] = md
        slugs[key] = heading_slugs(md)

    broken = []         # (源文件, 原始链接, 目标 key, 当前 fragment, 建议 fragment 或 None)
    for md in iter_markdown():
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\]\(([^)\s]+)\)", text):
            link = m.group(1)
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            base, _, frag = link.partition("#")
            if not frag:
                continue
            key = resolve(md, base) if base else page_key(md)
            if key is None or key not in slugs:
                continue  # 目标页不存在或未发布 —— 交给 lychee 报
            target_slugs = slugs[key]
            try:
                want = urllib_unquote(frag)
            except Exception:
                want = frag
            if want in target_slugs:
                continue  # 已正确
            cands = [s for s in target_slugs if norm(s) == norm(want)]
            suggestion = cands[0] if len(cands) == 1 else None
            broken.append((md, link, key, want, suggestion))

    if not broken:
        print("✓ 站内锚点检查通过")
        return 0

    fixed = 0
    if fix:
        by_file = {}
        for md, link, key, want, sug in broken:
            if sug is None:
                continue
            by_file.setdefault(md, []).append((link, sug))
        for md, pairs in by_file.items():
            text = md.read_text(encoding="utf-8", errors="replace")
            for link, sug in pairs:
                new_link = link.split("#")[0] + "#" + sug
                if link in text:
                    text = text.replace(link, new_link)
                    fixed += 1
            md.write_text(text, encoding="utf-8")

    print(f"发现 {len(broken)} 个失效锚点"
          + (f"，已自动修复 {fixed} 个" if fix else ""))
    for md, link, key, want, sug in broken:
        rel = md.relative_to(ROOT)
        if sug is not None:
            state = f"建议改为 #{sug}"
        else:
            state = "目标标题已改名或不存在 —— 需人工判断"
        print(f"  {rel}")
        print(f"      {link}")
        print(f"      {state}")
    return 0 if fix and fixed == len(broken) else 1


def urllib_unquote(s: str) -> str:
    from urllib.parse import unquote

    return unquote(s)


if __name__ == "__main__":
    sys.exit(main())

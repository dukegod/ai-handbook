#!/usr/bin/env python3
"""test_glossary_parser.py —— glossary_parser.py 的最小自测。

纯标准库，不依赖 mcp 包——这正是把解析逻辑单独拆出来的意义：
不用装 MCP SDK、不用起 server，就能验证"表格解析对不对"。

用法：
    python3 test_glossary_parser.py
    # 或（在项目 venv 里）
    uv run test_glossary_parser.py
"""
import tempfile
from pathlib import Path

import glossary_parser as gp

SAMPLE = """\
---
title: 术语表
---

# 术语表

## 阅读方式

- **首选写法**：正文里推荐的固定表达

## Claude 与 Anthropic 家族

| 首选写法 | 说明 | 边界 |
| --- | --- | --- |
| **Anthropic** | Claude 系列模型与 Claude Code 的出品公司 | 不用「Claude 公司」 |
| **Claude** | 模型本身 | 不指公司也不指工具 |

## MCP 生态

| 首选写法 | 一句话定义 |
| --- | --- |
| **MCP Server** | 提供工具/资源的服务端进程 |

## 常见易错

- ❌ `Claude 公司` → ✅ `Anthropic`
- ❌ `ClaudeCode` → ✅ `Claude Code`（中间有空格）

## 参考

- 占位
"""


def _write_sample():
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
    f.write(SAMPLE)
    f.close()
    return Path(f.name)


def test_parse_glossary_counts_and_categories():
    terms = gp.parse_glossary(_write_sample())
    assert len(terms) == 3, f"期望 3 条术语，实得 {len(terms)}"
    assert terms[0]["term"] == "Anthropic"
    assert terms[0]["category"] == "Claude 与 Anthropic 家族"
    assert terms[0]["note"] == "不用「Claude 公司」"
    assert terms[2]["term"] == "MCP Server"
    assert terms[2]["category"] == "MCP 生态"
    assert terms[2]["note"] == ""  # 两列表格没有第三列


def test_parse_glossary_stops_before_common_mistakes():
    terms = gp.parse_glossary(_write_sample())
    assert all("常见易错" not in t["category"] for t in terms)


def test_parse_common_mistakes():
    mistakes = gp.parse_common_mistakes(_write_sample())
    assert len(mistakes) == 2
    assert mistakes[0] == {"wrong": "Claude 公司", "right": "Anthropic", "note": ""}
    assert mistakes[1]["wrong"] == "ClaudeCode"
    assert mistakes[1]["right"] == "Claude Code"
    assert mistakes[1]["note"] == "中间有空格"


def test_find_term_exact_then_substring():
    terms = gp.parse_glossary(_write_sample())
    exact = gp.find_term(terms, "Claude")
    assert len(exact) == 1 and exact[0]["term"] == "Claude"
    sub = gp.find_term(terms, "claude")  # 大小写不敏感
    assert any(t["term"] == "Claude" for t in sub)
    sub2 = gp.find_term(terms, "anthro")
    assert any(t["term"] == "Anthropic" for t in sub2)


def test_find_term_empty_query_returns_empty():
    terms = gp.parse_glossary(_write_sample())
    assert gp.find_term(terms, "   ") == []


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✔ {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ✘ {t.__name__}：{e}")
    print(f"\n{len(tests) - failed}/{len(tests)} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

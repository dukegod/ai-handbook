---
description: 给 Claude Handbook 的一篇 md 做写作规范体检——frontmatter 必填字段、汉字数上限、术语易错、中英间距、结尾双组引导。用户说"检查这篇/这几篇文章"或"过一遍 style-guide"时用。
argument-hint: <file.md> [file2.md ...]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/check_page.py *)
---

## 体检结果

!`python3 ${CLAUDE_SKILL_DIR}/scripts/check_page.py $ARGUMENTS`

## Instructions

上面是 `check_page.py` 对指定文件的体检结果，规则来自 [contributing/style-guide.md](/contributing/style-guide) 第十节「PR 前自检 checklist」。逐条处理：

1. **先分类，再动手**：每条 `✘` 分成"脚本误报"还是"真实问题"——正则天然分不清"用错术语"和"举例说明什么是错的"，遇到明显不对劲的报告（比如术语命中落在一句正常陈述句里、间距问题落在链接或代码周围）先怀疑脚本，去源文件对应行读一遍上下文再下结论。
2. **只修真实问题**：汉字数超限就建议拆分点；缺「## 下一步」/「## 如果你想」就补上对应章节骨架；术语误用给出 glossary 对齐后的正确写法；中英间距问题直接在两侧补半角空格。
3. **status: published 缺 verifiedWith**——除非这篇是章导读（`index.md`）或 `contributing/` 下的元文档（这类页面按本项目约定不需要 verifiedWith），否则要求补 `claudeCode` / `model` / 一手来源链接 / `accessedAt`。
4. **改完重跑**：`python3 ${CLAUDE_SKILL_DIR}/scripts/check_page.py <file>` 确认问题清零，再告诉用户改了什么、跳过了什么误报以及为什么。
5. **别自动改标题党结论**：脚本没报的不代表这篇文章内容正确（比如逻辑错误、术语定义本身错了）——这是体检脚本的边界，仍需要人读。

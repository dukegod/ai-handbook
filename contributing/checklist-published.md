---
title: Published 门槛自检模板
description: 把一篇 draft 升到 published 时逐项要过的具体动作、命令与判据
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-11
verifiedWith:
  claudeCode: 2.1.220
  officialDocs: 'https://vitepress.dev/'
  accessedAt: 2026-08-11
---

# Published 门槛自检模板

> 本文是 [style-guide 第十节 PR 前自检 checklist](./style-guide#十、pr-前自检-checklist) 的**具体操作版**。前者告诉你「要检查什么」，本文告诉你「怎么检查、判据是什么、失败怎么办」。
>
> 定位：**从 `status: draft` 升到 `status: published` 的门槛清单**。每次改动老页面（哪怕只改一个错字）也走这份清单，只是大部分项目已经绿。

⏱ 预计执行时间：一篇约 15–30 分钟；批量刷 22 篇约 5–8 小时（不含发现问题需要重写的情况）。

## 使用节奏

1. 打开一篇 `status: draft` 的页面
2. 顺着本清单 12 项逐个打勾
3. 全绿后：`status: draft` → `status: published`；更新 `lastUpdated` 为今天
4. 在 sidebar `.vitepress/config.ts` 里去掉 `P('xxx')`（如有）
5. commit：`chore(publish): <path> 过 published 门槛`；清单状态粘到 commit 消息，回滚时可回溯每篇过关状态
6. ff-merge 到 `main`

## 完整清单（12 项）

### 内容层（4 项）

#### 1. Frontmatter 完整

判据：所有强制字段齐、格式正确、`status: published`、`lastUpdated` 为今天。

```yaml
---
title: ...                     # 必填 · 与 h1 一致
description: ...               # 必填 · 一句话，会显示在首页与搜索
audience: beginner | intermediate | advanced  # 必填
difficulty: 🟢 | 🟡 | 🔴        # 必填
status: published              # ★ 本次要从 draft → published
lastUpdated: YYYY-MM-DD         # ★ 本次要更新为今天
verifiedWith:                  # published 时必填（详见第 2 项）
  claudeCode: ...
  model: ...
---
```

失败常见：`description` 里含反引号 → YAML 解析报错。看 [CLAUDE.md 已知坑](/) 里 「YAML frontmatter 里 description 含反引号必须用单引号包裹」一节。

#### 2. `verifiedWith` 填写规范

**判据**：字段与文中示例的实际运行环境一致。谎报是 published 门槛第一红线。

| 字段 | 是否必填 | 填法 | 示例 |
|---|---|---|---|
| `claudeCode` | 若文中出现 CLI / hooks / skills / slash / MCP 用法则必填 | 本机 `claude --version` 输出的完整版本号 | `2.1.215` |
| `model` | 若文中出现具体模型行为、`/model` 命令、模型对比等则必填 | 用过的模型 ID（不是显示名）| `claude-opus-4-8` |
| `sdk` | 若文中出现 SDK 示例则必填 | 包名 + 版本 | `'@anthropic-ai/sdk@0.62.0'`；多个用逗号 |
| `officialDocs` | 若引用了官方文档某具体章节则必填 | 精确到锚点的 URL | `'https://docs.claude.com/en/docs/build-with-claude/prompt-caching'` |
| `accessedAt` | 与 `officialDocs` 同时出现时必填 | 最后一次核对官方文档的日期 | `2026-07-28` |

若某字段与本文无关（比如纯概念文没跑任何代码），**省略**该字段而不是留空——留空是「验过但没记录」，比不写更误导。

#### 3. 内容自检：跑过 = 我能复现

**判据**：文中每段可执行的示例（命令 / 代码块 / 提示词），作者本人在写作后 7 天内亲手跑过一遍。

具体操作：

- **命令示例**：本机跑一遍，把实际输出对照文中断言。差异要么改文，要么补版本注释（如 `# claude 2.1.180+ 起支持`）
- **代码示例**：能编译或运行的代码块，跑一遍确认无报错
- **提示词示例**：用文中给的提示对 Claude Code 跑一次，看结果符合文中描述
- **概念文**：走一遍文中「你能在这里学到」列出的每个知识点，向自己复述一遍——卡壳的地方就是没讲清楚的地方

失败常见：写完就发。**结果：一周后读者跑不通、翻旧 issue、发现是版本差**。防呆手段：在文中埋一段小 `verifiedWith` 记录（frontmatter 里）+ 一句正文（如「以下命令基于 Claude Code 2.1.215 亲测通过」）。

#### 4. 「不写什么」自查

**判据**：不重复 Anthropic 官方 API schema 全表；差异化在「为什么用 / 何时用 / 踩坑」。

具体自问：

- 「这一段是不是把官方 docs 翻译搬运一遍？」→ 是则删，改写成「为什么这个字段这么设计 + 什么时候要动它 + 踩过的坑」
- 「读者读完这段能做什么、避免什么？」→ 一句话答不上来则删

### 元规范层（4 项）

#### 5. 术语与 glossary 对齐

**判据**：文中所有专有名词与 [glossary.md](./glossary) 一致；新术语已补录 glossary。

具体操作：

```bash
# 把本文与 glossary 术语交叉核对
grep -oE '\b[A-Z][a-zA-Z]{2,}\b' <本文.md> | sort -u > /tmp/terms.txt
# 手工对照 /tmp/terms.txt 里出现的每个专有名词是否在 glossary 里
```

**三条禁止混用红线**（style-guide 第五节）：

- `Anthropic` = 公司
- `Claude` = 模型
- `Claude Code` = CLI 工具

任何一处混用即门槛不过。

#### 6. 中英混排前后有半角空格

**判据**：`使用 Claude Code` ✅；`使用ClaudeCode` ❌；`Claude Code是` ❌。

具体检查（正则近似）：

```bash
# 找一切中文紧邻英文字母的位置（可能是漏了空格）
grep -nP '[一-鿿][A-Za-z]|[A-Za-z][一-鿿]' <本文.md>
```

例外：术语连写（`GraphQL`、`TypeScript` 内部）、URL、代码块内。

#### 7. 「下一步」+「如果你想」齐备

**判据**：文档尾部至少有一个 `## 下一步`（线性下一篇）+ 一个 `## 如果你想`（横向跳转 3–5 个选项）。二者作用不同，只有一个都算不通过。

#### 8. 字数 ≤ 1500 汉字

**判据**：正文（不含 frontmatter / 代码块 / 表格）汉字数 ≤ 1500。超过则拆篇或砍冗余（一般能砍 20%+）。

```bash
grep -oP '[一-鿿]' <本文.md> | wc -l
```

### 技术层（4 项）

#### 9. 敏感信息脱敏

**判据**：

- API key 用 `sk-ant-****` 而不是完整值
- 内部路径（`/Users/liuhui15/...`、`~/.jd-corp/...`）替换为 `<user>` 或 `<project-root>`
- 真实同事名字 / 邮箱 / 内网 URL 全部脱敏

具体操作：

```bash
# 常见敏感串扫描
grep -nE '(sk-ant-|/Users/|@jd\.com|coding\.jd\.com/[a-z]+/[a-z-]+)' <本文.md>
```

例外：`coding.jd.com/sz-fe/claude-wiki` 是本站仓库 URL，允许出现；`docs.claude.com`、`code.claude.com` 等公开域名不算敏感。

#### 10. 外链可访问 + 官方文档注日期

**判据**：所有 http/https 链接 200 可达；官方文档链接后紧跟「（访问于 YYYY-MM-DD）」。

具体操作（最省事的批量方式）：

```bash
# 抽出所有 http/https 链接
grep -oE 'https?://[^)\s]+' <本文.md> | sort -u > /tmp/links.txt
# 逐个 curl -I 检查（HEAD 请求）
while read url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -I -L "$url")
  echo "$code $url"
done < /tmp/links.txt
```

任何 4xx / 5xx / DNS 失败即门槛不过——要么换链接，要么删引用。

引用官方文档格式：`[Anthropic 官方 Extended Thinking 文档](https://docs.claude.com/...)（访问于 2026-07-28）`。

#### 11. 截图打码完整

**判据**：所有截图里没有 API key、内网 URL、账号名、邮箱、真实文件路径。截图源文件（PSD / Figma 等）入 `assets/screenshots/YYYY-MM-DD/`。

具体自查：

- 打开每张截图放大 200% 检查
- 侧栏 / 状态栏 / 标签页标题都要看
- 深色主题的白色 tooltip 有时藏在角落——别漏

#### 12. `pnpm build` 无报错、无死链

**判据**：`pnpm build` 输出无 `error` / `warn` / `dead link`。

```bash
cd /Users/liuhui15/jd-projects/sz-fe/claude-wiki
rm -rf .vitepress/cache .vitepress/dist    # 清缓存，避免误报绿
pnpm build 2>&1 | grep -iE '(warn|error|dead)'
# 期望：无输出（除了 vite 常规 chunk-size 提示，那个可忽略）
```

死链的最常见来源：

- 相对链接 `./roadmap` 在被 include 到别的目录后失效（见 [CLAUDE.md 已知坑](/)）
- 术语表的锚点因 emoji 变化了 slug
- 引用了 `status: planned` 页面但那页还没建

## 参考

- [style-guide.md 第十节 PR 前自检 checklist](./style-guide#十、pr-前自检-checklist) — 本文的规范源
- [glossary.md](./glossary) — 术语对齐依据
- [roadmap.md](./roadmap) — v0.1.2 精修目标

## 下一步

- 拿一篇 draft 试跑本清单 → 从 [/claude-code/getting-started/what-is-claude-code](/claude-code/getting-started/what-is-claude-code) 开始
- 遇到不清楚的规范 → 回 [style-guide.md](./style-guide)

## 如果你想

- 查术语 → [术语表](./glossary)
- 起草新概念文 → [概念文模板](./template-concept)
- 起草新操作文 → [操作文模板](./template-howto)
- 看整体进度与阶段划分 → [路线图](./roadmap)

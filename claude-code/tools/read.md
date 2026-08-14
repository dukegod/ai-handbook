---
title: Read 读文件
description: Claude Code 的 Read 工具——按行读取文件、图片、PDF、Notebook，配合 offset/limit 精准定位
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Read 读文件

> **TL;DR**：`Read` 是 Claude Code 最基础的工具——读文本、看图片、翻 PDF、查 Notebook。掌握 `offset` + `limit` 精准读取，能省一半 token。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Read 工具的四种文件类型支持
- `offset` / `limit` 精准读取的用法与场景
- 大文件的最佳实践：先 Grep 定位，再 Read 指定行
- 图片 / PDF / Notebook 的读取限制

## 基本用法

`Read` 最简单的形式——读整个文件：

```
Read file_path="/path/to/file.js"
```

Claude 会自动选择合适的读取方式。文本文件按行号返回（`cat -n` 格式），图片直接展示，PDF 按页读取。

## 四种文件类型

| 类型 | 行为 | 限制 |
|------|------|------|
| **文本** | 按行返回，带行号 | 默认最多 2000 行 |
| **图片** | PNG/JPG/SVG 等，视觉展示 | 无特殊限制 |
| **PDF** | 按页读取 | 每次最多 20 页 |
| **Notebook** | 按 cell 返回，含输出 | `.ipynb` 格式 |

## 精准读取：offset + limit

大文件不需要全读。用 `offset` 跳过前面的行，用 `limit` 控制读取行数：

```
Read file_path="src/index.ts" offset="100" limit="50"
```

这会读取第 100–149 行。**配合 Grep 定位**是最高效的组合：

```
# 第 1 步：Grep 找到目标行号
Grep pattern="function handleAuth" path="src/"

# 第 2 步：Read 读取上下文
Read file_path="src/auth.ts" offset="42" limit="30"
```

::: tip 为什么先 Grep 再 Read？
`Read` 全文件会把所有内容塞进 context window，既慢又贵。先 `Grep` 出行号，再 `Read --offset --limit` 只读目标区域——**省 token、省时间、省成本**。
:::

## 读取目录

传入目录路径时，`Read` 返回目录内容列表（类似 `ls`），不会递归读取：

```
Read file_path="src/"
```

## 权限

- **工作目录内**：默认放行，无需确认
- **工作目录外**：需要在 `settings.json` 中放行对应路径

## 常见坑

**文件超过 2000 行**

`Read` 默认最多读 2000 行。超出时用 `offset` + `limit` 分段读取，或用 `Grep` 先定位关键行。

**二进制文件**

`Read` 不支持二进制文件（如 `.exe`、`.zip`）。尝试读取会返回错误提示。

**路径不存在**

传入不存在的路径会返回错误，不会自动创建文件（创建文件用 `Write`）。

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）

## 下一步

- 学会修改文件 → [Edit / Write 改文件](./edit-and-write)
- 学会搜索文件内容 → [Grep / Glob 搜索](./search)

## 如果你想

- 了解 Read 在工具总览中的位置 → [工具总览](./overview)
- 控制 Read 的权限范围 → [权限系统](../basics/permissions)
- 用 MCP 扩展更多文件操作能力 → [什么是 MCP](../mcp/what-is-mcp)

---
title: Notebook 编辑
description: Claude Code 的 NotebookEdit 工具——操作 Jupyter Notebook 单元格，数据科学工作流必备
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Notebook 编辑

> **TL;DR**：`NotebookEdit` 让 Claude Code 读写 Jupyter Notebook（`.ipynb`）的单元格。数据科学工作流的必备工具。

⏱ 预计阅读时间：4 分钟

## 你能在这里学到

- NotebookEdit 的三种操作模式：replace / insert / delete
- cell_id 的获取与使用
- 读取 Notebook 的方式
- 常见坑与最佳实践

## 读取 Notebook

用 `Read` 工具读取 Notebook，返回按 cell 组织的内容：

```
Read file_path="/path/to/notebook.ipynb"
```

输出格式：

```
<cell id="abc123" type="code">
import pandas as pd
df = pd.read_csv("data.csv")
</cell>

<cell id="def456" type="markdown">
# 数据分析
</cell>
```

每个 cell 有唯一的 `id` 属性，后续编辑需要用它。

## 三种编辑模式

### replace：替换单元格内容

```
NotebookEdit notebook_path="/path/to/notebook.ipynb"
             cell_id="abc123"
             new_source="import pandas as pd\nimport numpy as np"
```

### insert：插入新单元格

```
NotebookEdit notebook_path="/path/to/notebook.ipynb"
             cell_id="abc123"
             new_source="# 新的分析步骤\ndf.head()"
             cell_type="code"
             edit_mode="insert"
```

新 cell 插入在 `cell_id` 指定的 cell **之后**。省略 `cell_id` 则插入到**开头**。

### delete：删除单元格

```
NotebookEdit notebook_path="/path/to/notebook.ipynb"
             cell_id="abc123"
             edit_mode="delete"
             new_source=""
```

::: warning 删除不可逆
`delete` 操作直接移除 cell，无法撤销。确认 cell_id 正确再执行。
:::

## cell_type

| 类型 | 说明 |
|------|------|
| `code` | 代码单元格（可执行） |
| `markdown` | Markdown 文本单元格 |

插入时必须指定 `cell_type`；替换时保持原类型不变。

## 常见用法

### 修改现有代码

```
# 1. 读取 Notebook
Read file_path="analysis.ipynb"

# 2. 替换目标 cell
NotebookEdit notebook_path="analysis.ipynb"
             cell_id="abc123"
             new_source="df = pd.read_csv('new_data.csv')\ndf.describe()"
```

### 添加新分析步骤

```
NotebookEdit notebook_path="analysis.ipynb"
             cell_id="abc123"
             new_source="## 相关性分析\ndf.corr()"
             cell_type="markdown"
             edit_mode="insert"
```

### 清理无用 cell

```
NotebookEdit notebook_path="analysis.ipynb"
             cell_id="unused-cell-id"
             edit_mode="delete"
             new_source=""
```

## 权限

`NotebookEdit` 默认**需要确认**。可放行特定路径：

```json
{
  "permissions": {
    "allow": ["NotebookEdit(notebooks/**)"]
  }
}
```

## 常见坑

**cell_id 不存在**

原因：cell_id 来自旧的 Read 输出，Notebook 已被修改。

修复：重新 `Read` Notebook 获取最新的 cell_id。

**Notebook 路径错误**

原因：路径不在工作目录内。

修复：用绝对路径或确认相对路径正确。

**输出不显示**

`NotebookEdit` 只编辑 cell 源代码，不执行 cell。需要在 Jupyter 中手动运行或用 `Bash` 执行：

```bash
jupyter nbconvert --execute notebook.ipynb
```

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）
- [Jupyter Notebook 文档](https://jupyter-notebook.readthedocs.io/)（访问于 2026-08-13）

## 下一步

- 学会读取其他文件类型 → [Read 读文件](./read)
- 学会执行 Shell 命令运行 Notebook → [Bash 执行命令](./shell)

## 如果你想

- 了解 NotebookEdit 在工具总览中的位置 → [工具总览](./overview)
- 用 Claude Code 做数据分析 → [数据分析工作流](/cookbook/data-analysis-workflow)

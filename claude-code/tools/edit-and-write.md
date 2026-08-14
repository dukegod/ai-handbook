---
title: Edit / Write 改文件
description: Claude Code 的 Edit 与 Write 工具——精准替换 vs 整文件覆写，何时用哪个、踩坑与最佳实践
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Edit / Write 改文件

> **TL;DR**：`Edit` 做精准替换（推荐），`Write` 做整文件覆写（新建文件时用）。90% 的修改场景用 `Edit` 就够了。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Edit 与 Write 的核心区别与使用场景
- Edit 的 `old_string` / `new_string` 匹配规则
- `replace_all` 批量替换的用法
- 何时该用 Write 而不是 Edit

## Edit：精准替换

`Edit` 通过 `old_string` 精确匹配文件中的片段，替换为 `new_string`：

```
Edit file_path="src/app.ts"
     old_string="const port = 3000"
     new_string="const port = 8080"
```

**匹配规则**：

- `old_string` 必须与文件内容**完全一致**（含缩进、空格）
- 必须**唯一**——匹配到多处会报错（除非用 `replace_all`）
- 替换后的内容必须与 `old_string` **不同**

### 批量替换

`replace_all: true` 替换所有匹配项，不再要求唯一：

```
Edit file_path="src/utils.ts"
     old_string="console.log"
     new_string="logger.info"
     replace_all="true"
```

::: warning 注意
`replace_all` 会替换文件中**所有**匹配项。确认目标字符串不会误伤其他位置。
:::

## Write：整文件覆写

`Write` 创建新文件或完全覆写已有文件：

```
Write file_path="src/config.ts"
      content="export const config = { port: 8080 }"
```

**使用场景**：

- 创建新文件
- 需要完全重写的文件（改动超过 70%）

**不要用 Write 的场景**：

- 只改几行代码 → 用 `Edit`
- 文件很长，只改一小段 → 用 `Edit`

::: tip 为什么优先 Edit？
`Write` 要求你输出整个文件内容。文件有 500 行你只改 1 行，用 `Write` 意味着要把 499 行原样重写——浪费 token、容易出错。`Edit` 只传改动部分，精准且高效。
:::

## 读 → 改 → 验证流程

最佳实践是先读再改：

```
# 1. 读取目标区域
Read file_path="src/auth.ts" offset="40" limit="20"

# 2. 精准替换
Edit file_path="src/auth.ts"
     old_string="const timeout = 5000"
     new_string="const timeout = 30000"

# 3. 验证（可选）
Read file_path="src/auth.ts" offset="40" limit="5"
```

## 权限

两个工具都**默认需要确认**。可通过 `settings.json` 的 `permissions.allow` 放行特定路径：

```json
{
  "permissions": {
    "allow": ["Edit(src/**)", "Write(src/**)"]
  }
}
```

## 常见坑

**old_string 匹配失败**

原因：缩进不一致、多了/少了空格、换行符不同。

修复：先用 `Read` 精确读取目标行，复制内容作为 `old_string`。

**Write 覆写了已有文件**

`Write` 不会检查文件是否已存在。对已有文件用 `Write` 会**静默覆盖**全部内容。

修复：修改已有文件始终用 `Edit`；只在确认要整覆写时用 `Write`。

**文件不存在时 Edit 报错**

`Edit` 只能修改已有文件。创建新文件请用 `Write`。

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）

## 下一步

- 学会执行 Shell 命令 → [Bash 执行命令](./shell)
- 学会搜索文件内容 → [Grep / Glob 搜索](./search)

## 如果你想

- 了解 Edit/Write 在工具总览中的位置 → [工具总览](./overview)
- 控制文件修改的权限 → [权限系统](../basics/permissions)
- 编辑 Jupyter Notebook → [Notebook 编辑](./notebook)

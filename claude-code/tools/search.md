---
title: Grep / Glob 搜索
description: Claude Code 的 Grep 与 Glob 工具——按内容搜文件 vs 按路径匹配文件，高效定位代码的两把利器
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Grep / Glob 搜索

> **TL;DR**：`Grep` 按内容搜（ripgrep 语法），`Glob` 按路径匹配（glob 模式）。两者都无需权限，是 Claude 定位代码的首选工具。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Grep 与 Glob 的核心区别
- Grep 的 ripgrep 语法与常用模式
- Glob 的通配符匹配规则
- 先搜后读的最佳实践

## Grep：按内容搜索

`Grep` 底层调用 ripgrep，搜索文件内容并返回匹配的行：

```
Grep pattern="function handleAuth" path="src/"
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `pattern` | 搜索模式（支持正则） | `"TODO\|FIXME"` |
| `path` | 搜索目录 | `"src/"` |
| `include` | 文件名过滤 | `"*.ts"` |
| `exclude` | 排除目录 | `"node_modules"` |

### 常用模式

**搜函数定义**

```
Grep pattern="export function" path="src/" include="*.ts"
```

**搜 TODO 注释**

```
Grep pattern="TODO|FIXME|HACK" path="src/"
```

**搜配置项**

```
Grep pattern="apiKey|secret|token" path="src/" include="*.ts"
```

## Glob：按路径匹配

`Glob` 用通配符匹配文件路径，返回文件列表：

```
Glob pattern="src/**/*.ts"
```

### 通配符规则

| 通配符 | 含义 | 示例 |
|--------|------|------|
| `*` | 匹配任意字符（不含 `/`） | `"*.md"` |
| `**` | 匹配任意层级目录 | `"src/**/index.ts"` |
| `?` | 匹配单个字符 | `"file?.ts"` |

### 常用模式

**找所有 TypeScript 文件**

```
Glob pattern="**/*.ts"
```

**找所有 index 文件**

```
Glob pattern="**/index.{ts,js,md}"
```

**找特定目录下的文件**

```
Glob pattern="src/components/**/*.vue"
```

## 先搜后读：最佳实践

Grep/Glob 负责**定位**，Read 负责**读取**——这是最省 token 的组合：

```
# 1. Grep 找到目标行号
Grep pattern="class AuthService" path="src/"

# 输出：src/auth.ts:42: class AuthService {

# 2. Read 读取上下文
Read file_path="src/auth.ts" offset="38" limit="30"
```

::: tip 为什么不用 Read 全文件？
一个 500 行的文件，Read 全文消耗 500 行 token。Grep 定位到第 42 行，再 Read offset=38 limit=30，只消耗 30 行 token——**省 94%**。
:::

## Grep vs Glob 选择

| 场景 | 用哪个 |
|------|--------|
| 找包含特定文本的文件 | `Grep` |
| 找特定类型/路径的文件 | `Glob` |
| 找函数/类/变量定义 | `Grep` |
| 列出所有 `.md` 文件 | `Glob` |
| 搜配置文件内容 | `Grep` + `include` |

## 权限

两个工具都**无需权限确认**，默认放行。这是它们被优先使用的另一个原因。

## 常见坑

**Grep 搜不到结果**

原因：`path` 不在工作目录内，或 `include` 过滤太严。

修复：先用 `Glob` 确认文件存在，再放宽 `include` 条件。

**Glob 返回太多结果**

原因：`**` 匹配范围太广。

修复：缩小 `pattern` 范围，如 `src/**/*.ts` 代替 `**/*.ts`。

**正则语法错误**

原因：Grep 用 ripgrep 正则，不是 PCRE。

修复：复杂正则先在终端 `rg "pattern" src/` 测试。

## 参考

- [ripgrep 用户指南](https://github.com/BurntSushi/ripgrep)（访问于 2026-08-13）
- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）

## 下一步

- 学会读取搜索到的文件 → [Read 读文件](./read)
- 学会修改找到的代码 → [Edit / Write 改文件](./edit-and-write)

## 如果你想

- 了解 Grep/Glob 在工具总览中的位置 → [工具总览](./overview)
- 用 LSP 做更精准的代码跳转 → [工具总览 · 搜索](./overview#③-搜索3)

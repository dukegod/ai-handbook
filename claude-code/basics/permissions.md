---
title: 权限系统
description: allow / deny / ask 三档规则、6 种 permission mode、Bash / Read / Edit / MCP 规则语法、workspace trust 与 /permissions
audience: beginner
difficulty: 🟡
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/permissions'
  accessedAt: 2026-07-28
---

# 权限系统

> **TL;DR**：Claude Code 的权限分三档（allow / ask / deny），评估顺序 **deny → ask → allow**，第一个 match 决定。**读默认允许、Bash 与写默认问**。用 `/permissions` 交互管理，或写进 `.claude/settings.json`。要**硬约束**用 [Hook](/claude-code/customization/hooks) 或 [sandbox](https://code.claude.com/docs/en/sandboxing)——权限规则只是软约束。

⏱ 预计阅读时间：10 分钟

## 你能在这里学到

- 三档规则（allow / ask / deny）与评估顺序
- **6 种 permission mode**（`Shift+Tab` 循环）
- Bash / Read / Edit / WebFetch / MCP / Agent 各自的规则语法
- Wildcard 与 compound command 的匹配规则
- Workspace trust 与项目 allow rule 的关系
- 优先级与设置文件层级

## 前置

- 装好 Claude Code、跑过 [第一次对话](/getting-started/first-conversation)

## 一、三档规则：deny → ask → allow

Claude Code 的每次工具调用都要过一遍权限规则：

- **`allow`** — 无需批准直接执行
- **`ask`** — 每次触发前问你（default 模式下的默认行为）
- **`deny`** — 直接拒绝；bare 名的 deny 会**把工具完全从 Claude 的上下文里移除**

**评估顺序：deny → ask → allow**——第一个匹配决定结果（specificity 不影响顺序）。广泛的 `Bash(aws *)` deny 会覆盖更精细的 `Bash(aws s3 ls)` allow——**deny 不能带例外**，想留窗口用 [PreToolUse Hook](/claude-code/customization/hooks)。

### 默认行为（无规则时）

| 工具类别 | 默认 | "Yes, don't ask again" 保存到 |
| --- | --- | --- |
| 只读（Read / Grep） | **无需批准**（在工作目录 + `additionalDirectories` 内） | N/A |
| Bash | **需批准**（除内置只读命令白名单） | `.claude/settings.local.json`（v2.1.211+ 存 repo root） |
| 文件修改（Edit / Write） | **需批准** | **仅本次会话**（session end 失效） |

Bash 内置只读白名单：`ls` / `cat` / `echo` / `pwd` / `head` / `tail` / `grep` / `find` / `wc` / `which` / `diff` / `stat` / `du` / `cd` + git 只读命令。

## 二、6 种 Permission Mode

会话内按 **`Shift+Tab`** 循环切换。全部 6 种：

| 模式 | 行为 | 场景 |
| --- | --- | --- |
| **`default`**（Manual） | 首次用每个工具时问 | 陌生代码 / 刚上手 |
| **`acceptEdits`** | 自动接受文件编辑 + `mkdir` / `touch` / `rm` / `rmdir` / `mv` / `cp` / `sed` 等 fs 命令 | 熟悉且信任的操作 |
| **`plan`** | 只读探索，不改文件 | 让 Claude 先出方案（见 [Plan Mode](./plan-mode)） |
| **`auto`** | 后台安全检查自动批准 | 部分账号可用 |
| **`dontAsk`** | 无预允许时全部 deny | 严格 CI |
| **`bypassPermissions`** | ⚠️ 跳过所有 prompt | **仅在容器 / VM 里用** |

> ⚠️ `bypassPermissions` 会跳过对 `.git` / `.config/git` / `.claude` / `.vscode` / `.idea` 等目录写入的批准——**只在隔离环境用**。全局禁用：`permissions.disableBypassPermissionsMode: "disable"`。

**会话恢复时**：`plan` 与 `bypassPermissions` **不会恢复**，要在启动时重新指定；`auto` 只在账号仍满足要求时恢复。

## 三、规则语法

规则格式：`Tool` 或 `Tool(specifier)`。

### 匹配整个工具

```json
"Bash"           // 所有 Bash 命令；作为 deny 时工具从 Claude 上下文完全移除
"WebFetch"       // 所有 web fetch
"Read"           // 所有文件读取
```

`Bash(*)` 等价于 `Bash`。

### 精细控制

```json
"Bash(npm run build)"           // 精确匹配
"Bash(npm run *)"               // 通配前缀
"Read(./.env)"                  // 特定文件
"WebFetch(domain:example.com)"  // 域名
```

**通配符规则**：

- `*` 可出现在任何位置（前 / 中 / 后）
- `Bash(ls *)` 匹配 `ls -la`，**不**匹配 `lsof`（空格前的 `*` 有 word boundary）
- `Bash(ls*)` 匹配两者（无 boundary）
- `Bash(git * main)` 匹配 `git checkout main` / `git log main` 等
- `:*` 后缀等价于尾部 ` *`：`Bash(ls:*)` == `Bash(ls *)`

### 参数匹配（仅 deny / ask）

```json
"Agent(model:opus)"             // 只 deny Opus 请求
"Bash(run_in_background:true)"  // 只 deny 后台执行
```

⚠️ **allow 规则不支持参数匹配**——安全考虑。

## 四、常用工具的规则示例

**Bash**：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git status)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push *)"
    ]
  }
}
```

**Compound command**：Claude Code 识别 `&&` / `||` / `;` / `|` 分隔——**每个子命令独立匹配**。`Bash(safe-cmd *)` 不会让 `safe-cmd && rm -rf *` 通过。

**Wrapper 剥离**：`timeout` / `time` / `nice` / `nohup` / `command` / `builtin` / `xargs`（无 flag）等被剥离——`Bash(npm test *)` 也匹配 `timeout 30 npm test`。

**Read / Edit（gitignore 语法）**：

| 语法 | 含义 |
| --- | --- |
| `Read(//path)` | 文件系统根的**绝对路径** |
| `Read(~/path)` | home 目录 |
| `Read(/path)` | **settings 文件所在位置**（不是文件系统根！） |
| `Read(path)` 或 `Read(./path)` | 当前目录 |
| `Read(.env)` | 任意深度的 `.env`（bare 文件名 = `**/.env`） |

⚠️ **单斜杠 `/path` 不是绝对路径**——它 anchor 到 settings 文件位置（项目级 = repo root，用户级 = `~/.claude/`）。**绝对路径要用 `//`**。

**WebFetch**：`WebFetch(domain:example.com)` 匹配单域名；`domain:*.example.com` 匹配子域名（但不含裸域）。

**MCP**：`mcp__server` 或 `mcp__server__tool`。

**Agent**：`Agent(Explore)` / `Agent(Plan)` / `Agent(my-agent)`。

## 五、`/permissions`：交互管理

```text
/permissions
```

列出所有当前生效的规则 + 各自来源的 `settings.json` 文件。可以逐条查看、添加、删除、启停。命令行运行时按 **`Ctrl+E`** 可以让 Claude 给出对某 Bash / PowerShell 命令的**风险解释**（Low / Med / High）。

## 六、Workspace Trust

**项目级 `.claude/settings.json` 里的 `allow` 规则默认不生效**——需要你先接受该项目的 **workspace trust dialog**。这是防止拉一个不熟悉的仓库时它偷偷 auto-approve 危险操作。

- Trust 保存在 git repo root（外部仓库时是你启动 Claude 的目录）
- Trust 不 propagate 到嵌套项目
- **`deny` 与 `ask` 规则不需要 trust**（它们只是限制，本来就安全）

## 七、优先级与设置文件

从高到低（**deny 从任何层都生效**）：

1. **Managed settings**（企业）—— MDM / Group Policy 下发，不可覆盖
2. **命令行 flag**（`--allowedTools` / `--disallowedTools`）
3. **`.claude/settings.local.json`**（项目本地，v2.1.211+ 存 repo root）
4. **`.claude/settings.json`**（项目共享，入库）
5. **`~/.claude/settings.json`**（用户级）

用户级 allow + 项目级 deny → **deny 胜**。任何层 deny 都最高优先级。

## 常见坑

**deny 太广挡住了自己**

`Bash(aws *)` deny 会拦住 `aws s3 ls`——deny 不能带 allow 例外。想精细放行用 [PreToolUse Hook](/claude-code/customization/hooks)。

**`/path` 不是绝对路径**

项目 settings 里 `Read(/secrets/**)` 匹配的是 `<repo>/secrets/**` 而不是 `/secrets/**`。绝对路径**用 `//path`**。

**允许了 `Bash` 就等于把 shell 交出去**

`Bash` 无 specifier 时匹配一切。日常应按具体命令允许（`Bash(npm test)` / `Bash(git status)`），别一步到位。

**`.claude/settings.local.json` 被 commit**

按约定该文件**必须 gitignore**。一旦提交会泄漏你个人的偏好和 approval 授权。

**项目 allow 规则没生效**

先看 workspace trust dialog 是不是接受了。`/permissions` 里 rule 显示为灰色 = 未 trust。

## 参考

- [Anthropic Docs · Configure permissions](https://code.claude.com/docs/en/permissions)（访问于 2026-07-28）
- [Anthropic Docs · Permission modes](https://code.claude.com/docs/en/permission-modes)（访问于 2026-07-28）
- [Anthropic Docs · Sandboxing](https://code.claude.com/docs/en/sandboxing)（访问于 2026-07-28）
- [Anthropic Docs · Settings](https://code.claude.com/docs/en/settings)（访问于 2026-07-28）

## 下一步

- 学如何控制成本 → [成本与 Token 管理](./cost-and-tokens)

## 如果你想

- 硬约束某个工具调用 → [Hooks](/claude-code/customization/hooks)
- OS 级别隔离（沙箱） → [Anthropic Docs · Sandboxing](https://code.claude.com/docs/en/sandboxing)
- 深入 Plan Mode → [Plan Mode](./plan-mode)
- 查所有 settings.json 字段 → [定制与扩展 · Settings 配置文件](/claude-code/customization/settings)

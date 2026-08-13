---
title: CLI Flags
description: '`claude` 命令的全部 flag 与 subcommand 分组速查'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/cli-reference'
  accessedAt: 2026-07-28
---

# CLI Flags

> **本页是速查表**——用 `Ctrl+F`。原理与场景请去对应主题页。
>
> 数据来源：本机 `claude --help`（v2.1.220，2026-07-28 抓取）+ Anthropic 官方 [CLI reference](https://code.claude.com/docs/en/cli-reference)。若你本机 `claude --help` 与本表有出入，**以你本机为准**——Claude Code 大约两周一版，flag 增删频繁。

⏱ 预计阅读时间：6 分钟（作为速查用）

## 调用形态

```text
claude [options] [command] [prompt]
```

- 不带任何参数 → 进交互式会话
- `claude "问题"` → 进交互式会话并把初始 prompt 灌进去
- `claude -p "问题"` → **headless**：跑完打印结果就退（管道友好）
- `claude <subcommand>` → 走子命令分支（见下方 subcommand 表）

## Flag 按用途分组

### ① 会话控制

| Flag | 说明 |
| --- | --- |
| `-c, --continue` | 继续当前目录最近一次会话 |
| `-r, --resume [id]` | 按 session id / name 恢复；不带参数打开交互选择器 |
| `--fork-session` | 恢复时创建新 session id（不复用原 id） |
| `--session-id <uuid>` | 强制指定本次的 session id |
| `-n, --name <name>` | 给会话起个显示名（`/resume` 选择器、终端标题显示） |
| `--from-pr [value]` | 按 PR 号/URL 恢复关联会话；不带值打开搜索器 |
| `--no-session-persistence` | 禁用会话持久化（会话结束即弃，仅 `-p` 生效） |

### ② 模型与推理

| Flag | 说明 |
| --- | --- |
| `--model <name>` | 别名（`fable` / `opus` / `sonnet` / `haiku`）或全名（`claude-fable-5`） |
| `--fallback-model <list>` | 主模型过载/不可用时逐个回退（逗号分隔，仅 `-p` 生效） |
| `--effort <level>` | `low` / `medium` / `high` / `xhigh` / `max` / `ultracode`；`ultracode` 起会话为 `xhigh` 且开启 workflow 编排（v2.1.203+） |
| `--max-budget-usd <amt>` | 最大 API 花费上限；v2.1.217+ 触顶时**停止**后台子代理并报错（仅 `-p` 生效） |
| `--json-schema <schema>` | 结构化输出的 JSON Schema（仅 `-p`；v2.1.205+ 支持 `format` 关键字） |

### ③ 权限与安全

| Flag | 说明 |
| --- | --- |
| `--permission-mode <mode>` | `default` / `acceptEdits` / `auto` / `plan` / `manual` / `dontAsk` / `bypassPermissions`；`manual` 自 v2.1.200 起是 `default` 的别名 |
| `--allowedTools, --allowed-tools <tools>` | 免询问放行工具（逗号或空格分隔），如 `"Bash(git *) Edit"` |
| `--disallowedTools, --disallowed-tools <tools>` | 禁用工具（同上格式） |
| `--tools <tools>` | 只启用列表内工具（`""` 全关，`default` 全开） |
| `--dangerously-skip-permissions` | **绕过所有权限检查**——仅用于**无网络的沙箱** |
| `--allow-dangerously-skip-permissions` | 允许在会话中启用上者、但默认不开 |
| `--add-dir <dirs...>` | 授权额外目录的文件访问 |
| `--safe-mode` | **v2.1.169+**——关掉所有自定义（CLAUDE.md / skills / plugins / hooks / MCP …）排查配置问题用 |
| `--bare` | 极简模式：跳过 hooks / LSP / plugin sync / auto-memory / CLAUDE.md 自动发现；Anthropic 认证仅 `ANTHROPIC_API_KEY` 或 `apiKeyHelper` |
| `--setting-sources <list>` | 只加载指定 setting 来源（`user,project,local` 三选） |

### ④ Headless（`-p` 场景专用）

| Flag | 说明 |
| --- | --- |
| `-p, --print` | 打印结果并退出（管道 / CI 场景）——**workspace trust 对话框会被跳过** |
| `--input-format <fmt>` | `text`（默认）/ `stream-json` |
| `--output-format <fmt>` | `text` / `json`（单结果）/ `stream-json`（实时流式） |
| `--include-partial-messages` | 输出分片消息（需 `--output-format=stream-json`） |
| `--include-hook-events` | 输出 hook 生命周期事件（需 `--output-format=stream-json`） |
| `--forward-subagent-text` | **v2.1.211+**——把子代理的 text/thinking 作为消息回传（需 stream-json） |
| `--replay-user-messages` | stdin 里的 user 消息回显到 stdout（用于确认） |
| `--prompt-suggestions [bool]` | 生成下一 prompt 建议 |

### ⑤ Prompt / 上下文自定义

| Flag | 说明 |
| --- | --- |
| `--system-prompt <text>` | 用它作为 system prompt |
| `--append-system-prompt <text>` | 追加到默认 system prompt 后 |
| `--exclude-dynamic-system-prompt-sections` | 把 cwd / env / memory / git status 从 system prompt 移到首条 user 消息，改善跨用户 prompt 缓存命中 |
| `--file <specs...>` | 启动时下载文件资源；格式 `file_id:relative_path` |
| `--agent <name>` | 覆盖 `agent` setting |
| `--agents <json>` | 内联定义 subagent（JSON 对象） |
| `--brief` | 启用 `SendUserMessage` 工具（agent→user 通信） |
| `--betas <list>` | API beta headers（仅 API key 用户） |
| `--disable-slash-commands` | 禁用所有 skill |

### ⑥ Plugin / MCP / 集成

| Flag | 说明 |
| --- | --- |
| `--mcp-config <files...>` | 加载 MCP 配置（JSON 文件或字符串） |
| `--strict-mcp-config` | 只用 `--mcp-config`，忽略其它 MCP 配置 |
| `--plugin-dir <path>` | 加载本地目录/zip 的插件（可重复） |
| `--plugin-url <url>` | 从 URL 拉取插件 zip（可重复） |
| `--settings <file-or-json>` | 额外 settings.json 或 JSON 字符串 |
| `--ide` | 启动时自动连 IDE（仅当唯一 IDE 可用） |
| `--chrome` / `--no-chrome` | 开关 "Claude in Chrome" 集成 |
| `--remote-control [name]` | 启用 Remote Control（可命名） |
| `--remote-control-session-name-prefix <prefix>` | Remote Control 自动生成名的前缀（默认 hostname） |

### ⑦ Worktree / 后台

| Flag | 说明 |
| --- | --- |
| `-w, --worktree [name]` | 为本次会话新建 git worktree |
| `--tmux` | 为 worktree 建 tmux 会话（需配合 `-w`；iTerm2 优先原生分屏） |
| `--bg, --background` | 作为后台 agent 启动并立即返回（**v2.1.198+ 与 `-p` 互斥**，用 `claude agents` 管理） |

### ⑧ 元与显示

| Flag | 说明 |
| --- | --- |
| `-h, --help` | 打印帮助 |
| `-v, --version` | 打印版本号 |
| `--verbose` | 覆盖 config 的 verbose 设置 |
| `-d, --debug [filter]` | debug 模式（`api,hooks` 过滤或 `!1p,!file` 排除） |
| `--debug-file <path>` | debug 日志写入指定文件（隐式开 debug） |
| `--ax-screen-reader` | **v2.1.181+**——扁平文本、无装饰边框，读屏软件友好 |

## Subcommands

`claude` 后跟 subcommand 走完全独立的分支：

| Subcommand | 作用 |
| --- | --- |
| `agents` | 管理后台 agent（`list` / `attach` / `stop` / `respawn` / `rm` 等，详见 `claude agents --help`） |
| `auth` | 认证：`login` / `logout` / `status` |
| `auto-mode` | 检查或重置 auto mode 分类器；`defaults`（v2.1.208+）打印默认规则、`reset`（v2.1.212+）清 user settings 里的 `autoMode` |
| `doctor` | 只读安装诊断（不进 trust 对话框），会话内的 `/doctor` 是它的加强版 |
| `gateway` | **v2.1.195+**——启自建 SSO / policy gateway（`--config gateway.yaml`） |
| `install [target]` | 安装原生二进制，`stable` / `latest` / 指定版本 |
| `mcp` | 管理 MCP servers；`login <name>` / `logout <name>` 走 OAuth（v2.1.186+） |
| `plugin` / `plugins` | 管理插件 |
| `project` | 项目状态；`purge [path]` 清空本地状态 |
| `setup-token` | 生成 CI / 脚本用的长期 OAuth token |
| `ultrareview [target]` | 跑云端多代理 code review 并打印结论 |
| `update` / `upgrade` | 检查并升级 |

## 典型用法

```bash
# Headless 单次调用 + 结构化输出
claude -p "总结这段" --model sonnet --output-format json

# 恢复最近会话
claude -c

# CI 里跑 plan 模式（不允许写盘）
claude -p "分析这个 PR 的破坏性变更" --permission-mode plan --model opus

# 新起一个 worktree 边跑
claude -w feature-x

# 排查配置问题
claude --safe-mode

# 后台 agent + 命名
claude --bg --name "batch-refactor"
```

## 坑与陷阱

- **`--print` 场景专属 flag**：`--fallback-model` / `--max-budget-usd` / `--json-schema` / `--input-format` / `--output-format` / `--include-*` / `--replay-user-messages` / `--no-session-persistence` 都**只在 `-p` 下生效**，交互模式静默忽略
- **`--bg` 与 `-p` 互斥**（v2.1.198 起）——后台跑 headless 用 `claude agents` 派发
- **`--dangerously-skip-permissions` 与 `-p --permission-mode plan` 互斥**——headless 里想走 plan 只能分开写
- **workspace trust 在 `-p` 或非-TTY 下自动跳过**——只在你信得过的目录用 `-p`
- **`--safe-mode` 不影响管理员策略 setting**——如果你的组织通过 managed settings 强制某些配置，`--safe-mode` 仍会应用它们
- **`--tools`、`--allowed-tools`、`--disallowed-tools` 三者共存时** `disallowedTools` 优先级最高（拒胜过允许）
- **flag 名不稳定**：v2.1.111 已移除 `--enable-auto-mode`（改用 `--permission-mode auto`）；跨大版本升级前先跑 `claude --help` 对齐

## 参考

- Anthropic Docs · [CLI reference](https://code.claude.com/docs/en/cli-reference)（访问于 2026-07-28）
- Anthropic Docs · [Headless mode](https://code.claude.com/docs/en/sdk/sdk-headless)（访问于 2026-07-28）
- 本机 `claude --help`（v2.1.220）

## 下一步

- 环境变量总表 → [环境变量](./env-vars) 🚧
- settings.json 完整字段 → [定制与扩展 · Settings 配置文件](/claude-code/customization/settings)
- 内置 Slash Command 全表 → [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)

## 如果你想

- 学 headless / CI 场景怎么用 → [Headless 模式](/claude-code/advanced/headless) 🚧
- 学权限档位与放行规则 → [权限系统](/claude-code/basics/permissions)
- 学模型切换 → [模型选择](/claude-code/basics/model-selection)

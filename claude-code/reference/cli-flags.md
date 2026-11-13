---
title: CLI Flags
description: '`claude` 命令的全部 flag 与 subcommand 分组速查'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 在本机 Claude Code v2.1.319 重新抓取 `claude --help` 与各 subcommand 的 `--help`，逐条核对 flag / subcommand 的存在性与语义；官方 CLI reference 与 Headless mode 两条外链沿用 2026-07-28 的旧记录'
  claudeCode: 2.1.319
  model: claude-opus-5-5
  officialDocs: 'https://code.claude.com/docs/en/cli-reference'
  accessedAt: 2026-11-13
---

# CLI Flags

> **本页是速查表**——用 `Ctrl+F`。原理与场景请去对应主题页。
>
> 数据来源：本机 `claude --help`（v2.1.319，2026-11-13 抓取）+ Anthropic 官方 [CLI reference](https://code.claude.com/docs/en/cli-reference)。若你本机 `claude --help` 与本表有出入，**以你本机为准**——Claude Code 大约两周一版，flag 增删频繁。

⏱ 预计阅读时间：7 分钟（作为速查用）

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
| `-r, --resume [value]` | 按 session id / name 恢复；不带参数打开交互选择器（可带搜索词） |
| `--fork-session` | 恢复时创建新 session id（不复用原 id） |
| `--session-id <uuid>` | 强制指定本次的 session id（须为合法 UUID） |
| `-n, --name <name>` | 给会话起显示名（prompt 框、`/resume` 选择器、终端标题） |
| `--from-pr [value]` | 按 PR 号 / URL 恢复关联会话；不带值打开搜索器 |
| `--no-session-persistence` | 禁用会话持久化（不落盘、不可恢复，仅 `-p` 生效） |
| `--teleport [session]` | 恢复 teleport 会话，可指定 session id |
| `--desktop` | 改在 Claude Desktop 应用里打开（配合 `--continue` / `--resume` 选会话） |
| `--cloud [description\|session_id\|url]` | 按描述创建云端会话，或按 session id / claude.ai/code URL 接入已有云端会话 |
| `--environment <environment_id>` | 在自建环境（`ccpool_…`）上开云端会话 |

### ② 模型与推理

| Flag | 说明 |
| --- | --- |
| `--model <name>` | 别名（`fable` / `opus` / `sonnet` / `haiku`）或全名（如 `claude-opus-5-5`）；Fable 最新 `claude-fable-5-2` 需 v2.1.321+ |
| `--fallback-model <model>` | 主模型过载 / 不可用时逐个回退（逗号分隔，每轮开头重试主模型） |
| `--effort <level>` | `low` / `medium` / `high` / `xhigh` / `max`；`med` = `medium`；`ultracode` 不是档位，但写了仍生效——等价 `xhigh` + 开启 ultracode 编排 |
| `--max-budget-usd <amount>` | 最大 API 花费上限（仅 `-p` 生效） |
| `--json-schema <schema>` | 结构化输出的 JSON Schema 校验（仅 `-p`） |

### ③ 权限与安全

| Flag | 说明 |
| --- | --- |
| `--permission-mode <mode>` | `acceptEdits` / `auto` / `bypassPermissions` / `manual` / `dontAsk` / `plan`；`manual` 是内部 `default` 的别名，`default` 也能写 |
| `--allowedTools, --allowed-tools <tools...>` | 免询问放行工具（逗号或空格分隔），如 `"Bash(git *) Edit"` |
| `--disallowedTools, --disallowed-tools <tools...>` | 禁用工具（同上格式） |
| `--tools <tools...>` | 只启用列表内工具（`""` 全关，`default` 全开） |
| `--dangerously-skip-permissions` | **绕过所有权限检查**——仅用于**无网络的沙箱** |
| `--allow-dangerously-skip-permissions` | 允许在会话中启用上者、但默认不开 |
| `--restricted` | 受限模式：移除 Bash 等执行类内置工具与 WebFetch，忽略 user / project / local settings，文件工具限于工作目录，且拒绝 bypassPermissions |
| `--add-dir <directories...>` | 授权额外目录的文件访问 |
| `--safe-mode` | 关掉所有自定义（CLAUDE.md / skills / plugins / hooks / MCP 等），排查配置问题用 |
| `--bare` | 极简模式：跳过 hooks / LSP / plugin sync / auto-memory / CLAUDE.md 自动发现；认证仅 `ANTHROPIC_API_KEY` 或 `apiKeyHelper` |
| `--setting-sources <sources>` | 只加载指定 setting 来源（`user,project,local` 三选） |

### ④ Headless（`-p` 场景专用）

| Flag | 说明 |
| --- | --- |
| `-p, --print` | 打印结果并退出（管道 / CI 场景）——**workspace trust 对话框会被跳过** |
| `--input-format <format>` | `text`（默认）/ `stream-json` |
| `--output-format <format>` | `text` / `json`（单结果）/ `stream-json`（实时流式） |
| `--include-partial-messages` | 输出分片消息（需 `--output-format=stream-json`） |
| `--include-hook-events` | 输出 hook 生命周期事件（需 `--output-format=stream-json`） |
| `--forward-subagent-text` | 把子代理的 text / thinking 作为消息回传（需 `-p` + stream-json） |
| `--replay-user-messages` | stdin 里的 user 消息回显到 stdout（需 input / output 都是 stream-json） |
| `--prompt-suggestions [value]` | 生成下一条 prompt 建议；print / SDK 模式下每轮结束发 `prompt_suggestion` 消息 |
| `--permission-prompts <target>` | `-p` 下由谁回答权限询问：`host`（宿主或 `--permission-prompt-tool`）/ `none`（一律自动拒绝），默认 `host` |
| `--permission-prompt-tool <tool>` | 用指定 MCP tool 回答权限询问（仅 `-p`；`claude --help` 不显示，属 SDK 用法） |

### ⑤ Prompt / 上下文自定义

| Flag | 说明 |
| --- | --- |
| `--system-prompt <prompt>` | 用它作为 system prompt |
| `--append-system-prompt <prompt>` | 追加到默认 system prompt 后 |
| `--system-prompt-snapshot <on\|off>` | `on`（默认）= 每个会话只渲染一次 system prompt 并原样重发（含 resume）；`off` = 每次请求重新渲染 |
| `--exclude-dynamic-system-prompt-sections` | 把 cwd / env / memory 路径 / git status 从 system prompt 移到首条 user 消息，提升跨用户 prompt 缓存命中 |
| `--autocompact <auto\|tokens>` | auto-compact 窗口：`auto`（按模型调优）或 100k–1M tokens（如 `500k` / `200000`） |
| `--file <specs...>` | 启动时下载文件资源；格式 `file_id:relative_path` |
| `--agent <agent>` | 覆盖 `agent` setting |
| `--agents <json-or-file>` | 内联定义 subagent（JSON 对象）；`-p` 下也可给文件路径 |
| `--brief` | 启用 `SendUserMessage` 工具（agent→user 通信） |
| `--betas <betas...>` | API beta headers（仅 API key 用户） |
| `--disable-slash-commands` | 禁用所有 skill 与命令 |

### ⑥ Plugin / MCP / 集成

| Flag | 说明 |
| --- | --- |
| `--mcp-config <configs...>` | 加载 MCP 配置（JSON 文件或字符串，空格分隔） |
| `--strict-mcp-config` | 只用 `--mcp-config`，忽略其它 MCP 配置 |
| `--plugin-dir <path>` | 加载本地目录 / zip 的插件（可重复） |
| `--plugin-url <url>` | 从 URL 拉取插件 zip（可重复） |
| `--settings <file-or-json>` | 额外 settings.json 或 JSON 字符串 |
| `--ide` | 启动时自动连 IDE（仅当唯一 IDE 可用） |
| `--chrome` / `--no-chrome` | 开关 "Claude in Chrome" 集成 |
| `--remote-control [name]` | 以 Remote Control 开启交互式会话（可命名） |
| `--remote-control-session-name-prefix <prefix>` | Remote Control 自动生成名的前缀（默认 hostname） |

### ⑦ Worktree / 后台

| Flag | 说明 |
| --- | --- |
| `-w, --worktree [name]` | 为本次会话新建 git worktree |
| `--tmux` | 为 worktree 建 tmux 会话（需配合 `-w`；iTerm2 优先原生分屏，`--tmux=classic` 走传统 tmux） |
| `--bg, --background` | 后台启动并立刻返回，打印 session id（`claude attach` / `logs` / `stop` / `rm` 消费它）；配 `--resume <id>` 可在后台续跑同一 id |

### ⑧ 元与显示

| Flag | 说明 |
| --- | --- |
| `-h, --help` | 打印帮助 |
| `-v, --version` | 打印版本号 |
| `--verbose` | 覆盖 config 的 verbose 设置 |
| `-d, --debug [filter]` | debug 模式，可按类别过滤（如 `--debug=hooks,mcp` 或 `--debug='!hooks,!mcp'`） |
| `--debug-file <path>` | debug 日志写入指定文件（隐式开 debug） |
| `--ax-screen-reader` | 扁平文本、无装饰边框，读屏软件友好 |

## Subcommands

`claude` 后跟 subcommand 走完全独立的分支：

| Subcommand | 作用 |
| --- | --- |
| `agents` | 管理后台 agent（`--json` 可脚本化，详见 `claude agents --help`） |
| `attach <id\|name>` | 在当前终端打开一个后台会话 |
| `auth` | 认证：`login` / `logout` / `status` |
| `auto-mode` | 查看或重置 auto mode 配置：`config` / `critique` / `defaults` / `reset` |
| `doctor` | 只读安装诊断（不触发 trust 对话框）；会话内的 `/doctor` 才能修复问题 |
| `gateway` | 启企业 auth / telemetry gateway（`--config gateway.yaml`） |
| `import [source]` | 从别的 AI coding agent 导入配置（`codex` / `gemini` / `cursor`） |
| `install [target]` | 安装原生二进制：`stable` / `latest` / 指定版本 |
| `logs <id\|name>` | 打印后台会话最近的终端输出 |
| `mcp` | 管理 MCP servers；`login <name>` / `logout <name>` 走 OAuth |
| `plugin` / `plugins` | 管理插件 |
| `purge [path]` | 删除某项目的 Claude Code 本地数据（transcripts / tasks / file history / `~/.claude.json` 条目），仅限本机 |
| `respawn [id]` | 重启后台会话（`--all` 重启全部）以换到当前版本 |
| `rm <id>` | 删除后台会话及其 worktree（已退出的会话也能删） |
| `setup-token` | 生成 CI / 脚本用的长期 OAuth token（需 Claude 订阅） |
| `stop` / `kill <id>` | 停后台会话（对话保留，之后可 `attach` 或 `--resume`） |
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

- **`-p` 专属 flag**：`--max-budget-usd` / `--json-schema` / `--input-format` / `--output-format` / `--include-*` / `--forward-subagent-text` / `--replay-user-messages` / `--no-session-persistence` / `--permission-prompts` / `--permission-prompt-tool` 都**只在 `-p` 下生效**，交互模式静默忽略；`--fallback-model` 例外，交互模式同样生效
- **`--bg` 与 `-p` 互斥**——`--print` 起的会话没有可 attach 的交互终端；后台跑写 `claude --bg '<task>'`，别加 `--print`
- **`--bg` 与 `--cloud` / `--environment` 也互斥**——三者后端不同，要上云直接 `claude --cloud '<task>'` 或 `claude -p '<task>' --environment <id>`
- **`--desktop` 不能和子命令或 `--bg` 同用**
- **workspace trust 在 `-p` 或 stdout 非 TTY 时自动跳过**——只在你信得过的目录用 `-p`
- **`--safe-mode` 不影响管理员策略 setting**——managed settings 仍会生效
- **`--tools` / `--allowed-tools` / `--disallowed-tools` 三者共存时**，deny 规则优先（拒胜过允许）
- **`--effort` 写错不报错**：只告警 `Unknown --effort value` 并回落到默认档；`ultracode` 不在 `--help` 的档位里，但写了仍生效——等价 `xhigh` + ultracode 编排（需 workflows 已开且模型支持）
- **`--enable-auto-mode` 并没有被删**——仍在，但已 deprecated 且 `--help` 不显示；改用 `--permission-mode auto` 或 `claude auto-mode`
- **`claude project purge` 已改名 `claude purge`**——`claude project` 现在只提示迁移
- **flag 名不稳定**：跨大版本升级前先跑 `claude --help` 对齐

## 参考

- Anthropic Docs · [CLI reference](https://code.claude.com/docs/en/cli-reference)（访问于 2026-07-28）
- Anthropic Docs · [Headless mode](https://code.claude.com/docs/en/sdk/sdk-headless)（访问于 2026-07-28）
- 本机 `claude --help`（v2.1.319，2026-11-13 抓取）

## 下一步

- 环境变量总表 → [环境变量](./env-vars) 🚧
- settings.json 完整字段 → [定制与扩展 · Settings 配置文件](/claude-code/customization/settings)
- 内置 Slash Command 全表 → [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)

## 如果你想

- 学 headless / CI 场景怎么用 → [Headless 模式](/claude-code/advanced/headless) 🚧
- 学权限档位与放行规则 → [权限系统](/claude-code/basics/permissions)
- 学模型切换 → [模型选择](/claude-code/basics/model-selection)

---
title: Headless / CI 模式
description: 'claude -p 非交互调用——管道化、--output-format json/stream-json、--bare 极速启动、--allowedTools 自动批准、--json-schema 结构化输出、CI 集成'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  headlessDocs: 'https://code.claude.com/docs/en/headless'
  accessedAt: 2026-08-04
---

# Headless / CI 模式

> **TL;DR**：`claude -p "<prompt>"` 非交互跑 Claude Code——管道进出、脚本化、CI 集成。`--bare` 跳过 hooks/skills/CLAUDE.md 极速启动（CI 推荐）。`--output-format json` 拿结构化结果，`--allowedTools` 免交互批准工具，`--json-schema` 强制 schema 输出。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- `claude -p` 基本用法与 stdin/stdout 管道
- `--bare` 极速启动模式（CI 推荐）
- 三种输出格式：text / json / stream-json
- `--allowedTools` 与 `--permission-mode` 免交互
- `--json-schema` 结构化输出
- 会话续接：`--continue` / `--resume`
- CI 集成实践

## 前置

- 读过 [权限系统](../basics/permissions) 和 [Settings 配置文件](../customization/settings)
- 有 ANTHROPIC_API_KEY 或已登录

## 一、基本用法

```bash
claude -p "What does the auth module do?"
```

- 成功退出码 0，失败非 0（脚本可分支）
- 读 stdin、写 stdout——可管道

**管道数据进、结果出**：

```bash
cat build-error.txt | claude -p 'concisely explain the root cause' > output.txt
```

**stdin 上限 10MB**（v2.1.128+）——超了写文件、路径放 prompt 里。

## 二、--bare 极速启动（CI 推荐）

`--bare` 跳过 hooks / skills / plugins / MCP / auto memory / CLAUDE.md 自动发现——**CI 每台机器结果一致**。队友的 `~/.claude` hook 或项目 `.mcp.json` 不跑。

```bash
claude --bare -p "Summarize README.md" --allowedTools "Read"
```

**bare 模式**：

- 不读 OAuth / 系统钥匙串——必须设 `ANTHROPIC_API_KEY`（或 `--settings` 里 `apiKeyHelper`）
- 只有 Bash / 文件读 / 文件写工具
- 需要的上下文用 flag 传：

| 要加载 | flag |
| --- | --- |
| 系统提示补充 | `--append-system-prompt` |
| settings | `--settings <file\|json>` |
| MCP servers | `--mcp-config <file\|json>` |
| 自定义 agent | `--agents <json>` |
| plugin | `--plugin-dir` / `--plugin-url` |

**官方建议**：脚本化 / SDK 调用都用 `--bare`，未来会成为 `-p` 默认。

## 三、输出格式

```bash
# text（默认）
claude -p "Summarize this project"

# json（含 session_id / total_cost_usd / result）
claude -p "Summarize this project" --output-format json

# stream-json（实时流式）
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

**JSON 输出字段**：

| 字段 | 说明 |
| --- | --- |
| `result` | 文本结果 |
| `session_id` | 会话 ID（可 `--resume` 续接） |
| `total_cost_usd` | 本次花费 |
| `is_error` | 是否出错 |
| `subtype` | 结果子类型 |

**用 jq 提取**：

```bash
claude -p "Summarize" --output-format json | jq -r '.result'
```

## 四、--json-schema 结构化输出

强制返回符合 schema 的 JSON，放在 `structured_output` 字段：

```bash
claude -p "Extract main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

```bash
# 提取结构化部分
... | jq '.structured_output'
```

**schema 非法会报错退出**（v2.1.205+）。`format` 关键字当注解、不强制。

## 五、免交互批准工具

**`--allowedTools` 白名单**：

```bash
claude -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"
```

**权限规则语法**（同 settings.json）：

```bash
claude -p "Create a commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git commit *)"
```

` *` 前缀匹配——注意空格：`Bash(git diff *)` 匹配 `git diff` 开头，`Bash(git diff*)` 会误匹配 `git diff-index`。

**`--permission-mode`**：

- `acceptEdits`：文件写 + 常见 fs 命令（mkdir/touch/mv/cp）自动批准
- `dontAsk`：只认 `permissions.allow` 规则 + 只读命令集，**锁定 CI 推荐**

## 六、续接会话

```bash
# 第一次
claude -p "Review this codebase for performance issues"

# 续最近一次
claude -p "Now focus on the database queries" --continue

# 续指定 session
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

session ID 查找按当前项目目录 + git worktree 作用域。

## 七、自定义系统提示

```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

- `--append-system-prompt`：补充，保留默认行为
- `--system-prompt`：完全替换默认

## 八、CI 集成实践

### package.json 脚本（typo linter）

```json
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo report filename:line and the issue.\""
  }
}
```

### CI 推荐组合

```bash
claude --bare -p "<task>" \
  --allowedTools "Bash,Read,Edit" \
  --permission-mode acceptEdits \
  --output-format json
```

- `--bare`：环境一致
- `--allowedTools` + `--permission-mode`：免交互
- `--output-format json`：可解析

### stream-json 抓 system/init 事件

`system/init` 报 session 元数据（model / tools / MCP / plugins）。**CI 门禁**可查 `plugin_errors` / `mcp_server_errors` 非空时 fail：

```bash
claude -p "..." --output-format stream-json --verbose | \
  jq 'select(.subtype == "init") | .mcp_server_errors'
```

## 九、后台任务与退出

- `claude -p` 里起的 background Bash 任务：结果返回后 5 秒 grace 再杀（v2.1.163+）
- background subagent / workflow：等完成，上限 10 分钟（`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` 调）
- SIGTERM 终止：中断当前轮 + 杀进程树 + 跑 `SessionEnd` hook + 退出码 143

## 常见坑

**CI 里没设 API key**——bare 模式不读 OAuth。设 `ANTHROPIC_API_KEY` 或在 `--settings` 里配 `apiKeyHelper`。

**`--allowedTools` 通配符没空格**——`Bash(git diff*)` 误匹配 `git diff-index`。写成 `Bash(git diff *)`。

**stdin 超 10MB**——v2.1.128+ 报错退出。写文件、路径放 prompt。

**CI 里 plugin/MCP 没加载没报错**——`-p` 默认静默跳过。用 `--output-format stream-json` 抓 `system/init` 的 `plugin_errors` / `mcp_server_errors` 做门禁。

**stream-json 消费太慢**——Claude Code 等输出排空再退出（上限 30 秒）。慢消费者可能被截断。

## 参考

- [Anthropic · Run Claude Code programmatically](https://code.claude.com/docs/en/headless)（访问于 2026-08-04）
- [Anthropic · CLI reference](https://code.claude.com/docs/en/cli-reference)（访问于 2026-08-04）—— 全 flag 清单
- [Anthropic · GitHub Actions](https://code.claude.com/docs/en/github-actions)（访问于 2026-08-04）

## 下一步

- 后台与定时任务 → [后台与定时任务](./automation)
- Git 与 PR 工作流 → [Git 与 PR 工作流](./git-workflow)
- Worktree 隔离 → [Worktree 隔离](./worktree)

## 如果你想

- 用 Python / TypeScript SDK 编程控制 → [Anthropic · Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview)
- 看 stream-json 完整事件类型 → [Anthropic · Agent SDK · Streaming](https://code.claude.com/docs/en/agent-sdk/streaming-output)
- CI 里用 worktree 隔离 → `claude -p --worktree`（非交互跳过 trust 检查）

---
title: Hooks
description: Claude Code 的生命周期钩子——用 shell 脚本拦截工具调用、注入上下文、触发自动化，无需 LLM 参与决策
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-08
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  hooksDocs: 'https://code.claude.com/docs/en/hooks'
  accessedAt: 2026-08-08
---

# Hooks

> **TL;DR**：Hook 是 Claude Code 在**确定时机**跑的 shell 脚本——不走 LLM 决策、不消耗 token、不可覆盖。用它做「每次编辑后跑 lint」「拦截 `rm -rf`」「session 启动注入环境变量」这类确定性自动化。配置在 `settings.json` 的 `hooks` 字段里；stdin 收 JSON 输入，exit code 控制行为（0 = 通过、2 = 阻断）。

⏱ 预计阅读时间：12 分钟

## 你能在这里学到

- Hook 与 Skill 的本质区别（确定性 / 无 LLM / 不可覆盖）
- 完整事件清单：session 级 / turn 级 / 工具级 / 其它
- `hooks.json` 配置格式：matcher / command / timeout / if
- stdin JSON 输入结构与 exit code 语义
- 五种 hook 类型：command / http / mcp_tool / prompt / agent
- stdout JSON 高级控制（allow / deny / block / continue:false）
- 三个经典用例从头到尾走通

## 前置

- 知道 [Skill vs Command vs Agent](../skills/skills-vs-commands-vs-agents) 里 Hook 的定位
- 会写基础 shell 脚本、知道 `jq` 能解析 JSON
- Claude Code v2.1.220

## 一、Hook vs Skill 本质区别

| | Hook | Skill |
| --- | --- | --- |
| 触发 | **系统事件**（工具调用前/后、session 开始/结束……） | 用户敲 `/` 或 Claude 自己判断 |
| LLM 参与 | **否**——纯 shell / HTTP | 是——LLM 读 body 并执行 |
| Token 消耗 | 零（除非显式用 stdout 注入 context） | 加载到 context 占 token |
| 能否覆盖 | 不能被同名覆盖（多层配置**合并**） | 同名高优先级覆盖低优先级 |
| 典型场景 | 拦截危险操作、自动 lint、注入环境 | 领域知识、代码生成模板 |

**判断口诀**：需要 Claude 决策 → Skill；不需要决策、事件到了就跑 → Hook。

## 二、事件清单

### Session 级（一次 session 触发一次）

| 事件 | 时机 |
| --- | --- |
| `SessionStart` | session 启动或恢复 |
| `SessionEnd` | session 结束 |
| `Setup` | `--init-only` / `--init` / `-p --maintenance` 启动时 |

### Turn 级（每轮用户输入触发一次）

| 事件 | 时机 |
| --- | --- |
| `UserPromptSubmit` | 用户提交 prompt，Claude 处理之前 |
| `UserPromptExpansion` | 用户输入的命令展开后 |
| `Stop` | Claude 本轮回复结束 |
| `StopFailure` | 本轮因 API 错误中止 |

### 工具级（每次工具调用触发）

| 事件 | 时机 | 能阻断？ |
| --- | --- | --- |
| `PreToolUse` | 工具执行前 | ✅ exit 2 阻断 |
| `PostToolUse` | 工具执行成功后 | ❌ 已执行 |
| `PostToolUseFailure` | 工具执行失败后 | ❌ |
| `PostToolBatch` | 一批并行工具调用完成后 | ❌ |
| `PermissionRequest` | 工具需要权限决策时 | ✅ |
| `PermissionDenied` | 工具被自动模式分类器拒绝时 | ❌ |

### 其它事件

| 事件 | 时机 |
| --- | --- |
| `SubagentStart` / `SubagentStop` | subagent 启动 / 结束 |
| `TaskCreated` / `TaskCompleted` | 任务创建 / 完成 |
| `PreCompact` / `PostCompact` | 上下文压缩前 / 后 |
| `Notification` | Claude Code 发通知 |
| `InstructionsLoaded` | CLAUDE.md 或 `.claude/rules/*.md` 被加载 |
| `ConfigChange` | session 期间配置文件变更 |
| `CwdChanged` | 工作目录变更 |
| `FileChanged` | 监控文件变更 |
| `WorktreeCreate` / `WorktreeRemove` | worktree 创建 / 删除 |
| `TeammateIdle` | agent team 成员空闲 |

## 三、配置格式

Hook 配置在 `settings.json`（user / project / local 三层合并）的 `hooks` 字段里：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**三层嵌套**：

1. **事件名**（如 `PreToolUse`）
2. **Matcher 组**（过滤哪些工具触发）
3. **Hook handler 数组**（具体跑什么）

### Matcher 语法

| 写法 | 含义 |
| --- | --- |
| `"*"` / `""` / 省略 | 匹配所有工具 |
| `"Bash"` | 精确匹配 |
| `"Edit\|Write"` 或 `"Edit, Write"` | 多个精确匹配 |
| `"^Notebook"` / `"mcp__memory__.*"` | 正则（不自动锚定） |

### Handler 字段

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `type` | ✅ | `"command"` / `"http"` / `"mcp_tool"` / `"prompt"` / `"agent"` |
| `command` | 仅 command | 要执行的 shell 命令 |
| `if` | 否 | 权限规则过滤，如 `"Bash(git *)"` / `"Edit(*.ts)"` |
| `timeout` | 否 | 超时秒数（command 默认 600） |
| `async` | 否 | 后台运行不阻塞 |
| `statusMessage` | 否 | 自定义 spinner 文本 |

## 四、stdin 输入与 exit code

每个 hook 通过 **stdin** 收到一段 JSON，包含：

```json
{
  "session_id": "abc123",
  "cwd": "/home/user/my-project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Delete node_modules"
  }
}
```

各事件的 `tool_input` / 附加字段不同——统一规律是：**读 stdin、用 `jq` 提取你要的字段**。

### Exit code 语义

| Exit code | 含义 |
| --- | --- |
| **0** | 通过。stdout 被解析为 JSON（若有） |
| **2** | **阻断**。stderr 作为错误消息反馈给 Claude |
| **其它** | 非阻断错误。stderr 首行显示在 transcript，继续执行 |

**⚠️ 只有 exit 2 能阻断**——exit 1 是非阻断的（与直觉不同）。

### 哪些事件能被 exit 2 阻断

| 事件 | 阻断效果 |
| --- | --- |
| `PreToolUse` | 阻止工具执行 |
| `PermissionRequest` | 拒绝权限 |
| `UserPromptSubmit` | 阻止 prompt 处理 |
| `Stop` / `SubagentStop` | 阻止结束，继续对话 |
| `PreCompact` | 阻止压缩 |
| `WorktreeCreate` | 任何非零 exit 都中止创建 |

## 五、stdout JSON 高级控制

Exit 0 时 stdout 可输出 JSON 做更精细控制：

**阻断工具并给出原因**（替代 exit 2）：

```json
{
  "decision": "block",
  "reason": "Database writes disabled in this environment"
}
```

**PreToolUse 四种 permissionDecision**：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "rm -rf not allowed"
  }
}
```

`permissionDecision` 可选 `"allow"` / `"deny"` / `"ask"` / `"defer"`。

**让 Claude 完全停止**：

```json
{
  "continue": false,
  "stopReason": "Build failed, fix errors before continuing"
}
```

**注入上下文让 Claude 看到**：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts instead."
  }
}
```

**⚠️ 注意**：stdout 上限 **10,000 字符**；exit 2 时 stdout 被忽略，只有 exit 0 解析 JSON。

## 六、配置位置与合并规则

| 位置 | 作用域 | 能 commit |
| --- | --- | --- |
| `~/.claude/settings.json` | 你所有项目 | ❌ |
| `.claude/settings.json` | 单项目 | ✅ |
| `.claude/settings.local.json` | 单项目只你 | ❌ |
| managed settings | 组织全局 | 管理员控制 |
| plugin `hooks/hooks.json` | plugin 启用时 | ✅ 跟 plugin |

**合并而非替换**——同一事件在多层定义的 hook **全部跑**，不像 skill 同名覆盖。用 `disableAllHooks: true` 关闭全部非 managed hooks。

**环境变量**（在 `command` 里可用）：

| 变量 | 含义 |
| --- | --- |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录 |
| `${CLAUDE_PLUGIN_ROOT}` | plugin 安装目录（plugin hook） |
| `${CLAUDE_PLUGIN_DATA}` | plugin 持久数据目录 |

## 七、三个经典用例

### 用例 1：拦截危险 `rm` 命令

`.claude/hooks/block-rm.sh`：

```bash
#!/bin/bash
input=$(cat)
cmd=$(jq -r '.tool_input.command' <<<"$input")

if [[ "$cmd" == rm* ]]; then
  echo "Blocked: rm commands not allowed" >&2
  exit 2
fi
exit 0
```

配置（`.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "if": "Bash(rm *)", "command": ".claude/hooks/block-rm.sh" }]
      }
    ]
  }
}
```

### 用例 2：每次编辑后自动 lint

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "npx eslint --fix $(jq -r '.tool_input.file_path')", "timeout": 30 }]
      }
    ]
  }
}
```

### 用例 3：session 启动注入 sprint 上下文

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "cat .claude/sprint-context.md" }]
      }
    ]
  }
}
```

`SessionStart` 的 stdout（exit 0）会被注入到 Claude 看到的上下文里。

## 八、调试

- 敲 `/hooks` 打开只读浏览器——看所有事件、matcher、handler 来源
- `claude --debug` 启动——看完整 stderr、JSON 解析失败、stdout 内容
- stdin 里的 `transcript_path` 指向会话 JSONL——但它**异步写入**，可能滞后

## 九、实战补充：vibecoding 视角的 hook 设计

基础事件 + 配置 + stdout JSON 上面都讲了，这一节补 3 个**写多了才悟出来**的实战模式。

### 9.1 避免上下文膨胀：format 只管当前文件

PostToolUse 跑 `prettier --write .` 是最常见反模式——整项目 diff 倒进 context，挤爆窗口。

**正确做法**：PostToolUse 只 format **当前编辑文件**（用 `jq -r '.tool_input.file_path'` 提取）；formatter 改动频繁时**移到 git pre-commit 或 Stop hook**；lint 单文件足够，全量留给 CI。

### 9.2 路径感知：matcher + 脚本判断 + rules/ 联动

**两层过滤**：

| 层级 | 工具 | 示例 |
| --- | --- | --- |
| matcher 粗筛 | `settings.json` 的 matcher 字段 | `"Edit\|Write"` 限定到编辑类工具 |
| 脚本内精筛 | shell 里读 stdin 后判断扩展名 / 路径 | `[[ $FILE == *.ts* ]]` 只对 TS 文件跑 eslint |

更精细——按目录或框架分包——用 [`.claude/rules/`](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules) 的 **path-scoped 规则**联动 hook：rule 限定范围，hook 只在命中的路径上跑对应检查（[实战示例](/claude-code/basics/claude-md#path-scoped-rules-实战补充)）。

### 9.3 Stop hook + prompt hook：自验证模式

**用 Stop hook 强制 Claude 自验证**：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "prompt",
            "prompt": "跑 pnpm test 全绿才允许 stop，否则继续修。" }
        ]
      }
    ]
  }
}
```

`type: "prompt"` hook 起轻量 LLM 调用跑这段 prompt，exit code 决定是否阻断 stop。配合 lint 硬校验脚本形成「质量闭环」——Claude 不能轻易把没跑测试的代码说成完成。

> 实战参考：[claude-wiki 自身的 `.claude/` 配置](https://coding.jd.com/sz-fe/claude-wiki/tree/main/.claude)——链接检查 / 死链扫描 / sidebar 同步都是 hook 驱动的。

## 常见坑

**Exit 1 不阻断**——很多人以为非零就阻断，实际只有 **exit 2** 阻断。exit 1 是非阻断错误（仅显示 stderr 首行）。

**stdout 混了非 JSON 内容**——shell 的 `.bashrc` / `.zshrc` 里有 `echo` 或 `motd`，导致 JSON 解析失败。用 `#!/bin/bash` + 确保无额外输出，或写到独立脚本文件。

**hook 超时**——默认 600 秒（command 类型）；如果 hook 里调外部 API 或跑重活，调小 `timeout` 并加 `async: true` 后台跑。

**多层 hooks 全部执行不是覆盖**——不像 skill 同名覆盖，hooks 在 user / project / local / plugin 里**全部合并执行**。想关掉项目级 hook 只能 `disableAllHooks: true`（一刀切）或移除配置。

## 参考

- [Anthropic · Hooks](https://code.claude.com/docs/en/hooks)（访问于 2026-08-03）
- [Anthropic · Settings reference · hooks 字段](https://code.claude.com/docs/en/settings)（访问于 2026-08-03）
- [Skill vs Command vs Agent](../skills/skills-vs-commands-vs-agents) — 选型参考

## 下一步

- 把 hook 打包到 plugin 里分发 → [Plugins 与 Marketplace](../skills/plugins-marketplace)
- 配合 skill 做「拦截 + 知识注入」组合 → [Skill vs Command vs Agent · 组合使用](../skills/skills-vs-commands-vs-agents#四、组合使用)
- 看完整 settings.json 结构 → [Settings 配置文件](./settings) 🚧

## 如果你想

- 看有哪些现成的 hook 可用 → [内置 Skills 一览](../skills/built-in-skills)（bundled skill 部分行为用 hook 实现）
- 用 http 类型 hook 接外部 webhook → 参考 [Anthropic · HTTP hooks](https://code.claude.com/docs/en/hooks)
- 在 plugin 里配 hook → [Plugins 与 Marketplace · 目录结构](../skills/plugins-marketplace#三、写一个最小-plugin)

---
title: Settings 配置文件
description: 'Claude Code settings.json 完整指南——5 种 scope 优先级、permissions 合并规则、常用字段（env / model / apiKeyHelper / MCP / plugins / skills）、workspace trust 机制'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  settingsDocs: 'https://code.claude.com/docs/en/settings'
  accessedAt: 2026-08-04
---

# Settings 配置文件

> **TL;DR**：`.claude/settings.json` 是 Claude Code 的主配置。5 种 scope 按优先级覆盖：**managed > CLI > local > project > user**。权限规则特殊——**跨 scope 合并**而非覆盖。项目级 allow 规则需要 workspace trust 才生效（防恶意仓库）。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- 5 种 scope 的位置与优先级
- permissions 的合并规则（与普通字段不同）
- 常用字段速查：env / model / apiKeyHelper / MCP / plugins / skills
- workspace trust 机制
- managed settings 企业部署

## 前置

- 读过 [权限系统](../basics/permissions) 和 [Hooks](./hooks)

## 一、5 种 Scope 优先级

高 → 低：

| 优先级 | scope | 位置 | 共享 |
| --- | --- | --- | --- |
| 1（最高） | **Managed** | 服务端 / MDM / `/etc/claude-code/managed-settings.json` | IT 部署 |
| 2 | **CLI 参数** | `claude --xxx` | 临时 session |
| 3 | **Local** | `.claude/settings.local.json` | ❌ gitignore |
| 4 | **Project** | `.claude/settings.json` | ✅ 提交 git |
| 5（最低） | **User** | `~/.claude/settings.json` | ❌ 个人 |

**何时用哪个**：

- **User**：个人偏好（主题、编辑器模式）、跨项目插件、API key
- **Project**：团队共享（权限、hooks、MCP server、插件）
- **Local**：某项目个人覆盖、测试中配置、机器特定
- **Managed**：组织安全策略、合规要求、IT 统一配置

## 二、合并规则（关键）

| 字段类型 | 合并方式 |
| --- | --- |
| **标量**（string/number/bool） | 高优先级覆盖低 |
| **permissions**（allow/deny/ask） | **跨 scope 合并**（不覆盖） |
| **多数数组** | 合并 + 去重 |
| **`fallbackModel`** | 不合并，最高优先级文件整条提供 |

**permissions 特殊性**：你在 user scope allow 了 `Bash(npm test)`，project scope allow 了 `Bash(npm run lint)`——两条**都生效**，不是 project 覆盖 user。

**热更新**：Claude Code 监听 settings 文件，改后自动 reload，无需重启。例外：`model` 和 `outputStyle` 只在 session 启动时读，改后要 `/model` 切换或重启。

## 三、常用字段速查

### permissions

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "ask": [
      "Bash(git push *)"
    ]
  }
}
```

- `allow`：自动批准
- `deny`：自动拒绝
- `ask`：每次问

**规则语法**：`Tool(specifier)`，支持通配符 `*` / `**`。

### env

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

注入到每个 session 及 Claude Code 生成的子进程。设 `""` 可覆盖 shell 导出值。

### model 与 apiKeyHelper

```json
{
  "model": "claude-opus-4-8",
  "apiKeyHelper": "/bin/generate_temp_api_key.sh"
}
```

- `model`：session 启动时读一次，中途用 `/model` 切换
- `apiKeyHelper`：自定义命令生成 auth 值，作 `X-Api-Key` + `Authorization: Bearer` header

### MCP 相关

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["memory", "github"],
  "disabledMcpjsonServers": ["filesystem"]
}
```

- `enableAllProjectMcpServers`：批准 `.mcp.json` 全部 server
- `enabledMcpjsonServers` / `disabledMcpjsonServers`：按名批准/拒绝

### Plugins 与 Skills

```json
{
  "enabledPlugins": {
    "github": true
  },
  "extraKnownMarketplaces": {
    "sz-fe-plugins": {
      "source": { "source": "github", "repo": "sz-fe/claude-plugins" }
    }
  },
  "disableBundledSkills": true,
  "skillOverrides": {
    "code-review": "off"
  }
}
```

- `enabledPlugins`：启用/禁用 plugin（managed 可 force-enable）
- `extraKnownMarketplaces`：注册额外 marketplace
- `disableBundledSkills`：关掉内置 skills（`/init` 等命令仍可打但隐藏）
- `skillOverrides`：按名覆盖 skill（`off` / `name-only` / `full`）

### 其它常用

| 字段 | 默认 | 说明 |
| --- | --- | --- |
| `cleanupPeriodDays` | 30 | session 文件保留天数（最小 1） |
| `includeCoAuthoredBy` | true | git commit 加 Co-Authored-By |
| `alwaysThinkingEnabled` | false | 默认开 extended thinking |
| `autoCompactEnabled` | true | 接近 context 上限自动压缩 |
| `editorMode` | `"normal"` | `"normal"` / `"vim"` |
| `defaultShell` | `"bash"` | `!` 命令用的 shell |
| `fileCheckpointingEnabled` | true | 文件快照供 `/rewind` |
| `disableAllHooks` | false | 关掉所有 hook |

## 四、Workspace Trust

**项目级 `.claude/settings.json` 的 `permissions.allow` 规则需要 workspace trust 才生效**——防恶意仓库自动授权。

| 文件 | allow 规则生效条件 |
| --- | --- |
| `.claude/settings.json`（跟仓库） | 需 workspace trust |
| `.claude/settings.local.json`（gitignore） | **不需要** trust（你的文件） |
| `~/.claude/settings.json`（用户） | 不需要 trust |
| managed settings | 不需要 trust |

**首次 clone 一个带 `.claude/settings.json` 的仓库**：Claude Code 提示你信任目录，同意后 project 的 allow 规则才生效。

## 五、Managed Settings（企业）

**三种交付方式**（都不可被低 scope 覆盖）：

1. **服务端**：claude.ai admin console 推送
2. **MDM/OS 策略**：
   - macOS：`com.anthropic.claudecode` managed preferences
   - Windows：`HKLM\SOFTWARE\Policies\ClaudeCode` 注册表
3. **文件**：`/etc/claude-code/managed-settings.json`（Linux/WSL）

**Managed 专属字段**（部分）：

| 字段 | 作用 |
| --- | --- |
| `allowManagedPermissionRulesOnly` | 只认 managed 权限规则 |
| `allowManagedMcpServersOnly` | 只认 admin 定义的 MCP 白名单 |
| `allowManagedHooksOnly` | 只认 managed hooks + force-enabled plugin hooks |
| `availableModels` | 限制可选模型 |
| `forceLoginMethod` | 限制登录方式 |
| `strictKnownMarketplaces` | 锁 marketplace 白名单 |
| `disableSideloadFlags` | 拒绝 `--plugin-dir` / `--agents` 等 CLI flag |

**容错解析**：managed settings 解析**宽容**——单条写错只剔那条，不影响整体策略。`claude doctor` 看被剔的条目。

## 六、完整示例

`.claude/settings.json`（项目级，提交 git）：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(pnpm run lint)",
      "Bash(pnpm run test *)",
      "Bash(pnpm build)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "pnpm run format" }]
      }
    ]
  }
}
```

## 常见坑

**把个人偏好写进 project settings**——主题、编辑器模式这种个人偏好应该放 `~/.claude/settings.json`，别强加给团队。

**改了 `model` 字段没生效**——`model` 只在 session 启动时读。改 settings 后用 `/model` 切换或重启。

**项目 allow 规则不生效**——没信任工作目录。首次 clone 带 `.claude/settings.json` 的仓库要同意 trust 对话框。

**managed settings 写错一条全失效？**——不会。managed 解析宽容，单条错只剔那条。`claude doctor` 看详情。

**`fallbackModel` 想合并多 scope**——不行。最高优先级文件提供整条链，不合并。

## 参考

- [Anthropic · Settings reference](https://code.claude.com/docs/en/settings)（访问于 2026-08-04）
- [Anthropic · Managed settings](https://code.claude.com/docs/en/server-managed-settings)（访问于 2026-08-04）
- [MDM 部署模板](https://github.com/anthropics/claude-code/tree/main/examples/mdm)（访问于 2026-08-04）

## 下一步

- 键位定制 → [键位配置](./keybindings) 🚧
- Hooks 完整触发表 → [Hooks](./hooks)
- MCP 配置 → [.mcp.json 项目配置](../mcp/mcp-json-config)

## 如果你想

- 看权限规则完整语法 → [权限系统](../basics/permissions)
- 理解 plugin 启用机制 → [Plugins 与 Marketplace](../skills/plugins-marketplace)
- 企业部署 Claude Code → [Anthropic · Managed settings](https://code.claude.com/docs/en/server-managed-settings)

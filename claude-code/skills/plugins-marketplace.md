---
title: Plugins 与 Marketplace
description: 把 skill / hook / agent / MCP 打包成 plugin，通过 marketplace 分发给团队——三层关系、最小 plugin.json 与 marketplace.json、Anthropic 官方两个市场、团队级 extraKnownMarketplaces
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-30
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  pluginsDocs: 'https://code.claude.com/docs/en/plugins'
  marketplaceDocs: 'https://code.claude.com/docs/en/plugin-marketplaces'
  discoverDocs: 'https://code.claude.com/docs/en/discover-plugins'
  accessedAt: 2026-07-30
---

# Plugins 与 Marketplace

> **TL;DR**：Skill 是能力单元 → Plugin 是能力包（含 skills / agents / hooks / MCP / LSP）→ Marketplace 是 plugin 目录。个人用 `.claude/skills/` 就够；要**分发给团队 / 社区 / 多项目复用**才升级到 plugin。Anthropic 有官方 marketplace `claude-plugins-official`（首次启动 Claude Code 自动装）+ 社区 `claude-community`（手动 `/plugin marketplace add`）。

⏱ 预计阅读时间：10 分钟

## 你能在这里学到

- Skill / Plugin / Marketplace 三层关系一图看清
- 什么时候升级到 plugin（而不是继续用 `.claude/skills/`）
- 最小 `plugin.json` + 目录结构 + `--plugin-dir` 本地测试
- `marketplace.json` 分发格式与 5 种 plugin source
- `/plugin` 三大命令族：`marketplace` / `install` / `enable-disable`
- 团队级 `extraKnownMarketplaces` 设置——让 clone 项目的人自动看到 marketplace
- Anthropic 官方两个市场（`claude-plugins-official` / `claude-community`）区别

## 前置

- 会写一个基础 skill —— [写你的第一个 Skill](./custom-skill)
- 读过 [内置 Skills 一览](./built-in-skills) 知道 bundled skill 的分发形态
- Claude Code v2.1.220（`/plugin` 命令 v2.1.100+ 起）

## 一、三层关系

| 层 | 是什么 | 例 | 触发名 |
| --- | --- | --- | --- |
| **Skill** | 一个能力单元（一个 SKILL.md） | `/pr-desc` | `/skill-name` |
| **Plugin** | 一组能力打包（多 skills + hooks + MCP + agents） | `commit-commands` / `github` | 装完 `/plugin-name:skill-name` |
| **Marketplace** | 多 plugin 的 catalog | `claude-plugins-official` | `plugin-name@marketplace-name` |

Plugin 里的 skill **强制加命名空间**（`/my-plugin:hello`）——防止装多个 plugin 时同名 skill 冲突。**单文件例外**：plugin 根目录直接放 `SKILL.md` 会被识别为唯一 skill，用 frontmatter `name` 作触发名。

## 二、什么时候升级到 Plugin

按 Anthropic 官方指引：

| 选 | 场景 |
| --- | --- |
| **`.claude/skills/`** | 个人偏好、单项目定制、还在实验阶段、想要短名 `/hello` |
| **Plugin** | 分享给团队、跨项目复用、要版本管理、通过 marketplace 分发、能接受 `/my-plugin:hello` |

**先 skill 再 plugin**——Anthropic 建议先用 `.claude/skills/` 快速迭代验证，要分发时再打包成 plugin。

## 三、写一个最小 Plugin

**目录结构**（plugin 名 `hello-team`）：

```text
hello-team/
├── .claude-plugin/
│   └── plugin.json          # 必需：plugin 身份
├── skills/                  # 可选：多 skill 放这里
│   └── hello/SKILL.md
├── agents/                  # 可选：subagent 定义
├── hooks/hooks.json         # 可选：hook 配置
├── .mcp.json                # 可选：MCP servers
├── .lsp.json                # 可选：LSP servers（代码智能）
├── monitors/monitors.json   # 可选：后台监控
├── settings.json            # 可选：默认设置（agent / subagentStatusLine）
├── bin/                     # 可选：加进 PATH 的可执行文件
└── README.md                # 强烈建议
```

**`.claude-plugin/plugin.json` 必需**：

```json
{
  "name": "hello-team",
  "description": "团队专用问候流水线",
  "version": "1.0.0",
  "author": { "name": "SZ-FE Team" }
}
```

**⚠️ 高频坑**：`commands/` / `skills/` / `agents/` / `hooks/` 一律在 **plugin 根目录**，别塞进 `.claude-plugin/`——那个目录只放 `plugin.json`。

**本地测试**（不需 install）：

```bash
claude --plugin-dir ./hello-team
```

想同时载多个 plugin：`--plugin-dir` 重复用。改完 `SKILL.md` 后敲 `/reload-plugins` 热更新。

## 四、Marketplace：打包分发

Plugin 单机跑通后，要让别人一键装就建 marketplace。

**目录结构**（marketplace 根）：

```text
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json     # 必需：目录 catalog
└── plugins/
    └── hello-team/          # 见上节 plugin 结构
```

**`.claude-plugin/marketplace.json` 必需**：

```json
{
  "name": "sz-fe-plugins",
  "owner": { "name": "SZ-FE Team", "email": "sz-fe@example.com" },
  "plugins": [
    {
      "name": "hello-team",
      "source": "./plugins/hello-team",
      "description": "团队专用问候流水线"
    }
  ]
}
```

**Plugin source 五种**（每个 plugin 的 `source` 字段）：

| 类型 | 写法 | 场景 |
| --- | --- | --- |
| 相对路径 | `"./plugins/x"` | plugin 与 marketplace 同仓库 |
| GitHub | `{ "source": "github", "repo": "owner/repo" }` | plugin 分开仓库 |
| Git URL | `{ "source": "url", "url": "https://gitlab.com/..." }` | GitLab / 自建 Git |
| Git 子目录 | `{ "source": "git-subdir", "url": "...", "path": "..." }` | monorepo，稀疏 clone |
| npm | `{ "source": "npm", "package": "@my/plugin" }` | 走 npm registry |

**发布**：marketplace 仓库 push 到 GitHub / GitLab 即可。用户敲 `/plugin marketplace add owner/repo` 就能加。

## 五、安装与管理（用户视角）

**三大命令族**：

```text
/plugin marketplace add|remove|list|update <src>          # 管市场
/plugin install|uninstall|enable|disable <name>@<market>  # 管 plugin
/reload-plugins                                            # 热更新，改完后必敲
```

**三种 scope**：

| scope | 存在哪 | 谁能看到 |
| --- | --- | --- |
| **user** | `~/.claude/settings.json` | 你所有项目 |
| **project** | `.claude/settings.json`（跟仓库） | 所有 collaborator |
| **local** | `.claude/settings.local.json` | 只你、只这个项目 |

**装完必须 `/reload-plugins`** 才在本次 session 生效——否则等下次启动才装上。

## 六、Anthropic 官方两个 Marketplace

**`claude-plugins-official`**——首次启动 Claude Code **自动注册**：

```text
/plugin install github@claude-plugins-official
```

包含几大类：**代码智能 LSP**（`typescript-lsp`、`pyright-lsp`、`gopls-lsp` 等）/ **外部集成 MCP**（`github`、`atlassian`、`figma`、`vercel`、`sentry` 等）/ **安全审查**（`security-guidance`）/ **开发流**（`commit-commands`、`pr-review-toolkit`、`plugin-dev`、`agent-sdk-dev`）/ **输出风格**（`explanatory-output-style`、`learning-output-style`）。

**`claude-community`**——三方投稿、Anthropic 自动化审查通过、pin 到具体 commit SHA；**手动加**：

```text
/plugin marketplace add anthropics/claude-plugins-community
/plugin install <name>@claude-community
```

**别自己起名叫 `claude-plugins-official` / `claude-community` 等**——Anthropic 保留了一批 marketplace 名，占用会被 v2.1.205+ 拒加载。

## 七、企业与团队分发

**让 clone 仓库的人自动看到 marketplace**——项目 `.claude/settings.json` 加：

```json
{
  "extraKnownMarketplaces": {
    "sz-fe-plugins": {
      "source": {
        "source": "github",
        "repo": "sz-fe/claude-plugins"
      }
    }
  }
}
```

用户信任了工作目录后，Claude Code 会**提示他们装 plugin**。企业管理员在 managed settings 里能 force-enable / force-disable、锁 marketplace 白名单（`strictKnownMarketplaces`）。

## 常见坑

**目录结构乱塞**——把 `commands/` / `skills/` / `hooks/` 塞进 `.claude-plugin/`，Claude Code 不认。规则：**只有 `plugin.json` 在 `.claude-plugin/` 里，其它都在 plugin 根**。

**忘了 `/reload-plugins`**——`/plugin install` 之后不敲，本次 session 看不到新 skill。

**version 字段的语义**——`plugin.json` 里写了 `"version"`，用户只在你 bump 版本号时才收更新；**不写**则每次 commit SHA 都算新版本（git 兜底）。团队协作建议显式写版本。

**Plugin skill 与本地 skill 同名**——本地 `.claude/skills/` 优先级最高，plugin 里的**同名 agent** 会被覆盖；skill 因为强制 namespace `/plugin:name` 不冲突。

**`--plugin-dir` 加载 zip 需 v2.1.128+**——早期版本只支持目录形式。

## 参考

- [Anthropic · Create plugins](https://code.claude.com/docs/en/plugins)（访问于 2026-07-30）
- [Anthropic · Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)（访问于 2026-07-30）
- [Anthropic · Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)（访问于 2026-07-30）
- [Anthropic · Plugins reference](https://code.claude.com/docs/en/plugins-reference)（访问于 2026-07-30）—— 完整字段清单

## 下一步

- 拿你写好的 skill 打包成 plugin → 复习 [写你的第一个 Skill](./custom-skill)
- 想深入 subagent → [什么是 Subagent](../subagents-and-workflows/what-is-a-subagent) 🚧
- 想深入 MCP 使用层 → [什么是 MCP](../mcp/what-is-mcp) 🚧

## 如果你想

- 浏览官方 marketplace 已有 plugin → 敲 `/plugin` 进 Discover tab，或到 [claude.com/plugins](https://claude.com/plugins)
- 从 `.claude/skills/` 迁移到 plugin → [Anthropic · Convert existing configurations to plugins](https://code.claude.com/docs/en/plugins#convert-existing-configurations-to-plugins)
- 看 Hook 完整触发表 → [Hooks](../customization/hooks) 🚧

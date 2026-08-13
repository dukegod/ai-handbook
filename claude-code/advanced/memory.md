---
title: 全局记忆
description: 'Auto Memory 深度机制、.claude/rules/ 路径级规则组织、企业级 Managed CLAUDE.md 部署——CLAUDE.md 项目记忆之外的进阶记忆能力'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  memoryDocs: 'https://code.claude.com/docs/en/memory'
  accessedAt: 2026-08-04
---

# 全局记忆

> **TL;DR**：本页是 [CLAUDE.md 项目记忆](../basics/claude-md) 的进阶篇，聚焦三块没展开的能力：**Auto Memory 内部机制**（存储结构、加载限额、subagent 独立记忆）、**`.claude/rules/`** 路径级规则组织（比单一 CLAUDE.md 更细粒度）、**企业级全局部署**（Managed CLAUDE.md + `claudeMdExcludes`）。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- Auto Memory 的存储结构、加载限额与 subagent 独立记忆
- `.claude/rules/`：按文件路径精确加载规则，比 CLAUDE.md 更省 context
- 用户级 `~/.claude/rules/`——真正跨项目生效的"全局"规则
- 企业级 Managed CLAUDE.md 的部署方式与 `claudeMdExcludes`

## 前置

- 已读 [CLAUDE.md 项目记忆](../basics/claude-md)——默认你已理解四级继承、`/init`、`/memory`
- 已读 [Agent 类型清单 · Frontmatter 字段全表](../subagents-and-workflows/agent-types#四、frontmatter-字段全表)——理解 subagent 的 `memory` 字段

## 一、Auto Memory 内部机制

Auto Memory 是 Claude **自己写**的笔记——build 命令、debug 心得、代码风格偏好，不用你手动维护。

**存储结构**：

```text
~/.claude/projects/<project>/memory/
├── MEMORY.md           # 索引，每次会话开头加载
├── debugging.md        # 详细笔记，按需加载
├── api-conventions.md
└── ...
```

`<project>` 由 git 仓库推导——**同一仓库的所有 worktree 共享一份** auto memory；非 git 目录按项目根路径区分。想换位置，设 `autoMemoryDirectory`（写进项目 `.claude/settings.json` 需先过 workspace trust 才生效）。

**加载限额**：只有 `MEMORY.md` 的**前 200 行或 25KB**（先到者为准）在会话开头加载，YAML frontmatter 与 HTML 注释不计入。超限时那次写入仍成功，但 Claude Code 会提示 Claude 精简（拆到 topic 文件、合并或删旧条目）；持续超限则每次加载都会丢失尾部内容。Topic 文件（如 `debugging.md`）**不在启动时加载**，Claude 需要时按常规文件读取。

**时间戳**：Claude 写入带 frontmatter 的记忆文件时，Claude Code 自动记录 `modified`（ISO 8601，v2.1.214+），标注这条记忆的新鲜度。

**开关**：`/memory` 里切换，或 `settings.json` 设 `autoMemoryEnabled: false`，或环境变量 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`。

**Subagent 有自己的记忆**：主会话的 auto memory **不会**传给普通 subagent（`fork` 除外——它继承父会话全部上下文）。给 subagent frontmatter 设 `memory: project`（或 `user` / `local`）才会开启它自己的独立记忆目录。

**注意**：Auto Memory 是 machine-local——不跨机器、不跨云环境同步。

## 二、`.claude/rules/`：路径级规则组织

CLAUDE.md 建议 < 200 行，但项目规则往往按模块、语言、目录各不相同——**全塞一个文件既臃肿又浪费 context**（Claude 改 CSS 时不需要加载后端规范）。

**目录结构**（`.md` 递归发现，可分子目录）：

```text
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md
    ├── testing.md
    └── frontend/
        └── react.md
```

**不带 `paths` 字段**：和 `.claude/CLAUDE.md` 同优先级，每次会话都加载。

**带 `paths` 字段**：只在 Claude 读到匹配文件时才加载——省 context：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则
- 所有 endpoint 必须做输入校验
- 用标准错误响应格式
```

| glob 模式 | 匹配 |
| --- | --- |
| `**/*.ts` | 任意目录下所有 `.ts` |
| `src/**/*` | `src/` 下所有文件 |
| `src/**/*.{ts,tsx}` | 花括号展开，同时匹配两种后缀 |

花括号展开有预算上限（单条规则 1000 个展开模式 / 4 MiB），超预算的模式按字面量处理、不会匹配到任何文件——避免嵌套过多花括号组。

**真正的"全局"——用户级规则**：`~/.claude/rules/` 对你机器上**所有项目**生效，适合放个人偏好（项目规范仍应放项目里）：

```text
~/.claude/rules/
├── preferences.md
└── workflows.md
```

用户级规则比项目规则**先加载**，即项目规则优先级更高、可覆盖冲突项。

**跨项目共享**：`.claude/rules/` 支持 symlink，可以把一套规则链接进多个仓库：

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
```

## 三、企业级全局部署

组织级 CLAUDE.md 部署在 Managed policy 路径（见 [CLAUDE.md 项目记忆 · 四级继承](../basics/claude-md#二、四级继承-从广到窄) 的路径表），**任何用户设置都无法排除它**——通过 MDM / Ansible 等配置管理系统分发到所有开发机。

**不想单独分发文件？**`claudeMd` 键直接写进 `managed-settings.json`：

```json
{
  "claudeMd": "Always run `make lint` before committing.\nNever push directly to main."
}
```

**Managed CLAUDE.md 还是 Managed settings？**

| 需求 | 配置在 |
| --- | --- |
| 禁用特定工具 / 命令 / 路径 | Managed settings：`permissions.deny` |
| 强制 sandbox 隔离 | Managed settings：`sandbox.enabled` |
| 认证方式与组织锁定 | Managed settings：`forceLoginMethod` |
| 代码风格与行为指引 | Managed **CLAUDE.md** |

区别的本质：**settings 是客户端强制执行的规则，不管 Claude 怎么决定都生效；CLAUDE.md 只是塑造 Claude 的行为，不是硬约束。**

**大 monorepo 排除不相关的祖先 CLAUDE.md**：`claudeMdExcludes` 按路径 / glob 跳过（Managed policy 文件除外，那个跳不掉）：

```json
// .claude/settings.local.json
{
  "claudeMdExcludes": ["**/other-team/CLAUDE.md"]
}
```

## 常见坑

**不确定哪些指令文件实际加载了**——`/context` 看 **Memory files** 段，比猜测可靠。

**调试 rules 为什么没触发**——用 `InstructionsLoaded` hook 记录哪些文件何时因何加载，见 [Hooks](../customization/hooks)。

**项目规则和用户规则冲突**——项目规则后加载、优先级更高；两边都写了同一条建议就删掉用户级那份。

**Subagent"忘光"了主会话攒的经验**——这是设计如此，不是 bug。主会话 auto memory 默认不传给普通 subagent；要持久记忆，给 subagent 单独设 `memory` 字段。

**`MEMORY.md` 越写越大，Claude 一直被提醒精简**——把详细笔记移到 topic 文件，`MEMORY.md` 只留一行索引。

## 参考

- [Anthropic · How Claude remembers your project](https://code.claude.com/docs/en/memory)（访问于 2026-08-04）
- [Anthropic · Sub-agents · Enable persistent memory](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory)（访问于 2026-08-04）
- [Anthropic · Settings](https://code.claude.com/docs/en/settings)（访问于 2026-08-04）

## 下一步

- 回到 CLAUDE.md 基础 → [CLAUDE.md 项目记忆](../basics/claude-md)
- Git 与 PR 工作流 → [Git 与 PR 工作流](./git-workflow)
- 回到章导读，看到全貌 → [Claude Code 章导读](../)

## 如果你想

- 用硬约束替代"建议性"记忆 → [Hooks](../customization/hooks)
- 给 subagent 配置独立记忆 → [Agent 类型清单](../subagents-and-workflows/agent-types)
- 查所有 settings 字段 → [Settings 配置文件](../customization/settings)

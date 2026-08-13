---
title: 内置 Skills 一览
description: Claude Code 装好就有的 12 个 bundled skills——按日常运维 / 代码工作流 / 领域特化分类，含调用方式、版本门槛与开关方法
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-29
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  skillsDocs: 'https://code.claude.com/docs/en/skills#bundled-skills'
  commandsDocs: 'https://code.claude.com/docs/en/commands'
  accessedAt: 2026-07-29
---

# 内置 Skills 一览

> **TL;DR**：Claude Code 装好就有 **12 个 bundled skill**（`/doctor` / `/code-review` / `/verify` / `/loop` / `/batch` / …）——都能像自定义 skill 一样敲 `/name` 使用。可用 `disableBundledSkills` 整体关闭（只有 `/doctor` 顽固地留下），也可用同名 personal / project skill **完全覆盖**默认行为。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- **bundled skill** 与 **built-in command** 的本质差异（能否覆盖、能否关闭）
- 12 个 bundled skill 各自定位、调用方式、版本门槛
- 三类分组：日常运维（4）/ 代码工作流（5）/ 领域特化（3）
- 三种关闭 / 覆盖姿势：整体关、单个关、同名替换

## 前置

- 装好 Claude Code v2.1.220（部分 skill 有更严的版本要求，下文标注）
- 读过 [Skill vs Command vs Agent](./skills-vs-commands-vs-agents) — 分清 bundled skill 与 built-in command

## 一、bundled skill vs built-in command

- **built-in command**（`/help` / `/model` / `/config` / `/permissions` / `/context` / `/cd` / `/compact` …）——由 Claude Code 二进制**直接实现**、不是 markdown 模板，**不能覆盖也不能关闭**
- **bundled skill**（本页主角）——随二进制打包但**走标准 skill 机制**：可用 `disableBundledSkills` 关闭、可用同名 skill **完全覆盖**、可用 `skillOverrides` 单独设 `"off"` / `"name-only"`

**同名覆盖**：只要 `.claude/skills/code-review/SKILL.md` 存在，敲 `/code-review` 走的就是你的版本，bundled 那份被完全替换。这是二次开发 bundled 行为的主推入口。

## 二、日常运维（4 个）

**`/doctor`**（alias `/checkup`）—— 装好第一件事该敲

- **做什么**：安装诊断——检查配置、精简 CLAUDE.md、去重、看更新
- **特殊**：**唯一无法通过 `disableBundledSkills` 关掉**的 bundled skill（v2.1.205+ 起）。要隐藏必须 `DISABLE_DOCTOR_COMMAND=1` 环境变量，或 `skillOverrides: { doctor: "off" }`
- **场景**：报错找不到问题时、季度环境体检

**`/debug`** —— 打开 debug 日志诊断

- **做什么**：开启 debug logging、透过 session logs 排查
- **场景**：某个操作失败但错误信息模糊时

**`/loop`**（alias `/proactive`）—— 定时 / 自节奏循环

- **做什么**：把一段 prompt 按周期反复跑
- **参数**：`/loop [interval] [prompt]` —— 例 `/loop 5m 检查部署是否完成`
- **场景**：等 CI、等外部依赖、周期性检查

**`/fewer-permission-prompts`** —— 减少权限询问

- **做什么**：扫过往 transcript，把你反复批准的工具追加到 `.claude/settings.json` allowlist
- **场景**：一段时间后感觉总在批准同类操作

## 三、代码工作流（5 个）

**`/code-review`** —— review 当前 diff

- **做什么**：审视当前 diff、找 bug 与清理机会；支持 cloud multi-agent review
- **参数**：`/code-review [low|medium|high|xhigh|max|ultra] [--fix] [--comment] [target]`
- **v2.1.215+**：**仅手动触发**（Claude 不再自动调，避免 token 失控）
- **场景**：commit / PR 之前

**`/verify`** —— build 并运行 app 验证改动

- **做什么**：真正 build & run 验证改动，不退化到测试或类型检查
- **v2.1.215+**：**仅手动触发**
- **v2.1.200+**：会把学到的 build recipe 写到 `.claude/skills/verify/SKILL.md`，之后跟随；仓库根部这份会**替换**掉 bundled 版本
- **场景**：想确认 UI 改动不只是编译通过

**`/run`** —— 启动 app 看改动效果

- **做什么**：从项目类型（CLI / server / TUI / browser）+ README / `package.json` / `Makefile` 推断启动方式
- **v2.1.145+**
- **场景**：从 clean 环境把 app 跑起来看

**`/run-skill-generator`** —— 教 `/run` 与 `/verify` 怎么跑你的项目

- **做什么**：一次性录制 build / launch recipe，产出 `.claude/skills/run-<name>/`。之后 `/run` / `/verify` 都跟这份走
- **v2.1.145+**
- **场景**：项目需要 DB、env file、多步 build、GUI session 等非标准启动

**`/batch`** —— 大规模改动分解到 worktree

- **做什么**：把大改动拆成 5–30 个独立单元，每个单元开背景 subagent 在独立 git worktree 跑
- **参数**：`/batch <instruction>` —— 例 `/batch 把 src/ 从 Solid 迁到 React`
- **场景**：全量重命名、跨文件迁移、大量重构

## 四、领域特化（3 个）

**`/dataviz`** —— 图表与仪表盘设计指引

- **做什么**：色盲友好调色板校验、chart / dashboard 设计规则
- **v2.1.198+**
- **场景**：写 dashboard 需要选颜色 / 布局

**`/design-sync`** —— 同步 React design system 到 claude.ai/design

- **做什么**：把仓库里的 React design system 转成 claude.ai/design 项目
- **不可用环境**：Bedrock / GCP Vertex / Foundry / AWS
- **场景**：想让 Claude UI 里能看你的 design system

**`/claude-api`** —— Claude API 参考 + 模型迁移

- **做什么**：加载 Claude API 参考、可代码迁移到新模型 / 引导 Managed Agents 上手
- **参数**：`/claude-api [migrate|managed-agents-onboard]`
- **场景**：把老代码从 Claude 3.7 迁到 Claude 5、开始用 Managed Agents

## 五、关闭 / 覆盖

**整体关**（保留 `/doctor`）—— `~/.claude/settings.json`：

```json
{
  "disableBundledSkills": true
}
```

**单个关**：

```json
{
  "skillOverrides": {
    "code-review": "off"
  }
}
```

`skillOverrides` 三档：`"off"`（完全关）/ `"name-only"`（保留 `/name` 补全但不常驻 description）/ `"full"`（默认）。

**同名覆盖**（写你自己的版本替换 bundled 行为）：

```bash
mkdir -p .claude/skills/code-review
# 写 .claude/skills/code-review/SKILL.md ——敲 /code-review 走你这份
```

**隐藏 `/doctor`**：

```bash
export DISABLE_DOCTOR_COMMAND=1
```

## 六、常见坑

**忘了 `/verify` / `/code-review` v2.1.215+ 只能手动触发**——想让 Claude 自动跑，写你自己的同名 skill 替换 bundled 那份（自定义 skill 默认双向触发）。

**`/run` 推断错误**——用 `/run-skill-generator` 录一次真实 recipe。之后所有 agent 都跟着走，不再每次重新猜。

**Cowork / cloud session 里 bundled skill 不齐**——Cowork 与 cloud session **从 claude.ai 拉 skill**，不读 `~/.claude/skills/`。把 skill 提交到仓库 `.claude/skills/` 或在 claude.ai 账号里 enable。

**`/batch` 跑到一半失败**——每个单元跑在独立 worktree，可单独 replay 或丢弃；错误定位到单元而不是全量 rollback。

## 参考

- [Anthropic · Bundled skills](https://code.claude.com/docs/en/skills#bundled-skills)（访问于 2026-07-29）
- [Anthropic · Commands reference](https://code.claude.com/docs/en/commands)（访问于 2026-07-29）—— bundled skill 与 built-in command 全表
- [Anthropic · Skill overrides](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings)（访问于 2026-07-29）
- [Anthropic · Run and verify your app](https://code.claude.com/docs/en/skills#run-and-verify-your-app)（访问于 2026-07-29）

## 下一步

- 拿这些原生 skill 做参考写自己的 → [写你的第一个 Skill](./custom-skill) 🚧
- 把 skill 打包分发给团队 → [Plugins 与 Marketplace](./plugins-marketplace) 🚧

## 如果你想

- 从头看 skill 是什么 → [什么是 Skill](./what-is-a-skill)
- 完整 frontmatter 字段查表 → [SKILL.md 规范](./skill-md-spec)
- 看 built-in command 全表（不是 skill）→ [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)

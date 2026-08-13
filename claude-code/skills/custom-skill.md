---
title: 写你的第一个 Skill
description: 十分钟做一个 /pr-desc skill——从空目录到 SKILL.md 到本地验证到迭代，用 pr-desc 案例走通所有关键机制
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-29
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  quickstartDocs: 'https://code.claude.com/docs/en/skills#create-your-first-skill'
  bestPracticesDocs: 'https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices'
  accessedAt: 2026-07-29
---

# 写你的第一个 Skill

> **目标**：本篇结束后，你会有一个可用的 `/pr-desc` skill——从当前分支相对 `main` 的 diff 自动生成一段规整的 PR 描述。全程约 10 分钟。之后随手改成你自己的场景（commit message / release notes / migration checklist …）。

## 你将做到

- ✅ 3 分钟写出一个能敲的 `/pr-desc`
- ✅ 加参数、加权限、加动态 `git diff` 注入
- ✅ 用 should-trigger 提问验证 description 命中率
- ✅ 想清楚什么时候拆支持文件

## 前置检查清单

- [ ] Claude Code v2.1.220（`claude --version`）
- [ ] 一个 git 项目、有未提交或近期提交的改动可测
- [ ] 读过 [SKILL.md 规范](./skill-md-spec) 与 [写好触发描述](./writing-triggers)
- [ ] 会开新会话（`claude -p '<提问>' --verbose`）测触发

## 第 1 步：决定位置

三选一：

| 位置 | 谁能用 | 场景 |
| --- | --- | --- |
| `~/.claude/skills/pr-desc/` | 你所有项目 | 通用偏好、和团队规范无关 |
| `.claude/skills/pr-desc/`（项目内） | 只这个项目、能 commit | 团队约定的 PR 模板 |
| plugin `skills/` 目录 | 装了插件的地方 | 分发到多个团队 → 见 [Plugins 与 Marketplace](./plugins-marketplace) 🚧 |

本文用**项目级**（最贴近团队场景）。

```bash
mkdir -p .claude/skills/pr-desc
```

## 第 2 步：写最小可跑版本

新建 `.claude/skills/pr-desc/SKILL.md`：

````md
---
description: 从当前分支相对 main 的 diff 生成一段 PR 描述（Summary / Changes / Testing 三段）。用户说"写 PR 描述"、"生成 PR body"、"give me a PR message" 时用。
argument-hint: '[ticket-id]'
---

## 当前 diff

!`git --no-pager diff main...HEAD`

## 任务

阅读上方 diff，输出严格三段：

**Summary**
一句话概括本 PR 做了什么、为什么。

**Changes**
按文件 / 模块列 bullet 说关键改动。

**Testing**
如何验证——手动步骤 + 跑什么测试。

若参数 `$ARGUMENTS` 非空，把 `Ticket: $ARGUMENTS` 放在 Summary 顶部一行。
````

**关键点**：

- `` !`git --no-pager diff main...HEAD` `` 是**动态注入**（详见 [SKILL.md 规范 · 动态注入](./skill-md-spec#五、动态注入-cmd)），在 skill 内容送到 Claude 之前先跑
- `main...HEAD`（三个点）是「从 main 分叉后的所有变化」，与 `main` / `main..HEAD`（两个点）语义不同——PR 描述真正想要的是三个点
- `--no-pager` 防 git 默认 pager 卡住
- `$ARGUMENTS` 是全部参数字符串；如需多个位置参数用 `$0` / `$1` 或 frontmatter 声明 `arguments: [ticket branch]`

## 第 3 步：跑一次

到 Claude Code 里敲：

```text
/pr-desc
```

**预期**：Claude 加载 skill、跑一次 `git diff main...HEAD`、输出一段三段式描述。

带 ticket ID：

```text
/pr-desc PROJ-1234
```

**预期**：Summary 第一行 `Ticket: PROJ-1234`。

## 第 4 步：加免询问权限

默认每次 `git diff` 都要批。改 frontmatter 加：

```yaml
allowed-tools: 'Bash(git diff:*) Read'
```

**注意**：`allowed-tools` 只对**触发这个 skill 的那一轮**放行。下次用户发消息立即失效——想永久放行走 [`/permissions`](../basics/permissions) 或 `.claude/settings.local.json` 的 `permissions.allow`。

## 第 5 步：验证命中率

按 [写好触发描述](./writing-triggers#六验证should-trigger--should-not-trigger) 的建议，在 skill 目录里放一份 `TRIGGERS.md`：

```markdown
## should-trigger（必须触发）
- 帮我写这次 PR 的描述
- 生成 PR body
- give me a PR message
- 写一下 PR 的说明

## should-not-trigger（不该触发）
- 写 commit message（是另一个 skill）
- review 这个 diff
- 分析我改了啥
```

跑测试：

```bash
claude -p '帮我写这次 PR 的描述' --verbose
```

`--verbose` 里搜 `pr-desc`——命中就有一条 skill 加载日志。命中率 < 80% 回去改 description：加同义触发短语、或收窄 `when_to_use` 独立字段。

**验证点**：

- 全部 should-trigger 命中
- 全部 should-not-trigger 不加载
- 传 ticket ID 时 Summary 顶部有 `Ticket: XXX`

## 第 6 步：什么时候拆支持文件

**最小版本一直够用**——直到 SKILL.md 超过 500 行、或需要复用外部模板。拆的信号：

| 症状 | 拆到 | 引用方式 |
| --- | --- | --- |
| body 里挂长模板 | `template.md` | SKILL.md 里加：「参考同目录 `template.md` 的格式」 |
| 有脚本 | `scripts/x.sh` | `` !`${CLAUDE_SKILL_DIR}/scripts/x.sh` `` |
| 有长参考知识 | `reference.md` | 「如需详情读 `reference.md`」 |

**只放一级引用**——Anthropic 官方强调，不要 SKILL.md → `template.md` → `details.md` → ……多层链。Claude 遇到深层引用会用 `head -100` 预览，容易漏信息。

成型的 skill 目录：

```text
.claude/skills/pr-desc/
├── SKILL.md
├── template.md       # PR 模板正文
├── examples/
│   └── good.md       # 一个高质量 PR 参考
└── scripts/
    └── extract-ticket.sh
```

## 第 7 步：迭代节奏

Anthropic 官方推荐的迭代模式：**用 Claude A 帮改 description，用 Claude B 在真实任务里测**（[best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#develop-skills-iteratively-with-claude)）。

1. 当前会话（Claude A）里让它帮生成 / 修 skill
2. 开新会话（Claude B）随手扔真实场景
3. 观察 Claude B 是否命中触发、是否按你想的顺序读文件、是否漏读某段
4. 命中问题带回 Claude A：「刚才我说『帮我写 PR 描述』它没触发，加同义词」
5. 反复到命中率稳定 ≥ 80%

## 常见错误

**`git diff` 卡住**

原因：`git diff` 有 pager，`!` 里跑时 hang 到超时。

修复：用 `git --no-pager diff` 或先 `export PAGER=cat`。

**description 命中窄**

原因：只写"生成 PR 描述"，用户说"给我写个 PR body" 不触发。

修复：description 里堆 3–5 种真实说法（中英混）；仍不够就用 `when_to_use` 独立字段扩容。

**`git diff main` vs `git diff main...HEAD`**

原因：两个点 vs 三个点语义不同——两个点是「main 到 HEAD 的直接 diff」（含 main 后来的合并），三个点是「HEAD 相对分叉点的独立改动」。PR 描述通常要三个点。

修复：`main...HEAD` 不是 `main..HEAD`。

**skill body 里写「接下来做 X」**

原因：Skill body 加载后**驻留整段会话**（详见 [什么是 Skill · 生命周期](./what-is-a-skill#生命周期与-auto-compaction)），一次性步骤会在后续无意义地再跑。

修复：改「始终 X」的 standing instruction 语气。

**把 template.md 完整贴到 SKILL.md**

原因：SKILL.md body 加载后每轮都占 token。

修复：拆到独立文件，SKILL.md 里只写一句「参考 `template.md`」。

## 参考

- [Anthropic · Create your first skill (quickstart)](https://code.claude.com/docs/en/skills#create-your-first-skill)（访问于 2026-07-29）
- [Anthropic · Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（访问于 2026-07-29）
- [SKILL.md 规范](./skill-md-spec) — 完整 frontmatter 字段与语法
- [写好触发描述](./writing-triggers) — description 字符预算与验证详解

## 下一步

- 把 skill 打包分发给团队 → [Plugins 与 Marketplace](./plugins-marketplace) 🚧
- 让 skill 跑在独立 subagent 里 → [什么是 Subagent](../subagents-and-workflows/what-is-a-subagent) 🚧
- 精细控制 skill 能碰哪些工具 → [权限系统](../basics/permissions)

## 如果你想

- 看别人写的 skill 参考 → [内置 Skills 一览](./built-in-skills)
- 覆盖 bundled 行为 → [内置 Skills · 关闭 / 覆盖](./built-in-skills#五、关闭--覆盖)
- 深入 `!` bash 语法与限制 → [SKILL.md 规范 · 动态注入](./skill-md-spec#五、动态注入-cmd)

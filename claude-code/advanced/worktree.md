---
title: Worktree 隔离
description: 'Claude Code 用 git worktree 隔离并行 session——--worktree 启动、baseRef 选 fresh/head、subagent isolation、.worktreeinclude 携带 gitignore 文件、清理规则'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  worktreesDocs: 'https://code.claude.com/docs/en/worktrees'
  accessedAt: 2026-08-04
---

# Worktree 隔离

> **TL;DR**：`claude --worktree <name>` 在 `.claude/worktrees/<name>/` 开一个独立 git worktree——自己的文件 + 自己的分支，共享仓库历史。两个 session 并行改代码互不踩。subagent 加 `isolation: worktree` 也能各自隔离。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- Worktree 解决什么（并行 session 文件冲突）
- `--worktree` 启动与清理流程
- `worktree.baseRef`：`fresh` vs `head` 选型
- subagent `isolation: worktree`
- `.worktreeinclude` 携带 gitignore 文件
- worktree 与主 checkout 共享什么

## 前置

- 读过 [Subagent](../subagents-and-workflows/what-is-a-subagent) —— 理解 isolation 字段
- 会基本 git 操作

## 一、Worktree 解决什么

普通方式跑两个 Claude Code session 改同一仓库——**文件互相踩**：A session 改了 `auth.ts`，B session 也改，冲突。

**Worktree 隔离**：每个 session 在独立工作目录 + 独立分支，共享 `.git` 历史。A 在 `worktree-feature-a/` 改 auth，B 在 `worktree-fix-bug/` 修 bug——互不干扰，最后各自合回 main。

```text
主 checkout (main)
├── .claude/worktrees/
│   ├── feature-auth/      ← session A（分支 worktree-feature-auth）
│   └── fix-bug/           ← session B（分支 worktree-fix-bug）
└── （共享 .git 目录）
```

## 二、启动 Worktree

```bash
claude --worktree feature-auth
# 或简写
claude -w feature-auth
```

- worktree 创建在 `.claude/worktrees/feature-auth/`
- 新分支名 `worktree-feature-auth`
- 省略 name 会自动生成（如 `bright-running-fox`）

**另一个 terminal 跑第二个**：

```bash
claude --worktree fix-bug
```

两个 session 独立工作。**建议把 `.claude/worktrees/` 加进 `.gitignore`**，否则主 checkout 里显示一堆 untracked 文件。

**首次需 workspace trust**：没在目录跑过 Claude 的话先跑一次 `claude` 接受 trust 对话框，否则 `--worktree` 报错退出。`-p` 非交互模式跳过此检查。

## 三、清理 Worktree

退出交互式 worktree session 时：

| worktree 状态 | 行为 |
| --- | --- |
| **干净**（无改动） | 无名 session 自动删 worktree + 分支；有名 session 会先问 |
| **有改动**（改动/未跟踪文件/新 commit） | 提示 keep 或 remove |

- **keep**：保留目录 + 分支，之后可回来
- **remove**：删目录 + 分支 + 所有工作

**`-p` 非交互模式不清理**——用 `git worktree remove` 手动删。

## 四、baseRef 选型

`worktree.baseRef` 设置（settings.json）：

| 值 | 行为 | 适合 |
| --- | --- | --- |
| `"fresh"`（默认） | 从远端默认分支（通常 `main`）切 | 大多数场景——干净起点 |
| `"head"` | 从当前本地 `HEAD` 切 | subagent 要操作进行中的工作 |

```json
{
  "worktree": { "baseRef": "head" }
}
```

**不能设成具体分支名**——要从特定分支切就用 `git worktree add` 手动建。

**fresh 模式**自动保持 `origin/HEAD` 最新：超 24 小时没 fetch 会自动 fetch（上限 5 秒），失败用本地缓存。

## 五、从 PR 切 worktree

```bash
claude --worktree "#1234"
```

Claude Code fetch `pull/1234/head`，建 worktree 在 `.claude/worktrees/pr-1234/`。**引号包住**防 shell 把 `#` 当注释。

## 六、Subagent Worktree 隔离

subagent frontmatter 加 `isolation: worktree`：

```markdown
---
name: refactorer
description: 跨多文件做机械重构
isolation: worktree
---

对每个受影响文件应用重构，跑测试，报告结果。
```

- 每个 subagent 拿自己的临时 worktree
- 无改动的 worktree 自动删
- 有改动的留到周期清理扫除

**或临时指定**：session 里跟 Claude 说「use worktrees for your agents」。

**清理**：周期 sweep 删超过 `cleanupPeriodDays` 的 subagent/background worktree（跳过有未提交工作的）。运行中 `git worktree lock` 防并发清理。

## 七、.worktreeinclude 携带文件

worktree 是全新 checkout——gitignore 文件（`.env` / `.env.local`）不在。项目根加 `.worktreeinclude`（`.gitignore` 语法）自动复制：

```text
.env
.env.local
config/secrets.json
```

**只复制既匹配 pattern 又被 gitignore 的文件**——tracked 文件不会被复制。

## 八、Worktree 与主 checkout 共享什么

| 共享 | 说明 |
| --- | --- |
| **`.git` 目录** | git 命令写主仓库共享 `.git`，`git commit` 在 worktree 里能跑 |
| **项目级 plugin** | 主 checkout 装的 project scope plugin 在 worktree 也加载（v2.1.200+） |
| **权限批准** | worktree 里选「不再问」存到主 checkout 的 `.claude/settings.local.json`，全仓库 worktree 共享（v2.1.211+） |

## 九、手动管理 Worktree

```bash
git worktree add ../project-feature-a -b feature-a   # 新分支
git worktree add ../project-bugfix fix-issue-456     # 已有分支
cd ../project-feature-a && claude                    # 启动
git worktree list                                    # 列出
git worktree remove ../project-feature-a             # 删除
```

## 常见坑

**没加 `.gitignore` 导致主 checkout 一堆 untracked**——把 `.claude/worktrees/` 加进 `.gitignore`。

**worktree 里 `.env` 不见了**——fresh checkout 不带 gitignore 文件。加 `.worktreeinclude` 自动复制。

**`-p` 模式 worktree 堆积不清理**——非交互不弹清理提示。定期 `git worktree list` + `git worktree remove` 清。

**subagent worktree 被锁删不掉**——运行中的 worktree 有 lock。等 agent 结束或 `git worktree unlock <path>` 手动解。

**`.claude` 是 symlink 建 worktree 失败**——Claude Code 拒绝在 symlink 路径建 worktree。移除 symlink 重试。

## 参考

- [Anthropic · Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)（访问于 2026-08-04）
- [Git worktree 文档](https://git-scm.com/docs/git-worktree)（访问于 2026-08-04）

## 下一步

- 非交互 / CI 模式 → [Headless / CI 模式](./headless)
- 后台与定时任务 → [后台与定时任务](./automation)
- subagent 配合 worktree → [Subagent · isolation](../subagents-and-workflows/agent-types#四、frontmatter-字段全表)

## 如果你想

- 看 worktree + subagent 实战 → 让 Claude「use worktrees for your agents」
- 理解 worktree 与 subagent/team 的并行边界 → [Run agents in parallel](https://code.claude.com/docs/en/agents)
- 手动从特定分支切 worktree → `git worktree add` 见上文第九节

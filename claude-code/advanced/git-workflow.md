---
title: Git 与 PR 工作流
description: 'Claude Code 与 Git/PR 协作——分支策略、gh CLI 联动、Co-Authored-By 签名、commit message 规范、PR 描述生成、常见 commit/pr 自动化'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  commitDocs: 'https://code.claude.com/docs/en/commit'
  ghActionsDocs: 'https://code.claude.com/docs/en/github-actions'
  accessedAt: 2026-08-04
---

# Git 与 PR 工作流

> **TL;DR**：Claude Code 深度集成 git 与 GitHub——`gh` CLI 联动、自动 Co-Authored-By 签名、commit message 生成、PR 描述生成。推荐工作流：`content/publish-<slug>` 分支 → 改 → `git diff main` 让 Claude 生成 commit/PR 文案 → ff-merge 到 main → 删分支。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- 推荐分支策略
- `gh` CLI 联动
- Co-Authored-By 签名机制与控制
- commit message 生成规范
- PR 描述自动生成
- 常见自动化模式

## 前置

- 读过 [Headless / CI 模式](./headless)
- 装好 `gh` CLI 并 `gh auth login`
- 基本 git 操作

## 一、推荐分支策略

```text
main（默认分支，受保护）
 │
 ├─ content/publish-xxx    ← 功能分支
 ├─ fix/bug-yyy
 └─ feat/feature-zzz
```

**命名约定**（本站采用）：

- `content/publish-<slug>`：内容发布
- `fix/<bug>`：修 bug
- `feat/<feature>`：新功能

**工作流**：

```bash
git checkout -b content/publish-xxx
# ... 改代码 ...
git add -A && git commit -m "..."
git checkout main && git merge --ff-only content/publish-xxx
git branch -d content/publish-xxx
```

**Claude Code 的默认行为**（见 CLAUDE.md / system prompt）：

- 只在用户要求时 commit / push
- 在默认分支上先开分支
- commit message 末尾加 `Co-Authored-By: Claude ...`
- PR body 末尾加 `🤖 Generated with Claude Code`

## 二、gh CLI 联动

Claude Code 用 `gh` 做 GitHub 操作（PR / issue / review）：

```bash
gh pr create --title "..." --body "..."
gh pr list
gh pr diff 1234
gh pr review 1234 --approve
gh issue list
```

**让 Claude 代你操作**：

```text
帮我创建一个 PR，标题从最近的 commit 推断
```

Claude 调 `gh pr create`，标题/body 自动生成。

**PR 描述生成**（经典模式）：

```bash
git diff main...HEAD | claude -p "根据这个 diff 生成 PR 描述：Summary / Changes / Testing 三段"
```

或写成 skill（见 [写你的第一个 Skill](../skills/custom-skill) 的 `/pr-desc` 案例）。

## 三、Co-Authored-By 签名

Claude Code 默认在 commit message 末尾加：

```text
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

**控制**：

```json
// settings.json
{
  "includeCoAuthoredBy": false
}
```

或 `attribution` 字段自定义：

```json
{
  "attribution": {
    "commit": "🤖 Generated with Claude Code",
    "pr": ""
  }
}
```

**PR body** 默认末尾加：

```text
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

设 `"pr": ""` 可关掉。

## 四、commit message 生成

让 Claude 看 staged changes 生成 commit message：

```bash
git add -A
claude -p "看 staged changes 生成合适的 commit message" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git commit *)"
```

**本站 commit 规范**（Conventional Commits 变体）：

```text
<type>(<scope>): <subject>

<body 详细说明>

<footer>

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

- `type`：`content` / `fix` / `feat` / `docs` / `chore` / `refactor`
- `scope`：影响的模块路径
- `subject`：祈使句、现在时

## 五、PR 工作流自动化

### 从 diff 生成完整 PR

```bash
# 1. 建分支改代码
git checkout -b feat/new-api
# ... 改 ...

# 2. commit
git add -A && git commit -m "feat(api): add new endpoint"

# 3. push + 建 PR（Claude 生成 title/body）
gh pr create --title "..." --body "..."
```

### CI 里自动 review

GitHub Actions 用 `claude -p` 做 PR review：

```yaml
# .github/workflows/claude-review.yml
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude --bare -p "review this PR for bugs and security" \
            --output-format json
```

## 六、常见 git 命令让 Claude 跑

```text
帮我看下最近 5 个 commit
帮我 cherry-pick abc123 到 main
帮我 rebase 到 origin/main
帮我创建一个 tag v1.2.3
帮我看下 main 和我分支的差异
```

Claude 用 Bash 工具跑 git 命令——**破坏性操作（force push / reset --hard / 删分支）会先确认**。

## 七、diff 语义

写 skill / PR 描述时注意：

| 命令 | 语义 |
| --- | --- |
| `git diff main..HEAD` | main 与 HEAD 各自的差异（两点） |
| `git diff main...HEAD` | 自 main 分出后 HEAD 的变化（三点，PR 常用） |

**PR 描述用 `main...HEAD`**——只看本分支引入的变化，不含 main 上其它的。

## 常见坑

**忘了 `gh auth login`**——Claude 调 `gh` 报未认证。先 `gh auth login`。

**commit message 没加 Co-Authored-By**——检查 `includeCoAuthoredBy` 是否被设 false。

**force push 到受保护分支**——Claude 会先确认，但别在 CI 里给 `bypassPermissions`。受保护分支用 PR 流程。

**diff 命令用错**——PR 描述用 `main...HEAD`（三点）不是 `main..HEAD`（两点）。三点只看本分支变化。

**Claude 自动 commit 了不想提交的东西**——Claude 默认只在你说时 commit。用 `permissions.ask` 加 `Bash(git commit *)` 强制每次问。

## 参考

- [Anthropic · Commit with Claude Code](https://code.claude.com/docs/en/commit)（访问于 2026-08-04）
- [Anthropic · GitHub Actions](https://code.claude.com/docs/en/github-actions)（访问于 2026-08-04）
- [gh CLI 文档](https://cli.github.com/manual/)（访问于 2026-08-04）

## 下一步

- 全局记忆 → [全局记忆](./memory)
- Headless / CI 模式 → [Headless / CI 模式](./headless)
- 把 PR 描述生成写成 skill → [写你的第一个 Skill](../skills/custom-skill)

## 如果你想

- CI 自动 review PR → [Anthropic · GitHub Actions](https://code.claude.com/docs/en/github-actions)
- GitLab CI 集成 → [Anthropic · GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)
- 看 commit 命令完整选项 → [Anthropic · Commit](https://code.claude.com/docs/en/commit)

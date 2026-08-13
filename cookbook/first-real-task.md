---
title: 第一个真实任务
description: 用 Claude Code 给一个没测试的小函数补一套单测——20 分钟走完 Plan → Edit → Verify 全流程
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/common-workflows'
  accessedAt: 2026-07-28
---

# 第一个真实任务

> **目标**：跟着做完，你把一个「一直想补测试但一直没补」的小函数补上了单测。全程约 20 分钟、实际花费约 $0.10–$0.30（Sonnet 5）。

⏱ 预计阅读时间：8 分钟 · 动手 20 分钟

## 你将做到

- ✅ 用 Plan Mode 让 Claude 先规划、你确认后再动手
- ✅ 让 Claude 自己识别项目的测试框架（Vitest / Jest / pytest / …），不用你告诉它
- ✅ 得到一份能跑通、覆盖了边界情况的测试文件，并 commit 到分支

## 前置检查清单

开始前请确保：

- [ ] 装好 Claude Code v2.1.x：`claude --version`
- [ ] 已经跑通过 [第一次对话](/getting-started/first-conversation) —— 至少能启动、能授权工具
- [ ] 手上有一个 git 仓库（任意语言），里面有**一个还没测试的小函数**（20–80 行）
- [ ] 项目能本地跑测试（`pnpm test` / `npm test` / `pytest` / `go test ./...` 任一）

**没有合适的项目？** 建一个最小 Node 项目当练手：

```bash
mkdir slugify-demo && cd slugify-demo
pnpm init && pnpm add -D vitest
mkdir src && cat > src/slugify.ts <<'EOF'
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}
EOF
git init && git add . && git commit -m "chore: init"
```

这段 6 行函数就是你要补测试的对象——它有若干边界情况（空字符串、只有符号、开头结尾都是符号、Unicode、超长），全都值得写用例。

## 第 1 步：切一个干净分支

**动手改代码前先切分支**——万一 Claude 改砸了你 `git reset --hard` 一秒回原地。

```bash
git checkout -b claude-add-tests
claude
```

## 第 2 步：进 Plan Mode，先让它规划

`claude` 启动后**第一件事按 `Shift+Tab` 进 Plan Mode**——Plan Mode 下 Claude 只能 Read/Grep/Glob、不能改文件、不能跑 Bash 写盘副作用。参见 [Plan Mode](/claude-code/basics/plan-mode)。

然后发这段 prompt（**照抄，把 `<函数路径>` 换成你的**）：

```text
请为 `<函数路径>` 里的函数补一套单元测试。要求：

1. 先 Grep 一下项目根目录的 package.json / pyproject.toml / go.mod，确认测试框架和运行命令
2. 找项目里已有的一份测试文件参考（有的话），沿用它的风格
3. 一个函数对应一个测试文件；每个 describe 覆盖：正常路径 / 边界值 / 异常输入
4. 断言要看到具体值，不要只判 defined / truthy
5. 规划写完后我确认，你再动手

先给我 plan。
```

## 第 3 步：审 plan，别一路 Enter

Claude 会输出一份 plan，通常长这样：

```text
Plan:
1. Read src/slugify.ts, understand the function
2. Grep for existing *.test.ts in src/
3. Read one existing test as style reference
4. Write src/slugify.test.ts with 5-7 cases
5. Run `pnpm test` to verify all pass
```

**审 3 件事**：

- **它要读的文件**对不对？（有时它猜错入口）
- **测试用例列表**够不够？想不到的边界值现在就补一句「加上 Unicode 输入」
- **有没有多余动作**？（比如它想改源代码——本篇任务是**只写测试不改源码**，看到就否）

有问题**直接在对话里补一句**「plan 里加上 Unicode 输入 & 超长字符串两个 case」——Claude 会修订 plan。

## 第 4 步：确认执行

Plan 满意了，按 `Shift+Tab` **退出 Plan Mode**，回复：

```text
plan 可以，按计划做。允许 Edit 与 Write。
```

Claude 会开始写测试文件。它每次调用 Edit / Write 都会**弹权限提示**——第一次弹的时候选「**Allow for this session**」，后续同工具就免打扰（但仅本次会话有效，见 [权限系统](/claude-code/basics/permissions)）。

## 第 5 步：跑测试、修红

Claude 写完会自己请求跑 `pnpm test`。看输出——十有八九**第一次会挂 1–2 个**：

- 边界值 case 的**预期值**它猜错了
- 项目用的 assertion API 有细微差异（`.toBe` vs `.toEqual`）

直接把红色输出粘回去：

```text
测试挂了：
[粘贴 pnpm test 的报错]

修一下。
```

Claude 会 diff 出问题定位、给出修复。跑到全绿为止——一般 1–2 轮。

## 第 6 步：审 diff、commit

**全绿不等于对**——`git diff` 一眼：

```bash
git diff --stat
git diff src/slugify.test.ts
```

看 3 件事：

- 测试文件的**位置**对不对（应该跟源代码同目录或 `__tests__/` 下，别扔到项目根）
- 断言里是不是**每一个都在验证具体值**
- 有没有意外**动了源代码**（本篇要求只加测试文件）

没问题就 commit：

```bash
git add .
git commit -m "test: add unit tests for slugify"
```

## 常见错误

**Claude 想改源代码「让它更好测」**

信号：Plan 里出现「重构 XXX 让它更可测」这类项。

修复：在 prompt 里明确「**本次任务只加测试文件、不改源代码**」；如果它坚持源码有问题，让它**先补测试保底、再讨论重构**分开做——一次一个 commit。

**测试文件叫 `test.ts` 而不是 `slugify.test.ts`**

原因：Claude 没找到项目 test 匹配 glob 就自己起了个名。

修复：直接说「文件名跟 `<其它测试文件名>` 一样的命名规则」；或者让它先跑一次 `find . -name '*.test.*' -not -path '*/node_modules/*'` 看命名习惯。

**覆盖率报出来 100% 但断言全是 `.toBeDefined()`**

原因：你没在 prompt 里限定断言粒度。

修复：Prompt 里加「**每个 expect 都要验证具体值，禁止只用 toBeDefined / toBeTruthy**」，让它重写。

**Claude 一次改太多，你回滚不了**

原因：没在 Plan Mode 里逐步确认，或者一句「你看着做吧」放开。

修复：任何一次感觉「它做得太多」的时刻，`Ctrl+C` 打断、`git status` 看它动了什么、必要时 `git checkout -- .` 撤掉未 commit 的改动，然后重新起一个更小的任务。

**测试跑挂但 Claude 说「测试通过了」**

原因：Claude 有时会**幻觉**执行结果——尤其是它没真调 Bash 跑测试就先总结了。

修复：**永远你自己跑一次** `pnpm test`——别信总结，看实际输出。这条对任何 Claude Code 任务都适用。

## 参考

- Anthropic Docs · [Common workflows](https://code.claude.com/docs/en/common-workflows)（访问于 2026-07-28）
- [Plan Mode](/claude-code/basics/plan-mode)
- [权限系统](/claude-code/basics/permissions)

## 下一步

- 学写第一个 Skill → [写你的第一个 Skill](./build-first-skill)
- 学写第一个 MCP Server → [写你的第一个 MCP Server](./build-first-mcp-server)

## 如果你想

- 系统学 Claude Code → [Claude Code 精通](/claude-code/)
- 挑战更大的任务 → [用 Claude Code 重构老项目](./refactor-legacy-project) 🚧
- 学会拆任务的思路 → [深度提示工程 · best-practices](/claude-capabilities/prompting/best-practices)

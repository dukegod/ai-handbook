---
title: Bash 执行命令
description: Claude Code 的 Bash 工具——执行 Shell 命令、后台运行、超时控制与安全边界
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Bash 执行命令

> **TL;DR**：`Bash` 让 Claude Code 跑 Shell 命令——装依赖、跑测试、执行构建。默认需要确认，内置只读命令（`ls`、`git status` 等）自动放行。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Bash 工具的基本用法与参数
- 哪些命令自动放行、哪些需要确认
- 后台运行与超时控制
- 安全边界与常见坑

## 基本用法

```
Bash command="ls -la"
```

Claude 执行命令后返回 stdout/stderr。工作目录是项目根目录（或上次 `cd` 后的目录）。

## 权限：自动放行 vs 需要确认

**自动放行的命令**（只读，不改文件）：

`ls`、`cat`、`head`、`tail`、`grep`、`find`、`git status`、`git log`、`git diff`、`echo`、`pwd`、`wc` 等。

**需要确认的命令**（会修改文件或系统状态）：

`rm`、`mv`、`cp`、`npm install`、`git commit`、`git push`、`docker`、`curl`（POST）等。

::: tip 配置放行
常用命令可在 `settings.json` 中预放行，避免反复确认：
```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run build)"]
  }
}
```
:::

## 后台运行

长时间运行的命令用 `run_in_background: true`：

```
Bash command="pnpm dev" run_in_background="true"
```

后台命令不会阻塞 Claude，它会在命令退出时收到通知。适合：

- 开发服务器（`pnpm dev`）
- 测试 watcher（`jest --watch`）
- 构建任务（`pnpm build`）

## 超时控制

`timeout` 参数控制最大等待时间（毫秒），默认 120 秒，最大 600 秒：

```
Bash command="npm test" timeout="300000"
```

超时后命令被终止，Claude 收到已有的输出。

## 常见用法模式

**运行测试**

```
Bash command="npm test"
```

**安装依赖**

```
Bash command="pnpm install"
```

**查看 Git 状态**

```
Bash command="git status"
```

**组合命令**

```
Bash command="cd src && grep -r 'TODO' . | wc -l"
```

::: warning cd 不持久
每次 `Bash` 调用是独立的 Shell。`cd src && ...` 只在当次调用有效，下次调用还是项目根目录。
:::

## 安全边界

- Claude Code 的沙箱限制了部分危险操作
- `--dangerouslyDisableSandbox` 可关闭沙箱（不推荐）
- 网络请求、文件系统外操作受系统权限约束

## 常见坑

**命令找不到**

原因：PATH 环境变量与你的终端不同。

修复：用绝对路径（如 `/usr/local/bin/node`）或先 `which xxx` 定位。

**超时被杀**

原因：命令执行超过 timeout。

修复：增大 timeout 或用 `run_in_background`。

**交互式命令卡住**

原因：命令需要 stdin 输入（如 `npm init` 的交互式问答）。

修复：用非交互式 flag（如 `npm init -y`）或提前提供参数。

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）
- Anthropic Docs · [Permissions · Read-only commands](https://code.claude.com/docs/en/permissions#read-only-commands)（访问于 2026-08-13）

## 下一步

- 学会搜索文件内容 → [Grep / Glob 搜索](./search)
- 学会联网获取信息 → [WebFetch / WebSearch](./web)

## 如果你想

- 了解 Bash 在工具总览中的位置 → [工具总览](./overview)
- 控制 Bash 的权限范围 → [权限系统](../basics/permissions)
- 在 CI 中使用 Claude Code → [Headless / CI 模式](../advanced/headless)

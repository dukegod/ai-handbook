---
title: 安装与认证
description: macOS / Linux / Windows / WSL 全平台安装步骤、三种认证方式与常见报错
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/setup'
  accessedAt: 2026-07-28
---

# 安装与认证

> **目标**：装好 Claude Code、通过认证、跑通 `claude --version`。全程约 10 分钟。

⏱ 预计阅读时间：8 分钟

## 你将做到

- ✅ 在你的系统上装好 Claude Code
- ✅ 完成账号认证（3 种方式任选）
- ✅ 用 `claude --version` 与 `claude doctor` 验证安装正确
- ✅ 知道升级、卸载、常见报错的定位方法

## 前置检查

按下表核对你的系统满足官方要求（引自 [Anthropic Docs · Setup](https://code.claude.com/docs/en/setup)，访问于 2026-07-28）：

| 项 | 最低要求 |
| --- | --- |
| macOS | 13.0+ |
| Windows | 10 1809+ 或 Server 2019+ |
| Linux | Ubuntu 20.04+ / Debian 10+ / Alpine 3.19+ |
| 内存 | 4 GB+ |
| 架构 | x64 或 ARM64 |
| Shell | Bash / Zsh / PowerShell / CMD |
| 联网 | 需能访问 `anthropic.com`（[Anthropic 支持地区](https://www.anthropic.com/supported-countries)） |

**账号**：需要 Claude 的 **Pro / Max / Team / Enterprise / Anthropic Console** 之一。免费 Claude.ai 账号**不能**用 Claude Code。企业内网可走 Amazon Bedrock / Google Vertex / Microsoft Foundry，见文末。

## 第 1 步：选一种安装方式

**官方首推 Native Install**——最简单、自动后台升级、不依赖 Node.js。

::: code-group

```bash [macOS / Linux / WSL]
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell [Windows PowerShell]
irm https://claude.ai/install.ps1 | iex
```

```batch [Windows CMD]
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

:::

**其他方式（各有取舍）**：

| 方式 | 命令 | 说明 |
| --- | --- | --- |
| Homebrew | `brew install --cask claude-code` 或 `claude-code@latest` | macOS 用户熟悉，**不自动升级** |
| WinGet | `winget install Anthropic.ClaudeCode` | Windows 官方包管理，**不自动升级** |
| apt / dnf / apk | 见 [官方 Linux 包管理器](https://code.claude.com/docs/en/setup#install-with-linux-package-managers) | 企业 Linux 常用，签名仓库 |
| npm | `npm install -g @anthropic-ai/claude-code` | 需 Node.js 22+，**不要用 `sudo`** |

## 第 2 步：验证安装

```bash
$ claude --version
2.1.211 (Claude Code)
```

返回类似版本号即安装成功。想更全面的自检：

```bash
$ claude doctor
```

`claude doctor` 会检查安装健康度、`settings.json` 有效性、常见问题并给出修复建议——**装完先跑一遍**。

## 第 3 步：完成认证

首次运行 `claude` 时，Claude Code 会引导你认证。选一种：

### 方式 A：浏览器登录（推荐给个人用户）

```bash
$ claude
```

打开浏览器，用 Anthropic 账号（Pro / Max / Team / Enterprise）登录。登录状态保存在 `~/.claude/`。

### 方式 B：API Key（推荐给 API 用户）

```bash
$ export ANTHROPIC_API_KEY=sk-ant-****
$ claude
```

从 [Anthropic Console](https://console.anthropic.com/) 拿 key。`export` 只对当前 shell 生效——长期用请写进 `~/.zshrc` 或 `~/.bashrc`。

### 方式 C：接入非 Claude 模型

用 Anthropic 兼容端点或多供应商切换工具，让 Claude Code 跑智谱 GLM / MiniMax / DeepSeek / Moonshot / Kimi / 通义 Qwen 等**国内主流模型**。两种方式的完整配置见独立指南 → **[接入非 Claude 模型](/claude-code/ecosystem/third-party-models)**。

> ⚠️ 这是**社区/厂商方案，非 Anthropic 官方支持**。能力差异（Prompt Caching / Extended Thinking / Tool Use）与兼容性风险详见独立指南。

### 方式 D：企业内网（Bedrock / Vertex / Foundry）

企业内网无法直连 `anthropic.com` 时，走 [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock)、[Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai) 或 [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry)——**底层仍是 Anthropic 的 Claude 模型**，只是走第三方云托管。详细配置见 [企业部署](/claude-code/ecosystem/enterprise)。

## 第 4 步：跑一次

```bash
$ cd your-project
$ claude
```

进入交互界面即表示装好并认证成功。想直接体验一次任务，看 [第一次对话](./first-conversation)。

## 常见错误

**`command not found: claude`**

Native install 把二进制放在 `~/.local/bin/claude`。检查 PATH：

```bash
$ echo $PATH | tr ':' '\n' | grep '\.local/bin'
```

无输出则把 `export PATH="$HOME/.local/bin:$PATH"` 写进你的 shell rc。

**`The token '&&' is not a valid statement separator`**

你在 PowerShell 里跑了 CMD 命令。看提示符：`PS C:\` 开头是 PowerShell，`C:\` 不带 `PS` 是 CMD。用对应命令。

**`'irm' is not recognized as an internal or external command`**

反过来——你在 CMD 里跑了 PowerShell 命令。

**Alpine：`bash: not found`**

Alpine 默认没有 bash。先装：

```bash
apk add bash curl libgcc libstdc++ ripgrep
```

并在 `~/.claude/settings.json` 里设 `env.USE_BUILTIN_RIPGREP=0`。

**Free Claude.ai 账号登录后仍报无权限**

Claude Code 不支持免费账号——升级到 Pro / Max / Team / Enterprise，或改用 Console API Key。

**企业代理下 install 脚本失败**

`curl` 走 `https://claude.ai`。若你的网络无法直连，先设 `HTTPS_PROXY`：

```bash
$ export HTTPS_PROXY=http://your-proxy:port
$ export HTTP_PROXY=http://your-proxy:port
$ curl -fsSL https://claude.ai/install.sh | bash
```

## 升级与卸载

**升级**

- Native install：后台自动升级；也可 `claude update` 立即触发
- Homebrew：`brew upgrade claude-code`（或 `claude-code@latest`）
- WinGet：`winget upgrade Anthropic.ClaudeCode`
- apt / dnf / apk：走系统包管理器 upgrade
- npm：`npm install -g @anthropic-ai/claude-code@latest`（**不要**用 `npm update -g`）

**卸载**（Native install）

```bash
# macOS / Linux / WSL
$ rm -f ~/.local/bin/claude
$ rm -rf ~/.local/share/claude

# 清所有配置与会话历史（谨慎）
$ rm -rf ~/.claude ~/.claude.json
```

其他安装方式的完整卸载步骤见 [官方 Uninstall 章节](https://code.claude.com/docs/en/setup#uninstall-claude-code)。

## 参考

- [Anthropic Docs · Advanced setup](https://code.claude.com/docs/en/setup)（访问于 2026-07-28）
- [Anthropic Docs · Authentication](https://code.claude.com/docs/en/authentication)（访问于 2026-07-28）
- [Anthropic Docs · Troubleshoot installation](https://code.claude.com/docs/en/troubleshoot-install)（访问于 2026-07-28）
- [Anthropic 支持地区](https://www.anthropic.com/supported-countries)（访问于 2026-07-28）

## 下一步

- 走通第一个对话 → [第一次对话](./first-conversation)

## 如果你想

- 建立对内部机制的直觉 → [心智模型](./mental-model)
- 直接跳到实操 → [Cookbook · 第一个真实任务](/cookbook/first-real-task)
- 企业内网深入部署 → [企业部署 SSO / Bedrock / Vertex](/claude-code/ecosystem/enterprise)

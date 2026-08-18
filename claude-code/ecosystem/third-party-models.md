---
title: 接入非 Claude 模型
description: 用 Anthropic 兼容端点或多供应商切换工具，让 Claude Code 跑 GLM / MiniMax / DeepSeek / Kimi / Qwen 等国内模型的两种非官方方式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-29
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  minimaxDocs: 'https://platform.minimaxi.com/docs/token-plan/claude-code'
  bigmodelDocs: 'https://docs.bigmodel.cn/cn/guide/develop/claude'
  deepseekDocs: 'https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/'
  kimiDocs: 'https://platform.kimi.com/docs/guide/claude-code-kimi'
  aliyunDocs: 'https://help.aliyun.com/zh/model-studio/claude-code'
  ccrRepo: 'https://github.com/musistudio/claude-code-router'
  ccSwitchRepo: 'https://github.com/farion1231/cc-switch'
  accessedAt: 2026-07-29
---

# 接入非 Claude 模型

> ⚠️ **本页讲的是社区/厂商方案，不是 Anthropic 官方支持**。Anthropic 官方目前仅支持 Claude 模型（含 Bedrock / Vertex / Foundry 三种第三方云托管，底层仍是 Claude）。若你需要在 Claude Code 里跑智谱 GLM、MiniMax、DeepSeek、Moonshot / Kimi、通义 Qwen 等国内模型，走本页两种方式之一。

## 你能在这里学到

- Claude Code 接入非 Claude 模型的两种主流路径
- 每种方式的适用场景与取舍对比
- 以 MiniMax 为完整案例的配置步骤
- 其他国内厂商的 endpoint 与模型速查
- 常见坑（残留环境变量优先级 / onboarding / 能力差异）

## 前置知识

- 已装好 Claude Code（[安装与认证](/claude-code/getting-started/installation)）
- 拥有目标模型厂商的 API Key（[MiniMax](https://platform.minimaxi.com/) / [智谱 BigModel](https://bigmodel.cn/) / [DeepSeek](https://platform.deepseek.com/) / [Moonshot](https://platform.moonshot.cn/) 等）

## 两种方式速览

| | 方式一：Anthropic 兼容端点 | 方式二：多供应商切换工具 |
| --- | --- | --- |
| 原理 | 厂商侧提供 Anthropic Messages 协议的兼容 endpoint | 本地代理层：GUI/CLI 一键切换 |
| 配置位置 | `~/.claude/settings.json` 的 `env` | 工具 UI + `settings.json` |
| 依赖 | 无 | 需装 cc-switch / Claude Code Router 等 |
| 优势 | 简单直接、性能最好、无额外进程 | 多厂商快速切换、GUI 友好 |
| 缺点 | 需厂商已提供 Anthropic 兼容端点 | 引入额外进程与故障点 |
| 推荐场景 | 长期锁定某一家 | 频繁切多家 / 团队多人用 GUI |

## 方式一：Anthropic 兼容端点

大部分国内主流厂商已提供 Anthropic 协议兼容端点。只需在 `~/.claude/settings.json` 的 `env` 里覆盖几个环境变量。

### 第 1 步：清空可能残留的环境变量

**先做这一步**——否则 shell 里的 `export` 会覆盖 `settings.json`：

```bash
$ unset ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL
$ grep -rn ANTHROPIC ~/.zshrc ~/.bashrc ~/.profile
# 若有硬编码 export 行，删掉
```

### 第 2 步：编辑 `~/.claude/settings.json`

以 MiniMax（国内）为完整示例：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<你的 MiniMax API Key>",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3[1m]"
  }
}
```

**字段说明**：

- `ANTHROPIC_BASE_URL`：厂商的 Anthropic 兼容 endpoint
- `ANTHROPIC_AUTH_TOKEN`：厂商 API Key（**不是** `ANTHROPIC_API_KEY`）
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW`：自动 compact 阈值。默认按 Claude 200k，若你的模型上下文更长（如 MiniMax-M3 的 1M）调大以免过早 compact
- `ANTHROPIC_DEFAULT_{SONNET,OPUS,HAIKU}_MODEL`：把 Claude Code 内部的 Sonnet / Opus / Haiku 三档 alias 都映射到目标模型；也可以分别映射到不同模型混用

### 第 3 步：跳过登录引导

Claude Code 首启会强制走 Anthropic 账号登录，非 Claude 场景需在 `~/.claude.json` 里预标记完成：

```json
{
  "hasCompletedOnboarding": true
}
```

### 第 4 步：验证

```bash
$ cd your-project
$ claude
```

进入 TUI 后：

```
/status   # 应显示 ANTHROPIC_BASE_URL 指向厂商 endpoint
/model    # 应显示当前模型（如 MiniMax-M3）
```

### 各厂商 endpoint 速查

| 厂商 | ANTHROPIC_BASE_URL | 示例模型 | 官方教程 |
| --- | --- | --- | --- |
| **MiniMax**（国内） | `https://api.minimaxi.com/anthropic` | `MiniMax-M3[1m]` | [platform.minimaxi.com](https://platform.minimaxi.com/docs/token-plan/claude-code) |
| **MiniMax**（国际） | `https://api.minimax.io/anthropic` | `MiniMax-M3[1m]` | 同上 |
| **智谱 BigModel**（GLM） | `https://open.bigmodel.cn/api/anthropic` | `glm-5.2[1m]` / `glm-4.7` | [docs.bigmodel.cn](https://docs.bigmodel.cn/cn/guide/develop/claude) |
| **DeepSeek** | `https://api.deepseek.com/anthropic` | `deepseek-v4-pro` / `deepseek-v4-flash` | [api-docs.deepseek.com](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/) |
| **Moonshot / Kimi** | `https://api.moonshot.cn/anthropic` | `kimi-k3[1m]` / `kimi-k2.7-code` | [platform.kimi.com](https://platform.kimi.com/docs/guide/claude-code-kimi) |
| **阿里百炼**（Qwen） | `https://coding.dashscope.aliyuncs.com/apps/anthropic` | `qwen3.8-max-preview` / `qwen3.7-max` | [help.aliyun.com](https://help.aliyun.com/zh/model-studio/claude-code) |

> **阿里百炼多 endpoint**：上表用 **Coding Plan** 域名；另有 Token Plan（`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`）与按量计费专属域名（形如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`）。选哪个取决于你买的档位，见官方教程。
>
> **1M 上下文注意**：`[1m]` 后缀的模型（`MiniMax-M3[1m]` / `glm-5.2[1m]` / `kimi-k3[1m]`）需在 `settings.json` 里配合 `CLAUDE_CODE_AUTO_COMPACT_WINDOW: "1000000"`（或 `"1048576"`）才不会过早触发 compact。
>
> **以各厂商最新官方文档为准**——模型名、endpoint 与配置会随厂商迭代更新。

## 方式二：多供应商切换工具

想在多家厂商间快速切换？两个主流选择：

### cc-switch（GUI 工具）

MiniMax 官方教程推荐。适合不喜欢改 JSON 的用户。

- 项目：[github.com/farion1231/cc-switch](https://github.com/farion1231/cc-switch)
- macOS：`brew tap farion1231/ccswitch && brew install --cask cc-switch`
- Windows：[Releases](https://github.com/farion1231/cc-switch/releases) 下载安装包
- 用法：GUI 里为每家 provider 建一个配置 → 一键"启用"当前
- 注意：1M 上下文阈值仍需手动在 `settings.json` 加 `CLAUDE_CODE_AUTO_COMPACT_WINDOW`

### Claude Code Router（CLI + Web UI）

适合 CLI 用户、需 Docker 部署、或自定义路由规则。

- 项目：[github.com/musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
- 安装：`npm install -g @musistudio/claude-code-router`（需 Node.js 22+）
- 启动：`ccr ui` → 管理 UI `http://127.0.0.1:3458`，网关 `http://127.0.0.1:3456`
- 内置预设：**Z.AI / 智谱**、DeepSeek、Moonshot / Kimi、SiliconFlow、阿里百炼 等
- 完整文档：[ccrdesk.top](https://ccrdesk.top/)

## 常见坑

**残留环境变量优先级更高**

`ANTHROPIC_AUTH_TOKEN` 与 `ANTHROPIC_BASE_URL` 在 shell 里 `export` 后**优先级高于 `settings.json`**。配置总不生效时先：

```bash
$ echo $ANTHROPIC_AUTH_TOKEN
$ echo $ANTHROPIC_BASE_URL
$ grep -rn ANTHROPIC ~/.zshrc ~/.bashrc ~/.profile ~/.config/fish/
```

**能力差异必须注意**

- **Prompt Caching**：官方 Claude 端点保证生效，非 Claude 模型不一定支持——详见 [Prompt Caching](/claude-capabilities/api/prompt-caching)
- **Extended Thinking**：依赖模型支持（MiniMax-M3 支持，通过 `/config` → **Thinking mode** 切换；快捷键 macOS `Option+T` / Windows `Alt+T`）——详见 [Extended Thinking](/claude-capabilities/core/extended-thinking)
- **Tool Use** 精度：非 Claude 模型在多步 agentic 任务上通常比 Claude 差一档
- **上下文窗口**：调整 `CLAUDE_CODE_AUTO_COMPACT_WINDOW` 匹配模型实际窗口

**Onboarding 引导跳不过**

首启需要 `~/.claude.json` 里 `hasCompletedOnboarding: true`，否则强制拉浏览器登录 Anthropic 账号——非 Claude 场景永远登不上。

**国内网络仍需 provider 侧可达**

上述方案仅解决"协议适配"，不解决 endpoint 网络问题。确认自己网络到 `api.厂商.com` 可达。

**Claude Code 更新可能破坏兼容**

Claude Code 版本迭代快，非官方接入没有兼容承诺。升级 Claude Code 后**先跑一遍 `/status` 与 `/model`** 确认配置未被覆写。

## 维护提示

本页作为**社区/厂商接入方式的独立索引**，随生态迭代持续更新。后续会：

- 追踪各厂商模型名与 endpoint 变更（本轮已核实 MiniMax / 智谱 / DeepSeek / Kimi / 阿里百炼 五家）
- 追踪 Claude Code 破坏性更新对接入方式的影响
- 收录读者验证过的自定义 endpoint 配置

## 参考

- [MiniMax 官方 · Claude Code 接入](https://platform.minimaxi.com/docs/token-plan/claude-code)（访问于 2026-07-29）
- [智谱 BigModel · Claude API 兼容](https://docs.bigmodel.cn/cn/guide/develop/claude)（访问于 2026-07-29）
- [DeepSeek · Claude Code 集成](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/)（访问于 2026-07-29）
- [Moonshot Kimi · Claude Code 接入](https://platform.kimi.com/docs/guide/claude-code-kimi)（访问于 2026-07-29）
- [阿里百炼 · Claude Code 接入](https://help.aliyun.com/zh/model-studio/claude-code)（访问于 2026-07-29）
- [Claude Code Router · GitHub](https://github.com/musistudio/claude-code-router)（访问于 2026-07-29）
- [cc-switch · GitHub](https://github.com/farion1231/cc-switch)（访问于 2026-07-29）
- [Anthropic Docs · Third-party integrations](https://code.claude.com/docs/en/third-party-integrations)（访问于 2026-07-29）—— 官方仅覆盖 Claude 模型的第三方托管

## 下一步

- 回 [安装与认证](/claude-code/getting-started/installation) 继续入门主线
- 想理解 Claude Code 上下文机制 → [心智模型](/claude-code/getting-started/mental-model)

## 如果你想

- 用官方 Claude 模型 → [安装与认证 · 方式 A/B](/claude-code/getting-started/installation#第-3-步完成认证)
- 深入模型选型 → [模型选择](/claude-code/basics/model-selection) / [模型 ID 与定价](/claude-capabilities/models/model-ids)
- 长期把配置提交到项目共享 → [Settings 配置文件](/claude-code/customization/settings)

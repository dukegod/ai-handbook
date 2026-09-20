---
title: OpenClaw 深度评测
description: Peter Steinberger 出品的 self-hosted AI agent——基于 pi-agent-core 内核 + 多平台 Gateway + v2026.8.1 (2.0) 升级
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-09-20
verifiedWith:
  sources:
    - name: OpenClaw 官网
      url: https://openclaw.ai
      accessedAt: 2026-09-20
    - name: OpenClaw GitHub
      url: https://github.com/openclaw/openclaw
      accessedAt: 2026-09-20
    - name: OpenClaw Docs
      url: https://docs.openclaw.ai
      accessedAt: 2026-09-20
    - name: ChatterGo · OpenClaw Deep Dive 源码分析（v2026.1.30）
      url: https://www.chattergo.ai/blog/openclaw-deep-dive-architecture-agent-loop/
      accessedAt: 2026-09-20
    - name: BestHub · Why Pi Powers OpenClaw
      url: https://www.besthub.dev/articles/why-pi-s-minimalist-architecture-powers-openclaw-s-ai-coding-agent-34de9e6565d8
      accessedAt: 2026-09-20
    - name: OpenClaw 官方博客 · OpenClaw 2.0 (v2026.8.1)
      url: https://openclaw.ai/blog/openclaw-2-accidentally/
      accessedAt: 2026-09-20
    - name: OpenClaw Wiki · OpenClaw 2.0 What's New
      url: https://openclawwiki.com/posts/openclaw-2-0-whats-new
      accessedAt: 2026-09-20
    - name: Meta AI Labs · OpenClaw 2.0 技术解读
      url: https://metaailabs.com/openclaw-releases-openclaw-2-0-guided-model-setup-575-ms-control-ui-startup-and-one-trust-boundary-per-gateway
      accessedAt: 2026-09-20
---

# OpenClaw 深度评测

> **TL;DR**：奥地利工程师 Peter Steinberger 打造的 self-hosted AI agent——把极简的 pi-agent-core 包成"全能管家外壳"，三个月冲 145k stars。2026-08 释出 v2.0 (v2026.8.1)，从"个人助理"升级到"团队可协作的多人 agent"。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- OpenClaw 与 pi-agent-core 的"外壳 vs 内核"关系
- 三层架构（Gateway / Pi Engine / Channels）如何把 AI 跑在聊天软件里
- 8 层工具策略 + Heartbeat 主动触发这两个独特设计
- 与 Claude Code / Codex / PI-agent 的定位差异
- 什么时候适合用、什么时候不该用

## 作者与项目背景

### Peter Steinberger

| 维度 | 信息 |
|------|------|
| **身份** | 奥地利软件工程师 |
| **代表作** | **PSPDFKit** —— 全球 PDF SDK 龙头，被多家上市公司收购（2018） |
| **当前状态** | **2026-02 加入 OpenAI**；项目由独立团队继续维护 |
| **风格** | 个人项目驱动、scrappy、社区为先 |

> **重要变更**：2026-02 后 Steinberger 已加入 OpenAI 不再全职开发；项目由独立团队接管，v2.0 (v2026.8.1) 是团队接手后的首个重大版本。

### 三个月三次更名

OpenClaw 的名字本身就是一段故事——3 个月内换 3 次身份，每次都因为社区反应而调整：

| 时间 | 名字 | 触发事件 |
|------|------|----------|
| 2025-11 | **Clawdbot** | Steinberger 个人周末项目首发，致敬底层 Claude 模型 |
| 2026-01-27 | **Moltbot** | Anthropic 法务要求避开"Claude"字样 |
| 2026-01-30 | **OpenClaw** | 社区嫌 Moltbot 不顺口，**3 天后**再次改名 |

更名反而助推传播——"ClawCon"线下聚会（2026-02，San Francisco）+ "Moltbook"（AI agent 社交网络实验）形成病毒式传播链。

### 项目里程碑

| 时间 | 里程碑 |
|------|--------|
| 2025-11 | Clawdbot 首发，9k stars（24h 内） |
| 2026-01-30 | 更名 OpenClaw |
| 2026-02 | **145k stars**，进入 GitHub 史上最快增长项目行列 |
| 2026 上半年 | 单周 200 万访问量、20k+ forks、300+ 贡献者 |

## 核心定位：外壳，AI 管家

如果说 Pi-agent 是一个**极简的引擎**（4 个工具 + 极小 system prompt），那 OpenClaw 就是**装在外面的那层壳**——把引擎包装成"24 小时在线、能听懂你在任何聊天软件里说的话的私人助理"。

| 维度 | PI-agent | OpenClaw | Claude Code |
|------|----------|----------|-------------|
| **定位** | 底层框架 | 完整 Agent 产品 | 完整 CLI 产品 |
| **开箱即用** | ⭐（需自己组装） | ⭐⭐⭐⭐⭐（自带 100+ 技能） | ⭐⭐⭐⭐ |
| **可扩展性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **跨聊天平台** | ❌（要自己接） | ✅ 10+ 平台原生 | ❌（仅 CLI） |
| **托管方式** | 本地 | 自托管（Mac/Linux/VPS） | 云端 SaaS |
| **数据归属** | 本地 | 本地 | Anthropic 服务器 |

**一句话区分**：PI-agent = 引擎；OpenClaw = 装了引擎的整车。

## 技术架构

### 三层架构（核心创新）

OpenClaw 的 Pi Engine 不是单一进程，而是三个解耦层各自负责一件事：

```
┌─────────────────────────────────────────────────┐
│  Channels 层（输入适配器）                        │
│  WhatsApp · Telegram · Discord · Slack ·         │
│  Signal · iMessage · Matrix · Email              │
├─────────────────────────────────────────────────┤
│  Gateway 层（认证 + 路由 + 消息标准化）           │
│  → 把平台消息转成统一 MsgContext                  │
├─────────────────────────────────────────────────┤
│  Pi Engine 层（agent runtime，基于 pi-agent-core）│
│  3 层嵌套 Loop：会话调度 / Prompt组装 / 工具执行  │
└─────────────────────────────────────────────────┘
```

**为什么这样设计**：

- **Channels 解耦**：换平台不用改核心，加一个 adapter 就行
- **Gateway 单点**：认证、路由、限流、日志都集中，审计方便
- **Pi Engine 专注**：只负责 LLM 对话循环，复杂任务由 Subagent 接力

### Pi Engine 内部三层循环

pi-agent-core 提供基础 loop，OpenClaw 在其上包了三层职责分工：

| 层 | 职责 | 关键能力 |
|----|------|----------|
| **外层** | 会话调度 | Lane 队列保证每会话串行、上下文窗口保护（16k 硬下限、32k 预警） |
| **中层** | Prompt 组装 + API 调用 | 9 段式 system prompt（约 4,500 token）、ContextEngine 组装、模型选择与失败回切 |
| **内层** | 流式解析 + 工具执行 | tool_use 解析、8 层工具策略、循环检测（30-call 滑动窗口检测 4 种模式） |

**这套架构的工程价值**：跑 10+ 小时的企业流水线任务，单 tick 触发、事件驱动、状态可持久化——拔电源重启也能从事件日志恢复断电前状态。

### Heartbeat 主动触发

OpenClaw 区别于 ChatGPT/Claude Code 等"被动响应"产品的最大不同——**它会主动找你**：

```
┌─────────────────────────────────────────────┐
│  Heartbeat 机制                              │
├─────────────────────────────────────────────┤
│                                             │
│  用户消息 → 处理 → 响应                      │
│                ↓                            │
│         （任务完成/超时）                     │
│                ↓                            │
│         ⏰ Heartbeat 定时器触发               │
│                ↓                            │
│         后台任务：监控邮件 / 巡检 CI /        │
│         自动重启挂掉的服务 / 提醒开会         │
│                ↓                            │
│         推回用户的 WhatsApp / Telegram       │
│                                             │
└─────────────────────────────────────────────┘
```

这是为什么 OpenClaw 被定位为 **"AI employee"** 而非 chatbot——它不需要被提醒就能做事。

## 多平台支持

| 平台 | 集成方式 | 特殊能力 |
|------|----------|----------|
| **WhatsApp** | Business API | 群聊、语音消息、图片理解 |
| **Telegram** | Bot API | 内联键盘、inline query |
| **Discord** | Bot + Gateway | 服务器管理、slash command |
| **Slack** | OAuth | 工作流触发、消息快捷操作 |
| **Signal** | signal-cli | 端到端加密 |
| **iMessage** | macOS bridge | 仅 macOS 宿主 |
| **Matrix** | Client-Server | 去中心化 |
| **Email** | IMAP/SMTP | 自动回复、邮件 triage |

**核心承诺**：你在哪个聊天软件里都能找到它，且体验一致。

## 生态背书

| 背书方 | 时间 | 含义 |
|--------|------|------|
| **GitHub 史上最快增长** | 2026-02 | 145k stars、20k forks，超越 AutoGPT |
| **ClawCon 线下聚会** | 2026-02-04 | Frontier Tower SF，社区已成型 |
| **Moltbook 衍生项目** | 2026-01 | Matt Schlicht（Octane AI 联创）用 OpenClaw 搭 AI agent 社交网络 |
| **基于 pi-agent-core** | 持续 | 复用 Mario Zechner 的极简引擎 |
| **v2026.8.1 (2.0) 史上最大版本** | 2026-08-31 | 16,000+ PRs / 933 贡献者 / 7 周开发周期 |

| 维度 | 数据 |
|------|------|
| **GitHub stars** | 145k+（截至 2026-02，2.0 后未公开新数） |
| **Forks** | 20k+ |
| **贡献者** | 300+（v2.0 单版本就 933 贡献者） |
| **最新稳定版** | **v2026.8.1（2026-08-31）** |
| **协议** | MIT |
| **托管成本** | $3-5/月（基础 VPS） |

## OpenClaw 2.0 升级要点（v2026.8.1）

2026-08-31 释出的 v2026.8.1 是项目史上最大版本：**16,000+ PRs / 933 贡献者 / 7 周开发**。从"个人助理"升级为"团队可协作的多人 agent"。

### 1. 浏览器 app 重做为一等公民

之前 Control UI 是"设置面板"，现在是"对话主界面"——和 ChatGPT/Claude 一样打开直接进入会话。

| 指标 | 1.x | 2.0 |
|------|------|------|
| 启动时间 | ~1.6s | **575 ms** |
| JS 请求数 | 140 | **45** |
| 测试条件 | mocked Gateway + 50ms HTTP/1.1 | 同 |

新能力：docked panel 增加 Workspace 文件编辑器 + git Changes 面板（PR/CI 状态）+ 浏览器面板（元素检查 / 截图标注）+ 全屏 web terminal。

### 2. Shared cloud sessions：OpenClaw 走向多人协作

**这是 2.0 最重要的产品定位变化**——从"一人一助理"变成"小团队共享一助理"。

| 用例 | 场景 |
|------|------|
| **Handoff** | 早班开启研究任务，下午同事接手，agent 上下文完整保留 |
| **Pair debugging** | 两人同时观察 agent 实时执行 |
| **小团队运维** | 3-5 人共用一个 assistant 部署，不用各跑各的 |

权限边界：owner / admin 可设置 read / suggest / draft work / participate 四档。**注意**：文档明确说"这不是租户隔离、不是安全边界"——多租户产品场景仍不适用。

### 3. Guided setup 把"安装难"砍掉

1.x 时代新人最大的劝退点——一上来就要面对一堆配置。2.0 反过来：

```
检测本机已有 →
  ChatGPT / Claude / Codex 已登录？ → 直接复用
  本地 Ollama / LM Studio 模型？ → 直接检测
  环境变量已有 API key？ → 直接读取
  都没有？→ GPT-5.6（OpenAI 默认）/ Gemma 4（本地默认）
```

新 OpenAI 安装默认 GPT-5.6；本地 RAM-gated 默认 Gemma 4；llama.cpp 默认上下文提到 64K；node-llama-cpp 被托管 llama-server 取代。

### 4. 安全加固（回应 2026 上半年的安全事件）

2026 上半年 Immersive Labs / Bitsight 报告了暴露实例泄露 API key 和聊天记录的事件，2.0 的安全加固直接回应这类问题：

| 层 | 改动 |
|-----|------|
| **Runtime** | Gateway 处理 untrusted input 加固 |
| **Plugins + Skills** | 三方代码加载机制收紧 |
| **Secret handling** | 凭证从 agent 上下文隔离；新增 proxy 模式：受保护 secret 只发到 approved HTTPS 目的地，未绑定目的地 fail closed |

其他安全增强：
- `openclaw security audit` 命令：检查 inbound access / tool blast radius / network exposure / browser control / plugin allowlist
- **Permission modes**：sandboxing 章节正式产品化（之前是扩展默认行为，现在是 UI 选项）
- **2026 crowdsourced prompt injection arena**（272K 攻击 / 41 场景）：Claude Opus 4.5 = 0.5%，Sonnet 4.5 = 1.0%，Haiku 4.5 = 1.3%，Gemini 2.5 Pro = 8.5%。但 adaptive human attacker 仍 >80% 成功——所以工具策略 + exec approvals + sandboxing 仍是硬性兜底

### 5. Memory / Skills / Automations 工作流三件套

| 模块 | 升级 |
|------|------|
| **Memory** | 真正的 backbone：相关私人会话可召回；新 memory engine 从旧 QMD store 迁移；忘记派生记忆不抹原会话 |
| **Skills** | create → validate → install → review 全链路 + 自学习模式（agent 可把"被纠正的经验"转成 skill 提案） |
| **Automations** | 统一命名替代 cron（agent / UI / CLI / docs 一致）；分离"是否运行了"、"结果是否送达"、"请求是否完成" |

### 6. 关键 Breaking Change（升级前必看）

| 改动 | 影响 | 处理 |
|------|------|------|
| **Sessions 迁 SQLite** | 文件存储 → SQLite 存储 | 必须 `openclaw backup sqlite` 备份后再升级；旧版本无法读新格式 |
| **OpenProse 插件 + `/prose` 命令移除** | 用过的人不能继续用 | `.prose` 源文件保留，需走 Agent Skill migration path |
| **codex/* 和 openai-codex/* 路由统一到 openai/* ** | provider config / stored sessions / automations 都涉及 | `openclaw doctor --fix` 自动迁移 |
| **5 个 plugin SDK subpath 弃用** | 仅影响三方插件作者 | 截止 2026-09-01；普通用户无感 |

**升级建议**（来自官方与社区）：
- ✅ 依赖会话稳定性 / 看重安全改进 / 等团队功能的——立刻升
- ⏸️ 重度定制的生产实例 + 三方插件——等一个 patch 让插件作者先适配

### 7. 生态格局变化

- **2026-02**：Steinberger 加入 OpenAI，项目由独立团队继续
- **2026-08-31**：独立团队交出首个重大版本 v2026.8.1（16,000+ PRs 的工作量证明团队承接能力）

> **判断**：项目不再是"一人项目"，但 scrappy 风格延续——独立团队节奏未失，仍是"AI 管家外壳"路线最有希望的选手。

## 能力横评

## 能力横评

| 能力 | OpenClaw | Claude Code | Codex CLI | PI-agent | DeepSeek Harness |
|------|----------|-------------|-----------|----------|-----------------|
| **代码补全** | ✅（技能驱动） | ✅ | ✅ | ✅ | ✅ |
| **多平台聊天** | ⭐⭐⭐⭐⭐ | ❌ | ❌ | ❌ | ⭐⭐ |
| **主动触发** | ⭐⭐⭐⭐⭐（Heartbeat） | ⭐（hooks） | ⭐ | ⭐⭐（扩展） | ⭐⭐⭐ |
| **子代理系统** | ⭐⭐⭐⭐ | ⭐⭐（Task） | ⭐⭐ | ⭐⭐（扩展） | ⭐⭐⭐⭐⭐ |
| **沙箱安全** | ⭐⭐⭐⭐⭐（Docker + 8 层策略） | ⭐⭐ | ⭐ | ⭐⭐⭐（扩展） | ⭐⭐⭐⭐ |
| **MCP 生态** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **可观测性** | ⭐⭐⭐（事件日志） | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **数据归属** | 本地 | 云端 | 云端 | 本地 | 本地 |
| **月成本** | $3-5 VPS + LLM token | $20-200 | 按 token | 免费 + token | 免费 + token |

## 安全特性：8 层工具策略

OpenClaw 因为权限大（要读文件、执行 shell、发消息），安全是最重要的设计点：

```
profile → provider → global → agent → group → sandbox → subagent → approval
   ↓        ↓         ↓        ↓       ↓        ↓         ↓         ↓
 个人配置  模型选择   全局规则  角色规则  群聊规则  容器隔离  子代理    高危操作
                                                  限制      隔离    人工审批
```

**每层都做 allow/deny 决策**，最后才到执行层。bash 类高危命令会触发审批流（用户配置 approval workflow）。

**对比**：Claude Code 只有"问一次允许 / 永久拒绝"两档；PI-agent 默认 YOLO 模式；DeepSeek Harness 用 Cordis 插件做隔离。OpenClaw 这套 8 层级联是**最工程化**的安全模型。

## 适用场景

| 用户类型 | 推荐度 | 理由 |
|---------|--------|------|
| **个人 + 想跨平台用 AI** | ⭐⭐⭐⭐⭐ | 一个 OpenClaw 实例 = 所有聊天软件里的私人助理 |
| **小团队 + 自动化运维** | ⭐⭐⭐⭐⭐ | Heartbeat + 多平台 = 自建"数字员工" |
| **隐私敏感 / 私有化** | ⭐⭐⭐⭐⭐ | 自托管 + 本地数据 + 自带 API key |
| **企业 + 跨平台集成** | ⭐⭐⭐⭐ | 比 SaaS 灵活，比 PI-agent 开箱即用 |
| **纯 CLI 编码** | ⭐⭐ | Claude Code / Codex 更专注 |

**不太适合**：

- **不想自托管的团队**（托管 VPS 是必备）
- **追求极致安全审计**（8 层策略虽强，但工具链复杂度带来新攻击面）
- **新手用户**（作者原话："It's not meant for non-technical users"）
- **依赖 MCP 生态**（OpenClaw 主推技能系统，MCP 仅作为补充）

## 安装

```bash
# 方式 1：npm 安装
npm install -g @openclaw/cli

# 方式 2：脚本安装
curl -fsSL https://openclaw.ai/install.sh | sh

# 验证
openclaw --version

# 启动配置向导
openclaw init

# 跑起来
openclaw start
```

**前置条件**：

- Node.js ≥ 20
- 一个 LLM API key（Claude / DeepSeek / GPT）
- 一台能 24h 运行的 VPS（$3-5/月）

## 核心局限

### 1. 安全复杂度自找麻烦

工具越多、能力越大，潜在攻击面越大。Cybersecurity 社区对 OpenClaw 表达过关注——必须自己配 8 层策略 + 沙箱。

### 2. 仍处于"个人项目"阶段

作者原话："It's a free, open source hobby project that requires careful configuration to be secure. It's not meant for non-technical users."

### 3. API key 仍依赖第三方 LLM

自托管只是数据归属问题。要用 Claude 还是得付 Anthropic 钱。

### 4. 协议生态未稳

API 仍在快速迭代，企业级生产案例少。

## 参考

- [OpenClaw 官网](https://openclaw.ai)（访问于 2026-09-20）
- [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)（访问于 2026-09-20）
- [OpenClaw Docs](https://docs.openclaw.ai)（访问于 2026-09-20）
- [OpenClaw 官方博客 · OpenClaw 2.0 (v2026.8.1)](https://openclaw.ai/blog/openclaw-2-accidentally/)（访问于 2026-09-20）
- [OpenClaw Wiki · OpenClaw 2.0 What's New](https://openclawwiki.com/posts/openclaw-2-0-whats-new)（访问于 2026-09-20）
- [Meta AI Labs · OpenClaw 2.0 技术解读](https://metaailabs.com/openclaw-releases-openclaw-2-0-guided-model-setup-575-ms-control-ui-startup-and-one-trust-boundary-per-gateway)（访问于 2026-09-20）
- [ChatterGo · OpenClaw Deep Dive](https://www.chattergo.ai/blog/openclaw-deep-dive-architecture-agent-loop/) — v2026.1.30 源码分析
- [BestHub · Why Pi Powers OpenClaw](https://www.besthub.dev/articles/why-pi-s-minimalist-architecture-powers-openclaw-s-ai-coding-agent-34de9e6565d8)
- [PI-agent 深度评测](./pi-agent) — 内核引擎

## 下一步

- 对比 PI-agent（OpenClaw 的内核）→ [PI-agent 深度评测](./pi-agent)
- 对比 Claude Code → [Claude Code 深度评测](./claude-code)
- 团队引入 → [团队 AI 工作流](/ai-harness/workflows/team)

## 如果你想

- 看 OpenClaw 与 Hermes（同类项目）对比 → 待补充
- 理解外壳 vs 内核的工程权衡 → [AI Harness 工程](/ai-harness/)
- 立刻用起来 → [OpenClaw 官方 Quickstart](https://docs.openclaw.ai/quickstart)
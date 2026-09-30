---
title: MiniMax 全系
description: 'MiniMax-M3 / M3.1-Flash-Preview——1M 上下文、多模态编码旗舰、极致性价比、全模态矩阵'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: MiniMax 官方模型总览
      url: https://platform.minimax.io/docs/guides/models-intro
      accessedAt: 2026-09-30
    - name: MiniMax 官方按量定价
      url: https://platform.minimax.io/docs/guides/pricing-paygo
      accessedAt: 2026-09-30
    - name: MiniMax 官方模型发布记录
      url: https://platform.minimax.io/docs/release-notes/models
      accessedAt: 2026-09-30
---

# MiniMax 全系

> 7 家厂商里**性价比最激进（$0.3/M input）+ Agentic 定位最明确 + 全模态覆盖最广**。

## 一、公司背景

MiniMax 由前商汤科技副总裁闫俊杰创立，2021 年成立，总部上海。核心策略是 **「Agentic + 全模态 + 低价」**——不只做文本，语音 / 视频 / 图像 / 音乐全线自研。商业模式：API 计费 + 消费端产品（海螺 / Talkie）+ 企业方案。海外用 `platform.minimax.io`，国内用 MiniMax 开放平台。

## 二、模型矩阵（截至 2026-09）

| 模型 | 定位 | 上下文 | 主要场景 |
| --- | --- | --- | --- |
| **MiniMax-M3.1-Flash-Preview** | 前沿编码 / 多模态（预览） | 1M | 思考深度可调；官方注明**仅 Token Plan 与 MiniMax Code 提供** |
| **MiniMax-M3** | 前沿多模态编码旗舰 | 1M | 编码 / Agent 工作流 / 长上下文 / 多模态对话输入 |
| **MiniMax-M2.7 / M2.7-highspeed** | 上一代 | — | 递归自我改进路线的起点；highspeed 同性能、更低延迟 |
| **MiniMax H3 / H3 Max** | 视频生成 | — | 768P / 2K、4-15s；H3 Max 为高速档（480P / 768P） |
| **speech-2.8 / image-01** | 语音 / 图像 | — | TTS（40 语言）/ ASR / 文生图 |

> **产品线逻辑**：语言模型（`M3`）与多模态（`H3` 视频 / `speech` 语音 / `image` 图像）走**两条独立产品线**。截至 2026-09，`M3` 是官方按量计费的主力，`M3.1-Flash-Preview` 只在订阅通道内可用；`M2.7` 及更早版本（`M2.5` / `M2.1` / `M2`）官方已归入 Legacy。

## 三、技术架构

**Agentic + 编码优先** —— 官方对 `M3` 的定位是「frontier multimodal coding model」，对 `M3.1-Flash-Preview` 的定位是「frontier multimodal coding model，1M 上下文 + 可调思考深度」。与多数厂商「通用对话优先」不同，MiniMax 把**编码与 Agent 任务**写在模型描述的第一位。

**上一代的基准取向** —— `M2.7` 发布时（2026-03）的官方基准全部围绕 agent 任务设计：SWE-Pro 56.22%、VIBE-Pro 55.6%、Terminal Bench 2 57.0%。

> ⚠️ 上述数字来自 `M2.7` 发布页，**本轮（2026-09）未在官方模型总览页复核**；官方未公布 `M3` 的同口径基准对比表。

**全模态自研** —— 与多数厂商「文本为核、多模态为插件」不同，MiniMax 的语音 / 视频 / 图像 / 音乐是独立自研产品线，走「全模态矩阵」路线。官方同时提供 `M3` / `M2.7` / Music 3 / `H3` 的自部署路径（SGLang / ComfyUI）。

## 四、核心能力

| 能力 | 描述 |
| --- | --- |
| **Tool Use** | 函数调用 / Interleaved Thinking，官方称 `M3` 为 Agentic Model |
| **MCP 支持** | `API-vlm` + `web_search`（Beta，按次计费） |
| **可调思考深度** | `M3.1-Flash-Preview` 特有 |
| **全模态** | 文本 + 语音（speech-2.8）+ 视频（H3）+ 图像（image-01） |
| **协议兼容** | Anthropic SDK / OpenAI SDK / AI SDK，OpenAI Responses API 兼容端点 |
| **编码工具接入** | Token Plan 已覆盖 Claude Code / Codex / Cursor / TRAE / OpenClaw 等 |

## 五、部署形态

| 部署 | 平台 |
| --- | --- |
| **MiniMax API** | `platform.minimax.io`（海外）/ 国内开放平台 |
| **Token Plan** | 订阅制（Credits + 配额），`M3.1-Flash-Preview` 仅此通道 |
| **自部署** | SGLang（`M3` / `M2.7` / Music 3 / `H3`）、ComfyUI（`H3`） |
| **消费端** | 海螺 / Talkie 等产品 |

## 六、价格（截至 2026-09，官方按量定价）

| 模型 | Input | Output | 缓存读 |
| --- | --- | --- | --- |
| MiniMax-M3（输入 ≤ 512K） | $0.30 / MTok | $1.20 / MTok | $0.06 |
| MiniMax-M3（输入 > 512K） | $0.60 / MTok | $2.40 / MTok | $0.12 |
| MiniMax-M2.7 | $0.30 / MTok | $1.20 / MTok | $0.06 |
| MiniMax-M2.7-highspeed | $0.60 / MTok | $2.40 / MTok | $0.06 |

**价格说明**：

- `M3` 两档价格官方标注「**永久 5 折**」（划线价为 $0.60 / $2.40 / $0.12）
- `Priority` 档（`service_tier: priority`）为标准价的 **1.5 倍**，提供优先接入
- `MiniMax-M3.1-Flash-Preview` 官方**未列按量单价**，仅通过 Token Plan / MiniMax Code 提供
- **Music API 自 2026-08-20 起不再对新用户开放**付费接口，免费音乐生成接口下线；官方引导到 MiniMax Audio 与 Hugging Face 上的开源 MiniMax Music 3

**`M3` 在 512K 以内仍是 7 家厂商里 input 价最低的旗舰之一**（$0.3/M）——走「极致性价比 + agentic 能力」的错位竞争路线。

## 七、适合场景 / 不适合场景

**适合**：
- Agent 工作流 / 工具调用（Agentic 原生设计）
- 成本敏感的大规模调用
- 多模态需求（语音 / 视频 / 图像全套自研）
- 需要 1M 上下文的长任务（`M3` / `M3.1-Flash-Preview`）

**不适合**：
- 需要音乐生成 API（付费接口已对新用户关闭）
- 需要顶级通用推理质量的场景（官方未公布 `M3` 的同口径通用基准）
- 中文知识深度要求高的场景（中文生态弱于 Qwen / GLM / Kimi）

## 八、最新动态（2026-09）

**三条跟踪线**：

- **模型线**：M 系列语言模型。核心看「哪个模型是当前按量旗舰、上下文多大、思考深度是否可调」
- **多模态线**：`H3` 视频、`speech-2.8` 语音、`image-01` 图像。这条线迭代最快，也最容易被「关停 / 开放权重」类动作改变
- **产品线**：Token Plan 订阅体系，以及 Claude Code / Codex / Cursor 等编码工具的接入进度

**如何跟踪**：

1. **官方源**：[模型发布记录](https://platform.minimax.io/docs/release-notes/models)（带日期的完整发布流水）、[模型总览](https://platform.minimax.io/docs/guides/models-intro)（当前在售 + Legacy 分区）、[按量定价](https://platform.minimax.io/docs/guides/pricing-paygo)
2. **更新节奏**：语言模型约 2-4 个月一更（`M2.7` 2026-03 → `M3` 2026-06）；多模态线更快
3. **判断原则**：M 系列换代看「上下文 + 编码定位 + 定价」三要素；多模态线优先看**「是否开放权重 / 是否关停付费 API」**——这两类动作对现有集成的破坏性远大于版本号 +0.1

**截至 2026-09 的具体动态**（均据官方源）：

- **2026-06-01 发布 `MiniMax-M3`** —— 官方定位「最新 M 系列语言模型，面向 agentic reasoning、tool use、coding、多模态对话输入与长上下文任务」
- **2026-07-31 发布 `MiniMax H3`** —— 新一代通用**开源**多模态视频模型，能跨文本 / 图像 / 视频 / 音频理解创作意图；分辨率 768P / 2K，时长 4-15s
- **模型总览页新增 `MiniMax-M3.1-Flash-Preview`** —— 1M 上下文 + 可调思考深度，官方注明「仅通过 Token Plan 和 MiniMax Code 提供」。**该条目尚未进入官方「模型发布记录」页**，属总览页先行披露
- **2026-08-20 Music API 调整** —— 音乐生成 / 歌词生成付费接口不再向新用户开放，免费音乐接口（`music-3.0-free` / `music-2.6-free` / `music-cover-free`）下线；官方建议改用 MiniMax Audio 或 Hugging Face 上的开源 MiniMax Music 3
- **定价侧** —— `M3` 标注「永久 5 折」；`Priority` 档为标准价 1.5 倍；`M2.7` 及更早版本移入 Legacy 折叠区但仍可调用
- **自部署** —— 官方新增 `M3` / `M2.7` / Music 3 / `H3` 的自部署指南（`M3` 标注为实验性 SGLang baseline）

> ⚠️ **资本动态（据媒体报道，未经官方源核实）**：MiniMax 于 2026-01 登陆港交所（发行价 165 港元），2026-05-29 与中信证券签署辅导协议启动 A 股 IPO。2025 年全年总收入约 7904 万美元（同比 +158.9%），超 70% 来自海外；经调整净亏损约 2.51 亿美元。股价 2026-03 峰值超 1300 港元。以上均为财经媒体报道口径，引用前建议核对港交所公告。

## 关键洞察

- **价格是最大的武器**——$0.3/M input 直接打穿成本线，`M3` 换代后价格带没变
- **Agentic + 编码是明确路线**——官方把「编码 / Agent」写在模型描述第一位，不是「通用模型 + Agent 能力」
- **全模态矩阵**——少数全线自研多模态的中国厂商，但已开始「关停付费接口、转开源权重」的收缩动作

## 参考

- [MiniMax 官方模型总览](https://platform.minimax.io/docs/guides/models-intro)（访问于 2026-09-30）
- [MiniMax 官方按量定价](https://platform.minimax.io/docs/guides/pricing-paygo)（访问于 2026-09-30）
- [MiniMax 官方模型发布记录](https://platform.minimax.io/docs/release-notes/models)（访问于 2026-09-30）
- [中国 LLM 现状观察（2026-03）](https://merchmindai.net/blog/zh/post/china-llm-landscape-2026)（访问于 2026-08-14）

## 下一步

- 横向对比 7 家 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 按场景选型 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
- 看技术路线 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 如果你想

- 看 Kimi 档案 → [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看 GLM 档案 → [Zhipu · 智谱 GLM 全系](/ai-trends/cn-vendors/zhipu/)
- 看国内厂商动态 → [国内厂商](/ai-trends/cn-vendors/)

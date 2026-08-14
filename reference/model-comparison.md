---
title: 7 厂商横向对比
description: Claude / GPT / Grok / Kimi / MiniMax / GLM / Qwen 在性能基准、上下文、价格、部署、Tool Use 等 8 维度的横向对比
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: Anthropic 定价
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-08-13
    - name: OpenAI 定价
      url: https://openai.com/pricing
      accessedAt: 2026-08-13
    - name: Kimi 开放平台
      url: https://platform.moonshot.cn/docs
      accessedAt: 2026-08-13
    - name: 智谱 BigModel
      url: https://open.bigmodel.cn/
      accessedAt: 2026-08-13
    - name: DashScope 平台
      url: https://dashscope.aliyun.com/
      accessedAt: 2026-08-13
    - name: xAI 定价
      url: https://docs.x.ai/developers/pricing
      accessedAt: 2026-08-14
    - name: MiniMax 定价
      url: https://platform.minimax.io/docs/guides/pricing-paygo
      accessedAt: 2026-08-14
---

# 7 厂商横向对比

> 8 个维度、7 家厂商、一张速查表——**看完就能选型**。

## 一、模型矩阵对比

| 厂商 | 旗舰 | 中端 | 轻量 | 推理模型 | 开源 |
|------|------|------|------|----------|------|
| **Anthropic** | Opus 5 | Sonnet 5 | Haiku 4.5 | — | ❌ |
| **OpenAI** | GPT-5.6 Sol | GPT-5.6 Terra | GPT-5.6 Luna | o 系列 | 开源双轨 |
| **xAI** | Grok 4.6 | — | — | Grok 4.20-reasoning | ❌ |
| **Moonshot** | Kimi K3 | Kimi K2.5 | — | K3（总是推理） | K2.5 / K3 开源 |
| **MiniMax** | M2.7 | M2.5 | — | M2.7（agentic） | 部分 |
| **Zhipu** | GLM-5.2 | GLM-5.1 | GLM-4-Air | GLM-Z1 | GLM-5 全尺寸 |
| **Qwen** | Qwen3.8-Max | Qwen3.5 | 开源小尺寸 | — | 全尺寸 + 全模态 |

**结论**：OpenAI 推理最强（o-series），Qwen 开源最彻底，Anthropic Agent 最强，MiniMax 性价比最激进。

## 二、性能基准对比（旗舰模型）

> ⚠️ 具体分数以各厂商官方发布为准（Anthropic / OpenAI 发布博客、中文厂商技术报告），下表只保留**定性结论**，不收录未经核实的数字。

| 厂商 | 英文基准（MMLU 等） | 中文基准（C-Eval 等） | 编码基准 |
|------|------|------|------|
| Anthropic | 领先 | — | 领先（Opus 5 / Sonnet 5） |
| OpenAI | 领先 | — | 领先（GPT-5.6 Sol / o 系列） |
| xAI | 中上 | — | 长上下文编码（Grok 4.6） |
| Moonshot | — | 领先 | 长上下文编码强（Kimi K3） |
| MiniMax | 中上 | — | Agentic 基准（SWE-Pro 56.22%） |
| Zhipu | 中上 | 领先 | Agentic Coding 主推（GLM-5.2） |
| Qwen | 中上 | 领先 | 开源编码强（Qwen3.5） |

**结论**：英文基准 Claude/GPT 领先，中文基准 Kimi/Qwen/GLM 领先。**没有全能冠军，只有场景冠军**。

## 三、上下文窗口对比

| 厂商 | 默认 | 最大 | 长上下文技术 |
|------|------|------|-------------|
| Anthropic | 1M（Opus 5 / Sonnet 5） | 1M（Fable 5） | RoPE 插值 + 滑动窗口 |
| OpenAI | 短/长上下文双档 | 长上下文档（GPT-5.6） | RoPE 插值 |
| xAI | 500K（Grok 4.6） | 1M（4.20-reasoning） | 长上下文 + 推理模式 |
| Moonshot | 1M（K3） | 1M（K3） | LongRoPE 风格 |
| MiniMax | 205K（M2.7） | 205K | — |
| Zhipu | 200K（GLM-5.2） | 200K | RoPE 插值 |
| Qwen | 1M | 1M | RoPE 插值 + 滑动窗口 |

**结论**：Claude / Kimi / Qwen 的 1M 是当前主流上限，xAI Grok 4.20 推理线 1M。**长文档选 Claude/Kimi/Qwen/xAI**。

## 四、价格对比（旗舰模型，每百万 token）

| 厂商 | Input | Output | 缓存读 | 备注 |
|------|-------|--------|--------|------|
| Anthropic | $5（Opus 5） | $25 | $0.50 | Fable 5 为 $10/$50 |
| OpenAI | $5（Sol） | $30 | $0.50 | Terra $2 / Luna $0.2 |
| xAI | $2（Grok 4.6） | $6 | $0.50 | ≥200K prompt 时 $4 |
| Moonshot | $3（K3） | $15 | $0.30 | 缓存命中价 |
| MiniMax | $0.30（M2.7） | $1.20 | $0.06 | 7 家中最低 |
| Zhipu | $1.4（GLM-5.2） | $4.4 | $0.26 | — |
| Qwen | ¥12（Qwen3.8-Max） | ¥36 | ¥1.5 | 原价，不含优惠 |

**结论**：MiniMax 价格最低，国产（Zhipu / Qwen）次之，Claude / GPT 旗舰最贵。**成本敏感选 MiniMax/GLM/Qwen，质量优先选 Claude/GPT**。

## 五、部署方式对比

| 厂商 | API | 开源权重 | 私有化 | 端侧 | 国产化 |
|------|-----|----------|--------|------|--------|
| Anthropic | ✅ | ❌ | Bedrock/Vertex | ❌ | ❌ |
| OpenAI | ✅ | 开源双轨 | Azure | ❌ | ❌ |
| xAI | ✅ | ❌ | 企业方案 | ❌ | ❌ |
| Moonshot | ✅ | 部分 | Kimi 平台 | ❌ | ✅ |
| MiniMax | ✅ | 部分 | 企业方案 | ❌ | ✅ |
| Zhipu | ✅ | 全尺寸 | MaaS | ✅ | ✅ |
| Qwen | ✅ | 全尺寸+全模态 | 阿里云 | ✅ | ✅ |

**结论**：国产化/私有化选 Qwen/GLM，海外企业选 Claude (Bedrock/Vertex)、GPT (Azure) 或 xAI。

## 六、Tool Use / Agent 能力对比

| 厂商 | Function Calling | Agent 框架 | Computer Use | 特色 |
|------|-----------------|------------|--------------|------|
| Anthropic | ✅ 原生 | Agent SDK + Claude Code | ✅ Beta | Agent 最完整 |
| OpenAI | ✅ 原生（行业首创） | Assistants API | ❌ | Code Interpreter |
| xAI | ✅ 原生 | — | ❌ | Web/X Search 实时工具 |
| Moonshot | ✅ 原生 | — | ❌ | Deep Research |
| MiniMax | ✅ 原生 | Agent Teams | ❌ | 动态工具搜索 |
| Zhipu | ✅ 原生 | AllTools | ❌ | 搜索+计算+绘图组合 |
| Qwen | ✅ 原生 | Qwen-Agent（开源） | ❌ | 全模态 Agent |

**结论**：Agent 能力 Claude 最完整（Computer Use + SDK），OpenAI Function Calling 是行业标准。

## 七、多模态对比

| 厂商 | 文本 | 图片 | 音频 | 视频 | 全模态 |
|------|------|------|------|------|--------|
| Anthropic | ✅ | ✅ | ❌ | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ✅ | ❌ | ❌ |
| xAI | ✅ | ✅ | ✅ | ✅（专用模型） | ❌ |
| Moonshot | ✅ | ✅ | ❌ | ❌ | ❌ |
| MiniMax | ✅ | ✅ | ✅ | ✅ | ✅（全模态矩阵） |
| Zhipu | ✅ | ✅ | ❌ | ❌ | ❌ |
| Qwen | ✅ | ✅ | ✅ | ✅ | ✅（Omni） |

**结论**：Qwen / MiniMax 全模态最完整，Claude 多模态最弱（只有文本+图片）。

## 八、许可证 + 商业可用性

| 厂商 | 许可证 | 商业可用 | 备注 |
|------|--------|----------|------|
| Anthropic | 闭源 | API 付费 | Bedrock/Vertex 企业 |
| OpenAI | 闭源 + 开源双轨 | API 付费 / 开源免费 | 开源型号以官方为准 |
| xAI | 闭源 | API 付费 | X 订阅内置 |
| Moonshot | 部分开源 | API 付费 / 部分免费 | K2/K3 权重开源 |
| MiniMax | 部分开源 | API 付费 / 部分免费 | 多模态全系自研 |
| Zhipu | Apache 2.0 | API 付费 / 开源免费 | 全尺寸开源 |
| Qwen | Apache 2.0 | API 付费 / 开源免费 | 全尺寸+全模态开源 |

**结论**：开源选 Qwen/GLM，闭源选 Claude/GPT，中间路线选 Kimi / MiniMax。

## 速查决策表

| 场景 | 首选 | 备选 | 理由 |
|------|------|------|------|
| **英文编码 + Agent** | Claude Sonnet 5 | GPT-5.6 Sol | Tool Use + Agent 最完整 |
| **中文长文档** | Kimi K3 | Qwen3.8-Max | 1M 上下文 + 文件解析 |
| **数学/代码推理** | OpenAI o 系列 | GLM-Z1 | RLVR 推理最强 |
| **实时信息/社交数据** | xAI Grok 4.6 | — | X 生态 + Web/X Search |
| **本地/端侧部署** | Qwen 开源小尺寸 | GLM-4-Air | 全尺寸开源 + 端侧优化 |
| **企业合规（海外）** | Claude (Bedrock) | GPT (Azure) | 云厂商集成 |
| **企业合规（国内）** | Qwen (阿里云) | GLM (智谱云) | 国产化 + 私有化 |
| **多模态** | Qwen3.5 / MiniMax | GPT-5.6 Vision | 全模态最完整 |
| **极低成本** | MiniMax M2.7 | GLM-5.1 | $0.3/M input 全场最低 |

## 参考

- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape) — 4 大技术路线详解
- [7 厂商详情](/ai-trends/vendors/) · [Anthropic](/ai-trends/vendors/anthropic) · [OpenAI](/ai-trends/vendors/openai) · [xAI](/ai-trends/vendors/grok) · [Moonshot](/ai-trends/vendors/moonshot) · [MiniMax](/ai-trends/vendors/minimax) · [Zhipu](/ai-trends/vendors/zhipu) · [Qwen](/ai-trends/vendors/qwen)
- [模型选型决策树](./model-selection-guide) — 按 6 维度选型

## 下一步

- 用决策表选型 → [模型选型决策树](./model-selection-guide)
- 深入某家厂商 → [Anthropic](/ai-trends/vendors/anthropic) / [OpenAI](/ai-trends/vendors/openai) / [xAI](/ai-trends/vendors/grok) / [Moonshot](/ai-trends/vendors/moonshot) / [MiniMax](/ai-trends/vendors/minimax) / [Zhipu](/ai-trends/vendors/zhipu) / [Qwen](/ai-trends/vendors/qwen)

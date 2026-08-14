---
title: 5 厂商横向对比
description: Claude / GPT / Kimi / GLM / Qwen 在性能基准、上下文、价格、部署、Tool Use 等 8 维度的横向对比
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
---

# 5 厂商横向对比

> 8 个维度、5 家厂商、一张速查表——**看完就能选型**。

## 一、模型矩阵对比

| 厂商 | 旗舰 | 中端 | 轻量 | 推理模型 | 开源 |
|------|------|------|------|----------|------|
| **Anthropic** | Opus 5 | Sonnet 5 | Haiku 4.5 | — | ❌ |
| **OpenAI** | GPT-5.6 Sol | GPT-5.6 Terra | GPT-5.6 Luna | o 系列 | 开源双轨 |
| **Moonshot** | Kimi K3 | Kimi K2.5 | — | K3（总是推理） | K2.5 / K3 开源 |
| **Zhipu** | GLM-5.2 | GLM-5.1 | GLM-4-Air | GLM-Z1 | GLM-5 全尺寸 |
| **Qwen** | Qwen3.8-Max | Qwen3.5 | 开源小尺寸 | — | 全尺寸 + 全模态 |

**结论**：OpenAI 推理最强（o-series），Qwen 开源最彻底，Anthropic Agent 最强。

## 二、性能基准对比（旗舰模型）

> ⚠️ 具体分数以各厂商官方发布为准（Anthropic / OpenAI 发布博客、中文厂商技术报告），下表只保留**定性结论**，不收录未经核实的数字。

| 厂商 | 英文基准（MMLU 等） | 中文基准（C-Eval 等） | 编码基准 |
|------|------|------|------|
| Anthropic | 领先 | — | 领先（Opus 5 / Sonnet 5） |
| OpenAI | 领先 | — | 领先（GPT-5.6 Sol / o 系列） |
| Moonshot | — | 领先 | 长上下文编码强（Kimi K3） |
| Zhipu | 中上 | 领先 | Agentic Coding 主推（GLM-5.2） |
| Qwen | 中上 | 领先 | 开源编码强（Qwen3.5） |

**结论**：英文基准 Claude/GPT 领先，中文基准 Kimi/Qwen/GLM 领先。**没有全能冠军，只有场景冠军**。

## 三、上下文窗口对比

| 厂商 | 默认 | 最大 | 长上下文技术 |
|------|------|------|-------------|
| Anthropic | 200K | 1M（Fable 5 beta） | RoPE 插值 + 滑动窗口 |
| OpenAI | 128K | 200K（o-series） | RoPE 插值 |
| Moonshot | 1M | 1M（K3） | LongRoPE 风格 |
| Zhipu | 128K | 128K | RoPE 插值 |
| Qwen | 1M | 1M | RoPE 插值 + 滑动窗口 |

**结论**：Kimi 2M 最长，Claude Fable 1M 次之，Qwen 1M 第三。**长文档选 Kimi/Qwen/Claude**。

## 四、价格对比（旗舰模型，每百万 token）

| 厂商 | Input | Output | 缓存读 | 备注 |
|------|-------|--------|--------|------|
| Anthropic | $15 | $75 | $1.50 | Prompt Caching 5min |
| OpenAI | $10 | $30 | — | 无原生缓存 |
| Moonshot | ¥12（~$1.7） | ¥36（~$5） | — | 中文场景性价比高 |
| Zhipu | ¥15（~$2.1） | ¥45（~$6.3） | — | 中文场景性价比高 |
| Qwen | ¥10（~$1.4） | ¥30（~$4.2） | — | 性价比最高 |

**结论**：中文场景 Kimi/GLM/Qwen 比 Claude/GPT 便宜 5-10x。**Claude Prompt Caching 对长 prompt 场景可省 70%**。

## 五、部署方式对比

| 厂商 | API | 开源权重 | 私有化 | 端侧 | 国产化 |
|------|-----|----------|--------|------|--------|
| Anthropic | ✅ | ❌ | Bedrock/Vertex | ❌ | ❌ |
| OpenAI | ✅ | GPT-OSS | Azure | ❌ | ❌ |
| Moonshot | ✅ | 部分 | Kimi 平台 | ❌ | ✅ |
| Zhipu | ✅ | 全尺寸 | MaaS | ✅ | ✅ |
| Qwen | ✅ | 全尺寸+全模态 | 阿里云 | ✅ | ✅ |

**结论**：国产化/私有化选 Qwen/GLM，海外企业选 Claude (Bedrock/Vertex) 或 GPT (Azure)。

## 六、Tool Use / Agent 能力对比

| 厂商 | Function Calling | Agent 框架 | Computer Use | 特色 |
|------|-----------------|------------|--------------|------|
| Anthropic | ✅ 原生 | Agent SDK + Claude Code | ✅ Beta | Agent 最完整 |
| OpenAI | ✅ 原生（行业首创） | Assistants API | ❌ | Code Interpreter |
| Moonshot | ✅ 原生 | — | ❌ | Deep Research |
| Zhipu | ✅ 原生 | AllTools | ❌ | 搜索+计算+绘图组合 |
| Qwen | ✅ 原生 | Qwen-Agent（开源） | ❌ | 全模态 Agent |

**结论**：Agent 能力 Claude 最完整（Computer Use + SDK），OpenAI Function Calling 是行业标准。

## 七、多模态对比

| 厂商 | 文本 | 图片 | 音频 | 视频 | 全模态 |
|------|------|------|------|------|--------|
| Anthropic | ✅ | ✅ | ❌ | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ✅ | ❌ | ❌ |
| Moonshot | ✅ | ✅ | ❌ | ✅（2M） | ❌ |
| Zhipu | ✅ | ✅ | ❌ | ❌ | ❌ |
| Qwen | ✅ | ✅ | ✅ | ✅ | ✅（Omni） |

**结论**：Qwen 全模态最完整（Omni），Claude 多模态最弱（只有文本+图片）。

## 八、许可证 + 商业可用性

| 厂商 | 许可证 | 商业可用 | 备注 |
|------|--------|----------|------|
| Anthropic | 闭源 | API 付费 | Bedrock/Vertex 企业 |
| OpenAI | 闭源 + Apache 2.0（OSS） | API 付费 / OSS 免费 | GPT-OSS Apache 2.0 |
| Moonshot | 部分开源 | API 付费 / 部分免费 | K2 基础权重 Apache 2.0 |
| Zhipu | Apache 2.0 | API 付费 / 开源免费 | 全尺寸开源 |
| Qwen | Apache 2.0 | API 付费 / 开源免费 | 全尺寸+全模态开源 |

**结论**：开源选 Qwen/GLM，闭源选 Claude/GPT，中间路线选 Kimi。

## 速查决策表

| 场景 | 首选 | 备选 | 理由 |
|------|------|------|------|
| **英文编码 + Agent** | Claude Sonnet 5 | GPT-5.6 Sol | Tool Use + Agent 最完整 |
| **中文长文档** | Kimi K3 | Qwen3.8-Max | 1M 上下文 + 文件解析 |
| **数学/代码推理** | OpenAI o3 | GLM-Z1 | RLVR 推理最强 |
| **本地/端侧部署** | Qwen 3-7B | GLM-4-Air | 全尺寸开源 + 端侧优化 |
| **企业合规（海外）** | Claude (Bedrock) | GPT (Azure) | 云厂商集成 |
| **企业合规（国内）** | Qwen (阿里云) | GLM (智谱云) | 国产化 + 私有化 |
| **多模态** | Qwen3.5（原生多模态） | GPT-5.6 Vision | 全模态最完整 |
| **极低成本** | Qwen 3-0.5B（端侧） | GPT-OSS 20B（自部署） | 免费 |

## 参考

- [技术架构总览](./architecture) — 4 大技术路线详解
- [5 厂商详情](./anthropic) · [openai](./openai) · [moonshot](./moonshot) · [zhipu](./zhipu) · [qwen](./qwen)
- [选型决策树](./selection-guide) — 按 6 维度选型

## 下一步

- 用决策表选型 → [选型决策树](./selection-guide)
- 深入某家厂商 → [Anthropic](./anthropic) / [OpenAI](./openai) / [Moonshot](./moonshot) / [Zhipu](./zhipu) / [Qwen](./qwen)

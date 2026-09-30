---
title: 7 厂商横向对比
description: Claude / GPT / Grok / Kimi / MiniMax / GLM / Qwen 七家主厂商在性能基准、上下文、价格、部署、Tool Use 等 8 维度的横向对比（基准表另含 DeepSeek 共 8 家）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: Anthropic 定价
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-09-30
    - name: OpenAI 定价
      url: https://openai.com/pricing
      accessedAt: 2026-09-30
    - name: Kimi 开放平台
      url: https://platform.moonshot.cn/docs
      accessedAt: 2026-09-30
    - name: 智谱 BigModel
      url: https://open.bigmodel.cn/
      accessedAt: 2026-09-30
    - name: DashScope 平台
      url: https://dashscope.aliyun.com/
      accessedAt: 2026-09-30
    - name: xAI 定价
      url: https://docs.x.ai/developers/pricing
      accessedAt: 2026-09-30
    - name: MiniMax 定价
      url: https://platform.minimax.io/docs/guides/pricing-paygo
      accessedAt: 2026-09-30
---

# 7 厂商横向对比

> 8 个维度、7 家厂商、一张速查表——**看完就能选型**。

## 一、模型矩阵对比

| 厂商 | 旗舰 | 中端 | 轻量 | 推理模型 | 开源 |
|------|------|------|------|----------|------|
| **Anthropic** | Opus 5.5 | Sonnet 5.5 | Haiku 4.5 | Fable 5.1 / Mythos 5.1（思考不可关） | ❌ |
| **OpenAI** | GPT-6 Astra | GPT-6.1 Sol | GPT-6 Luna | GPT-6 `reasoning.effort`（o 系列已让位） | 开源双轨（GPT-OSS） |
| **xAI** | Grok 4.7 | — | — | Grok 4.20-reasoning（1M） | ❌ |
| **Moonshot** | Kimi K3 | Kimi K2.6 | Kimi K2.7 Code（编程） | K3（`reasoning_effort`） | K3 权重已开源 |
| **MiniMax** | MiniMax-M3 | M2.7（上一代，仍可调用） | M3.1-Flash-Preview（仅 Token Plan） | M3（agentic） | 部分（`M3` / `M2.7` 自部署） |
| **Zhipu** | GLM-5.3 | GLM-5.3-Flash（原生多模态） | GLM-4.7-Flash（免费） | GLM-5.3（思考常开，三档 `effort`） | GLM-4 起全尺寸（Apache 2.0） |
| **Qwen** | Qwen3.8-Max（快照 `-0902`） | Qwen3.7-Plus | Qwen3.8-Flash | Qwen3.8-Max（思考模式） | 全尺寸 + 全模态 |

> ⚠️ **2026-09 换代与下线**：Anthropic 的 Opus 5 / Sonnet 5 已退居 legacy 档（5.5 接替）；OpenAI 主线已从 GPT-5.6 切到 GPT-6（5.6 系列为上一代，Sol 促销价至少到 2026-11-21）；xAI 4.7 与 4.6 同价同上下文，**4.20 是独立的深度推理产品线、不是更新的 4.7**；**Moonshot 的 K2.5 与 K2 全系已下线**（2026-08 起调用返回 404）；MiniMax 的 M2.7 已归入 Legacy；Qwen 旗舰未换代，但主版本会静默漂移，生产应显式钉 `-0902` 快照。

**结论**：OpenAI 推理最强（GPT-6 的 `effort` 档位，o 系列已让位），Qwen 开源最彻底，Anthropic Agent 最强，MiniMax 性价比最激进。

## 二、性能基准对比（旗舰模型）

> 数据来源：[Artificial Analysis Intelligence Score](https://artificialanalysis.ai/leaderboards/models)（**2026-08 采集的第三方口径**）。AA 分数是综合智能评分，涵盖推理、编码、数学、指令遵循等多维度。
>
> ⚠️ **本表型号是 2026-08 当时的旗舰，不是 2026-09 的现行旗舰**。档案页未收录新一代旗舰（Opus 5.5 / GPT-6 Astra / Grok 4.7 / MiniMax-M3 / DeepSeek V4.1-Flash）的 AA 分，故保留原型号以便对照，不要按本表判断"当前最强"。「价格/任务」是 AA 的美元口径，与后文各家官方 API 定价（且币种不统一）不可直接换算。

| 厂商 | 旗舰模型（2026-08 口径） | AA 智能分 | 价格/任务 | 速度 (tok/s) |
|------|---------|----------|----------|-------------|
| **Anthropic** | Claude Opus 5 (max) | **63** | $2.34 | 53 |
| **xAI** | Grok 4.6 (high) | **61** | $0.84 | 58 |
| **OpenAI** | GPT-5.6 Sol (max) | **61** | $1.23 | 65 |
| **Moonshot** | Kimi K3 (max) | **60** | $0.84 | 38 |
| **Zhipu** | GLM-5.3 (max) | **60** | $0.68 | 85 |
| **Qwen** | Qwen3.8-Max | **58** | $1.13 | 44 |
| **DeepSeek** | V4-Pro-0813 (max) | **53** | $0.25 | 74 |
| **MiniMax** | M2.7 | — | $0.30 | — |

**关键发现——后训练 Scaling 是当前最大杠杆**：

- **GLM-5.3 vs 5.2**：同基座，纯靠后训练——官方口径是内部 Z.ai Code Bench 较 5.2 提升 50%；本表的 AA 分 53 → 60 为第三方口径，**2026-09 官方文档已找不到该分数出处**（见 [Zhipu 档案页](/ai-trends/cn-vendors/zhipu/)）
- **V4-Pro-0813 vs V4-Pro**：同代后训练迭代，AA 从 45 → 53（+8 分，第三方口径，官方仅可确证 DeepSWE 62.7）
- **开源已逼近闭源**：GLM-5.3 / Kimi K3（60 分）距 Claude Opus 5（63 分）仅差 3 分
- **价格优势巨大**：GLM-5.3（$0.68/任务）是 Claude Opus 5（$2.34/任务）的 1/3.4（AA 美元口径；智谱官方 API 定价为人民币 ¥8 / ¥28）

**结论**：前训练拼参数的红利已基本吃完，**下一战场是 RL 基建 + 任务合成**。用同一个基座（5.2 / Qwen3.8-Max / Kimi K3），今天就能通过后训练复现顶级编程/Agent 能力。

## 三、上下文窗口对比

| 厂商 | 默认 | 最大 | 长上下文技术 |
|------|------|------|-------------|
| Anthropic | 1M（Opus 5.5 / Sonnet 5.5 / Fable 5.1） | 1M（Haiku 4.5 为 200K） | 位置编码未公开；4.7 及之后换用新分词器（同文本约多 30% token） |
| OpenAI | 1,050,000（GPT-6 Astra） | 最大输入 922K / 最大输出 128K | >272K 输入切长上下文档计价（input ×2、output ×1.5） |
| xAI | 500K（Grok 4.7 / 4.6） | 1M（4.20 三变体） | `reasoning_effort` 四档 + 长会话压缩 |
| Moonshot | 1M（K3，1,048,576） | 1M（K3） | KDA 混合线性注意力；K2-0905 的 2M 档已随 K2 下线 |
| MiniMax | 1M（`M3` / `M3.1-Flash-Preview`） | 1M | 官方未披露 |
| Zhipu | 1M（GLM-5.3 / 5.3-Flash） | 1M（GLM-4.7-Flash 为 200K） | `GLM-5.3-Flash` 为线性 + 稀疏注意力混合架构 |
| Qwen | 1M（Qwen3.8-Max，1,000,000） | 最大输出 131,072 | 官方未披露位置编码 |

**结论**：1M 已是全行业主流档（Claude / Kimi / Qwen / GLM-5.3 / MiniMax-M3），GPT-6 Astra 的 1.05M 与 xAI Grok 4.20 推理线 1M 略高。**长文档选 Claude / GPT / Kimi / Qwen / xAI**。

## 四、价格对比（旗舰模型，每百万 token）

| 厂商 | Input | Output | 缓存读 | 备注 |
|------|-------|--------|--------|------|
| Anthropic | $4（Opus 5.5） | $20 | $0.20 | Fable 5.1 $10/$50；Haiku 4.5 $1/$5 |
| OpenAI | $10（GPT-6 Astra） | $50 | $1.00 | 缓存写 $12.50 另计；6.1 Sol $2/$10；Luna $0.10/$0.50 |
| xAI | $2（Grok 4.7） | $6 | $0.50 | ≥200K prompt 时 $4/$12；4.20 线 1M 反而更便宜（$1.25/$2.50） |
| Moonshot | ¥20（K3，人民币） | ¥100 | ¥2 | 缓存命中价；缓存写入另计 5min ¥20 / 1h ¥40 |
| MiniMax | $0.30（`M3`，≤512K） | $1.20 | $0.06 | 输入 >512K 时翻倍；标注「永久 5 折」 |
| Zhipu | ¥8（GLM-5.3，人民币） | ¥28 | ¥2 | 5.2 同价；5.3-Flash 仅 ¥0.8/¥2.8 |
| Qwen | ¥12（Qwen3.8-Max） | ¥36 | ¥1.5 | 原价，不含优惠；新加坡地域 ¥14.988/¥44.965 |

> ⚠️ **币种不统一**：Moonshot（Kimi）、Zhipu（GLM）、Qwen 官方定价均为**人民币**，Anthropic / OpenAI / xAI / MiniMax 为**美元**。跨厂商比价必须先统一币种，不能直接比大小。K3 输出价 ¥100/MTok 约为 GLM-5.3（¥28）的 3.6 倍、Qwen3.8-Max（¥36）的 2.8 倍。

**结论**：按美元口径 MiniMax（`M3`）最低、GPT-6 Astra 最贵（$10/$50 高于上一代 GPT-5.6 Sol 的 $4/$20）；**成本敏感选 MiniMax `M3`，质量优先选 Claude Opus 5.5 或 GPT-6.1 Sol（$2/$10）**。

## 五、部署方式对比

| 厂商 | API | 开源权重 | 私有化 | 端侧 | 国产化 |
|------|-----|----------|--------|------|--------|
| Anthropic | ✅ | ❌ | Bedrock/Vertex/Foundry | ❌ | ❌ |
| OpenAI | ✅ | GPT-OSS 双轨 | Azure + Bedrock | ❌ | ❌ |
| xAI | ✅ | ❌ | 企业方案 | ❌ | ❌ |
| Moonshot | ✅ | K3 权重已开源 | Kimi 平台 | ❌ | ✅ |
| MiniMax | ✅ | 部分（`M3` / `M2.7` 自部署） | 企业方案 | ❌ | ✅ |
| Zhipu | ✅ | 全尺寸（GLM-4 起） | MaaS + Managed Agents | ✅ | ✅ |
| Qwen | ✅ | 全尺寸+全模态 | 阿里云百炼 | ✅ | ✅ |

**结论**：国产化/私有化选 Qwen/GLM，海外企业选 Claude (Bedrock/Vertex)、GPT (Azure，2026-06 起也可走 Bedrock) 或 xAI。

## 六、Tool Use / Agent 能力对比

| 厂商 | Function Calling | Agent 框架 | Computer Use | 特色 |
|------|-----------------|------------|--------------|------|
| Anthropic | ✅ 原生 | Agent SDK + Claude Code | ✅ 已 GA（2026-08-19） | Browser Use / Files / Skills 同批转正 |
| OpenAI | ✅ 原生（行业首创） | Agents API（2026-09 公测） | ✅（Agents API 支持） | ⚠️ Assistants API 已于 2026-08-26 关停 |
| xAI | ✅ 原生 | Grok Build / Grok Bot | — | Web/X Search 实时工具 |
| Moonshot | ✅ 原生 | Kimi 托管智能体（Beta） | — | Deep Research |
| MiniMax | ✅ 原生 | Agent Teams | — | 动态工具搜索 |
| Zhipu | ✅ 原生 | AllTools + Managed Agents | — | 搜索+计算+绘图组合 |
| Qwen | ✅ 原生 | Qwen-Agent（开源） | — | 全模态 Agent |

**结论**：Agent 能力 Claude 最完整（Computer Use + SDK），OpenAI Function Calling 是行业标准——但 Assistants API 已于 2026-08-26 关停，新集成走 Responses API + Agents API。

## 七、多模态对比

| 厂商 | 文本 | 图片 | 音频 | 视频 | 全模态 |
|------|------|------|------|------|--------|
| Anthropic | ✅ | ✅ | ❌ | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ✅ | ❌ | ❌ |
| xAI | ✅ | ✅ | ✅ | ✅（专用模型） | ❌ |
| Moonshot | ✅ | ✅（K3 原生） | ❌ | ✅（K3 / K2.6 视频理解） | ❌ |
| MiniMax | ✅ | ✅ | ✅ | ✅ | ✅（全模态矩阵） |
| Zhipu | ✅ | ✅（GLM-5.3-Flash 原生） | ❌ | ❌ | ❌ |
| Qwen | ✅ | ✅ | ✅ | ✅ | ✅（Omni） |

**结论**：Qwen / MiniMax 全模态最完整，Claude 多模态最弱（只有文本+图片）。DeepSeek 的 V4.1-Flash 已原生多模态（唯一支持视觉的在售档），但本表未列该厂商。

## 八、许可证 + 商业可用性

| 厂商 | 许可证 | 商业可用 | 备注 |
|------|--------|----------|------|
| Anthropic | 闭源 | API 付费 | Bedrock/Vertex 企业 |
| OpenAI | 闭源 + 开源双轨 | API 付费 / 开源免费 | 开源型号以官方为准（GPT-OSS 20B/120B） |
| xAI | 闭源 | API 付费 | X 订阅内置 |
| Moonshot | 部分开源 | API 付费 / 部分免费 | K3 权重已开源（K2 已下线） |
| MiniMax | 部分开源 | API 付费 / 部分免费 | 多模态全系自研 |
| Zhipu | Apache 2.0 | API 付费 / 开源免费 | 全尺寸开源 |
| Qwen | Apache 2.0 | API 付费 / 开源免费 | 全尺寸+全模态开源 |

**结论**：开源选 Qwen/GLM，闭源选 Claude/GPT，中间路线选 Kimi / MiniMax。

## 速查决策表

| 场景 | 首选 | 备选 | 理由 |
|------|------|------|------|
| **英文编码 + Agent** | Claude Sonnet 5.5 | GPT-6.1 Sol | Tool Use + Agent 最完整 |
| **中文长文档** | Kimi K3 | Qwen3.8-Max | 1M 上下文 + 文件解析 |
| **数学/代码推理** | GPT-6 Astra（`effort` 档） | GLM-5.3（思考常开） | 推理时计算；o 系列已让位 |
| **实时信息/社交数据** | xAI Grok 4.7 | — | X 生态 + Web/X Search |
| **本地/端侧部署** | Qwen 开源小尺寸 | GLM 开源权重 | 全尺寸开源 + 端侧优化 |
| **企业合规（海外）** | Claude (Bedrock) | GPT (Azure) | 云厂商集成 |
| **企业合规（国内）** | Qwen (阿里云) | GLM (智谱云) | 国产化 + 私有化 |
| **多模态** | Qwen3.8-Omni / MiniMax | GPT-6（Vision） | 全模态最完整 |
| **极低成本** | MiniMax `M3` | DeepSeek V4.1-Flash | `M3` $0.30/MTok input；V4.1-Flash 谷时 $0.15/MTok |
| **性价比旗舰** | GLM-5.3 / GLM-5.3-Flash | MiniMax `M3` | 5.3-Flash 输入 ¥0.8/MTok（1M 上下文 + 原生多模态） |

> ⚠️ 表内「极低成本」「性价比旗舰」两行按官方 API 标价，币种不同（MiniMax / DeepSeek 为美元，Zhipu 为人民币），跨厂商比价前先统一币种。AA 基准分见第二节，为 2026-08 第三方口径。

## 参考

- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape) — 4 大技术路线详解
- [7 厂商详情](/ai-trends/vendors/) · [Anthropic](/ai-trends/vendors/anthropic/) · [OpenAI](/ai-trends/vendors/openai/) · [xAI](/ai-trends/vendors/grok/) · [Moonshot](/ai-trends/cn-vendors/moonshot/) · [MiniMax](/ai-trends/cn-vendors/minimax/) · [Zhipu](/ai-trends/cn-vendors/zhipu/) · [Qwen](/ai-trends/cn-vendors/qwen/) · [DeepSeek](/ai-trends/cn-vendors/deepseek/)
- [模型选型决策树](./model-selection-guide) — 按 6 维度选型

## 下一步

- 用决策表选型 → [模型选型决策树](./model-selection-guide)
- 深入某家厂商 → [Anthropic](/ai-trends/vendors/anthropic/) / [OpenAI](/ai-trends/vendors/openai/) / [xAI](/ai-trends/vendors/grok/) / [Moonshot](/ai-trends/cn-vendors/moonshot/) / [MiniMax](/ai-trends/cn-vendors/minimax/) / [Zhipu](/ai-trends/cn-vendors/zhipu/) / [Qwen](/ai-trends/cn-vendors/qwen/)

## 如果你想

- 看某家的完整档案与 2026-09 动态 → [Anthropic · Claude 全系](/ai-trends/vendors/anthropic/) / [OpenAI · GPT 全系](/ai-trends/vendors/openai/) / [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看技术路线差异 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 看国内厂商全貌 → [国内厂商](/ai-trends/cn-vendors/)

---
title: 7 厂商横向对比
description: Claude / GPT / Grok / Kimi / MiniMax / GLM / Qwen 七家主厂商在性能基准、上下文、价格、部署、Tool Use 等 8 维度的横向对比（基准表另含 DeepSeek 共 8 家）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-08
verifiedWith:
  sources:
    - name: Anthropic 定价
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-10-08
    - name: Claude Haiku 5.5 发布博客
      url: https://www.anthropic.com/claude-haiku-5-5
      accessedAt: 2026-10-08
    - name: OpenAI 定价
      url: https://openai.com/pricing
      accessedAt: 2026-10-08
    - name: Artificial Analysis 智能指数（第三方转录）
      url: https://benchmarklist.com/benchmarks/artificial_analysis_intelligence_index
      accessedAt: 2026-10-08
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
      accessedAt: 2026-10-08
    - name: MiniMax 定价
      url: https://platform.minimax.io/docs/guides/pricing-paygo
      accessedAt: 2026-09-30
---

# 7 厂商横向对比

> 8 个维度、7 家厂商、一张速查表——**看完就能选型**。

## 一、模型矩阵对比

| 厂商 | 旗舰 | 中端 | 轻量 | 推理模型 | 开源 |
|------|------|------|------|----------|------|
| **Anthropic** | Opus 5.5 | Sonnet 5.5 | **Haiku 5.5**（$0.10 / $0.50） | Fable 5.1 / Mythos 5.1（思考不可关） | ❌ |
| **OpenAI** | GPT-6 Astra | GPT-6.1 Sol | GPT-6 Luna | GPT-6 `reasoning.effort`（o 系列已让位） | 开源双轨（GPT-OSS） |
| **xAI** | Grok 4.7 | — | — | Grok 4.20-reasoning（1M） | ❌ |
| **Moonshot** | Kimi K3 | Kimi K2.6 | Kimi K2.7 Code（编程） | K3（`reasoning_effort`） | K3 权重已开源 |
| **MiniMax** | MiniMax-M3 | M2.7（上一代，仍可调用） | M3.1-Flash-Preview（仅 Token Plan） | M3（agentic） | 部分（`M3` / `M2.7` 自部署） |
| **Zhipu** | GLM-5.3 | GLM-5.3-Flash（原生多模态） | GLM-4.7-Flash（免费） | GLM-5.3（思考常开，三档 `effort`） | GLM-4 起全尺寸（Apache 2.0） |
| **Qwen** | Qwen3.8-Max（快照 `-0902`） | Qwen3.7-Plus | Qwen3.8-Flash | Qwen3.8-Max（思考模式） | 全尺寸 + 全模态 |

> ⚠️ **2026-10 换代与下线**：**Claude Haiku 5.5 于 2026-10-07 发布**（$0.10 / $0.50，1M 上下文，首个支持 `effort` 档位的 Haiku），Anthropic 全系完成 5.x 换代；同日 Sonnet 5.5 缓存读降价 50%（$0.20 → $0.10 / MTok）。OpenAI 主线仍为 GPT-6（5.6 系列为上一代，Sol 促销价至少到 2026-11-21）；xAI **Grok 5 截至 2026-10-08 未发布**，现行旗舰仍是 9-21 发布的 Grok 4.7（$2 / $6）；**Moonshot 的 K2.5 与 K2 全系已下线**（2026-08 起调用返回 404）；MiniMax 的 M2.7 已归入 Legacy；Qwen 旗舰未换代，但主版本会静默漂移，生产应显式钉 `-0902` 快照。

**结论**：OpenAI 推理最强（GPT-6 的 `effort` 档位，o 系列已让位），Qwen 开源最彻底，Anthropic Agent 最强 + 轻量档刚被 Haiku 5.5 拉到 $0.10 档（与 GPT-6 Luna 同价），MiniMax 性价比最激进。

## 二、性能基准对比（旗舰模型）

> 数据来源：**Artificial Analysis Intelligence Index**（**2026-10-03 口径**）。该指数是综合智能评分，涵盖推理、编码、数学、指令遵循等多维度标准化评测。
>
> ⚠️ **采集方式说明**：本次未能直接抓取 [artificialanalysis.ai](https://artificialanalysis.ai/leaderboards/models) 原站，下表数值取自 4 个独立聚合站的转录（[BenchmarkList](https://benchmarklist.com/benchmarks/artificial_analysis_intelligence_index)、[Ctrl+Alt+Debrief](https://ctrlaltdebrief.com/tools/benchmarks/intelligence_index)、[ModelGrep](https://modelgrep.com/best/smartest/prism-ml)、[DataLearner](https://www.datalearner.com/leaderboards)），四源在 1 位小数口径上**完全一致**，可信度较高。
>
> ⚠️ **本表只保留智能分**。上一版表里的「价格/任务」与「速度」两列已删除——不同聚合站对同一型号的 tok/s 报数相差 2 倍以上（如 Claude Opus 5.5 有 103 与 270 两种口径），属于不可靠数据。价格请以**各家官方定价**为准，见本篇第四节。

| 厂商 | 旗舰模型（2026-10 口径） | AA 智能指数 | 强度分档（max / 最高档） |
|------|---------|----------|------|
| **Anthropic** | Claude Opus 5.5 | **57.6** | 全场第一 |
| **Anthropic** | Claude Sonnet 5.5 | **56.0** | 输入价仅 Opus 的一半 |
| **Anthropic** | Claude Fable 5.1 | **53.4** | 最贵，$10 / $50 |
| **OpenAI** | GPT-6 Astra | **52.7** | 全场最贵，$10 / $50 |
| *（Google）* | *Gemini 4 Argon* | *52.6* | *未收录进本表，仅作参照* |
| **OpenAI** | GPT-6.1 Sol | **51.8** | 近 Astra 性能、$2 / $10 |
| **Anthropic** | Claude Opus 5（上一代） | 50.8 | 已退居 legacy |
| **xAI** | Grok 4.7 | 46.4 | 距榜首 11 分 |
| **Qwen** | Qwen3.8-Max（`-0902`） | 45.4 | 开源阵营最高 |
| **Zhipu** | GLM-5.3 | 44.8 | Apache 2.0 |
| **Moonshot** | Kimi K3 | 43.6 | 权重已开源 |
| **Zhipu** | GLM-5.3-Flash | 41.8 | ¥0.8 / ¥2.8 |
| **DeepSeek** | V4.1-Flash | 39.5 | 未进前 13 |
| **MiniMax** | `M3` | 未进前 25 | 价格最低档 |

**关键发现——`effort` 档位比换模型更影响性价比**：

- **同一个模型、只降一档 effort，成本差 3 倍**。据第三方榜单口径，Claude Opus 5.5 在 `max` 档单任务成本 $5.98、`high` 档 $1.82，智能分只从 58 掉到 54。**大多数场景不需要常年开 `max`。**
- **反直觉点**：Sonnet 5.5 在 `max` 档的单任务成本（$7.62）**高于** Opus 5.5 的 `max` 档（$5.98），尽管 Sonnet 的每 token 单价只有 Opus 一半——因为 Sonnet 的 token 消耗更高。**比价不能只看单价。**
- **开源已逼近闭源**：Kimi K3（43.6）、GLM-5.3（44.8）距 Claude Opus 5.5（57.6）差约 13 分，但价格低一到两个数量级。
- **榜单之间会打架**：另一份 2026-10-02 的加权综合榜把 **GPT-6 Astra 排第 1（88.8）、Claude Opus 5.5 排第 2（87.8）**，与 AA 指数的排序相反——因为它把 Agent（22%）+ 编码（20%）合计 42% 的权重压在 agentic 维度上，且榜单前 15 名里有 6 个是**估算值**而非实测。**看榜先看口径和实测比例，别只看名次。**

**结论**：前训练拼参数的红利已基本吃完，**下一战场是 RL 基建 + 任务合成**。用同一个基座（GLM-5.2 / Qwen3.8-Max / Kimi K3），今天就能通过后训练复现顶级编程 / Agent 能力。

## 三、上下文窗口对比

| 厂商 | 默认 | 最大 | 长上下文技术 |
|------|------|------|-------------|
| Anthropic | 1M（Opus 5.5 / Sonnet 5.5 / Fable 5.1 / Haiku 5.5） | 1M | 位置编码未公开；4.7 及之后换用新分词器（同文本约多 30% token）；Haiku 5.5 首次把轻量档拉到 1M |
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
| Anthropic | $4（Opus 5.5） | $20 | $0.20 | Fable 5.1 $10/$50；**Haiku 5.5 $0.10/$0.50**（2026-10-07 发布）；Sonnet 5.5 缓存读 10-07 降至 $0.10 |
| OpenAI | $10（GPT-6 Astra） | $50 | $1.00 | 缓存写 $12.50 另计；6.1 Sol $2/$10；Luna $0.10/$0.50 |
| xAI | $2（Grok 4.7） | $6 | $0.50 | ≥200K prompt 时 $4/$12；4.20 线 1M 反而更便宜（$1.25/$2.50） |
| Moonshot | ¥20（K3，人民币） | ¥100 | ¥2 | 缓存命中价；缓存写入另计 5min ¥20 / 1h ¥40 |
| MiniMax | $0.30（`M3`，≤512K） | $1.20 | $0.06 | 输入 >512K 时翻倍；标注「永久 5 折」 |
| Zhipu | ¥8（GLM-5.3，人民币） | ¥28 | ¥2 | 5.2 同价；5.3-Flash 仅 ¥0.8/¥2.8 |
| Qwen | ¥12（Qwen3.8-Max） | ¥36 | ¥1.5 | 原价，不含优惠；新加坡地域 ¥14.988/¥44.965 |

> ⚠️ **币种不统一**：Moonshot（Kimi）、Zhipu（GLM）、Qwen 官方定价均为**人民币**，Anthropic / OpenAI / xAI / MiniMax 为**美元**。跨厂商比价必须先统一币种，不能直接比大小。K3 输出价 ¥100/MTok 约为 GLM-5.3（¥28）的 3.6 倍、Qwen3.8-Max（¥36）的 2.8 倍。

**结论**：按美元口径 Haiku 5.5（$0.10 / $0.50）与 GPT-6 Luna 同价并列最低、GPT-6 Astra 最贵（$10 / $50 高于上一代 GPT-5.6 Sol 的 $4 / $20）；**成本敏感选 Haiku 5.5 或 GPT-6 Luna，质量优先选 Claude Opus 5.5 或 GPT-6.1 Sol（$2 / $10）**。

> ⚠️ **长 prompt 加价门槛两家不一样**：Anthropic 在 **prompt > 100K** 时 Haiku 5.5 跳到 $0.50 / $2.50（5 倍）；OpenAI 在 **输入 > 272K** 时切长上下文档计价。也就是说同一笔长上下文负载，在 Anthropic 侧更早触发加价——**做长上下文成本预估时不能套用别家的阈值**。

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
| Anthropic | ✅ 原生 | Agent SDK + Claude Code | ✅ 已 GA（2026-08-19） | Browser Use / Files / Skills 同批转正；**Python / TS SDK 于 2026-10-07 加入 computer use + browser use（beta）** |
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
| **极低成本（API）** | Claude Haiku 5.5 / GPT-6 Luna | MiniMax `M3` / DeepSeek V4.1-Flash | Haiku 5.5 与 Luna 同为 $0.10/$0.50；`M3` $0.30/MTok input；V4.1-Flash 谷时 $0.15/MTok |
| **高并发子 agent** | Claude Haiku 5.5 | GPT-6 Luna | Haiku 5.5 首个支持 `effort`，官方明确定位 subagent / compaction / 分类场景 |
| **性价比旗舰** | GLM-5.3 / GLM-5.3-Flash | MiniMax `M3` | 5.3-Flash 输入 ¥0.8/MTok（1M 上下文 + 原生多模态） |

> ⚠️ 表内「极低成本」「性价比旗舰」两行按官方 API 标价，币种不同（Anthropic / OpenAI / xAI / MiniMax / DeepSeek 为美元，Moonshot / Zhipu 为人民币），跨厂商比价前先统一币种。AA 基准分见第二节，为 2026-10-03 第三方转录口径。

## 参考

- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape) — 4 大技术路线详解
- [7 厂商详情](/ai-trends/vendors/) · [Anthropic](/ai-trends/vendors/anthropic/) · [OpenAI](/ai-trends/vendors/openai/) · [xAI](/ai-trends/vendors/grok/) · [Moonshot](/ai-trends/cn-vendors/moonshot/) · [MiniMax](/ai-trends/cn-vendors/minimax/) · [Zhipu](/ai-trends/cn-vendors/zhipu/) · [Qwen](/ai-trends/cn-vendors/qwen/) · [DeepSeek](/ai-trends/cn-vendors/deepseek/)
- [模型选型决策树](./model-selection-guide) — 按 6 维度选型

## 下一步

- 用决策表选型 → [模型选型决策树](./model-selection-guide)
- 深入某家厂商 → [Anthropic](/ai-trends/vendors/anthropic/) / [OpenAI](/ai-trends/vendors/openai/) / [xAI](/ai-trends/vendors/grok/) / [Moonshot](/ai-trends/cn-vendors/moonshot/) / [MiniMax](/ai-trends/cn-vendors/minimax/) / [Zhipu](/ai-trends/cn-vendors/zhipu/) / [Qwen](/ai-trends/cn-vendors/qwen/)

## 如果你想

- 看某家的完整档案与 2026-10 动态 → [Anthropic · Claude 全系](/ai-trends/vendors/anthropic/) / [OpenAI · GPT 全系](/ai-trends/vendors/openai/) / [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看技术路线差异 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 看国内厂商全貌 → [国内厂商](/ai-trends/cn-vendors/)

---
title: DeepSeek
description: 开源降本标杆——V4-Pro / V4.1-Flash、R1 推理模型、技术品牌与开放蒸馏
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-10-08
verifiedWith:
  sources:
    - name: DeepSeek 官方
      url: https://api-docs.deepseek.com
      accessedAt: 2026-10-08
    - name: DeepSeek 官方模型与定价
      url: https://api-docs.deepseek.com/quick_start/pricing
      accessedAt: 2026-10-08
    - name: DeepSeek 官方 Change Log
      url: https://api-docs.deepseek.com/updates
      accessedAt: 2026-10-08
    - name: DeepSeek-R1 发布
      url: https://api-docs.deepseek.com/news/news250120
      accessedAt: 2026-10-08
    - name: deepseek-ai 官方 Hugging Face 组织页
      url: https://huggingface.co/deepseek-ai
      accessedAt: 2026-10-08
    - name: DeepSeek-V4.1-Flash 官方模型卡（含技术报告）
      url: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
      accessedAt: 2026-10-08
---

# DeepSeek

> **TL;DR**：开源界的「降本标杆」——V3 / R1 证明低成本也能训出前沿模型，2026 年已迭代到 V4-Pro / V4.1-Flash 双档（1M 上下文 + 峰谷定价 + 最大输出 384K）。

## 一、定位

DeepSeek 是中国开源大模型的技术品牌担当：**训练成本低 + 开放权重 + 开放蒸馏（MIT）**。它改变了整个行业对「开源推理模型能不能打」的预期。

## 二、模型线（截至 2026-10）

官方在售 API 模型只有两档（模型名 `deepseek-v4-pro` 与 `deepseek-flash`），**两档上下文均为 1M、最大输出均为 384K**（官方定价页，访问于 2026-10-08）：

| 模型 | 时间 | 定位 | 官方上下文 | AA 智能分（第三方） |
| --- | --- | --- | --- | --- |
| **V4.1-Flash** | 2026-09-10 发布 | 轻量快速档，**唯一支持视觉**（原生多模态） | 1M / 最大输出 384K | — |
| **V4-Pro-0813** | 2026-08-13 GA | 当前旗舰（后训练迭代） | 1M / 最大输出 384K | **53** |
| **V4-Pro**（1.6T） | 2026-04-24 上线 API | 旗舰，已被 0813 取代 | 1M | 45 |
| **V4-Flash** | 2026-07-31 | **已退役**，请求转发到 V4.1-Flash | — | 52 |
| **R1** | 2025-01-20 | 开源推理模型，对标 o1 系列 | — | — |
| **V3** | 2024-12-26 | 降本里程碑（十分之一训练成本） | — | — |

> ⚠️ 「AA 智能分」与「V4-Pro 的 1.6T 参数」为第三方 / 模型卡口径，本次（2026-10-08）未在 API 文档站复核，仅作参考。上下文长度、最大输出、模型版本、定价与基准分均取自官方页。

**两档的接口能力完全对齐**（官方定价页）：JSON 输出、Tool Calls、Responses API、Anthropic API、Chat Prefix Completion（Beta）均支持；FIM Completion（Beta）仅非思考模式；**差异只有一条——Vision 仅 Flash 档支持**。

**官方定价**（美元 / 每百万 token，格式为「谷时 / 峰时」）：

| 模型 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 并发上限 |
| --- | --- | --- | --- | --- |
| **V4.1-Flash** | 0.003 / 0.006 | 0.15 / 0.30 | 0.60 / 1.20 | 2500 |
| **V4-Pro-0813** | 0.022 / 0.044 | 0.66 / 1.32 | 1.98 / 3.96 | 500 |

> **峰谷定价**：谷时价为峰时价的一半。峰时为 UTC 周一至周五 01:00–04:00 与 06:00–10:00（不含中国法定节假日），其余时段全部按谷时计（含周末与节假日全天）。该机制自 2026-08-16 16:00 UTC 起生效。对能错峰跑的批量任务，这是实打实的成本优化点。

> **后训练杠杆**：V4-Pro 从初版到 0813 更新，AA 综合分从 45 提升到 53（第三方口径）。官方 Change Log 可确证的是 0813 的编码成绩——DeepSWE 达 **62.7**（7-31 版 V4-Flash 为 54.4），验证了后训练在编码 / Agent 任务上的巨大潜力。

## 三、关键事件

- **V3（2024-12-26）**：训练成本约为同代闭源的十分之一——「降本」信号，引发全球对训练效率的讨论
- **R1（2025-01-20）**：开源推理模型，MIT 许可，API 输出可用于微调和蒸馏——「推理平民化」
- **V4（2026-04-24）**：V4-Pro 与 V4-Flash 上线 API，同时提供 OpenAI 与 Anthropic 两种接口格式；旧模型名 `deepseek-chat` / `deepseek-reasoner` 于 2026-07-24 停用
- **V4.1-Flash（2026-09-10）**：新架构家族中最小的一档，原生多模态，随发布整体降价；**同日官方在 Hugging Face 放出 MIT 许可权重与《DeepSeek_V41_Tech_Report.pdf》**
- **V4 系列权重全面 MIT 开放**：`V4-Flash-0731`（2026-07-31）、`V4-Pro-0813`（2026-08-13）、`V4-Flash-Vision-Exp`（2026-08-31）、`V4.1-Flash`（2026-09-10）均在 `deepseek-ai` 组织页以 MIT 发布（访问于 2026-10-08）

## 四、特点

- **技术品牌最强**：开发者心智、网页端与 API 使用习惯是核心资产
- **开放蒸馏**：R1 起允许蒸馏，催生大量衍生模型
- **价格激进**：API 定价长期处于低位

## 五、适合 / 不适合

**适合**：开源私有化、推理任务、成本敏感场景、二次开发（可蒸馏）。

**不适合**：需要完整商业生态支持（客服、部署、合规套件）的企业——DeepSeek 重模型轻服务。

## 六、最新动态（2026-10）

**三条跟踪线**：

- **模型线**：V4 家族双档（V4-Pro 旗舰 / V4.1-Flash 轻量）。核心看「哪一档是当前旗舰、是否支持视觉、上下文长度」
- **价格线**：峰谷定价 + 随发布降价。核心看「输出单价」——输出通常是成本的真实大头
- **生态线**：DeepSeek Harness 与各家 Agent 框架的官方适配（Claude Code、Codex、OpenCode、OpenClaw、WorkBuddy 等）

**如何跟踪**：

1. **官方源**：[Change Log](https://api-docs.deepseek.com/updates)（版本与降价的第一手来源）、[模型与定价](https://api-docs.deepseek.com/quick_start/pricing)、[Hugging Face 组织页](https://huggingface.co/deepseek-ai)（开源权重与模型卡的第一手来源）
2. **更新节奏**：2026 年迭代明显加密——04-24 上线 V4、07-31 V4-Flash、08-13 V4-Pro GA、08-21 视觉实验版、09-10 V4.1-Flash，基本月级
3. **判断原则**：只信 Change Log。媒体报道的「即将发布」在 DeepSeek 这条线上基本等于不准

**截至 2026-10-08 的具体动态**：

> 📌 **本轮核实结论：2026-09-30 ~ 2026-10-08 之间官方 API 侧无新模型发布、无降价**。Change Log 最新条目仍是 2026-09-10 的 V4.1-Flash，定价页价格与上一轮完全一致。以下为已确证的历史条目。

| 日期 | 事件 | 意义 |
| --- | --- | --- |
| 2026-10-01 | **V4.1-Flash Hugging Face 仓库更新**（新增 chat template） | 权重侧维护动作，API 侧无变化 |
| 2026-09-10 | **DeepSeek-V4.1-Flash 发布** | 新架构家族最小一档，**原生多模态**；实测 GPQA Diamond 90.9、Terminal-Bench 2.1 90.6、DeepSWE v1.1 74.2、Codeforces 3471 |
| 2026-09-10 | **V4.1-Flash 权重 + 技术报告开源**（MIT） | 官方 HF 仓库同日上线；模型卡披露 552B 骨干参数、prefill 激活 8B / decode 16B、45T tokens 预训练、1M 上下文 |
| 2026-09-10 | **V4-Flash / V4-Flash-Vision-Exp 退役** | 旧模型名 `deepseek-v4-flash`、`deepseek-v4-flash-vision-exp` 暂时转发到 V4.1-Flash |
| 2026-09-10 | **V4-Pro 明确继续服务** | 官方声明 2026-09-14 后 V4-Pro API 继续提供，计费方式不变 |
| 2026-09-10 | **随 V4.1-Flash 整体降价** | 见上表官方定价 |
| 2026-08-21 | V4-Flash-Vision-Exp 实验版 | 多模态 Agent 能力官方称接近 Opus-4.8，后于 09-10 被 V4.1-Flash 取代 |
| 2026-08-13 | **V4-Pro GA** | APP / Web / API 三端同步；DeepSWE 62.7；原生支持 OpenAI Responses API（适配 Codex）；思考强度新增 low / high / max 三档 |
| 2026-08-16 | **峰谷定价生效** | 谷时价为峰时价一半 |
| 2026-04-24 | V4 上线 API | 旧模型名 `deepseek-chat` / `deepseek-reasoner` 于 2026-07-24 停用 |

> 📌 **怎么用这条线**：V4-Pro 与 V4.1-Flash 的输出价差约 3.3 倍，但轻量档已经能吃下视觉与多数 Agent 任务。**默认从 V4.1-Flash 起步，确有必要再上 V4-Pro**，是当前性价比最高的组合。V4-Pro 不支持视觉，需要多模态时只能走 V4.1-Flash。

> ✅ **开源已确证（2026-10-08 更正上一轮结论）**：上一轮只核实了官方 API 文档站，Change Log 确实只记录 API 侧版本，因此当时标注「未列出 V4 系列权重的开源发布」。**本轮补充核实 Hugging Face 官方组织页后可以确认：`V4-Flash-0731`、`V4-Pro-0813`、`V4-Flash-Vision-Exp`、`V4.1-Flash` 的权重均已在 `deepseek-ai` 组织下以 MIT 许可发布，V4.1-Flash 还附带技术报告 PDF。** 私有化部署可直接取官方权重。

## 参考

- [DeepSeek 官方 API 文档](https://api-docs.deepseek.com)（访问于 2026-10-08）
- [DeepSeek 官方 Change Log](https://api-docs.deepseek.com/updates)（访问于 2026-10-08）
- [DeepSeek 官方模型与定价](https://api-docs.deepseek.com/quick_start/pricing)（访问于 2026-10-08）
- [R1 发布公告](https://api-docs.deepseek.com/news/news250120)（访问于 2026-10-08）
- [deepseek-ai 官方 Hugging Face 组织页](https://huggingface.co/deepseek-ai)（访问于 2026-10-08）
- [DeepSeek-V4.1-Flash 官方模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)（访问于 2026-10-08，MIT）

## 下一步

- 看总览 → [国内厂商](/ai-trends/cn-vendors/)
- 对比七家 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)

## 如果你想

- 看开源生态 → [开源项目推荐](/ai-trends/research-highlights/open-source)

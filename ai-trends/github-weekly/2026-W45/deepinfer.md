---
title: 'deepseek-ai/DeepInfer：批量不变推理——Agent 场景要的是可复现'
description: DeepInfer 深度解读——DeepSeek 生产级推理框架开源，batch-invariant inference、deterministic sampling、structured outputs 与置信度调度验证，以及 Agent 场景为什么必须要确定性
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-11-02
---

# deepseek-ai/DeepInfer：批量不变推理——Agent 场景要的是可复现

> **TL;DR**：24,861 star、**存活 16 天**、Apache-2.0。DeepSeek 把**驱动自家生产服务的推理框架**开源了，README 写得很直白：「DeepInfer is the high-performance inference framework that powers DeepSeek's large-scale production services」。但对做 Agent 平台的人来说，**最该看的不是吞吐，是那三个「确定性」开关：batch-invariant inference、deterministic sampling、structured outputs**——**Agent 的缓存、回归测试和合规审计，全都建立在这三件事上。**

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ 推理基础设施 ｜ 本周涨星 未进周榜 ｜ 总 star 24,861（存活 16 天）

## 是什么

[deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) 是 DeepSeek 高性能、大规模推理框架的开源版本，提供「**大规模服务所需的核心能力**」。目前支持的模型是 **DeepSeek-V4.1-Flash**（默认 checkpoint 为 `deepseek-ai/DeepSeek-V4.1-Flash-1017`）。

**关键前提要先说清楚**：README 明确写了，**完整推理服务所需的三样东西不在本次发布范围内**——**KV cache 系统、VE / Prefill / Decode 分离（README 说大部分引擎功能其实已经实现）、以及 prefill 与 decode 在数据并行副本之间的负载均衡**。**所以开源出来的是「引擎」，不是「服务」。**

## 技术亮点

**第一，batch-invariant inference 是给 Agent 场景准备的开关。** `DEEPINFER_BATCH_INVARIANT=1`（仅 NVIDIA）保证**模型结果在不同 batch 组成下保持一致**。这条能力对传统在线服务并不重要（每个请求独立算就行），但对 Agent 极其关键：

- **上下文缓存**要求同样的 prompt + 前缀在任何时候都得到同样的续写，否则缓存命中率和输出稳定性都会崩。
- **回归测试**要求同一个用例跑两次结果一致，否则 Agent 的行为无法被断言。
- **合规审计**要求可复现，否则「同样的输入为什么给出不同的输出」无法解释。

**第二，deterministic sampling 在 batch-invariant 之上再加一层确定性。** 设置 `DEEPINFER_BATCH_INVARIANT=1 DEEPINFER_ENABLE_MTP_VARLEN=0`，并给 `SamplingParams` 传固定的 `seq_seed`，即可在相同输入 token 和采样参数下产生**完全相同的输出**。

**第三，structured outputs 是原生能力，不是外挂。** 通过 `so_args={"schema_type": ..., "schema": ...}` 传给 `SamplingParams`，可以**用正则、JSON Schema 或 EBNF 语法约束生成**。这意味着 Agent 的工具调用输出可以直接被约束成合法 JSON，**不需要在下游再做一层解析和重试**。

**第四，DSpark 用置信度调度验证。** `DEEPINFER_ENABLE_MTP_VARLEN=1` 开启草稿 token 加速解码，用置信度估计来**调度验证**；`DEEPINFER_USE_NEXTN_DECODE` 控制最大草稿长度（默认 5）。**「用置信度决定要不要验证」比「固定多跑几步」更省算力**，这是把推理成本和输出质量挂钩的典型做法。

**第五，并行策略覆盖了主流 MoE 部署形态。** Attention DP / balanced CP、**MoE EP + EPLB**（专家并行 + 专家负载均衡）、decoder 的 SWA bounded replay（`DEEPINFER_YOCO_PREFILL_TRUNCATION_MODE=compact`，保留 140 个 token 后缀，覆盖 SWA 窗口加最大回退长度）。

**第六，硬件覆盖两家。** **NVIDIA SM100 GPU** 和 **华为昇腾 950 NPU**——**同一套框架双栈支持**，这在开源推理框架里不常见。

**第七，异步调度默认开启。** CPU 端的 batch 调度与设备执行重叠，README 说「zero-overhead batch scheduler」。另外还有异步调度、SWA 有界重放等一整排工程开关。

## 后续发展建议

**这份开源对内部平台的直接价值是：它把「Agent 需要确定性推理」这件事从口号变成了可配置的开关。** 四个判断：

- **如果内部平台要做任何形式的上下文缓存，先确认推理侧支持 batch-invariant，否则缓存的正确性无法保证。** 这是一条容易被忽略的依赖：**缓存命中率提升 30% 的诱惑很大，但如果同样 prompt 在不同 batch 下输出不同，缓存就会引入不确定性**。**建议把「同一 prompt 跨 batch 输出是否一致」列入内部模型服务的验收项。**
- **deterministic sampling 应当是内部 Agent 评测环境的默认配置。** 在做 harness 调优（见上期 `harness2` 的 Propose–Probe–Compose）时，**信号必须可复现**——否则「这次比上次好」可能只是采样随机性。**建议评测环境统一开启确定性采样并固定 `seq_seed`。**
- **structured outputs 应该被当成 Agent 工具调用的基础契约来推广。** 如果模型侧能保证输出符合 JSON Schema，**工具调用的解析层就可以从「正则抠 + 失败重试」变成「schema 校验 + 一次失败」**。这会直接改善 Agent 的成功率。**但要注意：这依赖所选模型和推理框架都支持，不能假设所有接入的模型都有**——内部平台应该把「是否支持结构化输出」做成模型接入时的一项登记。
- **开源的是引擎不是服务，这决定了它能怎么用。** README 明确说 KV cache 和负载均衡不在本次发布内，而**这两样恰恰是最难自己补齐的部分**。**建议把 DeepInfer 当作「内核参考实现」而不是「可直接上线的服务」**——它的价值在于让你看清 DeepSeek 生产环境的推理栈长什么样，尤其是 DSpark 和置信度调度这类优化思路。

**风险与局限**：**它不是一个能立刻装上就跑的服务**，README 自己列了三项缺失能力。构建门槛不低：**Linux、GCC ≥ 13.0、Python 3.12、CUDA 13（NVIDIA）或 CANN 9.2（昇腾）**，且必须先建空的 Python 3.12 环境再 `./build.sh`。**昇腾 950 的支持对国内部署环境是好消息**。**没有 release**（只能跟 git 走），229 个 open issue 相对 24,861 star（0.9%），但项目才 16 天、最后 push 停在 2026-10-26（一周前），**相比同期的 `dsh-superagent-prototype`（昨天还在 push），维护活跃度有差距**。性能数字只有两张 Pareto 图（prefill 在 4 张 SM100、decode 在 64 张 SM100 上测得，**均在单个 scale-up 域内**），**没有给出横向对比基线**——不要拿它和 vLLM / SGLang 的数字直接比。

## 下一步

- 想看 DeepSeek 同周开源的 Agent 运行时那一侧 → [dsh-superagent 深读](./dsh-superagent.md)
- 想看 harness 优化为什么需要可复现的推理 → [2026-W44 harness2 深读](../2026-W44/harness2.md)

## 如果你想

- 想看模型选型怎么做 → [模型选型决策树](../../model-selection/model-selection-guide.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)

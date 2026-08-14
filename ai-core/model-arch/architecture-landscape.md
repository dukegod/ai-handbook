---
title: 跨厂商架构路线
description: 5 家主流大模型的技术路线——dense vs MoE / 长上下文实现 / RL 训练方法 / 推理优化
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-11
verifiedWith:
  sources:
    - name: Anthropic Constitutional AI 论文
      url: https://www.anthropic.com/research/constitutional-ai
      accessedAt: 2026-08-11
    - name: DeepSeek GRPO 论文
      url: https://arxiv.org/abs/2402.03300
      accessedAt: 2026-08-11
    - name: Moonshot Kimi 技术报告
      url: https://moonshotai.github.io/Kimi-K2/
      accessedAt: 2026-08-11
    - name: Zhipu GLM 技术报告
      url: https://github.com/THUDM/GLM-4
      accessedAt: 2026-08-11
    - name: Qwen3 技术报告
      url: https://qwenlm.github.io/blog/qwen3/
      accessedAt: 2026-08-11
---

# 跨厂商架构路线

> 跨 5 家厂商的 4 大技术路线总览——这一页负责厂商路线地图，具体机制见 Dense vs MoE、长上下文技术和多模态架构。

## 一句话总览

5 家厂商的旗舰模型在 4 大路线上的选择趋同：**dense 已退场、MoE 成主流；长上下文走 RoPE 扩展；RL 训练从 RLHF 演进到 RLVR；推理优化堆叠 5 层**。下表是 4 路线的速查，详细论证见后续 4 节。

## 一、Transformer 架构演进

| 阶段 | 关键变化 | 代表模型 |
| --- | --- | --- |
| Encoder-Decoder | 编码-解码分离 | T5 / BART |
| Decoder-only | 统一生成式预训练 | GPT-3 / LLaMA 1 |
| Decoder-only + MoE | 稀疏激活的专家层 | Mixtral / DeepSeek-V3 / Kimi K2 |
| Decoder-only + 原生多模态 | 视觉/音频 token 化统一 | GPT-4o / Claude 3.5+ / Qwen-VL |

2026 年的主流选择是**第三/四阶段**——纯文本走 MoE，多模态走"token 化统一"。GLM-5 / Qwen3.5 / Kimi K3 / GPT-5.6 都在 MoE 路径上；Claude 是少数仍坚持 dense（或极小专家数）的厂商。

## 二、**dense vs MoE** 路线对比

**核心权衡**：

- **dense 模型**：每次推理激活全部参数，训练稳定但推理贵
- **MoE（Mixture of Experts）**：把 FFN 拆成 N 个专家，每次只激活 top-k 个（如 8/384），推理省但路由有负载不均衡问题

**5 家路线**：

| 厂商 | 模型 | 架构 | 专家数 | 激活数 |
| --- | --- | --- | --- | --- |
| Anthropic | Claude Opus 4.8 | dense（推测） | — | 全参 |
| OpenAI | GPT-5 | MoE（推测） | 未公开 | 未公开 |
| Moonshot | Kimi K2（历史） | MoE | 384 | 8 |
| Zhipu | GLM-4 / GLM-5 | MoE | 未公开 | 未公开 |
| Qwen | Qwen3.8-Max | MoE | 未公开 | 未公开 |

MoE 的**工程红利**：相同训练成本下参数总量可以做得更大；相同推理成本下性能可以追平 dense 大模型。**Kimi K2（2025 年）曾是公开最激进的 MoE 设计**——384 专家，激活 8，路由用 shared expert + routed expert 双轨。

### 2.1 MoE 路由细节

每个 token 通过 router 网络算出对所有专家的偏好分数（softmax 后），**取 top-k 个专家加权求和**作为该 token 的 FFN 输出。关键设计有 3 层：
- **辅助损失**（load balancing loss）—— 惩罚"全选某几个专家"的不均衡，让专家利用率接近 1/N
- **Shared vs Routed 双轨**——Kimi K2 / DeepSeek-V3 都加一个**始终激活**的 shared expert（学通用知识），剩下的 routed expert 才参与 top-k 路由
- **专家容量因子**（capacity factor）—— 每个专家最多处理的 token 数 = 总 token × (1/N) × capacity；超过就丢弃（drop token）

## 三、**长上下文** 4 种实现

| 路径 | 原理 | 代表 |
| --- | --- | --- |
| **RoPE 位置插值** | 旋转位置编码的频率缩放，外推到 200K+ | Claude / Kimi / Qwen |
| **滑动窗口注意力** | 每层只看局部窗口，长距离靠层数堆 | Mistral（早期） |
| **状态空间模型** | 替代注意力的线性复杂度方案 | Mamba / Hyena（实验） |
| **检索增强（RAG）** | 不靠模型，靠外挂检索 | 所有厂商都做 |

2026 主流是**RoPE 扩展 + 滑动窗口混合**——Claude 已稳定 200K、Kimi 到 2M、Qwen 3 已 1M。状态空间模型在实验中未成为主流。RAG 不算"模型能力"但**是行业落地不可缺的一环**。

### 3.1 RoPE 与位置扩展

**RoPE（Rotary Position Embedding）** 把每个位置编码成"复数相位的旋转"——`q_m^T R(m-n) k_n` 的内积天然带相对位置。**扩展到 200K+ 需做位置插值**：
- **PI（Position Interpolation）**——线性缩放频率（θ → θ/scale），简单但损失高频位置精度
- **LongRoPE**（Microsoft 2024）——搜索每个维度最优缩放因子，**Kimi 2M 用了类似思路**
- **YaRN**（Nous Research 2023）——结合 NTK-aware 插值 + 注意力 sink，**Claude 200K 推测用此**
- **滑动窗口 + 全局 attention 混合**——Mistral / Qwen 做法：局部层用滑动窗口（4K-8K 窗口），少数层用全 attention，**节省 KV cache 又保留长程依赖**

## 四、**RL 训练方法** 演进

| 方法 | 核心思想 | 代表 |
| --- | --- | --- |
| **RLHF** | 人类偏好排序 + PPO 训练 reward model | Claude 2 / GPT-3.5 / 早期 |
| **DPO / IPO** | 直接用偏好数据优化策略，去掉 reward model | LLaMA 3 / Mistral |
| **RLAIF** | 用 AI 而非人类做偏好标注（Constitutional AI） | Claude 全系 |
| **GRPO** | Group Relative Policy Optimization，去掉 critic | DeepSeek / GLM |
| **RLVR** | Reinforcement Learning with Verifiable Rewards | OpenAI o-series / Kimi K2 Thinking |

**当前行业共识**：通用对话走 RLAIF / DPO；推理模型走 RLVR（可验证奖励）。**Kimi K2 Thinking / OpenAI o-series 是 RLVR 标志**——它在数学/代码/逻辑题上用规则验证（答案对错）训练，效果超过"人类偏好"。

### 4.1 损失函数演进

- **PPO（RLHF 基础）**——训练 reward model + value function，用 PPO 优化策略。**问题**：4 个模型（policy / ref / reward / value）训起来不稳
- **DPO**——直接用偏好对 `(y_w, y_l)` 优化策略，**去掉 reward model**。损失函数：`log σ(β · log(π(y_w)/π_ref(y_w)) - β · log(π(y_l)/π_ref(y_l)))`
- **GRPO（DeepSeek 2024）**——**组内相对优势**取代 critic：同一 prompt 采样 N 个回答，**用组内奖励的归一化分数**当 advantage。**省一半显存**
- **RLVR**——verifier 替代人类偏好：数学题答案对错、代码题单测通过率，**完全可程序验证**。OpenAI o-series 推理能力飞跃的核心

## 五、**推理优化** 5 层

| 层 | 技术 | 适用 |
| --- | --- | --- |
| **量化** | INT8 / INT4 / FP8 / 二值化 | 显存紧张 / 端侧 |
| **KV cache 优化** | PagedAttention（vLLM）/ FlashAttention | 长上下文 / 高并发 |
| **Speculative decoding** | 小模型先草拟，大模型批量验证 | 推理延迟敏感 |
| **批处理** | Continuous batching | 高吞吐服务 |
| **端侧部署** | 模型量化 + 本地 runtime（llama.cpp / MLX） | 隐私 / 离线 |

推理优化是**叠加而非替代**——Claude API 后端同时跑 FlashAttention + PagedAttention + Speculative decoding + Continuous batching。端侧部署（Qwen 2.5 / GLM-4-Air）是 Qwen 和 GLM 的强项（开源权重 + 1.5B/7B 小模型），Claude 和 GPT 闭源不参与。

## 六、**多模态融合** 3 路径

| 路径 | 原理 | 代表 |
| --- | --- | --- |
| **原生多模态** | 视觉/音频在 pretrain 阶段 token 化统一 | GPT-4o / Claude 3.5+ / Gemini |
| **适配器** | 文本主干 + 视觉/音频 adapter 微调 | LLaVA / Qwen-VL / CogVLM |
| **混合专家** | 不同模态走不同 expert 路由 | GLM-4V（推测） |

2026 主流是**适配器路径**（开放权重标配）+ **原生多模态**（闭源旗舰）。混合专家还偏实验。

## 关键洞察

- **MoE 是 2026 主流**，dense 只剩 Claude 等少数厂商坚持（推测）
- **RL 训练范式转向 RLVR**——可验证奖励（数学/代码）让小模型能"自学"推理
- **开源 vs 闭源差距在缩小**——Qwen3.8-Max / GLM-5 在基准上追平 GPT-5.6 / Claude Opus 5
- **中文厂商的长上下文已超 1M**——Kimi 2M、Qwen 1M，Claude 200K 反而显得保守

## 七、2026 H2 趋势预测

4 个值得关注的演进方向：

1. **Test-time scaling（推理时算力堆叠）**——OpenAI o-series / Kimi K2 Thinking 已经验证"多花时间想=准确率提升"。2026 H2 会有更多模型加 thinking mode
2. **Agentic reasoning（推理 + 工具混合）**——Claude Computer Use / Kimi K2 Thinking 路线，**把推理过程外化成工具调用**让模型能"边想边查"
3. **Sparse attention（稀疏注意力）**——DeepSeek 2024 提出 NSA（Native Sparse Attention），**O(n) 复杂度替代 O(n²)**，长上下文推理成本砍半
4. **Multimodal long-context**——Fable 1M + GPT-5 多模态整合，**长视频理解 + 长文档问答**会成 2026 H2 重点

**预测**：2026 H2 主流厂商都会发"o-series 风格的 thinking 模式" + 1M+ 上下文 + 视频模态。开源侧 Qwen / GLM 会跟进。

## 参考

- [5 厂商档案](/ai-trends/vendors/) · [Anthropic](/ai-trends/vendors/anthropic) · [OpenAI](/ai-trends/vendors/openai) · [Moonshot](/ai-trends/vendors/moonshot) · [Zhipu](/ai-trends/vendors/zhipu) · [Qwen](/ai-trends/vendors/qwen)
- [横向对比表](/reference/model-comparison) —— 8 维度量化对比
- [模型选型决策树](/reference/model-selection-guide) —— 架构选择映射到业务场景
- [Anthropic · Constitutional AI](https://www.anthropic.com/research/constitutional-ai)
- [DeepSeek · GRPO 论文](https://arxiv.org/abs/2402.03300)
- [Moonshot · Kimi K2 技术报告](https://moonshotai.github.io/Kimi-K2/)
- [Zhipu · GLM-4 技术报告](https://github.com/THUDM/GLM-4)
- [Qwen3 技术报告](https://qwenlm.github.io/blog/qwen3/)

## 下一步

- 看具体厂商细节 → [厂商档案](/ai-trends/vendors/)
- 把架构选型映射到业务 → [模型选型决策树](/reference/model-selection-guide)

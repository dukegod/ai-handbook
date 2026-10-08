---
title: 字节豆包
description: '消费入口第一——Doubao Seed 2.1（Pro / Lite / Turbo）、火山方舟生态、流量分发优势'
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-10-08
verifiedWith:
  sources:
    - name: 火山方舟 · 模型列表（页脚标注最近更新 2026-09-28）
      url: https://docs.volcengine.com/docs/ark/model-list?lang=zh
      accessedAt: 2026-10-08
    - name: 火山方舟 · 模型价格（页脚标注最近更新 2026-10-08）
      url: https://docs.volcengine.com/docs/ark/model-pricing?lang=zh
      accessedAt: 2026-10-08
    - name: ByteDance Seed 官方 Seed2.1 模型页
      url: https://seed.bytedance.com/en/seed2_1
      accessedAt: 2026-10-08
    - name: ByteDance Seed 官方博客 · Seed2.1 Officially Released（2026-06-23）
      url: https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity
      accessedAt: 2026-10-08
    - name: ByteDance-Seed 官方 Hugging Face 组织页
      url: https://huggingface.co/ByteDance-Seed
      accessedAt: 2026-10-08
---

# 字节豆包

> **TL;DR**：国内消费级 AI 入口第一（2025-08 反超 DeepSeek）——赢在抖音 / 剪映 / 火山引擎的分发体系，而不是模型声量。

## 一、定位

字节的 AI 策略是**全链路商业闭环**：消费 App 入口（豆包）+ 企业 API（火山引擎）+ 云基础设施 + 多模态矩阵。豆包是当前国内 AIGC 应用用户规模第一的产品。

## 二、模型线（截至 2026-10）

火山方舟「模型列表」页把文本生成模型分成「推荐模型」与「往期模型」两块（访问于 2026-10-08）：

| 模型 ID | 定位 | 上下文窗口 | 官方说明 |
| --- | --- | --- | --- |
| **Doubao Seed Evolving** | 快速迭代模型（Seed 最新 Coding / Agent 模型，周级迭代） | 1024k | 深度思考 + 多模态理解 + GUI 任务处理 |
| **Doubao Seed 2.1 Pro**（`doubao-seed-2-1-pro-260915`） | 旗舰档 | 1024k | 同上，最大回答 256k / 最大思维链 256k |
| **Doubao Seed 2.1 Lite**（`doubao-seed-2-1-lite-260915`） | 主力档，高并发 | 1024k | 同样 1024k 上下文，限流放宽到 RPM 30000 / TPM 5000000 |
| **Doubao Seed 2.1 Turbo**（`doubao-seed-2-1-turbo-260628`） | 加速档 | 256k | 上下文档位更低 |
| ~~Doubao Seed 2.0 Pro / Lite / Mini~~ | **上一代，多个 ID 已标「即将下线」** | 256k | `doubao-seed-2-0-pro-260215`、`-lite-260215`、`-mini-260215` 等 |

> 📌 **产品线已从 Seed 2.0 推进到 Seed 2.1**。Seed 官方博客（2026-06-23）与模型页均把当前主线写作 **Seed2.1**，并说明该家族提供 **Pro 与 Turbo 两种尺寸**；火山方舟侧在 Pro / Turbo 之外还多一个 **Lite** 档（该 Lite 未出现在 Seed 官网的「两种尺寸」表述中）。

**官方对 Seed2.1 的定位**（引自 ByteDance Seed 官方博客，2026-06-23）：新一代面向真实生产力的 agent 模型，强调三件事——更可靠的通用 agent 能力（跨工具、跨环境的多步交付）、更稳定的端到端编码交付、更强的多模态与基础能力。官方明确「评估优先看真实工作流表现，而非单看静态基准分」。

> ⚠️ **开源线与闭源线的分工未变**：字节的公开权重主线仍是 Seed-OSS。官方 Hugging Face 组织页截至 2026-10-08 **没有新的 Seed-OSS LLM 权重**——该组织最近一次模型更新是 2026-07-03 的 `PAR`（研究向），通用对话 / agent 基座权重仍停在 2025-08 的 `Seed-OSS-36B`。2026 年的公开动作集中在研究模型与专项模型（记忆、对齐、图像、代码）。

## 三、关键事实

- **消费入口第一**：2025-08 反超 DeepSeek 后稳居国内 AI 应用第一；2026-02 用户规模 2.27 亿，领先 DeepSeek 近 1 亿（QuestMobile，经新浪科技转述，第三方口径）
- **流量分发**：优势来自抖音 / 剪映 / 火山引擎，不是论坛声量
- **模型商业化**：低价 API + 火山引擎生态
- **双轨策略**：闭源打消费（豆包 / Seed2.1），开源保开发者（Seed-OSS）

## 四、特点

- **分发为王**：豆包强在触达，不是基准分数
- **双轨策略**：闭源打消费，开源保开发者
- **火山引擎**：企业侧接入与算力输出
- **模型 ID 按日期滚动**：`260915` / `260628` 这类后缀就是快照版本，生产环境需要钉具体 ID

## 五、适合 / 不适合

**适合**：消费级应用、低价大规模 API 调用、字节生态内集成。

**不适合**：开发者生态导向的选型（开源权重不如 Qwen / DeepSeek 完整）、需要技术品牌背书的场景。

## 六、价格（截至 2026-10，火山方舟在线推理常规档，人民币 / 百万 Tokens）

| 模型 | 输入（非音频） | 输入（音频） | 缓存存储（/小时） | 缓存命中 | 输出 |
| --- | --- | --- | --- | --- | --- |
| Doubao Seed Evolving | ¥6.00 | — | ¥0.017 | ¥1.20 | ¥30.00 |
| Doubao Seed 2.1 Pro | ¥6.00 | — | ¥0.017 | ¥1.20 | ¥30.00 |
| Doubao Seed 2.1 Lite | ¥0.80 | ¥12.00 | ¥0.017 | ¥0.16 | ¥2.70 |
| Doubao Seed 2.1 Turbo | ¥3.00 | — | ¥0.017 | ¥0.60 | ¥15.00 |

**其他推理档位**（同页列出，同样按 2.1 系列计价）：

- **低延迟档**：Lite 输入 ¥1.60 / 输出 ¥5.40；Turbo 输入 ¥6.00 / 输出 ¥30.00
- **低优档 / 批量推理**：Pro 输入 ¥3.00 / 输出 ¥15.00；Lite 输入 ¥0.40 / 输出 ¥1.35；Turbo 输入 ¥1.50 / 输出 ¥7.50

**价格说明**：

- 2.0 系列按输入长度分三段计价（[0,32] / (32,128] / (128,256] 千 token），2.1 系列统一按输入长度上限计价，无分段
- Lite 与 Pro 的差距主要在**限流**（Lite RPM 30000 / TPM 5000000，Pro RPM 500 / TPM 1000000）而非功能——两者能力标签一致
- 上下文档位差异：Pro / Lite / Evolving 为 1024k，Turbo 为 256k

> ⚠️ 以上均为**火山方舟调用原价**，不含限时优惠；官方提示活动信息前往方舟控制台查看。

## 七、最新动态（2026-10）

**三条跟踪线**：

- **产品线 — Doubao Seed 系列**：`doubao-seed-evolving`（周级迭代）+ Seed 2.1 Pro / Lite / Turbo 三档。核心看「哪一档是当前旗舰、上下文多长」
- **下线线 — Seed 2.0**：方舟页面上多个 `2-0-*-260215` / `260628` ID 已标「即将下线」，迁移到 2.1 是明确方向
- **开源线 — Seed-OSS**：字节唯一权重公开的主线，私有化部署只看这条

**如何跟踪**：

1. **官方源**：[火山方舟模型列表](https://docs.volcengine.com/docs/ark/model-list?lang=zh)（页脚带「最近更新时间」）、[火山方舟模型价格](https://docs.volcengine.com/docs/ark/model-pricing?lang=zh)（同样带更新时间）、[ByteDance Seed 官网](https://seed.bytedance.com/en)、[ByteDance-Seed Hugging Face 组织页](https://huggingface.co/ByteDance-Seed)
2. **更新节奏**：方舟文档页的「最近更新时间」是最可靠的新鲜度信号——本次核实到模型列表页更新于 2026-09-28、模型价格页更新于 2026-10-08
3. **判断原则**：字节的模型**声量与开源活跃度不成正比**——不要用 GitHub / HF 的更新频率去推断模型强弱，反之亦然

**截至 2026-10-08 的具体动态**：

| 时间 | 事件 | 意义 |
| --- | --- | --- |
| 2026-10-08 | **火山方舟模型价格页更新**（页脚时间戳） | 本次核实到该页最新；价格表已切到 Seed 2.1 系列 |
| 2026-09-28 | **火山方舟模型列表页更新**（页脚时间戳） | 2.1 Pro / Lite 快照为 `-260915`，Turbo 快照为 `-260628` |
| 2026-08-05 | **Seed 音视频全双工 LLM 发布**（Seed 官网最新一条博客） | 面向全模态自然交互 |
| 2026-07-31 | **Seedance 2.5 发布** | 30 秒叙事视频生成，Seed 官网列为当前视频主线 |
| 2026-07-20 | **Seed Audio 1.0 发布** | 全场景音频生成 |
| 2026-07-08 | **Seedream 5.0 Pro 发布** | 当前图像生成主线 |
| 2026-06-23 | **Seed2.1 正式发布**（官方博客） | 当前通用模型主线；Pro / Turbo 两尺寸 |
| 2026-07-03 | ByteDance HF 最新更新为 `PAR`（研究向） | 通用 LLM 权重自 2025-08 起未再更新 |

> ⚠️ **仍未核实的项**：① Seed2.1 的参数规模——官方模型页与博客均未披露参数量，故此处不写；② 豆包消费端 App 的模型版本号与用户规模（官方未在可访问页面披露 2026-03 之后的更新数据）；③ Doubao Seed Evolving 的具体迭代节奏（官方只写「周级迭代」，无版本快照可钉）。

## 参考

- [火山方舟 · 模型列表](https://docs.volcengine.com/docs/ark/model-list?lang=zh)（访问于 2026-10-08，页脚标注最近更新 2026-09-28）
- [火山方舟 · 模型价格](https://docs.volcengine.com/docs/ark/model-pricing?lang=zh)（访问于 2026-10-08，页脚标注最近更新 2026-10-08）
- [ByteDance Seed 官网 · Seed2.1 模型页](https://seed.bytedance.com/en/seed2_1)（访问于 2026-10-08）
- [ByteDance Seed 官方博客 · Seed2.1 Officially Released](https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity)（发布于 2026-06-23，访问于 2026-10-08）
- [ByteDance-Seed 官方 Hugging Face 组织页](https://huggingface.co/ByteDance-Seed)（访问于 2026-10-08）
- [中国 LLM 现状观察（2026-03-24）](https://merchmindai.net/blog/zh/post/china-llm-landscape-2026)（第三方转述口径，访问于 2026-10-08）

## 下一步

- 看总览 → [国内厂商](/ai-trends/cn-vendors/)
- 对比七家 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)

## 如果你想

- 看闭源对手 → [百度文心](/ai-trends/cn-vendors/) / [腾讯混元](/ai-trends/cn-vendors/)

---
title: 字节豆包
description: 消费入口第一——豆包 / Seed 2.0、火山引擎生态、流量分发优势
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: 中国 LLM 现状观察（2026-03）
      url: https://merchmindai.net/blog/zh/post/china-llm-landscape-2026
      accessedAt: 2026-09-30
    - name: ByteDance Seed 2.0
      url: https://seed.bytedance.com/en/seed2
      accessedAt: 2026-09-30
    - name: ByteDance-Seed 官方 Hugging Face 组织页
      url: https://huggingface.co/ByteDance-Seed
      accessedAt: 2026-09-30
---

# 字节豆包

> **TL;DR**：国内消费级 AI 入口第一（2025-08 反超 DeepSeek）——赢在抖音 / 剪映 / 火山引擎的分发体系，而不是模型声量。

## 一、定位

字节的 AI 策略是**全链路商业闭环**：消费 App 入口（豆包）+ 企业 API（火山引擎）+ 云基础设施 + 多模态矩阵。豆包是当前国内 AIGC 应用用户规模第一的产品。

## 二、模型线（截至 2026-09）

| 模型线 | 说明 |
| --- | --- |
| **Seed 2.0** | 通用 agent 模型系列（Pro / Lite / Mini 三档），主打生产部署 |
| **豆包 2.0** | 消费端主力模型，日均 token 调用量增长 500 倍以上（官方口径） |
| **Seed-OSS / Seed1.5-VL** | 当前明确开源的主线 |

> ⚠️ **本节数据的时间边界**：上表的 Seed 2.0 / 豆包 2.0 版本号与三档划分，最后一次可确证的来源是 2026-03-24 发布的《中国 LLM 现状观察》，其转述的官方口径为「截至 2026-02-14 字节通用模型最新产品线已推进到 Seed 2.0，含 Pro / Lite / Mini 三尺寸」。**截至 2026-09-30，本次未能从可访问的官方源复核该版本号是否仍然最新**——原因见下方「六、最新动态」。定价数据本次一律未取到，故不列。

## 三、关键事实

- **消费入口第一**：2025-08 反超 DeepSeek 后稳居国内 AI 应用第一；2026-02 用户规模 2.27 亿，领先 DeepSeek 近 1 亿（QuestMobile，经新浪科技转述）
- **流量分发**：优势来自抖音 / 剪映 / 火山引擎，不是论坛声量
- **模型商业化**：低价 API + 火山引擎生态
- **开源与闭源分工**：Seed 2.0 未随发布同步放出权重，字节的开源主线是 Seed-OSS 与 Seed1.5-VL（截至 2026-03-24 口径）

## 四、特点

- **分发为王**：豆包强在触达，不是基准分数
- **双轨策略**：闭源打消费（豆包），开源保开发者（Seed-OSS）
- **火山引擎**：企业侧接入与算力输出

## 五、适合 / 不适合

**适合**：消费级应用、低价大规模 API 调用、字节生态内集成。

**不适合**：开发者生态导向的选型（开源权重不如 Qwen / DeepSeek 完整）、需要技术品牌背书的场景。

## 六、最新动态（2026-09）

**三条跟踪线**：

- **产品线 — 豆包**：消费端 App 本身的功能与用户规模
- **模型线 — Seed 系列**：Seed 2.0 等通用 agent 模型（Pro / Lite / Mini 三档）的版本迭代
- **开源线 — Seed-OSS**：字节唯一权重公开的主线，私有化部署只看这条

**如何跟踪**：

1. **官方源**：[ByteDance Seed 官网](https://seed.bytedance.com/)、[火山方舟文档](https://www.volcengine.com/docs/82379/1330310)、[ByteDance-Seed Hugging Face 组织页](https://huggingface.co/ByteDance-Seed)
2. **更新节奏**：消费端产品迭代快于模型线；模型线目前按季度级别推进
3. **判断原则**：字节的模型**声量与开源活跃度不成正比**——不要用 GitHub / HF 的更新频率去推断模型强弱，反之亦然

> ⚠️ **本次核实的可达性限制（2026-09-30）**：`seed.bytedance.com` 与 `volcengine.com` 文档站**均为纯客户端渲染（SPA），不返回服务端正文**，无 `llms.txt` / Markdown 端点，脚本抓取只能拿到空壳 HTML。因此本节**不含任何 Seed 2.0 的版本号、参数或定价数字**——取不到就不写。

**截至 2026-09-30 可确证的动态**（来源：ByteDance 官方 Hugging Face 组织页）：

| 时间 | 事件 | 意义 |
| --- | --- | --- |
| 持续至 2026-09-30 | **Seed-OSS-36B 仍是官方最后一个开源 LLM** | Base 与 Instruct 均发布于 2025-08-26，累计下载约 4.7 万 / 5.9 万，是该组织下载量最高的模型；**此后至今未再放出新的 Seed-OSS LLM 权重** |
| 2026-07-03 | PAR | 研究向发布，非对话 LLM |
| 2026-06-18 | Cola-DLM | 对话模型研究 |
| 2026-06-02 | TaskMem | Agent 记忆向研究 |
| 2026-05-28 | SimArt | 图像生成向 |
| 2026-04-21 | byteff2 | 特征向研究 |
| 2026-04-18 | Adversarial-Flow-Models | 安全 / 对齐向研究 |
| 2026-03-25 | Stable-DiffCoder-8B（Base / Instruct） | 稳定扩散式代码模型，非通用 LLM |

> 📌 **怎么读这张表**：字节 2026 年在 Hugging Face 上的公开动作**集中在研究模型与专项模型（记忆、对齐、图像、代码）**，通用对话 / agent 基座的权重自 2025-08 起未再更新。这与「消费端模型线在快速迭代」并不矛盾——闭源主干在 App 与火山方舟侧推进，公开权重是另一条节奏。

> ⚠️ **未能核实项**：① Seed 2.0 是否已迭代到 2.x 及各档具体版本；② 豆包 2.0 现状；③ 火山方舟（火山引擎）上的模型与定价；④ 用户规模是否有 2026-03 之后的新数据。以上均**留空而非估算**，需人工用浏览器打开官方页确认后回填。

## 参考

- [ByteDance Seed 官网](https://seed.bytedance.com/)（访问于 2026-09-30）
- [ByteDance Seed 2.0](https://seed.bytedance.com/en/seed2)（访问于 2026-09-30，客户端渲染，脚本无法取正文）
- [ByteDance-Seed 官方 Hugging Face 组织页](https://huggingface.co/ByteDance-Seed)（访问于 2026-09-30）
- [中国 LLM 现状观察（2026-03-24）](https://merchmindai.net/blog/zh/post/china-llm-landscape-2026)（访问于 2026-09-30）

## 下一步

- 看总览 → [国内厂商](/ai-trends/cn-vendors/)
- 对比七家 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)

## 如果你想

- 看闭源对手 → [百度文心](/ai-trends/cn-vendors/) / [腾讯混元](/ai-trends/cn-vendors/)

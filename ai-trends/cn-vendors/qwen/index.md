---
title: Qwen · 阿里通义千问全系
description: 'Qwen3.8-Max / Qwen3.7 / Qwen3.8-Omni——2.4T MoE、1M 上下文、全尺寸开源、阿里云百炼生态'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: 阿里云百炼 qwen3.8-max 模型信息
      url: https://help.aliyun.com/zh/model-studio/qwen3-8-max
      accessedAt: 2026-09-30
    - name: 阿里云百炼 模型大全
      url: https://help.aliyun.com/zh/model-studio/models
      accessedAt: 2026-09-30
    - name: Qwen 官方研究博客
      url: https://qwen.ai/research
      accessedAt: 2026-09-30
---

# Qwen · 阿里通义千问全系

> 7 家厂商里**开源最彻底（全尺寸 + 全模态）+ 端侧部署最成熟 + 阿里云生态最完整**。

## 一、公司背景

Qwen（通义千问）由阿里达摩院 2023 年推出，现属阿里云通义实验室。核心定位是**「全尺寸开源 + 端侧部署 + 阿里云集成」**——从小尺寸到大尺寸全尺寸开源，覆盖从手机到数据中心的全场景。商业模式：DashScope API + 阿里云百炼 + 开源权重。

## 二、模型矩阵（截至 2026-09）

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **Qwen3.8-Max** | 旗舰（2026-08 上线） | **1M** | 支持思考模式 | 复杂推理 / 长文档 / Agent / 法律金融设计 |
| **Qwen3.8-Max-0902** | 旗舰快照（2026-09-02） | 1M | 支持思考模式 | `qwen3.8-max` 的固定版本 |
| **Qwen3.7-Max** | 次旗舰 | — | — | 官方文档页存在，本轮未取到规格 |
| **Qwen3.7-Plus** | 主力 | — | — | 通用对话 / 工具调用 |
| **Qwen3.8-Flash** | 轻量 | — | — | 高并发 / 低成本 |
| **Qwen3.8-Omni-Flash** | 全模态 | — | — | 图 / 音 / 视理解 + 文本生成 |
| **Qwen3.8-Omni-Flash-Realtime** | 实时全模态 | — | — | 实时音视频对话 / ASR |
| **Qwen3.5-Omni-Plus** | 离线语音输出 | — | — | 需离线语音输出时使用 |
| **Qwen-Image-3.0-Pro / Wan3.0-Video** | 图像 / 视频生成 | — | — | 图像与视频生成 |
| **Qwen3.7-Text-Embedding / Rerank** | 向量 / 重排 | 8K | — | 检索增强 |

> **产品线逻辑**：`Qwen3.8-Max` 做旗舰（2.4T MoE），`Qwen3.7` 系列（Max / Plus）与 `Qwen3.8-Flash` 做主力与轻量，`Qwen3.8-Omni` 做全模态——**百炼上已形成「3.8 / 3.7 / 3.5」三条子线并行的结构**。

## 三、技术架构

**MoE 路径** —— `Qwen3.8-Max` 采用 **2.4 万亿参数 MoE 架构**（官方模型页明确「2.4 万亿参数的 MoE 架构旗舰模型」），具体专家数未公开。

**原生视觉** —— `Qwen3.8-Max` **输入模态支持 Image / Text / Video**（输出仅 Text），即旗舰模型自带视觉理解，不需要额外挂 VL 模型。

**1M 长上下文** —— 官方规格：上下文长度 **1,000,000**，最大输入 991,808，最大输出 131,072，**最大思维链长度 262,144**。思考模式下最大输入降为 983,616。

**协议与工具生态** —— 支持 Function Calling、结构化输出、前缀续写、上下文缓存、联网搜索（部分地域）、批量推理。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Function Calling** | 函数调用 / JSON Schema | 百炼 API |
| **上下文缓存** | 隐式缓存命中 + 显式缓存（创建 / 命中分别计价） | 百炼 API |
| **原生视觉** | 图片 + 视频理解，旗舰模型自带 | Qwen3.8-Max |
| **全模态** | 文本 + 图 + 音 + 视 | Qwen3.8-Omni-Flash |
| **实时交互** | 实时音视频对话 | Qwen3.8-Omni-Flash-Realtime |
| **图像 / 视频生成** | 文生图 / 图生视频 / 首尾帧 | Qwen-Image / Wan 系列 |
| **决策模型** | 一次前向完成分类、判断与评分 | `decision-model-preview`（邀测） |

**多地域是 Qwen 的差异点** —— `Qwen3.8-Max` 覆盖华北 2（北京）、新加坡、法兰克福、弗吉尼亚、东京、中国香港，**出海不必绕道**。

**端侧部署仍是 Qwen 最大优势** —— 官方持续提供全尺寸开源权重，支持 llama.cpp / MLX / Ollama 等主流推理框架。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **DashScope API** | `dashscope.aliyun.com` | 直接 API 调用 |
| **阿里云百炼** | 6 个地域 | 企业 MaaS / 出海 |
| **HuggingFace** | 开源权重 | 私有部署 / 微调 |
| **ModelScope** | 国内镜像 | 国内部署 |
| **端侧部署** | llama.cpp / MLX / Ollama | 手机 / PC / 嵌入式 |

## 六、价格（截至 2026-09，阿里云百炼官方定价）

**`qwen3.8-max`（华北 2（北京），单位：元 / 百万 Tokens）**：

| 计费项 | 价格 |
|------|------|
| 输入 | ¥12 |
| 输出 | ¥36 |
| 输入（缓存命中） | ¥1.5 |
| 显式缓存创建 | ¥15 |
| 显式缓存命中 | ¥1 |
| 输入（Batch File） | ¥6 |
| 输出（Batch File） | ¥18 |

**其他地域**（同页列出）：新加坡 ¥14.988 / ¥44.965；法兰克福、弗吉尼亚、东京与北京**同价**（¥12 / ¥36 / ¥1.5）。

**价格说明**：

- 以上为**调用原价**，不含限时优惠（官方提示前往百炼控制台查看活动）
- **限流采用动态机制**：北京与新加坡按百炼月消费档位调整 TPM；法兰克福 / 弗吉尼亚 / 东京 / 香港为固定 RPM 30,000 + TPM 5,000,000
- **开源版自部署免费**；API 端 `Qwen3.8-Max` 为旗舰价

## 七、适合场景 / 不适合场景

**适合**：
- 本地部署 / 端侧部署（全尺寸开源 + 端侧优化）
- 国产化替代（阿里云生态 + 完全开源）
- 出海业务（6 个地域，含新加坡 / 法兰克福 / 弗吉尼亚 / 东京 / 香港）
- 长文档与长视频解析（1M 上下文 + 原生视频输入）
- 多模态（文本 + 图 + 音 + 视频全链路）

**不适合**：
- 超长文档分析（1M 上下文；Kimi K2 系列的 2M 档已于 2026-05 随 K2 全系下线，现行 K3 同为 1M）
- 英文为主的场景（Claude / GPT 英文更强）
- 需要旗舰级编码 agent 性价比的场景（¥12 / ¥36 相对偏高）

## 八、最新动态（2026-09）

**三条跟踪线**：

- **旗舰线**：`Qwen3.8-Max` + 快照版本。核心看「上下文 / 原生模态 / 快照节奏」
- **多模态线**：`Qwen3.8-Omni`、`Qwen-Image`、`Wan` 视频。这条线子版本号推进最快
- **工具线**：向量 / 重排（`Qwen3.7-Text-Embedding` / `Rerank`）、决策模型（`decision-model-preview` 邀测）

**如何跟踪**：

1. **官方源**：[百炼模型大全](https://help.aliyun.com/zh/model-studio/models)（页脚带 `last-modified`，可判断新鲜度）、[qwen3.8-max 模型页](https://help.aliyun.com/zh/model-studio/qwen3-8-max)（含完整规格与分地域价格）、[Qwen 官方研究博客](https://qwen.ai/research)
2. **更新节奏**：旗舰主版本约数月一更，快照版本（`-MMDD`）滚动发布；多模态线更频繁
3. **判断原则**：**看快照而非只看主版本**——`qwen3.8-max` 会静默指向最新快照，生产环境应显式钉 `-0902` 这类快照 ID

**截至 2026-09 的具体动态**（均据官方源）：

- **旗舰仍是 `Qwen3.8-Max`，未换代** —— 百炼「模型大全」页（`last-modified` 2026-09-24）仍把 `qwen3.8-max` 列为文本生成首位
- **最新快照为 `qwen3.8-max-0902`**（别名 `qwen3.8-max-2026-09-02`）—— 官方描述为「编码深度再突破…协作智能体能力显著增强…视觉理解全面精进」，延续 1M 上下文、思考模式与完整工具生态
- **规格确认** —— 2.4 万亿参数 MoE；输入模态 Image / Text / Video，输出 Text；上下文 1,000,000，最大输出 131,072，最大思维链 262,144
- **旗舰定价未变** —— 仍为 ¥12 输入 / ¥36 输出 / ¥1.5 缓存命中（北京），与 2026-08 一致
- **多模态线扩展到 3.8** —— `qwen3.8-omni-flash`（离线音视频分析 + 文本生成）与 `qwen3.8-omni-flash-realtime`（实时音视频对话）同时在售；离线语音输出仍需 `qwen3.5-omni-plus`
- **工具线新动作** —— 音频侧新增 `qwen-audio-3.0-tts-plus`、`qwen-audio-3.1-asr-flash-streaming` / `filetrans`、`qwen-audio-3.1-realtime-plus`；向量侧为 `qwen3.7-text-embedding(-flash)` 与 `qwen3.7-text-rerank`
- **图像 / 视频线** —— `qwen-image-3.0-pro`、`wan2.7-image-pro`、`wan3.0-video`
- **官方博客已迁移** —— `qwenlm.github.io/blog` 现会重定向到 **`qwen.ai/research`**，旧 GitHub Pages 博客已停更（最新一篇为 2025-09 的 Qwen3Guard）

> ⚠️ **未能核实**：`qwen3.7-max` 的具体规格（仅确认官方文档页存在）；**Qwen 开源权重在 2026-09 的最新版本**——`QwenLM/Qwen` GitHub 仓库仍停留在 Qwen1（README 已声明不再维护、指向 `QwenLM/Qwen2`），无法据此判断当前开源主线版本，故此处不写具体版本号与参数量。

## 关键洞察

- **快照机制是 Qwen 特有的运维点** —— 主版本号会静默漂移，生产必须钉快照
- **旗舰自带原生视觉** —— `Qwen3.8-Max` 输入含 Image / Video，不必再拼 VL 模型
- **6 地域是出海护城河** —— 国内厂商里少见的原生多地域覆盖
- **阿里云生态仍是护城河** —— DashScope + 百炼 + 阿里云集成
- **开源主线的核实难度高于闭源** —— 官方博客已停更、GitHub 主仓未跟进，判断开源版本需另找渠道

## 参考

- [阿里云百炼 qwen3.8-max 模型信息](https://help.aliyun.com/zh/model-studio/qwen3-8-max)（访问于 2026-09-30）
- [阿里云百炼 模型大全](https://help.aliyun.com/zh/model-studio/models)（访问于 2026-09-30）
- [Qwen 官方研究博客](https://qwen.ai/research)（访问于 2026-09-30）
- [DashScope 平台](https://dashscope.aliyun.com/)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 看横向对比表 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 看 GLM 档案 → [Zhipu · 智谱 GLM 全系](/ai-trends/cn-vendors/zhipu/)
- 看国内厂商动态 → [国内厂商](/ai-trends/cn-vendors/)
- 看技术路线 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

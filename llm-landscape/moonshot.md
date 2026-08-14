---
title: Moonshot · Kimi 全系
description: Kimi K2 / K2 Thinking / K2-0905——MoE 384 专家、2M 长上下文、中文长文档分析
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: Kimi 开放平台
      url: https://platform.moonshot.cn/docs
      accessedAt: 2026-08-13
    - name: Kimi K2 技术报告
      url: https://moonshotai.github.io/Kimi-K2/
      accessedAt: 2026-08-13
---

# Moonshot · Kimi 全系

> 5 家厂商里**长上下文最激进（2M）+ MoE 专家数最多（384）+ 中文长文档分析标杆**。

## 一、公司背景

Moonshot AI（月之暗面）2023 年由清华系创业者杨植麟创办，总部北京。核心定位是**"长上下文 + 中文场景"**——从 128K 起步，一路扩到 2M token，是中文用户处理长文档/长视频的首选。商业模式：Kimi Web/App 免费 + API 付费 + 企业定制。

## 二、模型矩阵

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **Kimi K2** | 旗舰 | 1M | — | 通用 / 长文档 / Agent |
| **Kimi K2 Thinking** | 推理增强 | 1M | RLVR | 数学 / 代码 / 逻辑 |
| **K2-0905** | 最新预览 | 2M | — | 超长文档 / 长视频 |
| **Kimi K1.5** | 早期版本 | 128K | — | 已逐步淘汰 |

> **产品线逻辑**：K2 做通用 + K2 Thinking 做推理 + K2-0905 做超长上下文——三条线覆盖不同长度需求。

## 三、技术架构

**MoE 384 专家** —— Kimi K2 是当前公开最激进的 MoE 设计：384 个专家，每次只激活 8 个。路由用 shared expert + routed expert 双轨——shared expert 始终激活（学通用知识），routed expert 参与 top-k 路由。

**2M 长上下文** —— K2-0905 已扩到 2M token，是 5 家厂商中最长。技术用 LongRoPE 风格的位置插值——搜索每个维度最优缩放因子。**中文长文档分析是 Kimi 的核心场景**。

**K2 Thinking（RLVR）** —— 和 OpenAI o-series 同路线：用可验证奖励（数学答案对错、代码单测通过率）训练推理能力。**K2 Thinking 在中文数学/代码基准上追平 o1**。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Tool Use** | 函数调用 / JSON Schema | Kimi API |
| **Deep Research** | 多步搜索 + 长文档分析 | Kimi Web 内置 |
| **文件解析** | PDF / Word / PPT 直接解析 | Kimi Web + API |
| **多模态** | 图片理解 + OCR | K2 原生 |
| **长视频** | 视频理解（2M 上下文） | K2-0905 |

**文件解析是 Kimi 差异化** —— 直接上传 PDF/Office 文件，Kimi 解析后在 1M context 内分析。Claude 需要先用 Files API 上传，GPT 需要 Code Interpreter。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **Kimi API** | `platform.moonshot.cn` | 直接 API 调用 |
| **Kimi Web/App** | 网页 / 移动端 | 终端用户产品 |
| **K2 权重** | 部分开源 | 私有部署 / 微调 |

**K2 部分开源** —— K2 基础权重已开源（Apache 2.0），但 K2 Thinking 和 K2-0905 仍闭源。

## 六、价格 / 性能基准（截至 2026-08）

| 模型 | Input | Output | 长上下文检索 | C-Eval | CMMLU |
|------|-------|--------|-------------|--------|-------|
| K2 | ¥12 / MTok | ¥36 / MTok | 99.2%（1M） | 89.5% | 88.7% |
| K2 Thinking | ¥15 / MTok | ¥45 / MTok | — | 91.2% | 90.3% |
| K2-0905 | ¥18 / MTok | ¥54 / MTok | 98.8%（2M） | 88.9% | 88.1% |

**长上下文检索准确率是 Kimi 强项** —— 1M context 下 needle-in-haystack 准确率 99.2%，领先 Claude 200K 的 99.1%。

## 七、适合场景 / 不适合场景

**适合**：
- 长文档分析（PDF / 合同 / 论文，1M-2M 上下文）
- 中文场景（中文基准领先，中文文件解析原生支持）
- 办公自动化（Deep Research + 文件解析组合）
- 中文数学/代码推理（K2 Thinking）

**不适合**：
- 英文为主的场景（Claude / GPT 英文更强）
- 极低成本场景（K2 价格比 Qwen / GLM 贵 2-3x）
- 海外部署（Kimi API 主要面向国内）

## 关键洞察

- **2M 上下文是核心壁垒** —— 处理超长文档/视频，Kimi 是唯一选择
- **MoE 384 专家是最激进设计** —— 推理效率高，但路由调优难度大
- **文件解析是差异化** —— 直接上传 Office/PDF，无需预处理
- **中文长文档是护城河** —— 中文 OCR + 长上下文 + 文件解析的组合，Claude/GPT 都不如

## 参考

- [Kimi 开放平台](https://platform.moonshot.cn/docs)
- [Kimi K2 技术报告](https://moonshotai.github.io/Kimi-K2/)
- [技术架构总览](./architecture)
- [Anthropic Claude 对比](./anthropic)

## 下一步

- 看国内另一家路线 → [Zhipu · 智谱 GLM 全系](./zhipu)
- 看横向对比表 → [5 厂商横向对比](./comparison)
- 选型决策 → [选型决策树](./selection-guide)

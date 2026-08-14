---
title: 选型决策树
description: 按场景 / 中文要求 / 长文档 / 编码 / 推理 / 预算 6 维度选型——什么任务选什么模型
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: 5 厂商横向对比
      url: /reference/model-comparison
      accessedAt: 2026-08-13
---

# 选型决策树

> **6 个维度、5 个决策点、1 张速查表**——看完就能选型，避开"过度选型"和"配置浪费"。

## 决策树：按 6 维度选

```mermaid
flowchart TD
    A[开始选型] --> B{场景？}
    B -->|对话/通用| C{中文要求？}
    B -->|编码/Agent| D[Claude Sonnet 5]
    B -->|推理/数学| E[OpenAI o 系列 / GLM-Z1]
    B -->|多模态| F[Qwen3.5 原生多模态]
    
    C -->|高| G{长文档？}
    C -->|低| H[GPT-5.6 Terra]
    
    G -->|> 200K| I[Kimi K3 / Qwen3.8-Max]
    G -->|< 200K| J{预算？}
    
    J -->|敏感| K[Qwen3.5 开源 / GLM-4-Air]
    J -->|不敏感| L[Claude Sonnet 5]
```

### 维度 1：场景

| 场景 | 首选 | 理由 |
|------|------|------|
| 通用对话 | Claude Sonnet 5 / GPT-5.6 Terra | 性价比高，中英文都好 |
| 编码 + Agent | Claude Sonnet 5 | Tool Use + Agent 最完整 |
| 数学/代码推理 | OpenAI o 系列 / GLM-Z1 | RLVR 推理最强 |
| 长文档分析 | Kimi K3 / Qwen3.8-Max | 1M 上下文 |
| 多模态 | Qwen3.5 / MiniMax（原生多模态） | 全模态最完整 |

### 维度 2：中文要求

| 要求 | 首选 | 理由 |
|------|------|------|
| 高（中文原生） | Kimi / Qwen / GLM | 中文基准领先，中文文件解析原生 |
| 中（中英文均衡） | Claude Sonnet 5 | 中英文都好，Agent 最强 |
| 低（英文为主） | GPT-5.6 Sol / Claude Opus 5 | 英文基准最高 |

### 维度 3：长文档

| 长度 | 首选 | 理由 |
|------|------|------|
| < 200K | 任意旗舰模型 | 都够用 |
| 200K - 1M | Claude Fable 5 / Kimi K3 / Qwen3.8-Max | 1M 上下文 |
| > 1M | 暂无（主流旗舰封顶 1M） | Kimi K3 / Fable 5 的 1M 是当前上限 |

### 维度 4：编码能力

| 需求 | 首选 | 备注 |
|------|------|------|
| 最强编码 | Claude Opus 5 / Sonnet 5 | 官方 benchmark 见 Anthropic 发布博客 |
| 编码 + 推理 | Claude Opus 5 | Frontier-Bench 等官方评测领先 |
| 开源编码 | Qwen3.5 / Qwen-Coder | 自部署成本可控 |

### 维度 5：预算

| 预算 | 首选 | 备注 |
|------|------|------|
| 极低 | MiniMax M2.7 / GLM-5.1 | $0.3-1.4/MTok |
| 低 | GPT-5.6 Luna / Qwen3.5 开源（自部署） | $0.2/MTok 起 |
| 中 | Claude Sonnet 5 / GPT-5.6 Terra / Grok 4.6 | $2/MTok |
| 高 | Claude Opus 5 / GPT-5.6 Sol | $5/MTok |
| 顶 | Claude Fable 5 / GPT-5.6 Cyber | $10+/MTok |

### 维度 6：部署

| 部署 | 首选 | 理由 |
|------|------|------|
| API 直调 | 任意厂商 | 都支持 |
| 海外企业私有 | Claude (Bedrock/Vertex) / GPT (Azure) | 云厂商集成 |
| 国内企业私有 | Qwen (阿里云) / GLM (智谱云) | 国产化 + 私有化 |
| 端侧/本地 | Qwen3.5 开源小尺寸 / GLM-4-Air | 全尺寸开源 + 端侧优化 |

## 5 个常见决策点

### 1. "公司内 AI 助手选谁"

**需求**：中文 + 私有化 + 成本可控

**推荐**：Qwen3.5 开源（阿里云部署）或 GLM-5.1（智谱 MaaS）

**理由**：全尺寸开源 + 国产化合规 + 成本低（见各官方定价）

### 2. "个人 Claude Code 替代品"

**需求**：编码 + 工具调用 + 低成本

**推荐**：Claude Sonnet 5（$2/MTok）或 Qwen3.5 开源（自部署）

**理由**：Claude Agent 最完整，Qwen 开源免费

### 3. "长 PDF / 合同分析"

**需求**：长上下文 + 文件解析 + 中文

**推荐**：Kimi K3（1M 上下文 + 文件解析）或 Qwen3.8-Max（1M 上下文）

**理由**：Kimi 文件解析原生支持，Qwen 价格更低

### 4. "数学 / 物理 / 算法竞赛"

**需求**：推理能力最强

**推荐**：OpenAI o 系列（推理最强）或 GLM-Z1（中文推理最强）

**理由**：RLVR 训练，"想得更久 = 答得更准"

### 5. "国内业务 + 数据合规"

**需求**：国产化 + 私有化 + 数据不出境

**推荐**：Qwen（阿里云）或 GLM（智谱云）

**理由**：全尺寸开源 + 国内云厂商集成 + 数据合规

## 反向决策：哪些场景不该用 LLM

| 场景 | 问题 | 替代方案 |
|------|------|----------|
| 实时交易决策 | 延迟太高（100ms+） | 规则引擎 / 传统 ML |
| 精确数值计算 | 浮点误差 / 幻觉 | 计算器 / Wolfram Alpha |
| 法律/医疗诊断 | 责任归属不清 | 人工审核 + LLM 辅助 |
| 超大规模数据处理 | 成本太高 | 传统 ETL / Spark |

## 组合策略：Multi-model 路由

**思路**：便宜的模型处理简单任务，贵的模型处理复杂任务。

**示例路由**：

```
用户请求 → 简单分类？ → Qwen3.5 开源（自部署）
         → 需要推理？ → Claude Opus 5（$5/MTok）
         → 长文档？  → Kimi K3（$3/MTok）
```

**收益**：平均成本降低 60-80%，同时保持质量。

## 参考

- [5 厂商横向对比](./model-comparison) — 8 维度量化对比
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape) — 4 大技术路线详解
- [5 厂商详情](/ai-trends/vendors/) · [Anthropic](/ai-trends/vendors/anthropic) · [OpenAI](/ai-trends/vendors/openai) · [Moonshot](/ai-trends/vendors/moonshot) · [Zhipu](/ai-trends/vendors/zhipu) · [Qwen](/ai-trends/vendors/qwen)

## 下一步

- 选完型想接 SDK → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)
- 看部署案例 → [Cookbook](/cookbook/)
- 深入某家厂商 → [Anthropic](/ai-trends/vendors/anthropic) / [OpenAI](/ai-trends/vendors/openai) / [Moonshot](/ai-trends/vendors/moonshot) / [Zhipu](/ai-trends/vendors/zhipu) / [Qwen](/ai-trends/vendors/qwen)

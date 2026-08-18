---
title: 评估方法论
description: 如何设计评估、避免过拟合、评估结果解读
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: HELM 评估框架
      url: https://crfm.stanford.edu/helm/
      accessedAt: 2026-08-13
---

# 评估方法论

> **TL;DR**：好的评估 = 多维度 + 防过拟合 + 可复现。单一基准不可靠，需要组合使用。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 评估设计的核心原则
- 避免基准过拟合的方法
- 评估结果的正确解读
- 企业级评估实践

## 评估设计原则

### 1. 多维度

单一基准只能衡量一个维度。好的评估需要覆盖：

| 维度 | 基准 | 权重 |
|------|------|------|
| 知识广度 | MMLU / C-Eval | 中 |
| 代码能力 | HumanEval / SWE-bench | 高 |
| 推理能力 | GSM8K / MATH / GPQA | 高 |
| 人类偏好 | Arena | 高 |
| 实际场景 | 自定义测试集 | 最高 |

### 2. 防过拟合

**问题**：模型可能在公开基准上过拟合。

**解法**：

- **保留测试集**：不公开的测试集，只在最终评估时使用
- **动态基准**：Arena 等持续更新的基准
- **对抗测试**：故意设计的难题，防止单纯记忆

### 3. 可复现

- 记录评估环境（模型版本、采样参数、温度）
- 使用标准化评估框架（HELM / lm-evaluation-harness）
- 公开评估代码和数据

## 企业级评估

**场景**：企业选型时，需要评估模型在自己业务场景上的表现。

**流程**：

1. **定义评估维度**：业务需要哪些能力（编码、对话、知识、推理）
2. **构建测试集**：从真实业务数据中采样，覆盖典型场景
3. **标准化评估**：统一采样参数（temperature=0、max_tokens=...）
4. **人工评估**：关键场景人工打分
5. **成本评估**：性能/价格比

**测试集构建**：

| 类型 | 数量 | 说明 |
|------|------|------|
| 典型场景 | 100-500 | 覆盖 80% 使用场景 |
| 边界场景 | 50-100 | 测试极限情况 |
| 对抗场景 | 20-50 | 故意设计的难题 |

## 评估指标

| 指标 | 说明 | 适用 |
|------|------|------|
| **准确率** | 答案正确的比例 | 选择题 / 分类 |
| **pass@k** | k 次生成至少 1 次正确的概率 | 代码生成 |
| **BLEU / ROUGE** | 与参考答案的重叠度 | 翻译 / 摘要 |
| **人类评分** | 人工打分 | 对话 / 创作 |
| **延迟** | 响应时间 | 实时场景 |
| **吞吐** | 每秒处理的请求数 | 高并发 |

## 常见坑

**基准分数 ≠ 实际体验**

基准是标准化测试，实际使用更复杂。Arena 等人类偏好基准更接近实际。

**评估参数不一致**

不同评估使用不同参数（temperature、max_tokens），结果不可比。

**测试集泄露**

测试集数据混入训练集，导致分数虚高。需要严格隔离。

## 评估框架

| 框架 | 特点 | 适用 |
|------|------|------|
| **HELM** | Stanford 多维度评估 | 学术研究 |
| **lm-evaluation-harness** | EleutherAI 标准化框架 | 通用评估 |
| **OpenCompass** | 中文评估体系 | 中文模型 |
| **Chatbot Arena** | 人类偏好动态评估 | 实际体验 |

## 参考

- [HELM: Holistic Evaluation of Language Models](https://crfm.stanford.edu/helm/)
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [5 厂商横向对比](/ai-trends/model-selection/model-comparison)

## 下一步

- 看各家模型的基准表现 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 了解具体基准 → [基准测试](./benchmarks)
- 了解 AI 评估实践 → [Claude 能力 · 推理能力](/claude-capabilities/core/reasoning)

---
title: 基准测试
description: MMLU / HumanEval / GSM8K / Arena 等主流评测体系
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: MMLU 论文
      url: https://arxiv.org/abs/2009.03300
      accessedAt: 2026-08-13
    - name: HumanEval 论文
      url: https://arxiv.org/abs/2107.03374
      accessedAt: 2026-08-13
---

# 基准测试

> **TL;DR**：MMLU 测知识、HumanEval 测编码、GSM8K 测数学、Arena 测人类偏好。没有单一基准能衡量全部能力。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 主流基准测试的衡量维度
- 各基准的优缺点
- 如何正确解读基准分数
- 基准过拟合问题

## 主流基准

| 基准 | 衡量维度 | 题目数 | 难度 |
|------|----------|--------|------|
| **MMLU** | 知识（57 学科） | 14,042 | 中 |
| **HumanEval** | 代码生成 | 164 | 中 |
| **GSM8K** | 数学推理 | 8,500 | 中 |
| **GPQA** | 研究生级推理 | 448 | 高 |
| **MATH** | 竞赛数学 | 12,500 | 高 |
| **SWE-bench** | 真实软件工程 | 2,294 | 高 |
| **Arena** | 人类偏好 | 动态 | — |

## MMLU：知识广度

**内容**：57 个学科的选择题（STEM、人文、社科等）。

**优势**：覆盖面广，衡量知识广度。

**局限**：选择题格式，不测推理深度。基准泄露严重。

## HumanEval：代码能力

**内容**：164 个 Python 编程题，给函数签名和测试用例。

**衡量**：pass@k（生成 k 个答案，至少 1 个通过的概率）。

**局限**：题目简单，不反映真实软件工程。

## SWE-bench：真实工程

**内容**：GitHub 真实 issue，要求模型生成修复补丁。

**优势**：最接近真实软件工程。

**局限**：题目数量有限，评估成本高。

## GSM8K / MATH：数学推理

**GSM8K**：小学级数学应用题。

**MATH**：竞赛级数学题。

**衡量**：精确匹配（答案完全正确才算对）。

## Arena：人类偏好

**Chatbot Arena**：用户与两个匿名模型对话，投票选好的。

**优势**：最接近真实使用体验。

**局限**：样本偏差（用户群体不代表性）、成本高。

## 基准分数解读

**同一基准跨模型可比**：MMLU 88% vs 85% 有意义。

**不同基准不可直接比**：MMLU 88% vs HumanEval 80% 无意义。

**基准分数 ≠ 实际体验**：基准是标准化测试，实际使用更复杂。

## 基准过拟合

**问题**：模型针对基准训练，分数虚高。

**表现**：

- 基准分数高，实际体验差
- 同类题目做得好，变体题做得差

**应对**：

- 看多个基准的综合表现
- 关注 Arena 等动态基准
- 亲自测试实际场景

## 中文基准

| 基准 | 衡量维度 | 说明 |
|------|----------|------|
| **C-Eval** | 中文知识 | 52 学科，中文版 MMLU |
| **CMMLU** | 中文知识 | 67 学科 |
| **SuperCLUE** | 中文综合 | 多维度评估 |

**中文厂商在中文基准上整体领先**（C-Eval / CMMLU / SuperCLUE），具体分数以各家官方技术报告为准。

## 参考

- [MMLU: Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)（2020）
- [HumanEval: Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)（2021）
- [Chatbot Arena](https://chat.lmsys.org/)
- [5 厂商横向对比](/reference/model-comparison)

## 下一步

- 了解评估方法论 → [评估方法论](./methodology)
- 看各家模型的基准表现 → [5 厂商横向对比](/reference/model-comparison)

## 如果你想

- 选型决策 → [模型选型决策树](/reference/model-selection-guide)
- 了解 AI 评估实践 → [Claude 能力 · 推理能力](/claude-capabilities/core/reasoning)

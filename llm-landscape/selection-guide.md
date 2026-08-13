---
title: 选型决策树
description: 什么任务选什么模型——按场景 / 中文要求 / 长文档 / 编码 / 推理 / 预算 6 维度
audience: beginner
difficulty: 🟢
status: planned
lastUpdated: 2026-08-11
---

# 选型决策树

> 🚧 本页规划中，属于 Claude Handbook v0.4.3 路线图（LLM landscape 模块）。详见 [architecture review · v0.4.3](/contributing/architecture-review-2026-08-10)。

## 你能在这里学到

- 按 6 个核心维度（场景 / 中文 / 长文档 / 编码 / 推理 / 预算）做选型
- 避开"过度选型"和"配置浪费"
- 实战中的 5 个常见选型决策点

## 前置知识

- 已读过 [5 厂商横向对比](./comparison)
- 了解 [技术架构总览](./architecture) 的关键概念

## 内容大纲（v0.5 阶段 1 填充）

- [ ] 一、决策树：按 6 维度选
  - 维度 1：场景（对话 / 编码 / 推理 / Agent / 多模态）
  - 维度 2：中文要求（高 / 中 / 低）
  - 维度 3：长文档（< 200K / 200K-1M / > 1M）
  - 维度 4：编码能力（SWE-bench > 50% / 推理 > 80%）
  - 维度 5：预算（每百万 token 成本敏感度）
  - 维度 6：部署（API / 开源 / 私有化 / 国产化）
- [ ] 二、5 个常见决策点
  - "公司内 AI 助手选谁"（中文 + 私有化）
  - "个人 Claude Code 替代品"（编码 + 工具）
  - "长 PDF / 合同分析"（长上下文 + 文件解析）
  - "数学 / 物理 / 算法竞赛"（推理模型）
  - "国内业务 + 数据合规"（国产化 + MaaS）
- [ ] 三、**反向决策**：哪些场景**不**该用 LLM
- [ ] 四、组合策略：Multi-model 路由（便宜的 + 贵的）

## 参考

- [5 厂商横向对比](./comparison)
- [5 厂商详情](./anthropic) · [openai](./openai) · [moonshot](./moonshot) · [zhipu](./zhipu) · [qwen](./qwen)
- [architecture review](/contributing/architecture-review-2026-08-10)

## 下一步

- 选完型想接 SDK → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk) · [Anthropic Python SDK](/claude-capabilities/sdk/python-sdk)
- 看部署案例 → [Cookbook](/cookbook/)

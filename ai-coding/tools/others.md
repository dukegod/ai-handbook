---
title: Codex CLI / Trae 评测
description: OpenAI Codex CLI、字节 Trae 等新兴 AI 编程工具
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: OpenAI Codex
      url: https://openai.com/index/codex/
      accessedAt: 2026-08-13
    - name: Trae 官网
      url: https://trae.ai
      accessedAt: 2026-08-13
---

# Codex CLI / Trae 评测

> **TL;DR**：Codex CLI 推理最强但按 token 计费，Trae 免费但中文场景为主。

⏱ 预计阅读时间：5 分钟

## Codex CLI

### 核心特点

- **OpenAI 官方 CLI**：类似 Claude Code 的终端工具
- **推理能力最强**：基于 o-series 模型
- **按 token 计费**：无订阅，用多少付多少

### 优势

- 推理能力业界最强（o3 模型）
- CLI 原生，可脚本化
- 支持复杂逻辑推理

### 劣势

- 按 token 计费，成本不可预测
- Agent 能力不如 Claude Code
- MCP 生态不如 Claude Code

### 适用场景

- 数学/逻辑密集的编程任务
- 需要强推理的代码生成
- 成本不敏感的场景

## Trae

### 核心特点

- **字节跳动出品**：中文场景优化
- **免费使用**：无订阅费用
- **AI-native IDE**：基于 VS Code

### 优势

- 完全免费
- 中文提示词效果好
- IDE 体验完整

### 劣势

- Agent 能力较弱
- 国际化支持有限
- 生态不如 Cursor/Copilot

### 适用场景

- 中文开发团队
- 预算有限
- 简单代码补全需求

## 其他新兴工具

| 工具 | 厂商 | 特点 | 状态 |
|------|------|------|------|
| **PI-agent** | Earendil | 极简 Agent 框架、15+ 模型、MIT 开源 | 活跃 |
| **DeepSeek Harness** | DeepSeek | 插件一切、Cordis 内核、144k Star、MIT 开源 | 开发者预览 |
| **Windsurf** | Codeium | AI-native IDE | 公测 |
| **Aider** | 开源 | CLI + Git 集成 | 活跃 |
| **Continue** | 开源 | IDE 插件 + 多模型 | 活跃 |
| **Cody** | Sourcegraph | 代码搜索 + AI | 活跃 |

## 选型建议

| 需求 | 推荐 |
|------|------|
| 推理最强 | Codex CLI |
| 免费 + 中文 | Trae |
| CLI + Git | Aider |
| IDE + 多模型 | Continue |

## 参考

- [OpenAI Codex](https://openai.com/index/codex/)
- [Trae 官网](https://trae.ai)
- [AI Coding 工具全景](./overview)

## 下一步

- 团队引入 → [团队 AI 工作流](../workflows/team)
- 企业部署 → [企业部署指南](../enterprise/deployment)

## 如果你想

- 对比主流工具 → [AI Coding 工具全景](./overview)
- 选型决策 → [AI Coding 工具全景](./overview)

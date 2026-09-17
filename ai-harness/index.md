---
title: AI Harness 工程
description: AI Native 研发范式——设计理念、三层架构、资产飞轮、TDD 质量保障、迁移路径
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-17
---

# AI Harness 工程

> **TL;DR**：AI Harness 工程是把 AI 设为默认执行者的研发范式——设计理念、架构方法论、资产飞轮与质量保障的方法论合集。

## 你能在这里学到

- AI Native 是什么,它和"在传统流程里加 AI 助手"有什么本质区别
- 如何让工程结构对 AI 友好(三层架构、模块模板、状态契约)
- 如何把经验沉淀为可复用资产(Specs / Rules / Skills / Tests)
- 如何用 TDD 收敛 AI 的概率性产出
- 如何从现有项目分阶段迁移到 AI Harness 工程

## 与 Foundation Kit 的关系

| 仓库 | 定位 | 内容 |
|------|------|------|
| **本仓库(ai-handbook/ai-harness)** | 公开方法论 | 通用 AI Native 工程原理、模式、迁移路径 |
| [pipeline-architecture-wiki](https://coding.jd.com/sz-fe/pipeline-architecture-wiki)(内部) | Foundation Kit | 通用方法论 + 京东内部特定实践、Skill 工程化、模板 |

通用方法论在此维护。**京东特定的业务实践、组件库绑定、Skill 落地模板留在内部 Foundation Kit**。

## 阶段说明

本章节当前处于**阶段 2:内容迁移完成**。

- **阶段 1**(已完成):建立顶级导航、首页 feature 卡、AGENTS.md 关系说明
- **阶段 2**(已完成):将 `/ai-coding/architecture/` 下的 5 篇方法论迁移到本目录,清理旧路径
- **阶段 3**(规划中):在 wiki 侧清理通用方法论,仅保留京东特定实践

## 下一步

- 理解理念 → [设计理念:人机分工](./design-philosophy)
- 改造架构 → [三层架构与模块模板](./three-layer-architecture)
- 沉淀资产 → [资产飞轮机制](./asset-flywheel)
- 建立质量 → [TDD 质量保障](./tdd-quality)
- 迁移路径 → [迁移路径](./migration-guide)

## 如果你想

- 看 AI Coding 工具对比 → [AI Coding 落地](/ai-coding/)
- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 看团队工作流 → [团队 AI 工作流](/ai-coding/workflows/team)
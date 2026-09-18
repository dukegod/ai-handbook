---
title: AI Harness 工程
description: AI Native 研发范式——设计理念、三层架构、资产飞轮、TDD 质量、团队工作量与常见模式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-17
---

# AI Harness 工程

> **TL;DR**：AI Harness 工程是把 AI 设为默认执行者的研发范式——设计理念、架构方法论、资产飞轮、质量保障、团队工作量、常见模式的方法论合集。

## 你能在这里学到

- AI Native 是什么，它和"在传统流程里加 AI 助手"有什么本质区别
- 如何让工程结构对 AI 友好（三层架构、模块模板、状态契约）
- 如何把经验沉淀为可复用资产（Specs / Rules / Skills / Tests）
- 如何用 TDD 收敛 AI 的概率性产出
- 如何把 AI 工具嵌入团队工作流（多人协作、CI/CD、自动化 Code Review）
- AI 辅助三类常见编码动作——重构、测试、文档——的模式与边界
- 如何从现有项目分阶段迁移到 AI Harness 工程

## 与 Foundation Kit 的关系

| 仓库 | 定位 | 内容 |
|------|------|------|
| **本仓库（ai-handbook/ai-harness）** | 公开方法论 | 通用 AI Native 工程原理、模式、迁移路径 |
| [pipeline-architecture-wiki](https://coding.jd.com/sz-fe/pipeline-architecture-wiki)（内部） | Foundation Kit | 通用方法论 + 京东内部特定实践、Skill 工程化、模板 |

通用方法论在此维护。**京东特定的业务实践、组件库绑定、Skill 落地模板留在内部 Foundation Kit**。

## 内容结构

本章节按 **方法论 → 团队工作量 → 常见模式** 三层组织：

- **方法论**（5 篇）：讲清"是什么 / 为什么"——设计理念、三层架构、资产飞轮、TDD 质量、迁移路径
- **团队工作量**（3 篇）：落到团队场景的具体动作——多人协作工作流、CI/CD 集成、自动化 Code Review
- **常见模式**（3 篇）：落到编码动作的具体模式——代码重构、测试生成、文档生成

## 阶段说明

本章节当前处于**阶段 3：团队工作量与常见模式迁入**。

- **阶段 1**（已完成）：建立顶级导航、首页 feature 卡、AGENTS.md 关系说明
- **阶段 2**（已完成）：将 `/ai-coding/architecture/` 下的 5 篇方法论迁移到本目录，清理旧路径
- **阶段 3**（已完成）：将 `/ai-coding/workflows/` 和 `/ai-coding/patterns/` 迁入本目录，作为团队工作量和常见模式两个分组
- **阶段 4**（规划中）：在 wiki 侧清理通用方法论，仅保留京东特定实践

## 下一步

**方法论线**

- 理解理念 → [设计理念：人机分工](./design-philosophy)
- 改造架构 → [三层架构与模块模板](./three-layer-architecture)
- 沉淀资产 → [资产飞轮机制](./asset-flywheel)
- 建立质量 → [TDD 质量保障](./tdd-quality)
- 迁移路径 → [迁移路径](./migration-guide)

**落地线**

- 团队工作量 → [团队 AI 工作流](./workflows/team)
- 常见模式 → [代码重构模式](./patterns/refactor)

## 如果你想

- 看 AI Coding 工具对比 → [AI Coding 落地](/ai-coding/tools/overview)
- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 看实战 → [Cookbook](/cookbook/)

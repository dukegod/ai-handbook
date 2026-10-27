---
title: AI 研发体系
description: 从 AI coding、AI Native、AI 自交付到 AI 研发 Agent 平台的概念与阅读路径
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-27
---

# AI 研发体系

> **TL;DR**：从完成编码任务，到组织研发、形成交付闭环，再到平台承载与治理。

<script setup>
import { withBase } from 'vitepress'
</script>

## 你能在这里学到

- 四个主题分别解决什么问题
- 编码能力、研发方式、交付责任与平台能力如何连接
- 从哪组文章进入，以及哪些结论仍是理论假设

## 前置知识

- [Agent 与 Workflow](/getting-started/agents-and-workflows)

## 先看整体关系

![AI 研发体系：从编码任务、研发组织、交付闭环到平台承载的阅读路径](/diagrams/ai-engineering/overview.png)

[打开大图](/diagrams/ai-engineering/overview.png) · <a :href="withBase('/diagrams/ai-engineering/overview.drawio')" download>下载可编辑图源</a>

**箭头表示建设与阅读路径，不是行业演化定律或固定的成熟度阶梯。** 前三个主题讨论工作方式和责任范围，平台讨论如何承载它们。平台可以先支持编码任务；没有统一平台，也可以讨论和组织自交付。

## 四条主线

| 主线 | 核心问题 | 本章入口 |
| --- | --- | --- |
| AI coding | 怎样做好一个编码任务？ | [编码任务与方法](./patterns/)：上下文、任务拆分、实现、诊断、测试与审阅 |
| AI Native | 怎样围绕 AI 执行重新组织研发？ | [研发体系设计](./ai-native)：分工、架构、契约、知识、质量与团队协作 |
| AI 自交付 | 怎样从目标持续推进到可验收结果？ | [交付闭环](./ai-delivery/)：阶段关系、授权、证据、反馈与完成边界 |
| AI 研发 Agent 平台 | 怎样统一承载与治理这些工作？ | [平台定位](./agent-platform/)：项目、任务、能力、工具、上下文与追溯 |

## 用同一事项理解差别

以“改进知识搜索”为例：AI coding 关注实现查询、修正错误和验证行为；AI Native 关注需求、数据契约、代码结构与测试是否支持 AI 持续工作；AI 自交付关注这项改进是否完成约定验收、具备何种发布授权，以及使用效果如何判断；平台关注这些事项如何被组织、审阅和追溯。

它们可以同时出现在同一项目中。一次代码生成不能证明形成了 AI Native 研发体系；流程齐全不能证明交付成功；统一界面也不能证明结果可靠。

## 如何阅读

第一次阅读按四条主线顺序进入。已有明确问题时，可以直接选择：编码动作看 AI coding，团队与工程结构看 AI Native，完成条件看 AI 自交付，跨项目组织和治理看平台。

现有重构、测试与文档文章归入 AI coding；人机分工、三层代码架构、资产飞轮、TDD 与团队工作流归入 AI Native。文章原地址保留，产品横评仍在 [AI 工具](/ai-coding/)。

## 理论与公开内容边界

此组织方式是本站的概念框架。基本原则、设计选择和效果假设分别表述；新增概念页与交付、平台模型保持草案状态，不宣称效率、质量收益已得到验证。组织内部业务、仓库地址和环境配置不属于公开内容。

## 下一步

- 从具体工作进入 → [AI coding：编码任务与方法](./patterns/)

## 如果你想

- 比较具体产品 → [AI 工具](/ai-coding/)
- 直接理解交付 → [AI 自交付](./ai-delivery/)

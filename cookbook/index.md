---
title: Cookbook
description: Claude Code 与 Claude 能力的实战案例集；每个配方可复现、可复用
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-11
---

# Cookbook

> 概念文教你「是什么、为什么」，Cookbook 教你**在真实场景里怎么做**。

## 入选门槛

不是所有想法都进 Cookbook。一个案例值得成文，需要满足：

- **别处查不到**：不是官方文档已有的场景翻译
- **近 90 天可复现**：作者本人在最新版本亲手跑通
- **有踩坑**：只有"顺利跑通"的成功故事没什么价值，读者需要知道你在哪里差点翻车
- **有边界**：明确"这个方法适合什么、不适合什么"

## 目录

| 配方 | 适用场景 | 难度 |
| --- | --- | --- |
| [第一个真实任务](./first-real-task) | 用 Claude Code 完成一次 100 行以内的重构；含完整对话记录 | 🟢 |
| [写你的第一个 Skill](./build-first-skill) | 从 SKILL.md 到本地测试到复用；含常见触发失败的排查 | 🟡 |
| [写你的第一个 MCP Server](./build-first-mcp-server) | Python 版本，覆盖 stdio 传输、工具/资源两种能力、Claude Code 接入 | 🟡 |
| [用 Claude Code 重构老项目](./refactor-legacy-project) 🚧 | 30 万行 legacy 代码库；如何用 CLAUDE.md + Subagent 逐块推进 | 🔴 |
| [数据分析工作流](./data-analysis-workflow) 🚧 | Claude Code + Jupyter + dataviz Skill 做端到端数据探查 | 🟡 |
| [多 Agent 研究流水线](./multi-agent-research) 🚧 | Workflow 编排：Fan-out 检索 → 对抗验证 → 综合报告 | 🔴 |

## 阅读建议

**新手** 从第一篇开始。让 Claude Code 帮你重构一段代码，是最容易感受"能力边界"的场景。

**开发者** 直接跳到 Skill / MCP 两篇。Cookbook 里的这两篇比 [Claude Code · Skills](/claude-code/skills/what-is-a-skill) 或 [Claude Code · MCP](/claude-code/mcp/what-is-mcp) 更实操向。

**架构师** 关注多 Agent 编排与 legacy 项目重构两篇——它们展示了 Claude Code 在**规模**上的能力上限。

## 想贡献一个 Cookbook？

- 先读 [写作规范](/contributing/style-guide) 和 [操作文模板](/contributing/template-howto)
- 案例必须满足本页顶部四条入选门槛
- 配套的最小可复现仓库放 `examples/<case-name>/` 或独立仓库，主 Wiki 引用

## 下一步

- 从最简单的开始 → [第一个真实任务](./first-real-task)
- 回到概念学习 → [Claude Code 精通](/claude-code/)

## 如果你想

- 看真实项目落地经验 → [重构老项目](./refactor-legacy-project) 🚧
- 学多 Agent 编排 → [多 Agent 研究流水线](./multi-agent-research) 🚧

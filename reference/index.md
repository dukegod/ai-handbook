---
title: 速查手册
description: CLI Flags、Slash Commands、环境变量、settings.json Schema、模型 ID 与定价的速查表
audience: intermediate
difficulty: 🟢
status: published
lastUpdated: 2026-07-23
---

# 速查手册

> 不讲道理，只列事实。查一眼就走。

概念、原理、教程去看别的章节；这里只提供**表格化、可 Ctrl+F 搜索**的参考资料。

## 目录

| 页面 | 内容 |
| --- | --- |
| [CLI Flags](./cli-flags) | `claude` 命令的所有 flag 与用法 |
| [内置 Slash Commands](/claude-code/customization/slash-commands) | `/help`、`/model`、`/cost`、`/clear`、`/compact` 等 |
| [环境变量](./env-vars) 🚧 | `ANTHROPIC_API_KEY`、`CLAUDE_CODE_*` 系列 |
| [settings.json Schema](/claude-code/customization/settings) | 用户级 / 项目级 settings.json 字段全表 |
| [模型 ID 与定价](./model-ids) 🚧 | 全部 Claude 模型的 ID、context 长度、$/1M token |
| [5 厂商横向对比](./model-comparison) | Claude / GPT / Kimi / GLM / Qwen 的能力、价格、部署对比 |
| [模型选型决策树](./model-selection-guide) | 按场景、中文要求、长文档、编码、推理和预算选模型 |
| [术语表](./glossary) | 中英双语术语锁定；与 [contributing/glossary](/contributing/glossary) 内容相同 |

## 更新频率

Claude 生态月度级更新，速查表尤其容易过时。每篇速查表顶部标注：

- `verifiedWith`：验证时的 Claude Code / SDK 版本
- 上一次官方 changelog 扫描日期

超过 90 天没更新的速查表，浏览时请谨慎。以 [官方文档](https://docs.claude.com/) 为准。

## 下一步

- 从常用命令开始 → [CLI Flags](./cli-flags)
- 系统学习 → [Claude Code 精通](/claude-code/)

## 如果你想

- 查 Claude 模型 → [模型 ID 与定价](./model-ids) 🚧
- 选通用大模型 → [模型选型决策树](./model-selection-guide)
- 查 Claude Code 配置 → [定制与扩展 · Settings 配置文件](/claude-code/customization/settings)

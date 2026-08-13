---
title: 信息架构 review（2026-08-10）
description: v0.4.3 阶段产物——基于 133 个 .md 现状盘点 + 4 类问题 + 4 类修正建议的 review 报告
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-10
---

# 信息架构 review（2026-08-10）

> **背景**：v0.4.2 死链 0 错通过后，趁热对全站 133 个 .md 做一次架构盘点——22 篇 planned + 1 篇 draft + 33 篇 2026-07-23 时代内容长期没动，是 v0.5 阶段需要解决的 3 个主要遗留。

## 一、整体盘点

| 维度 | 数 | 占比 |
| --- | --- | --- |
| 全部 .md | 133 | 100% |
| wiki 文档（有 frontmatter） | 125 | 94% |
| **published** | 102 | **82%** |
| planned | 22 | 18% |
| draft | 1 | 1% |
| examples 仓库说明（无 frontmatter） | 8 | 6% |

## 二、子目录完成度矩阵

### claude-code/ 9 个子目录（6 满 3 缺）

| 子目录 | pub/total | 状态 |
| --- | --- | --- |
| advanced | 5/5 | ✅ 100% |
| basics | 7/7 | ✅ 100% |
| customization | 4/4 | ✅ 100% |
| mcp | 6/6 | ✅ 100% |
| skills | 7/7 | ✅ 100% |
| subagents-and-workflows | 4/4 | ✅ 100% |
| **tools** | **1/9** | **❌ 11%（8 planned）** |
| **ecosystem** | **1/5** | **❌ 20%（4 planned）** |
| **prompting** | **0/2** | **❌ 0%（2 planned）** |

### claude-capabilities/ 8 个子目录（**全 100% published**）

agentic / api / core / mcp-protocol / models / prompting / sdk / surfaces 全部完成——**项目最稳的部分**。

### 其他子目录

| 目录 | 状态 | 备注 |
| --- | --- | --- |
| getting-started/ | 6/6 ✅ | 入门闭环 |
| cookbook/ | 4/7 | 3 stub planned（refactor-legacy / data-analysis / multi-agent） |
| reference/ | 3/7 | **4 planned（速查手册基本空白）** |
| contributing/ | 6/7 | **1 draft（checklist-published.md）** |

## 三、4 类架构问题

### 3.1 重复 / 错位（高优，**建议先解决**）

| 主题 | A | B | 处理建议 |
| --- | --- | --- | --- |
| **slash-commands 重复** | `claude-code/customization/slash-commands.md` (pub) | `reference/slash-commands.md` (plan) | 概念/详细 → A；快速参考表段 → B |
| **settings schema 重复** | `claude-code/customization/settings.md` (pub) | `reference/settings-schema.md` (plan) | 详细 → A；schema 一览段 → B |
| **model-ids 重叠** | `claude-capabilities/models/*` (6 pub) | `reference/model-ids.md` (plan) | 改成"模型 ID 速查表"——**不是重复，是提炼** |
| **prompting 错位** | `claude-code/prompting/` (2 plan) | `claude-capabilities/prompting/` (6 pub) | **建议删 `claude-code/prompting/` 子目录**——重复 + 规划冲突 |

### 3.2 内容缺口（highest impact）

| 缺口 | 数 | 价值 / 备注 |
| --- | --- | --- |
| `claude-code/tools/` | 8 planned | **核心使用入口缺得最离谱**——Read / Write / Edit / Bash / Grep / Glob / WebFetch / TodoWrite |
| `claude-code/ecosystem/` | 4 planned | IDE 集成是企业用户入口——VS Code / JetBrains / Neovim / 企业部署 |
| `cookbook/` | 3 stub | 已知（refactor-legacy / data-analysis / multi-agent） |
| `reference/` | 4 planned | 速查手册：env-vars / model-ids / settings-schema / slash-commands |

### 3.3 内部不一致（小修）

- **`contributing/checklist-published.md` 唯一 draft** —— 发布 checklist 自己还没发布，**反讽**
- `./README.md` + `./index.md` 都存在，角色可能重叠

### 3.4 维护滞后（中期）

| lastUpdated | 篇数 | 备注 |
| --- | --- | --- |
| **2026-07-23** | **33**（32%） | v0.1 时代首批，1 个月没动——**潜在 stale** |
| 2026-07-28 | 17 | v0.1 末 |
| 2026-08-06 | 14 | v0.4.1 起步，4 天前 |
| 2026-08-07 | 34 | v0.4.2 高峰，**当天写完即 publish——stale 风险** |
| 2026-08-08 | 3 | v0.4.2 收尾 |
| 2026-08-10 | 1 | 今天（link-checking.md） |

**风险**：33 篇 v0.1 时代内容可能与现在的 Claude Code 行为不符（v0.1 → v0.4.2 期间 Claude Code 已多次升级）。

## 四、4 类修正建议（按 ROI 排）

### A. 清理（30 分钟）

1. 删 `claude-code/prompting/` 子目录（2 planned，重复）
2. `reference/slash-commands.md` 改为 `claude-code/customization/slash-commands.md` 的"速查段"
3. `reference/settings-schema.md` 改为 `claude-code/customization/settings.md` 的"schema 一览段"
4. publish `contributing/checklist-published.md`（draft → published）
5. 更新 `contributing/roadmap.md` + `claude-code/index.md` 章导读反映 22 planned 现状

### B. 补全（highest impact，v0.5 阶段 1）

按 ROI 排：

- `claude-code/tools/` 8 个（**最核心**，2-3 小时/批）
- `claude-code/ecosystem/` 4 个（**企业向**，1-2 小时/批）
- `reference/` 4 个（**速查表**——基于已 published 内容做"提炼"段，1-2 小时）
- `cookbook/` 3 stub（**已讨论，ROI 中等**）

### C. 维护机制（v0.5+ 持续）

1. **每月 lastUpdated 巡检**——`grep "2026-07-23"` 33 篇内容是否还准
2. **建立 changelog 体系**——`claude-capabilities/changelog.md` + 顶部"本模型最新变更"卡片
3. **path-scoped 巡检**——v0.4.2 已知 VitePress 中文锚点 false positive，标记 stale 段

### D. 长期重构（v0.6+ 候选）

1. `claude-code/prompting/` 整个子目录**或删或合**
2. `reference/` 重新定位——是速查？还是复制 customization 的精简版？需要**功能边界澄清**
3. `README.md` 角色——给 GitHub 用户 vs 给 VitePress 站点？合并到 `index.md`？

## 五、关键风险

1. **33 篇 v0.1 时代内容 stale 风险** —— Claude Code v2.1 → v2.1.220 已多次升级，部分行为可能已变
2. **22 planned 长期空置**——sidebar 仍展示，读者看到 placeholder 体验差
3. **`claude-code/tools/` 是最大漏洞**——读文件 / 改文件 / 跑命令是 Claude Code 三大能力，没这些文档用户怎么用？

## 六、落地节奏建议

| 阶段 | 内容 | 估时 |
| --- | --- | ------ |
| v0.4.3 | 本 review 报告（落盘）+ A 类清理 5 项 | 1 小时 |
| v0.5.0 | B 类补全：`claude-code/tools/` 8 篇首批 4 篇 | 2-3 小时 |
| v0.5.1 | B 类补全：tools 剩余 4 篇 + ecosystem 4 篇 | 2-3 小时 |
| v0.5.2 | B 类补全：reference 4 段速查 | 1-2 小时 |
| v0.5.3 | C 类维护机制：每月 lastUpdated 巡检 + changelog 体系 | 1-2 小时 |
| v0.6+ | D 类长期重构 | 待评估 |

## 参考

- [写作规范](/contributing/style-guide) — 1500 汉字上限 / frontmatter 强制字段
- [路线图](/contributing/roadmap) — v0.1 ~ v0.4 阶段历史
- [死链检查](/contributing/link-checking) — v0.4.2 阶段产物，本 review 同期
- [CLAUDE.md](/) — 内容开发工作流（写新篇 / 改已 published 的 6 步清单）

## 下一步

- 切到 A 类清理（30 分钟小改）→ [贡献指南 · 写作规范](/contributing/style-guide)
- 切到 B 类补全（v0.5 阶段 1）→ [路线图 v0.5+ 规划](/contributing/roadmap)
- 切到 C 类维护机制 → [死链检查 v0.4.2 阶段策略](/contributing/link-checking)

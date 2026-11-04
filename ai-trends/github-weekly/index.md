---
title: GitHub AI 动向
description: 每周一自动生成的 GitHub 榜单周报——本周热榜、本月热榜、本周涨星 TOP，并附重点仓库的深度解读与技术演进建议
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# GitHub AI 动向

> **TL;DR**：每周一 12:00 自动抓取 GitHub Trending，产出本周热榜、本月热榜、本周涨星 TOP，并对 AI / 大模型相关的重点仓库做深度解读与技术演进建议。

## 你能在这里学到

- 一周内 GitHub 生态的热度重心在哪（本周榜 / 本月榜 / 涨星榜三视角）
- 哪些仓库值得投入时间，以及它们**为什么**在涨
- AI Agent 生态从「模型能力」向「工程基础设施」迁移的具体证据
- 每个重点仓库的后续发展方向判断（基于技术路线与生态位置，非厂商宣传）

## 如何跟踪技术动向

先读本期判断，再查看相关仓库深读，最后对照历史周报观察同一方向的变化。重点关注 AI Agent、模型与推理、开发工具、上下文与记忆、安全及运行基础设施。

榜单热度用于发现线索，不等于技术成熟度或质量保证。每期数据按其标注窗口理解，不同窗口可能重叠；历史报告不代表项目当前状态。

## 报告结构

每周一个目录，主文档在周目录的 `index.md`：

```
ai-trends/github-weekly/
├── index.md          ← 你在这里，按周倒序索引
└── 2026-W45/
    ├── index.md      ← 本周榜单全表 + 本周判断
    ├── <repo>.md     ← 重点仓库深读（10 篇左右）
    └── ...
```

## 历史周报

| 周次 | 数据窗口 | 主题 |
| --- | --- | --- |
| [2026-W45](./2026-W45/index.md) | 2026-10-26 ~ 2026-11-02 | Skill 生态吞掉周榜 13/16，JetBrains 亲自下场做 harness，DeepSeek 开源 Agent 授权模型 |
| [2026-W44](./2026-W44/index.md) | 2026-10-20 ~ 2026-10-26 | harness 被拆成可自动优化的组件，插件层规范战先于协议开打 |
| [2026-W43](./2026-W43/index.md) | 2026-10-15 ~ 2026-10-21 | Agent 生态基础设施集中爆发：上下文工程、跨 harness 插件生态、Agent 联邦与沙箱运行时 |

## 数据口径

- **本周热榜 / 本月热榜**：GitHub Trending 官方榜（`since=weekly` / `since=monthly`），涨星数为页面自带口径。
- **本周涨星**：同上，按 `period_stars` 降序重排。
- **新锐仓库**：GitHub Search API 按 `created:` 过滤近 30 天新建仓库，按 star 排序。
- **原始数据快照**：由采集流程单独保存，不随站点公开发布。

> ⚠️ GitHub REST 的 `/stargazers` 接口已下线，无法自算任意窗口的精确涨星；第三方 star 历史数据（OSS Insight）自 2026-05 起官方标注严重降级，仅作趋势参考。因此周报涨星一律采用 GitHub Trending 官方口径。

## 下一步

- 先读 [2026-W45 本期周报](./2026-W45/index.md)，再按需进深读
- 想追 A2A 协议本身 → 看 [A2A 协议行业深度调研](../industry/a2a-protocol.md)

## 如果你想

- 看 Agent 工程范式与团队落地 → [AI Native 方法论](../../ai-harness/index.md)
- 看工具链横评 → [AI 工具全景](../../ai-coding/tools/overview.md)
- 看模型选型 → [模型选型决策树](../model-selection/model-selection-guide.md)

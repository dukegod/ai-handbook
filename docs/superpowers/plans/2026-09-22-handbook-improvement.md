---
title: AI Handbook 改进计划
description: '先整理入口，再打通学习路径，补齐实战与维护机制'
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-09-22
---

# AI Handbook 改进计划

> **For agentic workers:** 执行时使用 superpowers:executing-plans 逐项推进；本文件是规划草案，尚未开始实施。

**Goal:** 让中文读者能找到适合自己的路线，完成真实任务，并辨认内容的验证状态。

**Architecture:** 保留现有内容目录和 URL，以导航、导读和跨页链接改善组织。先完成入口整理，再补案例，最后固化检查机制。

**Tech Stack:** VitePress 1.6.4、Vue、Markdown、pnpm、GitHub Actions。

**Spec:** 本次对话的结构审查结论、项目 `AGENTS.md` 与 `contributing/style-guide.md`；下列范围与验收标准为执行依据。

## 约束与取舍

- 推荐渐进整理；全面迁移目录增加链接维护成本，单纯扩篇不能解决阅读路径问题。
- 保留中文全栈定位，优先服务开发者学习与落地，Claude 继续作为深度专题。
- Node.js ≥ 20；pnpm 10.28.1；保留动态 base 和 `.npmrc` 的 hoist 设置。
- 新页面同步 sidebar；正文遵守术语、元数据、1500 汉字及结尾引导规范。
- 修改日期不等于验证日期；不把 draft 批量改为 published，不虚填验证版本。
- 本轮不安排目录迁移、主题重做、i18n 或搜索替换。提交和发布另按用户指令执行。

## 阶段一：入口一致（P0）

**文件：** `index.md`、`README.md`、`CLAUDE.md`、`AGENTS.md`、`contributing/roadmap.md`、`.vitepress/config.ts`、`ai-harness/index.md`、`ai-trends/index.md`。

- [ ] 按正文状态校正施工标记、完成度、模块描述；上下文文件按仓库同步机制维护。
- [ ] 顶部入口整理为入门、核心技术、工具、Harness、模型与厂商、产品动向、Claude 专题；贡献入口移至页脚。
- [ ] 模型与厂商使用下拉导航直达已有选型及厂商页面，保留原 URL。
- [ ] 首页“完整大纲”改为“内容路线图”；README 补 Harness；路线图以当前阶段开篇，旧里程碑折叠保留。
- [ ] Harness 导读聚焦读者收益；迁移记录与内部协作关系移入维护说明，并保持相对链接正确。

**验收：** 导航目标均存在；published 与施工标记无冲突；桌面与移动端均能找到各模块；现有 URL 不变。

## 阶段二：三条阅读路线（P0）

**文件：** `getting-started/index.md`、`index.md`、`ai-coding/index.md`、`ai-harness/index.md`、`cookbook/index.md` 及路线涉及页面的结尾引导。

- [ ] 入门线：什么是 AI → 大语言模型 → 能力边界 → 选工具 → 提示词；产出一条可验证的个人任务提示词。
- [ ] 开发者线：工具全景 → Claude Code 安装与认证 → 项目规则 → `cookbook/first-real-task.md`；产出经过测试和 diff 审查的小改动。
- [ ] 团队线：Harness 设计理念 → 三层架构 → TDD → 团队工作流 → 资产沉淀；产出试点清单与验收约定。
- [ ] 每条路线注明受众、前置条件、必读顺序、产出；开发者线明确当前以 Claude Code 为示范。

**验收：** 从首页可进入三条路线；必读节点均为可用正文；读者无需进入路线图判断下一步。

## 阶段三：完成实战闭环（P1）

**文件：** `ai-coding/tools/{overview,codex-cli,cursor,claude-code}.md`、`cookbook/refactor-legacy-project.md`、`cookbook/index.md`、`ai-trends/product-updates/monthly.md`、`.vitepress/config.ts`。

- [ ] 优先核验三款工具：统一任务、环境、版本、成本条件、结果、失败边界；无实测依据的排名删除或限定。
- [ ] 完成老项目重构案例：提供可获取的起点、复现步骤、回归断言和验收结果；示例放 `examples/refactor-legacy-project/`。
- [ ] 先将“月度产品速报”改名为“产品动态跟踪方法”，保持 URL；有真实首期后再建设按月归档，不预承诺频率。

**验收：** 案例在干净环境可复现；选型事实有对应一手来源和核验日期；不能验证的页面保留 draft。

## 阶段四：维护机制（P1）

**文件：** `.vitepress/theme/index.ts`、`.vitepress/theme/components/VersionBanner.vue`、新增 `ContentStatus.vue`、`contributing/checklist-published.md`、`package.json`、新增 `scripts/check-content.mjs`。

- [ ] 正文顶部区分 draft、planned、published；导航统一使用相同状态语义。
- [ ] 时效提示改用中性措辞与本页参考来源；时间较久只提示需复核，不直接判定事实错误；内部链接适配 base。
- [ ] 增加内容检查：必填元数据、状态合法性、导航目标、published 与施工标记冲突。历史问题先列清单，修复后纳入阻断。
- [ ] 用有效页、缺字段、非法状态、缺目标、标记冲突五类临时样例验证检查器；每月优先复核选型与安装页面。

**验收：** 五类样例结果符合预期；抽查三种状态页面；通用 AI 页面不出现 Claude 专属提示。

## 交付检查

- [ ] 每阶段运行 `git diff --check`、`pnpm build`、`pnpm check-links`，区分内部错误与外网访问失败。
- [ ] 导航和组件变更分别验证本地根路径及 `VITEPRESS_BASE=/ai-handbook/ pnpm build`。
- [ ] 本地通过不等同于线上验收；发布后另查首页、路线、搜索、移动端与旧链接。
- [ ] 本计划实施前只完成阶段一、二的范围确认；后续代码任务执行前细化接口与测试，不一次铺开全部阶段。

## 下一步

优先实施阶段一，再交付三条阅读路线；完成后评估是否进入案例补齐。

## 如果你想

更快体现落地价值，可在前两阶段后优先完成重构案例，其余评测逐篇核验。

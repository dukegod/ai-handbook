---
title: 路线图
description: Claude Handbook 分阶段内容路线；v0.1 到 v0.4+ 的取舍与里程碑
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-11
---

# 路线图

> 一个人写 100 篇技术文档是长跑。这份路线图明确「哪一版做什么、不做什么」，让每一版都能形成闭环。

## 全局原则

- **每一版都能形成闭环**：新读者跟着当前版本走，能走通一条完整学习路径，不遇到"路线图里但还没写"的死链
- **验证优先于覆盖**：先写 20 篇打磨模板，再谈扩张
- **贴近实际使用**：每篇文档在正式发布前，作者本人至少用它跑通过一遍相关任务
- **每季度归档一次**：无人问津 + 已严重过时的文档果断归档，不硬撑

## v0.1 · 站点骨架与写作元规范（当前）

**目标**：站点跑通、写作规范就位、读者能从首页找到完整大纲。

**已完成：**

- ✅ VitePress 站点搭建 + 中文本地搜索
- ✅ 完整目录树的占位页面（约 100 篇）
- ✅ 写作规范五件套：本文 + [style-guide](./style-guide) + [glossary](./glossary) + [template-concept](./template-concept) + [template-howto](./template-howto)
- ✅ 首页 + 六个章节的 index 导读
- ✅ Frontmatter / 时效横幅 / 术语约束 / PR checklist 就位

**v0.1.1 · 入门闭环 22 篇（全部初稿完成 ✅）**

::: tip v0.1.1 初稿进度（2026-07-28 更新）
- **A 段入门**：5/5 初稿完成 ✅
- **B 段基础**：8/8 初稿完成 ✅ + **`context-window.md` 于 v0.1.2 尾声直升 published（2026-07-29）**
- **C 段亮点与参考**：3/3 初稿完成 ✅
- **D 段元维护**：1/1 初稿完成 ✅
- **F 段增补**：1/1 完成

初稿完成 = frontmatter `status: draft`；正式**进版**需 `status: published` 并补齐 `verifiedWith` 与 [PR 前 checklist](./style-guide#十、pr-前自检-checklist)。下一步：**进入 v0.1.2 精修阶段**，逐篇过 published 门槛。
:::

**v0.1.2 · Published 门槛升级（全部完成 ✅）**

::: tip v0.1.2 published 进度（2026-07-28 更新）
- **A 段入门**：5/5 已过 published 门槛 ✅
- **B 段基础**：8/8 已过 published 门槛 ✅ + `context-window.md` 从 planned 直升 published ✅（9/9 全齐）
- **C 段亮点与参考**：3/3 已过 published 门槛 ✅
- **D 段元维护**：1/1 已过 published 门槛 ✅
- **F 段增补**：1/1 已过 published 门槛 ✅

**v0.1.1 骨架 + v0.1.2 published 门槛闭环达成**——19 篇正式文档（B 段 `context-window.md` 于 v0.1.2 尾声一并补齐）全部通过 12 项 [Published 门槛自检](./checklist-published) 并落库。下一步进入 v0.2 · Claude Code 扩展生态。
:::

**A. 入门（5 篇 · 全部初稿完成 ✅ · **全部已过 published 门槛 ✅**）**

- [x] [/getting-started/what-is-claude-code](/getting-started/what-is-claude-code) · 836 汉字 · **published 2026-07-28**
- [x] [/getting-started/installation](/getting-started/installation) · 774 汉字 · **published 2026-07-28**
- [x] [/getting-started/first-conversation](/getting-started/first-conversation) · 1070 汉字 · **published 2026-07-28**
- [x] [/getting-started/mental-model](/getting-started/mental-model) · 1415 汉字 · **published 2026-07-28**
- [x] [/getting-started/comparisons](/getting-started/comparisons) · 1098 汉字 · **published 2026-07-28**

**B. Claude Code 基础（9 篇 · 全部初稿完成 ✅ · **全部已过 published 门槛 ✅**）**

- [x] [/claude-code/basics/sessions](/claude-code/basics/sessions) · 1252 汉字 · **published 2026-07-28**
- [x] [/claude-code/basics/claude-md](/claude-code/basics/claude-md) · 1229 汉字 · **published 2026-07-28**
- [x] [/claude-code/basics/permissions](/claude-code/basics/permissions) · 1093 汉字 · **published 2026-07-28**
- [x] [/claude-code/basics/context-window](/claude-code/basics/context-window) · 1197 汉字 · **published 2026-07-29**
- [x] [/claude-code/basics/cost-and-tokens](/claude-code/basics/cost-and-tokens) · 1237 汉字 · **published 2026-07-28**
- [x] [/claude-code/basics/model-selection](/claude-code/basics/model-selection) · 1116 汉字 · **published 2026-07-28**
- [x] [/claude-code/basics/plan-mode](/claude-code/basics/plan-mode) · 1224 汉字 · **published 2026-07-28**
- [x] [/claude-code/tools/overview](/claude-code/tools/overview) · 1219 汉字 · **published 2026-07-28**
- [x] [/claude-code/customization/slash-commands](/claude-code/customization/slash-commands) · 1205 汉字 · **published 2026-07-28**

> **note · 2026-07-29**：`basics/context-window.md` 原计划延后到 v0.2 与 `long-context` / `prompt-caching` / `extended-thinking` 一起系统展开，v0.1.2 收官时**决定拉齐**：核心概念（200k/1M 边界、`/context` 结构、auto-compact 幸存表、`paths:` scoped rule 与 skill body 的 compact 行为）已足够独立成篇，且横向引用点 [sessions](/claude-code/basics/sessions) / [cost-and-tokens](/claude-code/basics/cost-and-tokens) / [claude-md](/claude-code/basics/claude-md) 全部到位，读者从任何一条相邻页面链过来都不空。v0.2 时的 [long-context](/claude-capabilities/core/long-context) 可专注 API 层（batching、streaming、1M pricing 边界），不必再重讲 CLI 视角。

**C. 一个亮点与两个参考（3 篇 · 全部初稿完成 ✅ · **全部已过 published 门槛 ✅**）**

- [x] [/claude-code/skills/what-is-a-skill](/claude-code/skills/what-is-a-skill) · 1259 汉字 · **published 2026-07-28**
- [x] [/reference/cli-flags](/reference/cli-flags) · 1095 汉字 · **published 2026-07-28**
- [x] [/cookbook/first-real-task](/cookbook/first-real-task) · 1207 汉字 · **published 2026-07-28**

**D. 元维护（1 篇 · 初稿完成 ✅ · **已过 published 门槛 ✅**）**

- [x] [/reference/glossary](/reference/glossary) · **published 2026-07-28** — 通过 VitePress include 复用 [contributing/glossary](./glossary) 作单一真相源

**E. 视觉与体验（5 项 · 全部完成 ✅）**

- [x] 站点 logo 与 favicon ✅（2026-07-28 交付 · [logo.svg](/logo.svg) 主 8-芒星 + 斜环 + 环上小行星，favicon 去环留星保证 16×16 可辨识；4 版草稿归档在 `assets/logo-drafts/`）
- [x] 首页 hero 配图 ✅（2026-07-28 交付 · [hero.svg](/hero.svg) 主星光晕 + 斜环 + 尾巴虚线，与 logo 元素一致）
- [x] 时效横幅 Vue 组件（`<VersionBanner />`）✅（90 天黄警 / 180 天红警，2026-07-28 交付）
- [x] 难度徽章样式（`<DifficultyBadge />`）✅（🟢入门 / 🟡进阶 / 🔴高阶 三档胶囊，2026-07-28 交付）
- [x] `pnpm build` 输出无死链警告 ✅（2026-07-28 验证：build 0 warning / 0 dead link）

**F. 增补（out-of-plan · 2026-07-24 追加 · **已过 published 门槛 ✅**）**

- [x] [/claude-code/ecosystem/third-party-models](/claude-code/ecosystem/third-party-models) — 接入非 Claude 模型（国内主流两种方案）· 1112 汉字 · **published 2026-07-28**

> **增补理由**：国内主流厂商（智谱 GLM / MiniMax / DeepSeek / Kimi / Qwen 等）都通过 **Anthropic 兼容端点** 或 **多供应商切换工具**（cc-switch / Claude Code Router）接入 Claude Code。这是中文 wiki 的高频需求，独立成篇便于长期维护——各厂商 endpoint / 模型名会持续变化，集中一处比散落多篇更可控。作为「入门后可选的进阶补充」。

**v0.1 完成标志：** 一个第一次听说 Claude Code 的中文读者，能从首页开始，按左侧 sidebar 阅读，用 15 分钟看完前 5 篇后开始用 Claude Code；再用 1 小时读完剩余 17 篇建立完整的工作认知。

## v0.2 · Claude Code 扩展生态（✅ 全部收官 2026-08-06）

**目标**：填齐 Skills / Hooks / MCP / Subagents 这条主线的所有页面。

::: tip v0.2 全量收官（2026-08-06 更新）
v0.2.1 新增交付物全部就位：示例仓库（`examples/check-page` + `examples/glossary-mcp-server`，含 uv 锁定的 Python 环境与 SKILL/MCPServer 双层结构）+ Cookbook 实战 2 篇（`build-first-skill` / `build-first-mcp-server`，均已 published）。`v0.2 完成标志` 两半句全部达成——v0.2 严格意义上 100% 收官，下一步进入 v0.3。
:::

**1. Skills 系列 6 篇（`what-is-a-skill` 之外，该篇已在 v0.1 完成）—— 全部完成 ✅**

- [x] [skill-md-spec](/claude-code/skills/skill-md-spec) · 1379 汉字 · **published 2026-07-29**
- [x] [writing-triggers](/claude-code/skills/writing-triggers) · 1173 汉字 · **published 2026-07-29**
- [x] [skills-vs-commands-vs-agents](/claude-code/skills/skills-vs-commands-vs-agents) · 1030 汉字 · **published 2026-07-29**
- [x] [built-in-skills](/claude-code/skills/built-in-skills) · 997 汉字 · **published 2026-07-29**
- [x] [custom-skill](/claude-code/skills/custom-skill) · 250 汉字（教程型，代码示例占比高）· **published 2026-07-29**
- [x] [plugins-marketplace](/claude-code/skills/plugins-marketplace) · 820 汉字 · **published 2026-07-30**

**2. Hooks —— 完成 ✅**

- [x] [hooks](/claude-code/customization/hooks) · 1227 汉字 · **published 2026-08-03**

**3. MCP 使用层 6 篇 —— 全部完成 ✅**

- [x] [what-is-mcp](/claude-code/mcp/what-is-mcp) · 856 汉字 · **published 2026-08-03**
- [x] [transports](/claude-code/mcp/transports) · 696 汉字 · **published 2026-08-03**
- [x] [official-servers](/claude-code/mcp/official-servers) · 612 汉字 · **published 2026-08-03**
- [x] [build-your-own](/claude-code/mcp/build-your-own) · 686 汉字 · **published 2026-08-03**
- [x] [auth-and-debug](/claude-code/mcp/auth-and-debug) · 698 汉字 · **published 2026-08-03**
- [x] [mcp-json-config](/claude-code/mcp/mcp-json-config) · 646 汉字 · **published 2026-08-03**

**4. Subagents 与 Workflow 4 篇 —— 全部完成 ✅**

- [x] [what-is-a-subagent](/claude-code/subagents-and-workflows/what-is-a-subagent) · 836 汉字 · **published 2026-08-04**
- [x] [agent-types](/claude-code/subagents-and-workflows/agent-types) · 795 汉字 · **published 2026-08-04**
- [x] [workflow-orchestration](/claude-code/subagents-and-workflows/workflow-orchestration) · 974 汉字 · **published 2026-08-04**
- [x] [multi-agent-patterns](/claude-code/subagents-and-workflows/multi-agent-patterns) · 862 汉字 · **published 2026-08-04**

**5. 定制化剩余 —— 全部完成 ✅**

- [x] [settings](/claude-code/customization/settings) · 811 汉字 · **published 2026-08-04**
- [x] [keybindings](/claude-code/customization/keybindings) · 913 汉字 · **published 2026-08-04**

**6. 高阶 5 篇 —— 全部完成 ✅**

- [x] [worktree](/claude-code/advanced/worktree) · 732 汉字 · **published 2026-08-04**
- [x] [headless](/claude-code/advanced/headless) · 641 汉字 · **published 2026-08-04**
- [x] [automation](/claude-code/advanced/automation) · 810 汉字 · **published 2026-08-04**
- [x] [git-workflow](/claude-code/advanced/git-workflow) · 482 汉字 · **published 2026-08-04**
- [x] [memory](/claude-code/advanced/memory) · 1104 汉字 · **published 2026-08-04**

**新增交付物（v0.2.1 全部完成 ✅ · 2026-08-06）：**

- [x] Skill 与 MCP Server 的最小可复现仓库（入 `examples/`，含双目录：[/examples/check-page](/examples/check-page/README) Skill 模板 + [/examples/glossary-mcp-server](/examples/glossary-mcp-server/README) MCPServer 模板，均带 README 站外可读）
- [x] Cookbook 补充两篇：[build-first-skill](/cookbook/build-first-skill)（**published 2026-08-06**）/ [build-first-mcp-server](/cookbook/build-first-mcp-server)（**published 2026-08-06**）——分别以新实例 `weather-poke` Skill / `quote-mcp-server` MCP 串完完整流程，避开与 examples 撞名

**v0.2 完成标志 ✅：** 一个用过一段时间 Claude Code 的中级用户，能在这里找到自定义扩展的完整指南；跟着 Cookbook 写出的 Skill / Hook / MCP Server 能复制 examples 仓库结构稳定复用——两半句全部达成。v0.2 收官。

## v0.3 · Claude 能力全景（分 3 段，v0.3.1 已收官 2026-08-06）

**目标**：把视角从 CLI 用户扩展到 API/SDK 开发者；"每一步都有可运行代码"作为硬约束。

**内容清单（全量 ~46 篇）：**

- **模型家族 6 篇**（含 Fable 5 定位核实与撰写）—— ✅ v0.3.1 完成
- **核心能力 6 篇**：reasoning / extended-thinking / coding / vision / long-context / tool-use —— ✅ v0.3.1 完成
- **深度提示工程 6 篇**：从入门 best-practices 到 Prefill + XML —— ⏳ v0.3.2
- **API 9 篇**：Messages / Tool Use / Streaming / Structured Outputs / Prompt Caching / Message Batches / Files / Token Counting / Admin & Usage —— ⏳ v0.3.2
- **SDK 7 篇**：Python / TS / Agent SDK / Tool Runner / Managed Agents / Claude Code SDK / overview —— ⏳ v0.3.2
- **MCP 协议层 3 篇** —— ✅ v0.3.3 收官
- **Agentic 3 篇**：Computer Use / Multi-agent / Safety —— ✅ v0.3.3 收官
- **产品面 6 篇**：Claude.ai / Artifacts / Desktop / Web / Mobile / Slack —— ✅ v0.3.3 收官

### v0.3.1 · 模型家族 + 核心能力 12 篇（✅ 2026-08-06 收官）

::: tip v0.3.1 收官（2026-08-06 更新）
12 篇正文全部 published，pnpm build 0 死链 / check_page 0 命中。
:::
**模型家族 6**（API/SDK 视角，不重复 v0.1 model-selection 的 CLI 视角内容）：

- [x] [概览](/claude-capabilities/models/overview) · 683 汉字 · **published 2026-08-06**
- [x] [Opus 5](/claude-capabilities/models/opus) · 691 汉字 · **published 2026-08-06**
- [x] [Sonnet 5](/claude-capabilities/models/sonnet) · 753 汉字 · **published 2026-08-06**
- [x] [Haiku 4.5](/claude-capabilities/models/haiku) · 656 汉字 · **published 2026-08-06**
- [x] [Fable 5](/claude-capabilities/models/fable) · 854 汉字 · **published 2026-08-06**
- [x] [选型（API 视角）](/claude-capabilities/models/choosing-model) · 863 汉字 · **published 2026-08-06**

**核心能力 6**（新主题为主，少量与 v0.1/v0.2 已 published 文档通过链接分工）：

- [x] [推理能力](/claude-capabilities/core/reasoning) · 1090 汉字 · **published 2026-08-06**
- [x] [Extended Thinking](/claude-capabilities/core/extended-thinking) · 1034 汉字 · **published 2026-08-06**
- [x] [代码能力](/claude-capabilities/core/coding) · 812 汉字 · **published 2026-08-06**
- [x] [视觉能力](/claude-capabilities/core/vision) · 628 汉字 · **published 2026-08-06**
- [x] [长上下文](/claude-capabilities/core/long-context) · 729 汉字 · **published 2026-08-06**
- [x] [工具使用](/claude-capabilities/core/tool-use) · 747 汉字 · **published 2026-08-06**

**v0.3.1 完成标志 ✅：** "想用 Claude API/SDK 的人能选型 + 调 API + 调工具"达成——选型看 [choosing-model](/claude-capabilities/models/choosing-model)，调 API 看 [Messages API 准备页](/claude-capabilities/api/messages)，调工具看 [tool-use](/claude-capabilities/core/tool-use)；"每一步可运行代码"在 v0.3.1 通过最小调用示例落地，**完整**可运行代码到 v0.3.2 SDK 篇重落地。

**v0.3.1 收尾修复 2 处**：

- 章导读 [claude-capabilities/index.md](/claude-capabilities/index.md) 的 mermaid 图"Opus 4.8" → "Opus 5"（与 v0.1 model-selection 对齐）
- 占位 [models/opus.md](/claude-capabilities/models/opus) 的 frontmatter title 同步为 Opus 5

### v0.3.2 · 提示工程 + API + SDK 22 篇（分 3 段，v0.3.2.1 已收官 2026-08-07）

**目标**："每一步都有可运行代码"硬约束集中落地——补 SDK 仓库骨架（anthropic-sdk-python / -typescript / agent-sdk 的最小可复现 example），Cookbook 增加"API/SDK 实战"系列。

#### v0.3.2.1 · 提示工程 6 篇（✅ 2026-08-07 收官）

::: tip v0.3.2.1 收官（2026-08-07 更新）
6 篇正文全部 published，pnpm build 0 死链 / check_page 0 命中。
:::
- [x] [最佳实践](/claude-capabilities/prompting/best-practices) · 845 汉字 · **published 2026-08-07**
- [x] [System Prompt 设计](/claude-capabilities/prompting/system-prompts) · 641 汉字 · **published 2026-08-07**
- [x] [思维链](/claude-capabilities/prompting/chain-of-thought) · 852 汉字 · **published 2026-08-07**
- [x] [Few-shot 示例](/claude-capabilities/prompting/few-shot) · 784 汉字 · **published 2026-08-07**
- [x] [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml) · 641 汉字 · **published 2026-08-07**
- [x] [常用模板](/claude-capabilities/prompting/templates) · 615 汉字 · **published 2026-08-07**

**v0.3.2.1 完成标志 ✅：** "想 prompt 调优的人能拿到 8 条核心原则 + 5 种设计模式 + 12 个实战模板"达成；与 v0.3.1 core/reasoning / extended-thinking 形成 prompt 层 vs API 层分工。

**v0.3.2.1 收尾合规**：每篇 published 都同步去除 sidebar 🚧 标记（CLAUDE.md 第 95 行红线）——本次 6 篇 commit 都已正确处理。

#### v0.3.2.2 · API 9 篇（✅ 2026-08-07 收官）

::: tip v0.3.2.2 收官（2026-08-07 更新）
9 篇正文全部 published，pnpm build 0 死链 / check_page 0 命中。"每一步可运行代码"硬约束集中落地——每篇含完整 Python + TypeScript + curl 示例，复制即用。
:::
- [x] [Messages API](/claude-capabilities/api/messages) · 553 汉字 · **published 2026-08-07**
- [x] [Tool Use API](/claude-capabilities/api/tool-use) · 296 汉字 · **published 2026-08-07**
- [x] [流式响应](/claude-capabilities/api/streaming) · 344 汉字 · **published 2026-08-07**
- [x] [结构化输出](/claude-capabilities/api/structured-outputs) · 291 汉字 · **published 2026-08-07**
- [x] [Prompt Caching](/claude-capabilities/api/prompt-caching) · 370 汉字 · **published 2026-08-07**
- [x] [Message Batches](/claude-capabilities/api/message-batches) · 305 汉字 · **published 2026-08-07**
- [x] [Files API](/claude-capabilities/api/files) · 314 汉字 · **published 2026-08-07**
- [x] [Token Counting](/claude-capabilities/api/token-counting) · 248 汉字 · **published 2026-08-07**
- [x] [Admin & Usage](/claude-capabilities/api/admin-usage) · 223 汉字 · **published 2026-08-07**

**v0.3.2.2 完成标志 ✅：** "想用 Claude API 的人能调通 9 大端点"达成——Messages / Tool Use / Streaming / Structured Outputs / Prompt Caching / Batches / Files / Token Counting / Admin & Usage，每篇含完整可运行代码（curl + Python + TypeScript），与 v0.3.1 core/tool-use 视角分工（核心能力 vs 协议层）。

**v0.3.2.2 收尾合规**：9 篇 commit 都正确处理 sidebar 🚧 同步（CLAUDE.md 第 95 行）。

#### v0.3.2.3 · SDK 7 篇（✅ 2026-08-07 收官）

::: tip v0.3.2.3 收官（2026-08-07 更新）
7 篇正文全部 published。v0.3.2 段（提示工程 6 + API 9 + SDK 7 = 22 篇）**整段收官**。
:::
- [x] [SDK 概览](/claude-capabilities/sdk/overview) · 578 汉字 · **published 2026-08-07**
- [x] [Python SDK](/claude-capabilities/sdk/python-sdk) · 281 汉字 · **published 2026-08-07**
- [x] [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk) · 193 汉字 · **published 2026-08-07**
- [x] [Agent SDK](/claude-capabilities/sdk/agent-sdk) · 205 汉字 · **published 2026-08-07**
- [x] [Tool Runner](/claude-capabilities/sdk/tool-runner) · 185 汉字 · **published 2026-08-07**
- [x] [Managed Agents](/claude-capabilities/sdk/managed-agents) · 248 汉字 · **published 2026-08-07**
- [x] [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk) · 198 汉字 · **published 2026-08-07**

**v0.3.2.3 完成标志 ✅：** "客户端封装全景"达成——3 官方 SDK（Python / TypeScript / Agent SDK）+ 4 高层封装（Tool Runner / Managed Agents / Claude Code SDK / overview）覆盖完整客户端生态，与 v0.3.2.2 API 协议层分工（HTTP vs 客户端封装）。

**v0.3.2 段全段收官 ✅：** 6 提示工程 + 9 API + 7 SDK = 22 篇全部 published。"每一步都有可运行代码"硬约束全面落地。

**v0.3.2.3 收尾合规**：7 篇 commit 都正确处理 sidebar 🚧 同步（CLAUDE.md 第 95 行）。

**未完成（v0.3.2 收尾遗留）**：roadmap 段"examples/ 仓库骨架"规划里 `anthropic-sdk-python-minimal` / `-typescript-minimal` / `agent-sdk-minimal` 3 个仓库**未实际起骨架**——文档讲了"仓库结构应该是 X"但没真做。**v0.3.3 之前**或 v0.3.3 收官时一并补。

### v0.3.3 · MCP 协议层 + Agentic + 产品面 12 篇（✅ 2026-08-07 收官）

::: tip v0.3.3 收官（2026-08-07 更新）
v0.3.3 段 12 篇正文全部 published。**v0.3 整段（46 篇）全部收官**——模型家族 6 + 核心能力 6 + 提示工程 6 + API 9 + SDK 7 + MCP 协议 3 + Agentic 3 + 产品面 6 = 46 篇。
:::

**MCP 协议层 3**（与 v0.2 mcp/* 使用层分工）：

- [x] [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec) · 457 汉字 · **published 2026-08-07**
- [x] [Server 作者指南](/claude-capabilities/mcp-protocol/server-authoring) · 350 汉字 · **published 2026-08-07**
- [x] [Client 实现要点](/claude-capabilities/mcp-protocol/client-implementation) · 327 汉字 · **published 2026-08-07**

**Agentic 3**（多 agent 协作 / Computer Use / 安全）：

- [x] [Computer Use](/claude-capabilities/agentic/computer-use) · 321 汉字 · **published 2026-08-07**
- [x] [多 Agent 模式](/claude-capabilities/agentic/multi-agent-patterns) · 423 汉字 · **published 2026-08-07**
- [x] [安全](/claude-capabilities/agentic/safety) · 524 汉字 · **published 2026-08-07**

**产品面 6**（Anthropic 产品矩阵）：

- [x] [Claude.ai](/claude-capabilities/surfaces/claude-ai) · 434 汉字 · **published 2026-08-07**
- [x] [Artifacts](/claude-capabilities/surfaces/artifacts) · 279 汉字 · **published 2026-08-07**
- [x] [桌面应用](/claude-capabilities/surfaces/desktop-app) · 339 汉字 · **published 2026-08-07**
- [x] [Web 应用](/claude-capabilities/surfaces/web-app) · 358 汉字 · **published 2026-08-07**
- [x] [移动端](/claude-capabilities/surfaces/mobile) · 283 汉字 · **published 2026-08-07**
- [x] [Claude in Slack](/claude-capabilities/surfaces/claude-in-slack) · 215 汉字 · **published 2026-08-07**

**v0.3.3 完成标志 ✅：** "v0.3 整段收官"达成——46 篇全 published，覆盖 Claude 完整能力图谱（模型 / 核心能力 / 提示工程 / API / SDK / MCP 协议 / Agentic / 产品面）。

**v0.3 完成标志 ✅（roadmap 原定）**：
> "一个想构建 AI 应用的工程师，能在这里选型、选模型、选 API/SDK、选提示技巧，且每一步都有可运行代码。"

达成路径：
- **选型 / 选模型** → [模型家族总览](/claude-capabilities/models/overview) + [选型（API 视角）](/claude-capabilities/models/choosing-model)
- **选 API** → [Messages API](/claude-capabilities/api/messages) 9 篇
- **选 SDK** → [SDK 概览](/claude-capabilities/sdk/overview) 7 篇
- **选提示技巧** → [最佳实践](/claude-capabilities/prompting/best-practices) 6 篇
- **每一步可运行代码** → v0.3.2.2 API 9 + v0.3.2.3 SDK 7 篇完整落地

**v0.3.3 收尾合规**：12 篇 commit 都正确处理 sidebar 🚧 同步（CLAUDE.md 第 95 行）。

**v0.3 收尾遗留**：

1. `examples/` 仓库骨架 `anthropic-sdk-python-minimal` / `-typescript-minimal` / `agent-sdk-minimal` 3 个**未实际起**（roadmap 规划了但没做）
2. v0.3.3 claude-ai.md / artifacts.md 等产品面页未在 roadmap 里更新 sidebar 链接（v0.3.3 收尾时 sidebar 同步处理了 P() 去包裹，链接部分后续 review 时补）

**目标**：补齐横切参考（协议 / 安全 / 形态），与 v0.1/v0.2 已 published 文档做最后一遍交叉引用核对。

预计 2-3 周。

**v0.3 完成标志：** 一个想构建 AI 应用的工程师，能在这里选型、选模型、选 API/SDK、选提示技巧，且每一步都有可运行代码。v0.3.1 达成选型 / 模型 / 工具部分；v0.3.2 达成 API / SDK / 提示工程的可运行代码部分；v0.3.3 补齐横切。

## v0.4+ · 精修与工程化

### v0.4.1 · 死链检查基础设施（✅ 收官 2026-08-08）

**commit `018111a`**：

- `lychee.toml`（49 行配置）/ `scripts/check-links.sh`（本地命令包装）/ `.github/workflows/lychee.yml`（CI workflow，failMode=warning）
- `contributing/link-checking.md`（197 行操作文档）
- `package.json` 加 `pnpm check-links` script
- `CLAUDE.md` 第 96 行升级为"跑 `pnpm build` + 跑 `pnpm check-links` 验死链"
- `.gitignore` 加 `.lycheecache` + `scripts/.lychee-out`

### v0.4.2 · 死链 0 错通过 + failMode=error（✅ 收官 2026-08-08）

**commit `58b9363`**：

- lychee 0.24 schema 升级（verbose 字符串 / accept 数组 / root_dir / fallback_extensions）
- 3 处 `messages-batches` URL 拼错修复
- ~20 类 false positive 排除（coding.jd.com / logo/hero/favicon / docs.claude.com 迁移中 / npmjs 反爬 / claude.ai 403 / aws timeout / platform 废弃 API 路径等）
- `failMode: warning` → `error`
- check-links.sh 用 `--files-from` 避 0.24.2 CLI 多 glob bug
- `contributing/link-checking.md` 升级（5 场景 + 调试段 + 已知限制）

**实测**：139 个 .md 0 错通过。

### v0.4.3 · 信息架构 review + LLM landscape 模块（✅ 收官 2026-08-11）

**commit `7b24083`（架构 review）**：

- `contributing/architecture-review-2026-08-10.md`（published）—— 133 个 .md 盘点 + 4 类问题 + 4 类修正建议
- sidebar contributing 段加 "架构 review" entry

**commit `47dfeba`（LLM landscape 骨架）**：

- 顶级新目录 `llm-landscape/`（9 篇 stub）
- 5 厂商：Anthropic / OpenAI / Moonshot / Zhipu / Qwen
- 配套：architecture / comparison / selection-guide
- sidebar 顶级加 "LLM landscape" 段

**配套收尾（本阶段）**：

- roadmap.md lastUpdated 升级 + v0.4.1/4.2/4.3 子段
- claude-code/index.md + cookbook/index.md 残留 🚧 清理
- llm-landscape/index.md 入口段升级

### v0.4+ · 剩余路线（v0.5+ 候选）

**内容层：**

- Cookbook 案例扩充到 10+ 篇（每篇必须别处查不到、近 90 天可复现）—— 暂缓
- 破坏性更新回溯与"迁移指南"专题
- 中文语境专项：中文提示词技巧 / 中文代码注释 / 繁简处理
- awesome-claude 4 篇新主题（superpower / sdd / sdd-workflow / product-pipeline）—— 暂缓（与现有已覆盖）
- v0.5 阶段 1：llm-landscape 9 篇 stub 填实（先做 architecture 总览 + Anthropic 1 篇试水）
- v0.5 阶段 2：claude-code/tools/ 8 个工具页补全（核心使用入口，最高 ROI）
- v0.5 阶段 3：claude-code/ecosystem/ 4 个 IDE 集成（VS Code / JetBrains / Neovim / 企业部署）
- v0.5 阶段 4：reference/ 4 段速查（基于已 published 内容做"提炼"段）
- v0.5 阶段 5：cookbook/ 3 个 stub 扩写
- v0.5 阶段 6：跨工具工程化方案文档（multi-tool-strategy.md）—— Codex/Claude Code/Cursor/Trae 兼容
- v0.5 阶段 7：每月 lastUpdated 巡检 + changelog 体系

**工程层：**

- Algolia DocSearch（或 pagefind 保留本地搜索能力）
- CI 部署：GitHub Actions / coding.jd.com Pages
- 术语 lint（vale.sh + 自定义词典）
- 版本切换（Claude Code v1 / v2 文档共存，若需）
- SEO 优化：中文标题 + 英文关键词副标题
- i18n 英文版（如有精力）

**协作层：**

- 若开源到 GitHub 公开：GitHub Issues 收集读者提问 → 补文档
- 若继续私有：每季度做一次「归档 vs 更新」决策

## 版本与命名约定

- 主版本号（v0.1 → v0.2）：主线内容里程碑
- 次版本号（v0.1.1）：同一主线里的小批量交付
- 每次里程碑合入 `main` 时打 tag：`v0.1.0` / `v0.2.0` …
- 每篇文档 frontmatter 的 `status: published` 才算"进版"

## 风险与止损

**~~Fable 5 定位风险~~ · 2026-07-24 已核实解除**

三个官方源交叉核实完成——`code.claude.com/model-config` / `platform.claude.com/models/overview` / `claude.com/blog · Choosing a Claude model`——事实（`$10/$50 per MTok`、1M context、adaptive thinking always on、"specialist for long-running agents"）已落到 [claude-code/basics/model-selection](/claude-code/basics/model-selection)，未来写 [claude-capabilities/models/fable](/claude-capabilities/models/fable) 时直接引用。

**内容膨胀风险**

若某版本发现自己在填空而不是在解决实际问题，立刻暂停扩张，回到"打磨 20 篇最常用"的模式。

**孤军奋战风险**

单人维护 100+ 篇长期不可持续。视情况：

- v0.2 结束前决定：是否开源到 GitHub 接受 PR
- v0.3 结束前决定：是否邀请合作者

## 参考

- [Diátaxis 文档框架](https://diataxis.fr/) — 四象限（概念/操作/参考/教程）的划分（访问于 2026-07-23）
- [写作规范](./style-guide)
- [术语表](./glossary)

## 下一步

- 开始写 v0.1 第一篇 → [/getting-started/what-is-claude-code](/getting-started/what-is-claude-code)
- 校准写作模板 → [概念文模板](./template-concept) / [操作文模板](./template-howto)

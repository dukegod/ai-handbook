---
title: '2026-W44 GitHub 周报：harness 被拆成组件，插件层开打规范战'
description: 2026-10-20 ~ 2026-10-26 的 GitHub 热榜与涨星盘点——Google 把 harness 拆成 8 个可自动优化的组件，Anthropic / Google / Cursor 三家同时抢插件分发层
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-26
---

# 2026-W44 GitHub 周报

> **TL;DR**：本周热榜 14 个条目里有 10 个是上周没出现过的新面孔，**换手率高到不能用「连续上榜」当趋势指标**。值得记的两条线：Google Research 的 `harness2` 第一次把 harness 本身当成**可拆解、可被模型自动优化**的工程对象；Anthropic、Cursor、Google 三家同时把「插件包」当分发单元，**插件层的规范战比协议战先开打**。

📅 数据窗口：2026-10-20 ~ 2026-10-26 ｜ 榜单来源：GitHub Trending 官方口径

⏱ 预计阅读时间：9 分钟

## 一、本周热榜全表（14 个）

| # | 仓库 | 本周涨星 | 总 star | 语言 | 一句话 |
| --- | --- | ---: | ---: | --- | --- |
| 1 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | **+15,072** | 47,179 | JavaScript | Agent 安全审计 Skill，结论机器可读、验证独立 |
| 2 | [stablyai/orca](https://github.com/stablyai/orca) | **+9,622** | 106,019 | TypeScript | 多 Agent 编排台，worktree 隔离 + 手机端操控 |
| 3 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | +6,903 | 135,395 | Python | 代码库转知识图谱，用遍历代替 grep |
| 4 | [anomalyco/opencode](https://github.com/anomalyco/opencode) | +5,921 | 221,586 | TypeScript | 开源 AI 编码 Agent |
| 5 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +5,612 | 72,287 | TypeScript | 写 HTML 渲染视频，为 Agent 设计 |
| 6 | [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | +4,790 | 142,998 | Python | 节点式扩散模型 GUI 与后端 |
| 7 | [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) | +3,254 | 13,555 | Rust | 跨 20+ harness 的长期记忆与交接 |
| 8 | [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | +2,987 | 79,317 | TypeScript | Agent 联邦：跨信任边界的协作 |
| 9 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | +2,937 | 223,929 | — | 单个 CLAUDE.md 约束 LLM 的编码坏习惯 |
| 10 | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | +2,790 | 33,029 | Python | 11 个岗位角色的 Claude 插件包 |
| 11 | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | +2,245 | 44,590 | Python | Claude Code 官方插件目录 |
| 12 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +1,770 | 30,191 | TypeScript | 手机 / Web / 桌面三端的 Agent 控制面 |
| 13 | [vllm-project/vllm](https://github.com/vllm-project/vllm) | +1,445 | 95,521 | Python | 高吞吐 LLM 推理与服务引擎 |
| 14 | [android/skills](https://github.com/android/skills) | +1,070 | 9,737 | Kotlin | Android 官方 Agent Skills |

## 二、本月热榜 TOP（GitHub Trending `since=monthly`）

| # | 仓库 | 本月涨星 | 总 star | 方向 |
| --- | --- | ---: | ---: | --- |
| 1 | [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | +50,977 | 87,128 | 本地语音模型 |
| 2 | [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | +25,486 | 53,798 | **Agent Memory** |
| 3 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +24,611 | 47,179 | **Agent 安全审计 Skill** |
| 4 | [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | +24,081 | 107,349 | **Agent 组织管理平台** |
| 5 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | +22,882 | 288,942 | Harness 性能优化 |
| 6 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +19,211 | 72,287 | Agent 生成视频 |
| 7 | [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) | +16,847 | 73,881 | AI 工程教程 |
| 8 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | +16,493 | 87,912 | **Harness 设计语言** |
| 9 | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | +14,822 | 94,365 | 逆向框架 |
| 10 | [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) | +12,957 | 41,648 | 免费 LLM API 聚合 |
| 11 | [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) | +11,062 | 19,910 | **Agent 沙箱运行时** |
| 12 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +8,817 | 103,159 | 跨会话记忆注入 |
| 13 | [mksglu/context-mode](https://github.com/mksglu/context-mode) | +8,324 | 32,286 | 上下文优化 |
| 14 | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | +7,932 | 44,590 | 官方插件目录 |
| 15 | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | +7,387 | 33,029 | **岗位角色插件包** |

> 完整 21 条见原始数据快照。

## 三、本周涨星 TOP 10

| 排名 | 仓库 | 本周涨星 | 涨星/存量比 |
| ---: | --- | ---: | ---: |
| 1 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +15,072 | **32%** |
| 2 | [stablyai/orca](https://github.com/stablyai/orca) | +9,622 | 9% |
| 3 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | +6,903 | 5% |
| 4 | [anomalyco/opencode](https://github.com/anomalyco/opencode) | +5,921 | 3% |
| 5 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +5,612 | 8% |
| 6 | [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | +4,790 | 3% |
| 7 | [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) | +3,254 | **24%** |
| 8 | [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | +2,987 | 4% |
| 9 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | +2,937 | 1% |
| 10 | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | +2,790 | 8% |

## 四、新锐仓库（近 30 天新建）

| 仓库 | star | 存活天数 | 方向 |
| --- | ---: | ---: | --- |
| [storytold/photocraft](https://github.com/storytold/photocraft) | 72,915 | 25 | Rust 写的开源照片编辑器 |
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 35,812 | 8 | Android / Google TV 卸载预装软件 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 22,550 | 9 | DeepSeek 模型推理框架 |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 20,684 | 17 | 生成等距图的 Agent Skill |
| [google-research/harness2](https://github.com/google-research/harness2) | 19,723 | 19 | **Google Research 的递归 harness** |
| [storytold/pdfcraft](https://github.com/storytold/pdfcraft) | 17,871 | 25 | Rust 写的开源 PDF 编辑器 |
| [storytold/filmcraft](https://github.com/storytold/filmcraft) | 16,302 | 25 | Rust 写的非线性视频编辑器 |
| [storytold/wordcraft](https://github.com/storytold/wordcraft) | 16,076 | 18 | Word 的 clean-room Rust 复刻 |
| [openai/math](https://github.com/openai/math) | 15,509 | 19 | Lean 形式化的数学证明 |
| [storytold/lightcraft](https://github.com/storytold/lightcraft) | 14,662 | 25 | Rust 写的非破坏性 RAW 照片编辑器 |

> `storytold` 一个组织在近 30 天里连出 **9 个万星仓库**（photocraft / pdfcraft / filmcraft / wordcraft / lightcraft / vectorcraft / effectcraft / cadcraft / gridcraft），合计 169,762 star，且全部是「用 Rust 从零重写一个成熟商业软件」。上周是 4 个，本周变成 9 个——**这是本周最值得注意的造星现象，模式是组织化批量复刻 + 干净室实现**。

## 五、本周判断

1. **周榜对 AI 项目已经不能当趋势指标用。** 本周 14 个条目里 **10 个是上周没出现的新面孔**，上周 11 个掉榜（含 W43 冠军 `morluto/rea`，上周 +157,631，本周直接消失）。4 个留榜项目的涨星**全部在降温**：`claude-plugins-official` 从 +5,650 掉到 +2,245（-60%）、`hyperframes` 从 +5,994 掉到 +5,612。**结论：周榜是「当周注意力快照」，判断趋势必须看月榜 + 是否连续两周在榜。**
2. **两种涨星模式必须分开判读，而且热度 ≠ 维护。** 「新项目爆发」型的特征是周涨星占存量比例高：`security-audit-skill` 32%、`ai-memory` 24%、月榜的 `OpenShell` 56%、`hindsight` 47%。「大项目持续吸量」型比例低但绝对量大：`opencode` 只占 3% 仍有 +5,921。**但比例和热度都不能替代维护状态**——`security-audit-skill` 自 9/14 未 push、没有 release，却拿下本周涨星第一；`andrej-karpathy-skills` 自 4/20 未 push、没有 license，却攒到 223,929 star。
3. **harness 第一次成为可被模型自动优化的工程对象。** `google-research/harness2` 把 harness 拆成 8 个可编辑组件（system prompt、guardrails、memory、tool guidance、subagents、skills、scripts、plugins），用 **Propose–Probe–Compose** 在同一任务上反复试探并合成新 harness，3 个 benchmark、4 种 model-harness 配置下最高提升 11.5 分。**上周的 ECC 是「人手工调优 harness」，这周是「让模型自己改 harness」——harness 工程从手艺变成方法的标志。**
4. **插件 / Skill 层的规范战正式开打，而且发生在协议之前。** `anthropics/knowledge-work-plugins`（11 个岗位插件 = skills + connectors + slash commands + sub-agents）、`android/skills`（Google 出品，跟随 agentskills.io 开放标准，**明确只做「eval 显示 LLM 不擅长」的用例**）、`cursor/plugins`（自有 `.cursor-plugin/plugin.json` 清单）三家同时把「插件包」当分发单元。**Agent 资产的分发与发现层正在先于 A2A 协议统一成型**——这正是 A2A 之前的那一层。
5. **「人在环内」的入口正从 IDE 挪到常驻小部件和手机。** `orca` 的手机 companion、`coucou` 的 Mac 刘海常驻 + iPhone 审批权限请求、`t3code` 的四端控制面、`paperclip` 的 24/7 自治 + 预算治理。**审批入口的竞争和协议竞争同步发生，而审批入口天然是权限边界——谁掌握它，谁就掌握了 Agent 的行为边界。**

## 六、数据口径与局限

- 涨星数一律采用 GitHub Trending 页面自带的官方口径（`stars this week` / `this month`），不做二次推算。
- GitHub REST `/stargazers` 接口已全量下线，无法自算任意时间窗的精确涨星；OSS Insight 等第三方数据自 2026-05 起严重降级、仅为下界，只作趋势佐证。
- Trending 榜单每页仅 15 个条目（GitHub 已从 25 下调），本周实际抓到 **14 条**——**不是 Top 15 之外的完整榜单**。
- 「涨星/存量比」为本周（或本月）涨星 ÷ 当前总 star，用于区分「新项目爆发」与「大项目持续吸量」。
- 「新锐仓库」由 GitHub Search API 按 `created:` 过滤近 30 天、star > 300 的新建仓库排序得出，与周榜口径不同，两表不可直接相加。

## 下一步

- 按下面的深读逐个展开，或直接挑感兴趣的仓库看
- 想理解这轮基础设施升温背后的协议层动向 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)

## 本期深读

| 仓库 | 一句话 | 方向 |
| --- | --- | --- |
| [google-research/harness2](./harness2.md) | 把 harness 拆成 8 个组件，让模型自己改 harness | Harness 工程 |
| [cloudflare/security-audit-skill](./security-audit-skill.md) | 找漏洞的 Agent 不能是验证漏洞的 Agent | Agent 运行时安全 |
| [akitaonrails/ai-memory](./ai-memory.md) | 20+ harness 共用一份记忆，交接是有归属的协议 | 记忆系统 |
| [stablyai/orca](./orca.md) | 30+ CLI Agent 并排跑，每个一个隔离 worktree | 多 Agent 协作 |
| [Graphify-Labs/graphify](./graphify.md) | 用 AST 知识图谱替代 grep，每条边标明是抽取还是推断 | 上下文工程 |
| [pbakaus/impeccable](./impeccable.md) | 62 条确定性规则，把设计审美变成可执行检查 | Harness 规则化 |
| [paperclipai/paperclip](./paperclip.md) | 给 Agent 团队配预算、权限和审计日志 | Agent 组织治理 |
| [anthropics/knowledge-work-plugins](./knowledge-work-plugins.md) | 11 个岗位插件，把角色、工具、流程打包成可分发单元 | 插件生态 |
| [android/skills](./android-skills.md) | Google 出品，只做 eval 显示 LLM 不擅长的用例 | Skill 生态标准 |
| [Louis-CFM/coucou](./coucou.md) | 刘海常驻小组件 + 手机端审批 Agent 的权限请求 | 人在环内 |

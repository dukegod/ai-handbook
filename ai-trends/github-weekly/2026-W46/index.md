---
title: '2026-W46 GitHub 周报：NVIDIA 下场做语义层，Agent 从「单技能」转向「多 Agent 团队」'
description: '2026-11-03 ~ 2026-11-09 的 GitHub 热榜与涨星盘点——17 个周榜条目里 15 个是 Agent / harness / skill 类，NVIDIA 发布 auto-ontology 把语义层做成 Agent 的上下文来源，t3code 涨星 +15,379 拿下冠军，OpenMausBot 把多 Agent 团队做成聊天应用'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-09
---

# 2026-W46 GitHub 周报

📅 数据窗口：2026-11-03 ~ 2026-11-09 ｜ 来源：GitHub Trending 官方口径

> **TL;DR**：本周 17 个周榜条目里 **15 个面向 Agent 工具链**，合计吸走 **86,736 star，占周榜总涨星 92,392 的 93.9%**。三条值得记：**NVIDIA 亲自下场做 Agent 的语义层**（`auto-ontology` 单周 +9,327，涨星占存量 88.6%）；**`t3code` 拿下涨星冠军 +15,379（占存量 29.2%）**——一个「Agent harness 控制面」把注意力从「写 skill」拉到「管 harness」；**`OpenMausBot` 把多 Agent 团队做成了聊天应用**，靠 permission broker 挡审批。

## 一、本周热榜全表（17 个）

> 榜位按 **Trending 页面顺序**（趋势分排名）列出，**与涨星排序不一致**——涨星排序见第三节。

| 榜位 | 仓库 | 本周涨星 | 总 star | 语言 | 一句话 |
| --- | --- | ---: | ---: | --- | --- |
| 1 | [NVIDIA/auto-ontology](https://github.com/NVIDIA/auto-ontology) | **+9,327** | 10,523 | Python | 语义图谱层 |
| 2 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +6,443 | 114,978 | TypeScript | 跨会话记忆 |
| 3 | [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk) | +2,313 | 12,153 | Rust | 并行 Agent 工作区 |
| 4 | [anthropics/skills](https://github.com/anthropics/skills) | +3,169 | 189,801 | Python | 官方 Skills 规范源 |
| 5 | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | +5,235 | 37,083 | Shell | 49 个 Agent 工作室 |
| 6 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | +7,621 | 18,553 | TypeScript | 聊天式 Agent 团队 |
| 7 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | **+15,379** | 52,694 | TypeScript | Harness 控制面 |
| 8 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +6,356 | 51,077 | CSS | 反 AI 味设计 |
| 9 | [Renhuai123/ziwei-doushu](https://github.com/Renhuai123/ziwei-doushu) | +4,191 | 17,061 | TypeScript | 紫微斗数排盘 + AI 解读 |
| 10 | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | +8,342 | 99,981 | Python | 自适应反爬（含 Agent Skill） |
| 11 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | +2,190 | 47,777 | Rust | Agent 浏览器 CLI |
| 12 | [mattpocock/skills](https://github.com/mattpocock/skills) | +9,635 | 318,693 | Shell | 工程师用 skill 合集 |
| 13 | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | +1,857 | 11,762 | Markdown | 界面设计 skill |
| 14 | [github/spec-kit](https://github.com/github/spec-kit) | +4,045 | 148,768 | Python | Spec 驱动开发包 |
| 15 | [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) | +1,706 | 15,620 | Python | 开源 PR 审查 |
| 16 | [hyprwm/Hyprland](https://github.com/hyprwm/Hyprland) | +1,465 | 40,573 | C++ | Wayland 合成器（非 AI） |
| 17 | [blader/humanizer](https://github.com/blader/humanizer) | +3,118 | 66,630 | Python | 去 AI 味写作 |

## 二、本月热榜 TOP（GitHub Trending `since=monthly`，按本月涨星降序）

| # | 仓库 | 本月涨星 | 总 star | 涨星/存量比 | 方向 |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | [morluto/rea](https://github.com/morluto/rea) | +425,123 | 444,235 | **95.7%** | **逆向工程 MCP** |
| 2 | [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | +50,169 | 105,173 | 47.7% | 本地语音克隆 |
| 3 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +40,289 | 67,038 | 60.1% | **Agent 安全审计 Skill** |
| 4 | [boykopovar/AnyPS5](https://github.com/boykopovar/AnyPS5) | +39,354 | 52,376 | 75.1% | PS5 可执行移植 |
| 5 | [storytold/artcraft](https://github.com/storytold/artcraft) | +33,780 | 39,959 | 84.5% | 创作引擎 |
| 6 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | +28,008 | 106,308 | 26.3% | **编码 Agent 的设计词汇表** |
| 7 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +25,840 | 52,694 | 49.0% | **Harness 控制面** |
| 8 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +22,360 | 81,181 | 27.5% | Agent 写视频 |
| 9 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +21,146 | 51,077 | 41.4% | 反 AI 味设计 |
| 10 | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | +17,344 | 98,836 | 17.5% | 逆向框架 |
| 11 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +17,296 | 114,978 | 15.0% | 跨会话记忆 |
| 12 | [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | +16,065 | 57,126 | 28.1% | 终身个性化辅导 |

> 本月榜抓到 12 条，完整清单见原始数据快照。

## 三、本周涨星 TOP 10

| 排名 | 仓库 | 本周涨星 | 涨星/存量比 | 判读 |
| ---: | --- | ---: | ---: | --- |
| 1 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +15,379 | 29.2% | 持续爆发，月内累计 +25,840 |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | +9,635 | **3.0%** | 巨量存量持续吸量 |
| 3 | [NVIDIA/auto-ontology](https://github.com/NVIDIA/auto-ontology) | +9,327 | **88.6%** | 新项目爆发 |
| 4 | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | +8,342 | 8.3% | 存量走量 |
| 5 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | +7,621 | 41.1% | 新项目爆发 |
| 6 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +6,443 | 5.6% | 存量走量 |
| 7 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +6,356 | 12.4% | 持续吸量 |
| 8 | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | +5,235 | 14.1% | 持续吸量 |
| 9 | [Renhuai123/ziwei-doushu](https://github.com/Renhuai123/ziwei-doushu) | +4,191 | 24.6% | 垂直领域新项目 |
| 10 | [github/spec-kit](https://github.com/github/spec-kit) | +4,045 | 2.7% | 大项目持续吸量 |

## 四、新锐仓库（近 30 天新建）

> 数据源：GitHub Search API 按 `created:>2026-10-10 stars:>300` 过滤，命中 1,036 个仓库。

| 仓库 | star | 存活天数 | 方向 |
| --- | ---: | ---: | --- |
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 54,838 | 23 | 电视盒子清理 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 25,685 | 24 | **DeepSeek 推理框架**（上期已深读） |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 23,016 | 9 | **「理解任何软件」工具** |
| [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) | 21,322 | 9 | **DeepSeek Agent 原型**（上期已深读） |
| [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) | 18,181 | 22 | GeForce 提速 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 16,373 | 15 | **DeepSeek Harness 进手机** |
| [seedds/nxnative](https://github.com/seedds/nxnative) | 13,789 | 27 | 原生化工具 |
| [heydamir/unslop](https://github.com/heydamir/unslop) | 12,092 | 11 | 反 AI 味 UI |
| [pengchujin/aerial-tv](https://github.com/pengchujin/aerial-tv) | 10,772 | 20 | 给国产电视做干净桌面 |
| [l0ng-ai/openidea](https://github.com/l0ng-ai/openidea) | 7,931 | 19 | Rust 重写的 IntelliJ 风格 IDE |

**两条新信号**：**DSH 生态开始往终端下沉**——`dsh-Go`（Dart，15 天，16,373 star）把 DeepSeek Harness 装进口袋；**微软亲自下场做 Agent 成本控制**——`microsoft/TokenEconomizer`（27 天，5,306 star，star 榜第 27 位）自述是「Experience-Driven Cost Control for Coding Agents」，**大厂开始把 token 成本当成要治理的一等指标**。

## 五、本周判断

1. **NVIDIA 发布的不是模型，是 Agent 的「可信上下文层」。** `auto-ontology` 单周 +9,327，**涨星占存量 88.6%**。README 第一句就是主张：**「一个收入指标答得再快，如果数字是错的就没有价值」**——建语义目录 / 本体层，生成 SQL 后**对照已认证的定义和血缘做校验**，答案带 provenance，经 MCP / CLI / API 喂给任意 harness。**这和 W45 的 `claude-seo` 是一件事的两半**：一个管「系统能不能被 Agent 读懂」，一个管「数字对不对」。

2. **涨星冠军从「skill」换成了「harness 控制面」，注意力上移一层。** `t3code` 单周 +15,379、涨星占存量 29.2%、月内累计 +25,840（占存量 49.0%），把「写一个 skill」压到第二。爆发点是**同时控 Claude Code、Codex、Cursor、Grok Build、OpenCode、Antigravity、fx**，配手机远控、worktree 隔离、permission modes。**上期「Skill 生态吞掉周榜」要修正为「Skill 是入口，harness 控制面才是这个季度的竞争焦点」**——skill 决定 Agent 会做什么，控制面决定**哪个 Agent 在哪个工作区、用谁的订阅、在谁的权限下做**。

3. **多 Agent 下沉到「可用的产品形态」，而产品的核心不是协作，是权限。** `OpenMausBot` 单周 +7,621、涨星占存量 41.1%。README 写死了要替代的四个闭源产品：**xAI 的 Grok Bot、Meta 的 Muse、OpenAI 的 dots、Manus 的 Cue**——**四个闭源个人 Agent 产品七周内集中发布，是这波热度真正的源头**。两点值得抄：**每个 bot 是本地跑 CLI 的真 agent**，复用你自己的登录和订阅；**permission broker 是独立一层**，**审批是架构组件而不是提示词里的一句话**。

4. **Skill 生态分成两条路线：通用工程方法 vs 垂类设计规范。** `mattpocock/skills` 单周 +9,635，涨星只占存量 3.0% 但绝对值排第二。README 开头就站队：**明确反对流程框架「占有流程」**，主张 skill 要小、可改、可组合，按「谁能调用」分 user-invoked 与 model-invoked 两轴。另一边 `jakubkrehel/skills`（+1,857）**全是界面维度**：排版、颜色、可访问性、布局、文案，外加 `break`（把组件渲染成所有可能状态）。**「反 AI 味设计」已从单项目长成一组竞品**。

5. **多 Agent 的组织形态开始被当作正经的架构问题解，而不是模板套用。** `Claude-Code-Game-Studios`（+5,235，涨星占存量 14.1%）定义了 **49 个 Agent 的五条协作规则**：**垂直委派**、**同级可咨询但不能做绑定性跨域决策**、**冲突向上升级到共同父级**、**跨部门变更由 `producer` 协调**、**Agent 不改自己领域外的文件除非显式委派**。另一面是它明确写 **「Collaborative, Not Autonomous」**：提问 → 给方案 → 你决定 → 出草稿 → 你批准，**没有你的签字什么都不落盘**。

## 六、数据口径与局限

- 涨星数一律采用 GitHub Trending 页面自带的官方口径（`stars this week` / `this month`），不做二次推算；已用独立解析复核 Trending 原始 HTML，17 条周榜与 12 条月榜逐条一致。
- GitHub REST `/stargazers` 接口已全量下线，无法自算任意窗口的精确涨星；本期未采用 OSS Insight（自 2026-05 起官方标注严重降级，仅能作趋势下界）。
- Trending 每页仅 15 个条目（GitHub 已从 25 下调），本周抓到 **17 条**——**不等于「Top 15 之外没有更多」**。
- 「涨星/存量比」= 涨星 ÷ 总 star，区分「新项目爆发」与「大项目持续吸量」，对新项目天然偏高。第一节「榜位」是 **Trending 页面顺序**，**不是涨星排名**。
- **需标注的两处异常**：`morluto/rea` 月榜涨星 +425,123、占存量 95.7%，却**未进本周周榜**，OSS Insight 返回 500、`/stargazers` 要求鉴权，**该量级「未核实」**；`cloudflare/security-audit-skill` 月涨 +40,289，但最后一次提交是 **2026-09-14**、无 release——**「流量先于工程」的反例**。

## 下一步

- 按下面的深读逐个展开，或挑感兴趣的仓库看
- 想看这轮升温背后的协议动向 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)

## 本期深读

| 仓库 | 一句话 · 方向 |
| --- | --- |
| [NVIDIA/auto-ontology](./auto-ontology.md) | 语义层 + provenance |
| [pingdotgg/t3code](./t3code.md) | 涨星冠军 · 控制面 |
| [milind-soni/OpenMausBot](./openmausbot.md) | 权限 broker |
| [max-sixty/worktrunk](./worktrunk.md) | worktree 隔离 |
| [mattpocock/skills](./mattpocock-skills.md) | 反流程占有 |
| [jakubkrehel/skills](./interface-skills.md) | 界面 skill 合集 |
| [Donchitos/Claude-Code-Game-Studios](./game-studios.md) | 五条协作规则 |
| [vercel-labs/agent-browser](./agent-browser.md) | a11y 树 + ref |
| [github/spec-kit](./spec-kit.md) | 可组合原语 |
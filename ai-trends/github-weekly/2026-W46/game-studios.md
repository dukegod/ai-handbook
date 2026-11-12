---
title: 'Donchitos/Claude-Code-Game-Studios：49 个 Agent 的组织问题，靠五条规则解决'
description: Claude Code Game Studios 深度解读——垂直委派 / 同级咨询 / 冲突升级 / 变更传播 / 领域边界这五条多 Agent 协作规则，以及 15 个 hook 与 14 条 path-scoped rule 如何把约束落到文件层面
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-09
---

# Donchitos/Claude-Code-Game-Studios：49 个 Agent 的组织问题，靠五条规则解决

> **TL;DR**：37,083 star、4,882 fork、96 open issue，MIT。**本周涨星 +5,235，涨星占存量 14.1%**。README 标题写着 **49 agents. 74 skills. One coordinated AI team.**——但真正值得学的不是 49 这个数字，而是它给 49 个 Agent **定下的五条协作规则**和 **15 个 hook**。

📅 数据窗口：2026-11-03 ~ 2026-11-09 ｜ 🏷️ 多 Agent 协作 / Harness 工程 ｜ 本周涨星 +5,235 ｜ 总 star 37,083

## 是什么

[Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) 是一套**放进 `.claude/` 目录的 Claude Code 模板**——把一次会话变成一个完整的游戏开发工作室。

它的规模数字是：**49 个 Agent**（设计、程序、美术、音频、叙事、QA、制作）、**74 个 skill**（`/start`、`/design-system`、`/create-epics`、`/dev-story` 等覆盖工作流各阶段）、**15 个 hook**、**14 条 rule**。

README 对「为什么」的表述很实在：**「Building a game solo with AI is powerful — but a single chat session has no structure. No one stops you from hardcoding magic numbers, skipping design docs, or writing spaghetti code.」**——**单会话没有结构，需要一个像真实工作室那样的组织替代它。**

它也回答了一个容易被误解的问题：**「Does it produce games, or documents?」**——**「It runs the game and looks at it」**。

## 技术亮点

**第一，五条协作规则是整个项目最值钱的部分。** README 的 "Agent Coordination" 原文：

1. **垂直委派**——directors 委派给 leads，leads 委派给 specialists。
2. **同级咨询**——同层 Agent 可以互相咨询，**但不能做有约束力的跨域决策**。
3. **冲突解决**——分歧向上升级到共同父级（设计归 `creative-director`，技术归 `technical-director`）。
4. **变更传播**——跨部门变更由 `producer` 协调。
5. **领域边界**——**Agent 不会修改自己领域之外的文件，除非有显式委派**。

**这五条合起来是一套完整的组织法**：谁向谁汇报、谁能决定什么、吵起来找谁、跨边界归谁、**谁能碰哪些文件**。**尤其第 5 条——「不越界改文件」——把多 Agent 最常见的失败模式（互相覆盖改动）在规则层面掐死了。**

**第二，它明确写「Collaborative, Not Autonomous」。** 协作协议五步：**Ask**（Agent 先提问，不直接给方案）→ **Present options**（给 2-4 个方案附优缺点）→ **You decide**（你来定）→ **Draft**（出草稿）→ **Approve**（**没有你的签字什么都不落盘**）。README 补了一句：**「You stay in control. The agents provide structure and expertise, not autonomy.」** `guided` / `autonomous` 设置和 Claude Code 自身的 auto mode 会拿掉部分提问来换速度——**这条边界可调，但默认在「协作」一侧**。

**第三，15 个 hook 把规则从文档变成机制。** 几个关键的：

- **`validate-commit.sh`**：检查硬编码值、TODO 格式、JSON 有效性、设计文档章节，**不符合就提前退出**。
- **`validate-read.sh`**：**拒绝整文件读取超过 40 KB 的设计文档，只返回标题**，让重试只读一节。
- **`log-agent.sh` / `log-agent-stop.sh`**：**Agent 启动与停止的审计轨迹**。
- **`validate-agent-artifact.sh`**：**警告某个 subagent 停止时没有写出它 brief 里指定的那份文件**。

**「拒绝读超长文档、只给标题」这一条特别聪明**——**它是用 hook 治 Agent 的上下文浪费，而不是靠提示词请求 Agent「省着点读」。**

**第四，14 条 path-scoped rule 把编码规范绑在文件路径上。** `src/gameplay/**` 要求数据驱动、delta time、无 UI 引用；`src/core/**` 要求热路径零分配、线程安全、API 稳定；`src/ui/**` 要求不持有游戏状态、**本地化就绪、可访问性**；`design/gdd/**` 要求必需章节；`prototypes/**` **放宽标准但要求 README 和假设文档**。**同一套规则同时映射 Godot、Unity、Unreal 三种目录布局。**

**第五，权限规则与设计哲学都有出处。** `settings.json` 里自动放行测试运行、封禁强制 push、`rm -rf`、读取 `.env`，**Bash 与 PowerShell 两条路径都覆盖**；设计哲学引用 MDA 框架、自我决定理论、心流设计、Bartle 玩家类型和**验证驱动开发**——**这让它的规则集不是拍脑袋。**

## 后续发展建议

**这个项目是「多 Agent 组织形态」目前最完整的一份可抄文本，比任何 A2A 协议草案都具体。** 四个判断：

- **多 Agent 平台真正缺的不是协议，是「组织法」。** 同榜的 `OpenMausBot` 做「多个 bot 各自跑、审批走 broker」，`t3code` 做「控制多个 harness」——**它们解决的是「有几个 Agent」和「怎么启动」**。**但「多个 Agent 一起改一个仓库时，谁说了算、谁不能碰什么」，只有 Game Studios 给了答案。** 内部平台**建议把这五条规则当平台默认行为**：垂直委派层级、同级只咨询不决策、冲突升级路径、跨域变更的协调人、**文件级领域边界**。**尤其第五条「不越界改文件」应该是平台强制的，不该指望 Agent 自觉。**

- **「不写文件就不算完成」这条审计思路值得单独抽出来。** `validate-agent-artifact.sh` 检查**「Agent 停止时有没有写出它 brief 里指定的那份文件」**——**等于给每个 Agent 派了一个可验证的完成契约**，比「Agent 说它做完了」可靠得多。内部平台**建议把「Agent 任务的完成条件」做成可校验的产物清单，而非自然语言描述**——**产出物缺失可被机器发现，是把 Agent 纳入质量体系的最短路径。**

- **hook 是把 Agent 约束从「建议」变成「机制」的正确位置。** 15 个 hook 里最有价值的两条不是拦写入，而是**限上下文（拒读大文档只给标题）**和**记审计（Agent 启停轨迹）**。**hook 的价值不在「阻止危险操作」，而在「减少浪费 + 留下证据」。**

- **「规则按路径生效」是让编码规范可执行的关键抽象。** path-scoped rule 把规范绑到**代码落点**上，**改哪个目录就得满足哪套标准**，而不是写在文档里靠人记住。这和 spec-kit 的「流程原语」是同一思路：**把规范变成按上下文自动生效的机制**。**建议优先做路径级规则，而不是写更长的规范文档。**

**风险与局限**：**37,083 star 配 96 open issue（0.26%）**，维护密度健康；**最新 release 是 v1.2.0（2026-10-19）**，距今 21 天，**不像 `OpenMausBot` 那样每天发版**——说明它**已过大规模迭代期**。**它是最完整的 Claude Code 绑定项目**：Agent 全在 `.claude/agents`，skill 在 `.claude/skills`，hook 走 `.claude/hooks`，**换 harness 基本等于重写**；README 明说 **「This is a template, not a locked framework. Everything is meant to be customized.」**——**定制是它的一部分，但成本由用户承担**。它的**领域假设非常具体**（引擎、美术资产、GDD、叙事 canon），**映射表只覆盖 Godot / Unity / Unreal**——**其他领域要复用，得自己重写那 14 条路径规则**。它**没有 eval、没有效果数据**，49 个 Agent 有没有让游戏做得更好，README 全是机制描述。最后，**15 个 hook 是 Claude Code 特有的机制**，别的 harness 没有等价物——**这既是护城河也是天花板**。

## 下一步

- 想看权限与审批那条线 → [OpenMausBot 深读](./openmausbot.md)
- 想看流程原语怎么组织 → [spec-kit 深读](./spec-kit.md)

## 如果你想

- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看团队落地的方法论 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)

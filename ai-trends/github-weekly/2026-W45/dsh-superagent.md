---
title: 'deepseek-ai/dsh-superagent-prototype：把 Agent 权限写成七个领域概念'
description: DeepSeek 主动型 Agent 系统原型深度解读——Policy / Eval / Mandate / Ticket / Assignment / Subscription 七个概念与三档触发强度如何构成一套可审计的 Agent 授权模型，以及它对内部 Agent 平台设计的启示
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-11-02
---

# deepseek-ai/dsh-superagent-prototype：把 Agent 权限写成七个领域概念

> **TL;DR**：这是 DeepSeek 官方开源的**研究原型**（README 明确写明「not an official DeepSeek product」，且已为发布做了裁剪），1 天拿下 8,965 star。但它真正值钱的不是代码，而是**一份把 Agent 权限写成领域模型的公开设计**：Source / Trigger / Thread / Eval / Mandate / Ticket / Assignment / Subscription 七个概念，加上 **explicit / inferred / not admitted** 三档触发强度。**权限在这里是一等公民，而且权限变更不追溯撤销已发出去的授权**——这套结构和 W43 的 A2A 调研是同一个问题的两面。

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ Agent 平台 ｜ 本周涨星 未进周榜 ｜ 总 star 8,965（存活 1 天）

## 是什么

[deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) 是 DeepSeek 在 2026-10-31 开源的 **dsh-superagent**：一个针对单个 GitHub 仓库的**主动型**编码 Agent，以 bundle 形式打包进 [DeepSeek Harness](https://www.deepseek.com/en/harness/)。

它的行为模式是：监听 GitHub（可选飞书），被允许的人提出请求后，它开一个 work item，**在自己的 Agent session 和独立目录里干活**，然后回到原对话里回一个 PR。Web 面板只显示「需要人处理」的部分。

README 的第一句原则是整个设计的纲：**take as little human attention as possible, and give as much value as possible**——每一条消息、通知、问题、设置、面板元素都要付出别人的注意力，**回报不超过成本就删掉**。作者还写了一句很实在的话：Agent 能替整个团队干活，也能浪费整个团队的注意力，所以**它只在被请求时、或在团队写下的规则允许时才行动**。

配套论文是 *Exploring Super-agent Design: Towards a More Autonomous Agent System*，README 明确说明代码是为发布裁剪过的，**论文里讨论的一些设计是未来方向，本原型并未实现**——这一条读的时候务必注意。

## 技术亮点

**第一，七个领域概念撑起整份授权模型，每个概念只守一条规则。** `001-domain.md` 用一张表列出每个概念的「定义 / 守的规则 / 为什么存在」，几个关键点：

- **Trigger** 是不可变事件，是「审计与幂等的单位」——**接受同一个 Trigger 两次只会产生一个 Ticket**。
- **Mandate** 是「接受这次请求授予了什么」，包含 Policy 版本、范围、强度、命中的规则、发送者在该 Source 上的身份。**它不可变；范围变宽就是新的 Ticket。**
- **Ticket** 是「一份被授权的工作单元」，**只有 Eval 能创建它**，它自己定义自己的状态，不跟随 Executor。
- **Subscription** 是 Ticket 与 Thread 的多对多关系，让**后续讨论能自动到达 Executor，而不需要有人再提一次 Agent**。

**第二，权限强度只有三档，而且判定规则是可枚举的。** `002-authorization.md` 明确列出 **explicit / inferred / not admitted** 三档：名单内的人直接 @ Agent 是 explicit；名单外的人在已有 Ticket 的 Thread 上追问是 inferred；**其他 Bot 的消息一律 not admitted**。每个 Source 有一张 admission table，行是「接收范围」（飞书群、GitHub 的新 Issue / 新 PR / 评论 / 默认分支 CI），列是「名单内未 @ / 名单外 @ 了 / 名单外没 @」三种情况，每格三选一。

**第三，Policy 变更不追溯撤销已有授权，但会打断正在跑的判断。** 这是整套设计里最反直觉、也最值得抄的一条：改了规则，**已经发出去的 Mandate 不会被撤销**（只有人主动 stop 才停），但**正在跑的 Eval 必须丢弃重来**。配套的是：不同 Source 上的身份**永不互相映射**——同一个「人」在飞书和在 GitHub 是两个身份。

**第四，架构文档直接给了代码索引，Engine 是唯一写入方。** `007-architecture.md` 把 Intake / Evals / Tickets / Assignments / Replies 五个部分列成依赖单向流动的表，**所有 Engine 方法都是同步的，每个命令在一个事务里改完聚合**，端口在事务里排队外部工作、适配器在提交后执行。

## 后续发展建议

**这份设计的价值不在代码，在「权限是一个有生命周期的一等对象」这个决定。** 四个判断：

- **直接借鉴 Mandate + Subscription 两个概念。** 内部平台最常见的做法是「Agent 拿到一个任务令牌，跑完就结束」，结果是**任务边界、上下文延续、权限归属全是隐式的**。建议把「工作单元」和「授权凭据」拆成两个对象——比在任务表里加一堆 flag 干净得多，且天然可审计。
- **「权限变更不追溯撤销」值得单独讨论后再定。** 它降低了系统复杂度，但意味着**收紧策略不会立刻止血**——跨信任边界场景里可能不可接受。建议区分两类变更：**收紧「谁能发起」立即生效，放宽「能做什么」也立即生效，但已下发 Mandate 的范围变更走通知 + 显式 stop，而不是静默失效**。
- **先建内部评测集，再谈 Agent 自主度。** 每个判断都挂在 Eval 上，但 Eval 本身没有公开评测集或准确率数字。**内部平台推进自主 Agent 之前，最该做的是把「这个请求该不该被接受」「这个范围够不够」变成可回归的用例**。
- **它的「少概念、少设置」原则比领域模型更值得抄。** `000-philosophy.md` 明确写：**一个业务需求，要么变成某个已有概念的属性，要么变成 Agent 遵循的一段提示词文本，不为它新增概念，也不为它新增设置项**。建议给配置模型设一条硬规则：新需求先尝试落成已有概念的属性，失败了再讨论加概念。

**风险与局限**：README 写得很清楚——**研究原型，不是 DeepSeek 官方产品**，是为发布裁剪过的版本，与内部版本不同，论文里的部分设计未实现，可能仍有 bug。1 天 8,965 star、904 fork、**0 个 open issue**（刚创建）；**没有 release**；建仓 2026-10-31，最后 push 同日。**热度完全跑在成熟度前面，建议按「设计参考」而非「可用组件」对待**——但它的 `docs/` 结构本身（000 到 008，每篇只依赖前面几篇）就是一份写得极好的 Agent 平台设计文档模板。

## 下一步

- 想看同一问题的协议侧（跨系统而不是跨信任边界） → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)
- 想看 harness 该被拆成哪些可配置组件 → [harness2 深读](../2026-W44/harness2.md)

## 如果你想

- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看内部平台该承载哪些能力 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看 Agent 工具形态横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)

---
title: 'cloudflare/security-audit-skill：让 Agent 审计代码，并给出机器可读的结论'
description: Cloudflare security-audit-skill 深度解读——六阶段审计流程、覆盖账本与对抗式验证如何让 AI 安全审计的结论可机检，以及它对内部平台审计契约的借鉴价值
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-10-26
---

# cloudflare/security-audit-skill：让 Agent 审计代码，并给出机器可读的结论

> **TL;DR**：这是 Cloudflare 把自家漏洞发现 harness 的单仓起点开源出来的版本，六阶段跑完安全审计。值得抄的不是提示词，是三个机制：**覆盖账本**（知道自己漏了什么）、**对抗式验证**（找漏洞的 Agent 绝不能是验证漏洞的 Agent）、**三态结论**（`confirmed` / `needs_validation` / `rejected` 是正式交付物，不是「成功 / 失败」二元结果）。本周涨星 +15,072，占存量 32%，全榜第一。

📅 数据窗口：2026-10-20 ~ 2026-10-26 ｜ 🏷️ Agent 运行时安全 ｜ 本周涨星 +15,072 ｜ 总 star 47,179

## 是什么

[cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) 是一个 **coding-agent skill**：把你的编码 Agent 变成安全审计员。README 说得很清楚——它是 Cloudflare 漏洞发现 harness 的**单仓起点**，真正的 harness 已长成多阶段、fleet 级的系统，公开这个仓是给外部复现用的起点。

六个阶段：

1. **侦察（Reconnaissance）** —— 摸清架构、信任边界、输入面、历史证据，产出 `architecture.md` 和 `coverage-ledger.json`。
2. **覆盖式狩猎** —— 按账本条目分派**相互隔离**的 hunter，再用 coverage critic 找出账本没覆盖的缝隙。
3. **候选验证** —— 每个候选交给一个**全新的 verifier**，任务是**证伪它**而不是确认它。
4. **结构化输出** —— 写出 `confirmed` / `needs_validation` / `rejected` 三类记录到 `findings.json`，并按 `report-schema.json` 校验。
5. **独立记录复核** —— 新的 Agent 复核结论的源码依据；实质性替换的结论再交给另一个独立 verifier。
6. **目标中立报告** —— 从已复核记录和覆盖账本推导 `REPORT.md`、`FINDINGS-DETAIL.md`、`NEEDS-VALIDATION.md`。

配套 15 个狩猎类文件，从内存安全、AI 与 LLM（prompt injection、输出处理）、Web 协议与认证、客户端侧、供应链、云与部署、RPC 协议，到桌面移动与本地 IPC。

## 技术亮点

**第一，三态结论把「不确定」变成可交付物。** `confirmed` 要求完整源码溯源和有边界的观测结果；`needs_validation` 要求写明**具体那条未解决的事实**且不带严重级别；`rejected` 记录被证伪的候选。**大多数「AI 跑安全扫描」的方案只有两态，于是模型要么过度自信地报一堆假阳性，要么什么都报不出来。三态设计让「我还需要确认 X」成为合法且结构化的输出**——这是它相对同类工具最大的工程差异。

**第二，覆盖账本把「漏了什么」变成显式状态。** 账本按条目分派 hunter，再让 coverage critic 找缝隙。多次运行**可叠加**——复用历史账本定向补缺口、重验变动源码，且**不把过期或未解决的旧工作算作已覆盖**，堵住了「跑过一次就以为扫全了」这个漏洞。

**第三，对抗式验证是结构上的隔离，不是提示词里的叮嘱。** 设计原则很硬：*the agent that checks a finding is never the agent that found it*。第 4 阶段和每次第 5 阶段的结论替换后，父流程都会跑 `validate-findings.cjs`；账本建立和每次更新后跑 `validate-coverage-ledger.cjs`。**两个校验器都是零依赖的 `.cjs`，用 Node.js 直接跑，不需要 LLM。**

**第四，沙箱是前置条件，不是加分项。** 对目标代码的构建、测试、进程、浏览器、模拟器、fuzzer，必须有**操作系统强制的沙箱**——禁用外部网络、净化过的白名单环境、强制资源上限、只允许写入分配的 scratch 路径。**没有这些控制，工作流不会执行目标代码，而是把线索保留为 `needs_validation`。** 这把「用 Agent 审计 AI 写的代码」最大的风险敞口，用架构约束而非提示词堵住了。

## 后续发展建议

**这个仓值得拆成两部分抄：结论格式，和「不确定」的处理方式。**

- **结论格式可以直接当内部平台的验收契约模板。** `findings.json` + `report-schema.json` + 三态判定，是现成的「AI 结论 + 证据等级」结构。**内部平台做代码评审、扫描、诊断类 Agent 时建议照抄这个三态设计**：区分「已确认」「待验证（附具体待验证事实）」「已否决」，每条已确认结论带完整溯源。这比「输出一份报告」强得多，因为**下游可以按状态分派处理**：confirmed 进阻断流程，needs_validation 进人工队列，rejected 丢弃。
- **覆盖账本的思路值得搬到「Agent 自评」场景。** 内部平台要证明 Agent 能力覆盖率，同样需要一份账本：哪些用例类别被覆盖过、覆盖结论何时失效、哪些只是「跑过但没结论」。**AI 系统最危险的状态不是报错，而是「看起来跑过了」**——账本正是为了让「没覆盖」显式可见。
- **对抗式验证可以下沉为平台的通用模式。** 如果诊断结论会用于阻断或放行决策，那么**出结论的 Agent 和复核结论的 Agent 必须分离**，复核针对「推翻」而非「确认」提问。这与 harness2 的「judge 必须同指标」是同一类约束——**把正确性约束放进工具链，而不是写进规范文档。**

**风险与局限**：审计能力上限取决于底座模型，项目提供的是编排与证据纪律，不是漏洞知识；「审计 Agent 审计 AI 写的代码」存在共同盲区——对抗式验证能降低误报，但**不能保证无漏报**，模型系统性犯同一类错时验证 Agent 可能跟着犯。项目自 2026-09-14 后没有 push、也没有 release，周涨星几乎全来自传播，**生产依赖引入前要评估上游不维护的情况**；15 个狩猎类文件对 Web / 移动 / 云 / 协议覆盖较全，但动态分析、运行时漏洞不在其内。

## 下一步

- 看 harness 的其他组件怎么拆 → [harness2 深读](./harness2.md)
- 看另一个方向的运行时安全（内核级拦截）→ [OpenShell 深读](../2026-W43/openshell.md)
- 想理解信任边界怎么划 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)

---
title: 'JetBrains/thinkrail：IDE 厂商亲自下场，harness 变成 IDE 本体'
description: JetBrains 官方 agentic IDE thinkrail 深度解读——git worktree 隔离、SPEC.md 知识图谱、MCP server 权限分级与公司 LLM 网关接入，以及 IDE 厂商下场对 Agent 运行时分发格局的影响
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# JetBrains/thinkrail：IDE 厂商亲自下场，harness 变成 IDE 本体

> **TL;DR**：**7,010 star 换来 82.2% 的周涨星比——全榜最高，说明它的流量几乎全部来自本周。** thinkrail 不是 JetBrains 的插件，是 JetBrains 自己的 agentic IDE：把 `pi` coding agent 装进真实 IDE，用 git worktree 隔离每次改动，用 `SPEC.md` 图谱当唯一事实源，MCP server 的调用**逐次征求同意**，还能直接接公司 LLM 网关。**IDE 厂商开始自己提供 Agent 运行时，「插件宿主」这个位置就不安全了。**

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ Harness 工程 ｜ 本周涨星 +5,760 ｜ 总 star 7,010

## 是什么

[JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) 的自我描述是「**越用越好的 agentic IDE**——今天靠 living specs 学习你的项目，明天构建自己的能力」。它是 **JetBrains Incubator 项目**，底层包着 [`pi`](https://www.npmjs.com/package/@earendil-works/pi-coding-agent) coding agent，上面套了一层完整的 IDE。

仓库主分支信息：Apache-2.0，2026-07-08 建仓，**最新 release v0.3.1 发布于 2026-11-01**（前一天），326 个 open issue。

## 技术亮点

**第一，工作区隔离用 git worktree，做成了可沉淀的「货架」。** 打开任何 git 仓库作为 project，从里面切出 worktree 作为 workspace，各自独立分支和目录，Agent 并行干活不碰你的 checkout。**完成的和休眠的 worktree 会自动「沉淀」到每个 project 自己的架子上**——PR 合并或关闭后、或静置一周后触发，再次进入该项目时原样回来。顶栏显示当前分支相对 `origin` 的位置和 PR 状态，下一步（发布 / push / 开 PR）一键可达。

**第二，`SPEC.md` 是唯一事实源，而且 Agent 会维护它。** 代码旁边是一张由 `SPEC.md` 文件组成的**连通图谱**，Agent 通过专用的 `spec_*` 工具读取、检索和维护它，「意图因此能跨越 session 存活」。Specs 工具是只读的，在 workbench 里渲染成树。

**第三，MCP server 的权限是逐次征求的，不是一刀切。** README 写得很具体：ThinkRail **会在聊天里先问**，才调用那些没有标记为只读的 server 工具；仓库自己声明要关掉的 server 会保持关闭直到你批准；OAuth server 的登录在 Settings 里完成；每个 chat 旁边显示自己挂的 server、后台命令和 subagent。

**第四，能直接接公司 LLM 网关。** Settings → Providers → **Custom servers** 支持任何 OpenAI 兼容服务——LiteLLM、sglang、vLLM、Ollama、LM Studio、llama.cpp，能列出该 server 提供的模型及其 context 与能力，配置写进 `pi` 的 `models.json`，终端里的 `pi` CLI 也能用。**这对企业内部场景是最实用的一条。**

**第五，多 Agent 是原生的。** 每个 workspace 可以同时开多个 `pi` session，各有各的模型和实时 token / 成本读数；可以把某个 turn 导流、排队后续消息、委派给 subagent、协作维护一份共享计划（Agent 更新、你来改），每完成一步都能单独提交和评审。

## 后续发展建议

**thinkrail 真正释放的信号是「运行时位置」之争，不是「IDE 又一个好产品」。** 三个判断：

- **对内部平台，最该抄的是它的权限颗粒度，而不是界面。** 「调用没标只读的 MCP 工具前先问一次」是一条极简但正确的规则——**它把「只读工具免打扰、可写工具逐次确认」这个判断下沉到了 IDE 层**。内部平台常见的做法是按 server 整体授权（一次信任，全域放行），颗粒度太粗。**建议按工具粒度而不是按 server 粒度做授权**——尤其是写操作工具，逐次确认的成本远低于一次误写。
- **`SPEC.md` 图谱是「意图活过 session」的最小可行方案，值得直接试。** 它没有走复杂的方向图或向量库，就是一组 Markdown 文件 + Agent 主动维护。**内部平台的「上下文工程」不必从知识图谱做起，先让 Agent 维护一份人类可读的规格文档**，成本极低且可 diff、可 review。这和上期 `graphify` 那种「用遍历代替 grep」的路线是两种极端，thinkrail 这一端更轻。
- **但它暴露了一个风险：厂商下场会挤压 harness 层的独立空间。** thinkrail 的形态是「厂商 IDE + 第三方 agent（`pi`）+ 厂商自己的扩展体系」。**内部平台选型时要分清哪些是可替换的**：Agent 运行时、扩展机制、模型接入这三层的可替换性差别很大。**模型接入层已经基本标准化（OpenAI 兼容协议），运行时层正在分化，扩展层还没定**——**投资应该放在还没定的那一层**。
- **成本读数值得单独注意。** 每个 session 显示实时 token 和成本，**这是「Agent 成本可见化」的 IDE 级实现**。内部平台如果要把 Agent 从「工具」变成「同事」，**成本必须实时可见**，否则规模化使用时的账单问题会一次性爆出来。

**风险与局限**：**JetBrains Incubator 项目**，README 自己写明「Next, we're adding full extension support」——扩展体系还在建。326 个 open issue 相对 7,010 star 是极高的比例（**4.7%**），说明产品处于早期且反馈极其密集。Linux 桌面版依赖较新（Ubuntu 24.04+、glibc 2.38+、GTK 3、WebKitGTK 4.1）。**7,010 star 里 82.2% 是本周涨的，本周流量占绝对主导，目前还谈不上生态沉淀。**

## 下一步

- 想看 harness 被拆成可自动优化组件的另一种解法 → [harness2 深读](../2026-W44/harness2.md)
- 想看另一个把「人需要介入」做成产品的形态 → [dsh-superagent 深读](./dsh-superagent.md)

## 如果你想

- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看团队落地的方法论 → [AI Native 方法论](../../../ai-harness/index.md)

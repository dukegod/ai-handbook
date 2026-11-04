---
title: 'thedotmack/claude-mem：把记忆检索做成三层递进，让 token 成本变成可见数字'
description: claude-mem 深度解读——生命周期 hook 采集、SQLite + Chroma 混合检索、三层递进 MCP 工具与渐进式披露，以及跨 8+ harness 部署同一份记忆的工程取舍
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# thedotmack/claude-mem：把记忆检索做成三层递进，让 token 成本变成可见数字

> **TL;DR**：109,575 star、9,581 fork，**最新 release v15.8.1（2026-11-01）**，Apache-2.0。它的技术核心不是「记住一切」，而是**「只把需要的部分取回来」**：四个 MCP 工具组成三层递进检索——`search` 拿紧凑索引（每条约 50–100 token）→ `timeline` 看时间线上下文 → `get_observations` 只取筛出来的完整条目（每条约 500–1,000 token）。**它还把 token 成本直接显示出来——记忆系统的正确指标不是存了多少，是取回时花了多少。**

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ 记忆系统 ｜ 本周涨星 +5,852 ｜ 总 star 109,575

## 是什么

[thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) 的自我描述是「**给每一个 Agent 的跨会话持久上下文**」：捕获 Agent 在会话里做的一切，用 AI 压缩，把相关上下文再注入未来的会话。

它的部署范围极广：README 和描述里点名支持 **Claude Code、OpenClaw、Codex、Gemini、Hermes、Copilot、OpenCode** 等，安装方式是 `npx claude-mem install --ide <目标>`，可选项包括 `opencode`、`t3code`、`antigravity`、`omp`、`pi`、`dsh`（DeepSeek Harness，带 `--dsh-profile tui`）。Pi 和 DeepSeek Harness 走的是 **worker runtime**。

## 技术亮点

**第一，采集靠生命周期 hook，不靠 Agent 自觉。** 六个 hook 各司其职：SessionStart、UserPromptSubmit、PreToolUse、PostToolUse、Stop、SessionEnd。每个都是**一条无 shell 的命令**（`claude-mem hook claude-code <event>`），由安装器放到 PATH 上的一个小启动器执行。**这意味着「Agent 忘了记录」这件事在架构上就不可能发生**——记忆采集是宿主环境的责任，不是 Agent 的任务。

**第二，检索的三层递进是整个设计里最值得学的一条。** README 把四个 MCP 工具的工作流写得很明确：

| 层 | 工具 | 返回 | 单条成本 |
| --- | --- | --- | ---: |
| 1 | `search` | 紧凑索引 + ID | 约 50–100 token |
| 2 | `timeline` | 结果周围的时序上下文 | — |
| 3 | `get_observations` | 只取筛出来的 ID 的完整内容 | 约 500–1,000 token |

**Agent 先拿到索引自己判断相关性，再决定要不要拉详情。** 这和「把整段历史塞进上下文」是完全不同的成本模型。README 把它叫 **progressive disclosure**（渐进式披露），并强调它带 **token 成本可见性**。

**第三，存储是 SQLite + FTS5 加 Chroma 向量库的混合检索。** 全文检索负责精确匹配，向量库负责语义召回，二者互补。压缩结果、摘要、会话记录都落在本地 SQLite。

**第四，记忆的边界是可控的，而且给出了三种精细控制。**

- **私有标记**：`<private>` 标签的内容直接排除在存储之外——**在「全量记忆」成为默认的年代，明确的隐私排除通道比什么都重要。**
- **截图默认关闭**：工具截图的副本存本地 `~/.claude-mem/media-v1/`，只有开了 Cloud Sync 才上传，而且图片推理还要**单独再开一次**。
- **上下文配置**：可以细粒度控制哪些内容被注入。

**第五，它开始从个人记忆走向团队协作。** `TeamBrain` 提供一个共享工作区，带真实的工作列表、成员归属和关联结论——**每个人自己选择共享什么，个人请求和评审笔记保持隔离**。另外还有 `Local My Work` 面板：实时请求、进度、人工交接和一个保存的评审队列。

**第六，插件市场是安装方式之一。** Claude Code 里可以 `/plugin marketplace add thedotmack/claude-mem` 然后 `/plugin install claude-mem`。README 里有个很实用的警告：Claude-Mem 虽然发布在 npm 上，但 `npm install -g claude-mem` **只装 SDK 库，不注册 hook 也不起 worker 服务**，必须用 `npx claude-mem install` 或 `/plugin` 命令。

## 后续发展建议

**claude-mem 示范了「记忆系统该按什么指标来验收」——这条比它的实现更值钱。** 四个判断：

- **内部平台建记忆系统时，先定「取回成本」这个指标，再定「存了多少」。** 大多数记忆系统的验收指标是「召回了多少相关条目」，这会鼓励系统往「多存」的方向优化，结果是上下文越来越贵。**claude-mem 的做法是让 Agent 先看索引再决定拉不拉详情，并把每层的 token 成本标出来**——建议内部平台把「一次会话的记忆注入平均成本」做成核心监控指标。
- **采集走宿主 hook，不依赖 Agent 自觉，这条必须照抄。** 内部平台如果让 Agent 自己决定「什么值得记」，结果一定是 Agent 记的都是它觉得重要的（通常是它刚做过的），而不是用户真正需要的。**记忆采集应该是平台的管道能力，不是 Agent 的可选动作。**
- **「渐进式披露」这个思路可以直接套到 RAG 之外的场景。** 同样的三层递进（索引 → 时序 / 结构上下文 → 详情）完全适用于代码检索、需求文档检索、日志排查。**内部平台可以把它抽象成一个通用的「检索协议」，而不是只给记忆模块用。**
- **隐私排除要从第一天就有，不能事后补。** `<private>` 标记 + 截图默认关闭 + 云同步显式开关，这三条加起来是一个完整的设计态度。**内部平台涉及员工数据时，建议一开始就把「本地优先 + 显式上传」做成默认形态**，而不是先全量云端再补合规。

**风险与局限**：**109,575 star 对应 176 个 open issue（0.16%），维护密度相当健康**，最新 release v15.8.1 就发在前一天，**这个项目是本仓库近几期里少见的「热度与工程节奏匹配」的样本**。但它的复杂度也在涨：README 有 **30 多种语言的 i18n 文档目录**、独立的 worker 服务（由 Bun 管理）、本地 Web viewer、OpenClaw gateway、Telegram / Discord / Slack 的实时观察流、TeamBrain、Cloud Sync——**「记忆系统」这个筐里已经装了不少额外功能**。README 特别提醒 **`npm install -g` 装不了完整功能**，说明安装路径本身还有门槛。另外**项目名和描述都绑死在 Claude Code 生态**（虽然是多 harness 通用），认知上仍会被当成「Claude Code 的记忆插件」而不是「跨 harness 的记忆层」。**没有官方 release 之外的版本语义**，版本追踪靠 npm tag。

## 下一步

- 想看 skill 生态里「分发层」长什么样 → [vercel-labs/skills 深读](./vercel-skills.md)
- 想看另一个把「上下文压缩」做成产品的形态 → [2026-W44 context-mode 相关讨论](../2026-W44/index.md)

## 如果你想

- 想看团队落地的方法论 → [AI Native 方法论](../../../ai-harness/index.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)

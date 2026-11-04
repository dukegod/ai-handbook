---
title: 'vercel-labs/skills：75+ harness 的 skill 分发 CLI，和它刚长出来的锁文件'
description: vercel-labs/skills 深度解读——跨 75+ agent 的安装分发、skills.sh 目录、skills-lock.json 锁文件与 experimental_sync 的 npm 依赖同步机制，以及分发层正在固化的事实
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-11-02
---

# vercel-labs/skills：75+ harness 的 skill 分发 CLI，和它刚长出来的锁文件

> **TL;DR**：37,660 star、3,255 fork、**1,229 个 open issue**。它是 [skills.sh](https://skills.sh) 这个 skill 目录背后的 CLI，**支持 75+ 个 agent**。真正值得注意的不是 `npx skills add`，而是两个正在成形的机制：`skills-lock.json` 记录项目级 skill 依赖，以及 `experimental_sync` **把 npm 依赖里附带的 skill 同步进项目**——**这意味着 skill 有机会像依赖一样被版本化和锁住。**

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ Skill 分发层 ｜ 本周涨星 未进周榜 ｜ 总 star 37,660

## 是什么

[vercel-labs/skills](https://github.com/vercel-labs/skills) 是「**开放 Agent Skills 生态的 CLI**」——一句话说清楚它的定位：**它是 skill 的 npm**。

安装一个 skill：

```bash
npx skills add vercel-labs/agent-skills
```

然后选要装哪些 skill、装给哪些 coding agent。默认装进当前项目，`-g` 则全局可用。还可以只装一个 skill 到一个 agent：

```bash
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a claude-code
```

## 技术亮点

**第一，命令集覆盖了分发层该有的全生命周期。**

| 命令 | 作用 |
| --- | --- |
| `npx skills add <source>` | 安装（支持单 skill + 指定 agent） |
| `npx skills find [query]` | 搜索 skill |
| `npx skills list` | 列出已安装的 skill |
| `npx skills use <source>@<skill>` | **不安装，直接用**（打印提示词，或直接拉起对应 agent） |
| `npx skills check` | 检查可用更新 |
| `npx skills update [skills...]` | 更新 |
| `npx skills remove [skills...]` | 卸载 |
| `npx skills init [name]` | 生成 skill 模板 |

**`skills use` 这个命令值得单独说**：它把「临时用一个 skill」和「安装一个 skill」分开了。**这解决了 Agent 生态里一个真实的摩擦——用户往往想试一下，但不想留下安装痕迹。**

**第二，`skills-lock.json` 让 skill 变成可锁定的项目依赖。** `experimental_install` 的作用是「**恢复 `skills-lock.json` 里记录的项目 skill**」。配合 `experimental_sync`（把 npm 依赖里捆绑的指令同步进项目），形成了一个还不完整但方向明确的机制：**skill 可以随依赖进版本库、可以被锁、被同事复现。**

**第三，`experimental_sync` 的机制设计得很聪明。** README 的例子：

```bash
npm install -D skills agent-browser
npx skills experimental_sync -y
```

有些 npm 包会把给 Agent 用的指令和代码一起发布。`sync` 把它们链进你的项目，**这样它们会随依赖一起升级**；同时还会安装 `package.json` 里声明的 skill pack。**这把「skill」从「用户手动装的东西」变成了「依赖声明的一部分」**——背后有对应的 RFC（issues/2323）。

**第四，生态的两个官方锚点。** [skills.sh](https://skills.sh) 是发现目录，[agentskills.io](https://agentskills.io) 是规范站——**Vercel 同时占住了「发现」和「规范」两个位置**，这和 Anthropic 只占规范、Cursor 只占自有格式是不同的布局。

**第五，遥测是可关闭的，而且它自己也做安全审计请求。** README 明确写明可以用 `DISABLE_TELEMETRY=1` 或 `DO_NOT_TRACK=1` 关闭，并单独列出收集了哪些内容。

## 后续发展建议

**分发层一旦有了锁文件，skill 就从「配置」变成了「依赖」——这个变化会改写内部平台的设计前提。** 四个判断：

- **`skills-lock.json` 这个设计值得直接借鉴到内部平台。** 内部平台如果让用户「手工挑几个 skill 装上」，环境必然漂移。**建议内部平台的 skill 也有一个锁文件：记录 skill 的来源、版本、hash 和安装位置**，并提供一条命令恢复整个清单。这条对「Agent 环境可复现」的价值远高于它看起来的样子。
- **`experimental_sync` 指向一个更大的问题：skill 的来源该怎么治理。** 「npm 包顺带带 skill」意味着**代码依赖会隐式改变 Agent 的行为**。内部平台必须提前定规则：**哪些来源的 skill 可以自动同步，哪些必须走审核**。**这类「隐式行为变更」的传播路径，是 Agent 平台比传统软件平台更危险的地方**——传统依赖只影响运行时行为，skill 影响的是 Agent 的决策。
- **`skills use` 这个「不安装就能用」的入口，是降低试用门槛的关键设计。** 内部平台推广新 skill 时，**最有效的路径往往不是「装到你的环境里」，而是「这一次先用一下」**。建议内部平台提供等价的「一次性试用」入口。
- **但要清醒：分发层现在还很脆。** 75 个 agent 意味着**每个 agent 的目录约定、加载机制、hook 能力都不一样**。README 里有个细节很说明问题——`superpowers` 那个项目就得为每个 harness 单独写一份安装说明，包括「Hermes 没有 post-compaction hook」这类坑。**「统一分发」的统一程度是有限的，最终还是要回到每个 harness 的特性上。**

**风险与局限**：**1,229 个 open issue 相对 37,660 star 是 3.3%**，对一个 CLI 工具来说偏高，说明**兼容矩阵的维护成本远高于预期**。核心命令带 `experimental_` 前缀的（`experimental_sync`、`experimental_install`）README 明确警告：**名称、选项和行为可能在任何版本变更或移除，不另行通知**——**这意味着依赖它们的流程要留退路**。需要 **Node.js 22.20 或更高**（门槛不低）。MIT 协议，最新 release **v1.7.4（2026-10-19）**，比 Anthropic 的 `agentskills.io` 规范站更像是**事实上的分发中枢**。

## 下一步

- 想看规范本身长什么样（只有两个必填字段） → [anthropics/skills 深读](./anthropic-skills.md)
- 想看另一家的插件规范长什么样 → [cursor/plugins 深读](./cursor-plugins.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)

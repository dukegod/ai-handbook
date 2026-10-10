---
title: DeepSeek Harness 深度评测
description: DeepSeek Harness 评测——已发布桌面端的开源 Agent 运行时，Cordis 内核 + 一切皆插件 + 四种运行模式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-10
verifiedWith:
  sources:
    - name: DeepSeek Harness 官网
      url: https://deepseek.com/harness/
      accessedAt: 2026-10-10
    - name: GitHub 仓库
      url: https://github.com/deepseek-ai/deepseek-harness
      accessedAt: 2026-10-10
---

# DeepSeek Harness 深度评测

> **TL;DR**：DeepSeek 出品的开源 Agent 运行时——「一切皆插件」，Cordis 内核驱动全模块化架构。**已有桌面端（macOS / Windows）+ Web UI + 源码三种用法**，MIT 协议，246k Star。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- DeepSeek Harness 的定位（Agent 运行时 + 可用产品）
- Cordis 内核 + 插件架构的设计哲学
- 4 种运行模式的适用场景
- 自动化任务与插件生态这两块「非编码」能力
- 与 PI-agent / Claude Code / Codex 的差异化

## 核心定位：产品 + 运行时，两层身份

DeepSeek Harness（`dsh`）最早是 Agent Harness 框架，现在**已经同时是可用产品和开源运行时**。

官网自己的说法最准确：

> DeepSeek Harness 现在，**开箱即用**
> 无论处理日常工作、编写代码，还是构建自己的 Harness，都可以从这里开始。
> DeepSeek Harness 面向全球开放测试并同步开源，以可自由组合的插件，拓展 Agent 能力。

> 📌 **2026-10 定位修正**：早期资料把它描述为「框架，不是产品」，这个说法已经过时。桌面端已发布（macOS Apple 芯片 13+ / Windows 64 位 10+），官网下载页写明「支持后台运行和本地文件读写，更方便地处理长时间、复杂任务」。

**三种用法**：

| 用法 | 命令 / 入口 | 说明 |
|------|------------|------|
| **一键使用** | `npx dsh` | 装好 Node.js 直接启动 Web UI |
| **桌面端** | 官网下载 | macOS / Windows 原生客户端 |
| **源码安装** | clone 仓库 + `pnpm run build` | 完整可控 |

> ⚠️ 官网下载页同时标注「当前版本仍在持续迭代中，部分功能和体验也在持续完善」——**预览版定位未变**。

| 维度 | DeepSeek Harness | PI-agent | Claude Code | Codex |
|------|-----------------|----------|-------------|-------|
| **定位** | Agent 运行时 + 产品 | Agent 框架 | CLI 产品 | 多端 Agent 产品 |
| **核心理念** | 插件一切 | 原语优先 | 开箱即用 | 开箱即用 |
| **开源协议** | MIT | MIT | 商业 | CLI Apache 2.0 / 产品闭源 |
| **Star 数** | **246.6k** | — | — | — |
| **成熟度** | 预览版 | 早期 | 成熟 | 成熟 |

## 架构：Cordis 内核 + 插件一切

### Cordis 内核的边界

官网对内核职责的界定值得单独记：

> **Cordis 内核只负责插件的加载、卸载和依赖关系，不承载 Agent 的具体能力。**

这条边界正是「UI 本身也是插件」能成立的原因——内核对「什么是能力」毫无预设。

### 插件分类

所有 Agent 能力通过插件交付，通过 Cordis 的服务和事件机制协作：

| 插件类型 | 职责 |
|---------|------|
| **Models** | 底层 AI 模型接入 |
| **Tools** | Shell、文件编辑、搜索等基础工具 |
| **Skills** | 高层 Agent 能力 |
| **Sessions** | 对话和状态管理 |
| **Sandboxes** | 隔离执行环境 |
| **Storage** | 数据持久化 |
| **Loops** | 迭代处理 |
| **Scheduling** | 任务编排 |
| **UI** | 用户界面（本身也是插件） |

**关键设计**：开发者无需改动源码，即可在配置层选择、替换或扩展任一能力。

### 可追溯性：Trajectory 视图

模型看到的一切都会写入**仅追加设计的会话日志**，包括系统提示词、思维链、工具调用与结果、子 Agent 调度，以及每一次上下文注入。

官网展示的 Trajectory 视图结构：

- **三条泳道**：输入 / 模型 / 工具
- **五类记录**：系统、用户、上下文、助手、工具调用
- **每个步骤可展开**：概述 / 参数 / 结果 / Schema / 计时

恢复、分叉、检索与回放共享同一份事件流。这是本轮核到的几家里可观测性最细的。

## 4 种运行模式

官网口径（注意：**Code 模式已更名为 PTC 模式**，Creator 模式称「创造模式」）：

| 模式 | 能力 | 适用场景 |
|------|------|---------|
| **标准模式** | 文件编辑、Shell、文件与网页检索、Skills、计划、目标、子代理、工作流 | 通用 Agent 开发 |
| **PTC 模式** | 标准模式全部能力 + Code Mode SDK，让模型用一个 **TypeScript 程序**组合多步操作 | 复杂代码生成 |
| **极简模式** | 仅持久 `bash` 与 `str_replace_editor` 双工具 | 基准测试、模型评测 |
| **创造模式** | 标准模式全部能力 + 检查运行时、在内存中试验 Cordis 插件、据此组合创作新 preset | 开发自定义 Agent preset |

## 非编码能力：这块被严重低估

DeepSeek Harness 的能力边界**已经越过「编码 Agent」**。官网列出的以下几项与前面几家的产品线高度重合：

### 自动化任务

支持**定时与周期执行**。官网演示的三个场景：

- 每周五 17:00 整理本周项目记录，生成周报
- 每天 09:00 汇总销售表格，标出异常变化
- 每周一 10:00 运行项目测试，汇总失败项

这已经不是「写代码」，是持续性工作系统。

### 七款官方插件

智能体团队、自动授权审查、自动化任务、语音输入、终端、Agent 循环、子智能体。

### Agent 可以现场写插件

**创造模式下用对话创建插件**。官网演示的案例是「帮我写一个『番茄时钟』插件」，全程工具调用序列可见（加载技能 → 检查提供方 → 查询运行时 → 读取 → 思考 → 写入 → 编辑 → 运行命令验证），**用时 5 分 24 秒完成并验证通过**。

> **这条最值得注意**：插件系统从「人装」变成了「Agent 自己写」。它和 Anthropic 的 dynamic workflows（见 [Agent 工作台的产品形态与设计取舍](./agent-workspace)）在做同一件事——让编排层从静态配置变成运行时生成——只是 DeepSeek 落在插件层，Anthropic 落在编排层。

## 核心优势

### 1. 极致模块化，且边界清晰

与 PI-agent 的「原语优先」类似，但更彻底——**UI 本身也是插件**。内核只管依赖不管能力，整个系统没有「不可替换」的部分。

### 2. 可追溯性最强

仅追加日志 + 三泳道 Trajectory 视图，完整记录模型每一个决策和行动。这是 PI-agent 和 Claude Code 都不具备的深度。

### 3. 社区体量

GitHub **246.6k Star / 29.6k Fork**（2026-10-10 实测）。插件通过 `dsh-plugin` GitHub Topic 发现。

### 4. DeepSeek 模型原生集成

对 DeepSeek 系列模型有原生优化；官网首页同时主推 DeepSeek-V4.1-Flash。

### 5. 多语言与文档

TypeScript/JavaScript 为主，支持 Python 组件。文档中英文双版本。

## 核心局限

### 1. 预览版，API 不稳定

官网明确标注预览版，且下载页写明「当前版本仍在持续迭代中」。**生产环境慎用**。

### 2. 学习曲线陡峭

Cordis 内核 + 插件架构 + 4 种运行模式，概念密度远高于 Claude Code / Codex。

### 3. 缺乏开箱即用体验

官网自己写的是「现在，开箱即用」，但那指的是**有桌面端可下载**。要深度定制仍需理解插件体系、配置运行模式、组装能力栈。

### 4. 模型支持信息不透明

官网与 README 均未列出具体支持哪些模型。插件架构理论上可接入任意模型，实际生态成熟度未知。

### 5. 生态依赖 macOS / Windows 桌面

Intel Mac 明确标注「暂不支持」，需 Apple 芯片。

## 与 PI-agent 对比

> 📌 四家主流开源 harness（Pi / DeepSeek Harness / Codex CLI / OpenCode）的内核设计对比见 → [四个开源 Harness 对比](./open-harness-comparison)

| 维度 | DeepSeek Harness | PI-agent |
|------|-----------------|----------|
| **内核** | Cordis（插件管理） | 自研扩展系统 |
| **模块化粒度** | 极细（UI 也是插件） | 粗（扩展 / Skills） |
| **可追溯性** | ⭐⭐⭐（仅追加日志 + Trajectory） | ⭐ |
| **运行模式** | 4 种（标准 / PTC / 极简 / 创造） | 4 种（Interactive / Print / RPC / SDK） |
| **模型支持** | DeepSeek 原生 + 插件扩展 | 15+ 提供商 |
| **有无可用产品** | ✅ 桌面端 + Web UI | ❌ 纯框架 |
| **社区** | 246.6k Star | 较小 |

> ⚠️ 两者的成熟度标注都是「非生产就绪」，但性质不同：DeepSeek Harness 有官方产品形态（预览版），PI-agent 仍是纯框架。

## 规范与配置：AGENTS.md 原生支持

DeepSeek Harness 仓库自带 `AGENTS.md`（README 明确写了「For agents, follow AGENTS.md」），对跨工具规范有原生支持。

### 规则文件加载链

```
项目根/AGENTS.md          # 项目级（团队共享）
├── 子目录/AGENTS.md      # 目录级（天然路径作用域）
├── .agents/              # Agent 配置目录
└── 插件配置              # 通过 Cordis 服务注入
```

### 路径作用域

通过**子目录 AGENTS.md** 实现：

```
src/pages/AGENTS.md     # 仅 pages 相关文件被涉及时生效
src/common/AGENTS.md    # 仅 common 相关文件被涉及时生效
```

### 与 Claude Code / Codex / Cursor / Trae 的兼容

| 场景 | 解法 |
|------|------|
| Codex 用户也要读 dsh 的规则 | 把通用规范放 `AGENTS.md`，Codex 原生支持 |
| Claude Code 用户也要读 dsh 的规则 | 把通用规范放 `AGENTS.md`，Claude Code 新版同时读取 |
| Cursor 用户也要读 dsh 的规则 | 把通用规范放 `AGENTS.md`，Cursor 兼容读取 |
| Trae 用户也要读 dsh 的规则 | 把通用规范放 `AGENTS.md`，Trae 原生支持 |
| dsh 专属配置 | 留在 Cordis 插件配置中，其他工具忽略 |

## 适用场景

**最适合**：

- 需要深度可观测性的 Agent 开发（Trajectory 追溯）
- DeepSeek 模型用户（原生集成）
- 想构建自定义 Agent preset 的高级开发者（创造模式）
- 需要极细粒度模块化的团队（每个组件可替换）
- 模型基准测试（极简模式）
- 定时 / 周期性重复工作（自动化任务插件）
- 想让 Agent 自己扩展能力（创造模式现场写插件）

**不太适合**：

- 需要开箱即用体验的新手（桌面端能跑，但深度定制门槛高）
- 追求稳定 API 的生产环境（预览版）
- 非 DeepSeek 模型用户（模型生态成熟度未知）
- 团队协作（缺乏内置的团队规范机制）
- Intel Mac 用户（桌面端不支持）

## 最佳实践

1. **先用桌面端或 `npx dsh` 跑通，再考虑源码安装**：先建立体感，插件体系比看起来陡
2. **从标准模式开始**：先体验完整工具集，再按需裁剪
3. **用 AGENTS.md 做跨工具规范**：仓库自带且明确推荐给 agent 用
4. **用 Trajectory 视图调试**：三泳道 + 五类记录，排查工具调用问题
5. **关注 `dsh-plugin` Topic**：社区插件生态是核心竞争力
6. **极简模式做基准测试**：评测不同模型的裸能力
7. **创造性任务试创造模式**：让它写插件比手写配置更快

## 未核实项

- **版本号**：搜索结果提到 v0.1.5（2026-09-10，与 V4.1-Flash 训练结合、新增标准化 UI 扩展入口与文件上传），但来源是百度百科，**未在 GitHub Releases 或官网一手核实**。GitHub Releases 区块因限流未能加载。
- **Star 数时点**：246.6k 为 2026-10-10 实测，随时间变化。

## 参考

- [DeepSeek Harness 官网](https://deepseek.com/harness/)
- [GitHub 仓库](https://github.com/deepseek-ai/deepseek-harness)（246.6k Star / MIT）
- [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- [PI-agent 深度评测](./pi-agent)
- [AI 工具全景](./overview)

## 下一步

- 看形态收敛逻辑 → [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- 对比 PI-agent → [PI-agent 深度评测](./pi-agent)
- 对比 Claude Code → [Claude Code 深度评测](./claude-code)
- 团队引入 → [团队 AI 工作流](/ai-harness/workflows/team)

## 如果你想

- 对比主流工具 → [AI 工具全景](./overview)
- 看非编码 Agent 形态 → [跨角色交付](./cross-role-delivery)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
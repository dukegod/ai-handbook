---
title: DeepSeek Harness 深度评测
description: DeepSeek 开源的"插件一切"Agent 框架——Cordis 内核 + 全模块化架构评测
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-08-17
verifiedWith:
  sources:
    - name: DeepSeek Harness 官网
      url: https://www.deepseek.com/harness/en/
      accessedAt: 2026-08-17
    - name: GitHub 仓库
      url: https://github.com/deepseek-ai/deepseek-harness
      accessedAt: 2026-08-17
---

# DeepSeek Harness 深度评测

> **TL;DR**：DeepSeek 出品的开源 Agent 框架——"插件一切"设计，144k Star，Cordis 内核驱动全模块化架构。不是产品，是让 AI 模型"做事"的运行时。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- DeepSeek Harness 的定位（Agent 运行时 vs 编程工具）
- Cordis 内核 + 插件架构的设计哲学
- 4 种运行模式的适用场景
- 与 PI-agent / Claude Code / Codex 的差异化
- 适用场景与不适用场景

## 核心定位：Agent 运行时，不是编程产品

DeepSeek Harness（简称 `dsh`）是 DeepSeek 官方开源的 **Agent Harness 框架**——它不直接写代码，而是提供一个**运行时环境**，让 AI 模型能在真实世界中理解环境、使用工具、完成任务。

核心哲学：**"模型是 Agent 的灵魂，Harness 是它的身体。"**

| 维度 | DeepSeek Harness | PI-agent | Claude Code | Codex |
|------|-----------------|----------|-------------|-------|
| **定位** | Agent 运行时框架 | Agent 框架 | CLI 产品 | CLI 产品 |
| **核心理念** | 插件一切 | 原语优先 | 开箱即用 | 开箱即用 |
| **开源协议** | MIT | MIT | 商业 | 商业 |
| **Star 数** | 144k | — | — | — |
| **成熟度** | 开发者预览 | 早期 | 成熟 | 成熟 |

## 架构：Cordis 内核 + 插件一切

### Cordis 内核

DeepSeek Harness 构建在 **Cordis**（来自 Cordiverse 项目）之上——一个外部插件管理系统，负责插件的挂载、卸载和依赖管理。所有 Agent 能力都通过插件交付，通过 Cordis 的服务和事件机制连接。

### 插件分类

每个组件都是可替换的插件，无需修改源码：

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

**关键设计**：所有配置通过组合完成，无需触碰源码。

### 可追溯性

模型看到的一切都被记录在**追加写入的会话日志**中——包括系统提示、推理过程、工具调用、子代理调度、上下文注入。**Trajectory 视图**支持按来源检查记录，可恢复、分叉、搜索和重放。

## 4 种运行模式

| 模式 | 能力 | 适用场景 |
|------|------|---------|
| **Standard** | 完整工具集：文件编辑、Shell、搜索、Skills、规划、目标、子代理、工作流 | 通用 Agent 开发 |
| **Code** | Standard + Code Mode SDK，模型可在单个 TypeScript 程序中编排多步操作 | 复杂代码生成 |
| **Minimal** | 仅 bash + `str_replace_editor`，极简环境 | 基准测试、模型评测 |
| **Creator** | Standard + 运行时检查、内存插件实验、预设编写指导 | 开发自定义 Agent 预设 |

## 核心优势

### 1. 极致模块化

与 PI-agent 的"原语优先"类似，但更彻底——**UI 本身也是插件**。整个系统没有"不可替换"的部分。

### 2. 可追溯性最强

追加写入日志 + Trajectory 视图，完整记录模型的每一个决策和行动。这是 PI-agent 和 Claude Code 都不具备的深度可观测性。

### 3. 144k Star 的社区生态

GitHub 144k Star、14.7k Fork，社区活跃度极高。插件通过 `dsh-plugin` GitHub Topic 发现。

### 4. DeepSeek 模型原生集成

作为 DeepSeek 官方工具，对 DeepSeek 系列模型（DeepSeek-V3、DeepSeek-Coder、DeepSeek-R1）有原生优化。

### 5. 多语言支持

TypeScript/JavaScript 为主，同时支持 Python 组件。文档完整支持中英文。

## 核心局限

### 1. 开发者预览阶段

明确标注"THERE WILL BE COMPATIBILITY-BREAKING CHANGES"——API 不稳定，生产环境慎用。

### 2. 学习曲线陡峭

Cordis 内核 + 插件架构 + 4 种运行模式，概念密度远高于 Claude Code / Codex。

### 3. 缺乏开箱即用体验

不像 Claude Code 装好就能写代码——dsh 需要理解插件体系、配置运行模式、组装能力栈。

### 4. 模型支持信息不透明

官网和 README 均未列出具体支持哪些模型。插件架构理论上可接入任意模型，但实际生态成熟度未知。

## 与 PI-agent 对比：两个框架的差异

| 维度 | DeepSeek Harness | PI-agent |
|------|-----------------|----------|
| **内核** | Cordis（插件管理） | 自研扩展系统 |
| **模块化粒度** | 极细（UI 也是插件） | 粗（扩展/Skills） |
| **可追溯性** | ⭐⭐⭐（追加日志 + Trajectory） | ⭐ |
| **运行模式** | 4 种（Standard/Code/Minimal/Creator） | 4 种（Interactive/Print/RPC/SDK） |
| **模型支持** | DeepSeek 原生 + 插件扩展 | 15+ 提供商 |
| **成熟度** | 开发者预览 | 早期 |
| **社区** | 144k Star | 较小 |
| **学习曲线** | 陡峭 | 中等 |

## 规范与配置：AGENTS.md 原生支持

DeepSeek Harness 仓库自带 `AGENTS.md` + `.agents/` + `.claude/` 目录，对跨工具规范有原生支持。

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
- 想构建自定义 Agent 预设的高级开发者（Creator 模式）
- 需要极细粒度模块化的企业（每个组件可替换）
- 模型基准测试（Minimal 模式）

**不太适合**：

- 需要开箱即用体验的新手
- 追求稳定 API 的生产环境（开发者预览阶段）
- 非 DeepSeek 模型用户（模型生态成熟度未知）
- 团队协作（缺乏内置的团队规范机制）

## 最佳实践

1. **从 Standard 模式开始**：先体验完整工具集，再按需裁剪
2. **用 AGENTS.md 做跨工具规范**：与其他工具团队协作时的通用入口
3. **用 Trajectory 视图调试**：排查 Agent 决策问题的利器
4. **关注 `dsh-plugin` Topic**：社区插件生态是核心竞争力
5. **Minimal 模式做基准测试**：评测不同模型的裸能力

## 参考

- [DeepSeek Harness 官网](https://www.deepseek.com/harness/en/)
- [GitHub 仓库](https://github.com/deepseek-ai/deepseek-harness)（144k Star）
- [PI-agent 深度评测](./pi-agent)
- [AI Coding 工具全景](./overview)

## 下一步

- 对比 PI-agent → [PI-agent 深度评测](./pi-agent)
- 对比 Claude Code → [Claude Code 深度评测](./claude-code)
- 团队引入 → [团队 AI 工作流](../workflows/team)

## 如果你想

- 对比主流工具 → [AI Coding 工具全景](./overview)
- 选型决策 → [AI Coding 工具全景](./overview)

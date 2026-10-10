---
title: Trae 深度评测
description: 字节跳动 Trae 评测——TRAE IDE 与 TRAE Work 双产品线、免费的中文 AI 编程工具
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-10
verifiedWith:
  sources:
    - name: Trae 官网
      url: https://trae.ai
      accessedAt: 2026-08-17
    - name: Introducing TRAE Work（TRAE 官方博客）
      url: https://www.trae.ai/blog/trae_work_0609
      accessedAt: 2026-10-10
    - name: Introducing The New SOLO（TRAE 官方博客）
      url: https://www.trae.ai/blog/new_solo_beta_0331
      accessedAt: 2026-10-10
    - name: TRAE 产品矩阵（TRAE 官方文档）
      url: https://docs.trae.cn/ide_trae-overview
      accessedAt: 2026-10-10
---

# Trae 深度评测

> **TL;DR**：免费、中文场景优化。**产品线已经分裂成 TRAE IDE 和 TRAE Work 两个独立产品**——不是融合，是从内嵌 SOLO 拆出来再改名。

⏱ 预计阅读时间：4 分钟

## 产品形态：两个产品，不是一个

这是本页最需要更新的一条认知。官方博客原话：

> TRAE IDE goes deep into software engineering. TRAE Work goes wide across professional work. **Two products. One shared mission.**

时间线：

| 时间 | 事件 |
|------|------|
| 2026-03-31 | 独立 SOLO 上线 beta（Desktop + Web），从 IDE 拆出 |
| 2026-06-09 | SOLO 正式改名 **TRAE Work**，扩展到 Desktop / Web / Mobile |

**为什么拆**：社区反馈内嵌在 IDE 里的 SOLO「能力阉割、上限不高」，大改动最终还是要人工接手。独立后才拿到全自动化能力的上限。

**为什么改名**：官方说用户开始把它带进预料外的场景——写产品文档、分析数据集、做调研报告，**The work had outgrown the name**。

### 产品矩阵

| 产品 | 定位 | 特点 |
|------|------|------|
| **TRAE IDE** | 面向开发者的 AI 原生 IDE | 保留编辑器 / 终端 / 调试 / Git；IDE 模式 + SOLO 模式双模 |
| **TRAE Work** | AI 工作助手 | Desktop / Web / Mobile 三端；Work / Code / Design 三模式 |
| **TRAE Plugin** | VS Code / JetBrains 插件 | 零迁移成本接入现有 IDE |
| **TRAE CLI** | 终端 Code Agent | 可脚本化，支持非交互模式嵌入 CI/CD |
| **TRAE 企业版** | 团队治理 | 席位管理、用量限额、企业知识库、OpenAPI |

> 📌 官方文档在不同时期对 TRAE Work 的模式命名不一致（早期博客称 Code Mode + MTC Mode，最新博客称 Work / Code / Design）。这里以最新博客为准。形态的完整分析见 → [Agent 工作台的产品形态与设计取舍](./agent-workspace)

## 核心特点

- **字节跳动出品**：中文场景优化
- **免费使用**：无订阅费用
- **AGENTS.md + CLAUDE.md 双支持**：跨工具兼容性好
- **三端同步**：手机下发任务、电脑执行

## 优势

- 完全免费
- 中文提示词效果好
- IDE 体验完整
- 4 层规则加载体系，灵活度高
- TRAE Work 的移动端在同类里较早落地

## 劣势

- 国际化支持有限
- 生态不如 Cursor / Copilot
- IDE 模式的 Agent 能力弱于独立 Work（原 SOLO 内嵌版的已知问题）

## 规范与配置：4 层规则加载体系

Trae 的规则加载机制比多数工具更灵活——支持 AGENTS.md、CLAUDE.md、`.trae/rules/` 三套文件，是跨工具兼容性最好的 IDE 之一。

### 规则文件加载链

```
内置工作区规则（IDE 设置开启）
├── 项目根/AGENTS.md          # 跨工具通用（原生支持 ✅）
├── 项目根/CLAUDE.md          # Claude 兼容（原生支持 ✅）
├── 项目根/.trae/rules/       # Trae 专属规则（4 种生效方式）
├── 项目根/.trae/skills/      # Trae 专属技能（按需加载）
└── 子目录/AGENTS.md          # 目录级（AI 读取该目录文件时加载）
```

### 路径作用域

Trae 支持两种路径作用域机制：

**方式一：子目录 AGENTS.md（推荐）**

```
src/pages/AGENTS.md     # 仅 pages 相关文件被涉及时生效
src/common/AGENTS.md    # 仅 common 相关文件被涉及时生效
```

**方式二：.trae/rules/ glob 匹配**

```
.trae/rules/
├── always.md              # 始终生效
├── react-components.md    # glob: 匹配 src/components/**
└── api-conventions.md     # description: AI 智能判断
```

### .trae/skills/ 技能系统

Trae 的技能文件（`.trae/skills/`）与规则不同——**按需加载**，描述匹配时才注入上下文：

```
.trae/skills/
├── generate-page-tasks/SKILL.md   # 生成页面任务
├── create-module-code/SKILL.md    # 创建模块代码
└── code-review/SKILL.md           # 代码审查
```

注意：`.claude/skills/` 在 Trae 里**不会被自动识别**，需要迁移到 `.trae/skills/`。

### 与 Claude Code / Codex / Cursor 的兼容

| 场景 | 解法 |
|------|------|
| Codex 用户也要读 Trae 的规则 | 把通用规范放 `AGENTS.md`，Codex 原生支持 |
| Claude Code 用户也要读 Trae 的规则 | 把通用规范放 `CLAUDE.md` 或 `AGENTS.md`，Claude Code 均支持 |
| Cursor 用户也要读 Trae 的规则 | 把通用规范放 `AGENTS.md`，Cursor 兼容读取 |
| Trae 专属配置 | 留在 `.trae/rules/` 和 `.trae/skills/`，其他工具忽略 |

### Trae 用户的跨工具最佳实践

- **通用规范写 AGENTS.md**：跨工具兼容的铁律、构建命令、代码风格
- **高频约束放 AGENTS.md**：组件库铁律、业务身份识别（常驻上下文）
- **低频 SOP 做成 .trae/skills/**：如"如何梳理页面架构"（按需加载，省上下文）
- **.trae/rules/ 放 Trae 专属**：glob 路径规则、UI 创建规则
- **避免只写 CLAUDE.md**：Codex 不认，但 AGENTS.md 三个工具都认

## 适用场景

- 中文开发团队
- 预算有限
- 简单代码补全需求（TRAE IDE）
- 文档 / 数据 / 调研类任务（TRAE Work）
- 与 Claude Code / Codex 团队协作（AGENTS.md 通吃）

## 参考

- [Trae 官网](https://trae.ai)
- [Introducing TRAE Work](https://www.trae.ai/blog/trae_work_0609)
- [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- [AI 工具全景](./overview)

## 下一步

- 看形态收敛逻辑 → [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- 团队引入 → [团队 AI 工作流](/ai-harness/workflows/team)

## 如果你想

- 对比主流工具 → [AI 工具全景](./overview)
- 看跨角色协作 → [跨角色交付](./cross-role-delivery)

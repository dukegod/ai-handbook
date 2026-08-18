---
title: Trae 深度评测
description: 字节跳动 Trae 评测——免费的中文 AI 编程 IDE
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-08-17
verifiedWith:
  sources:
    - name: Trae 官网
      url: https://trae.ai
      accessedAt: 2026-08-17
---

# Trae 深度评测

> **TL;DR**：免费使用，中文场景优化，适合预算有限的中文开发团队。

⏱ 预计阅读时间：3 分钟

## 核心特点

- **字节跳动出品**：中文场景优化
- **免费使用**：无订阅费用
- **AI-native IDE**：基于 VS Code
- **AGENTS.md + CLAUDE.md 双支持**：跨工具兼容性好

## 优势

- 完全免费
- 中文提示词效果好
- IDE 体验完整
- 4 层规则加载体系，灵活度高

## 劣势

- Agent 能力较弱
- 国际化支持有限
- 生态不如 Cursor/Copilot

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
- 简单代码补全需求
- 与 Claude Code / Codex 团队协作（AGENTS.md 通吃）

## 选型建议

| 需求 | 推荐 |
|------|------|
| 免费 + 中文 | Trae |
| 推理最强 | Codex CLI |
| CLI + Git 集成 | Aider |
| IDE + 多模型 | Continue |

## 参考

- [Trae 官网](https://trae.ai)
- [AI Coding 工具全景](./overview)

## 下一步

- 团队引入 → [团队 AI 工作流](../workflows/team)
- 企业部署 → [企业部署指南](../enterprise/deployment)

## 如果你想

- 对比主流工具 → [AI Coding 工具全景](./overview)
- 选型决策 → [AI Coding 工具全景](./overview)

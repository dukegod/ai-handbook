---
title: Cursor 深度评测
description: AI-native IDE 的优势、局限与适用场景
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: Cursor 官方文档
      url: https://docs.cursor.com
      accessedAt: 2026-08-13
---

# Cursor 深度评测

> **TL;DR**：AI-native IDE——在 VS Code 基础上深度集成 AI，多模型支持是核心差异化。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Cursor 的核心优势与局限
- AI-native IDE 的设计理念
- 与 Claude Code / Copilot 的差异化
- 适用场景与不适用场景

## 核心优势

### 1. AI-native IDE

Cursor 基于 VS Code 构建，但 AI 是一等公民：

- **Tab 补全**：AI 预测下一步输入
- **Cmd+K**：选中代码后 AI 修改
- **Chat**：对话式编程
- **Composer**：多文件编辑

### 2. 多模型支持

Cursor 支持多种模型：

- Claude（Opus / Sonnet / Haiku）
- GPT-4o / GPT-5
- 自定义模型（API Key）

**多模型是 Cursor 的独特优势**——可以根据任务选择最合适的模型。

### 3. 上下文理解

- 自动索引整个项目
- 理解代码结构和依赖
- 支持 @引用文件、函数、文档

### 4. 完整 IDE 体验

- 调试器
- Git 集成
- 终端
- 插件生态

## 核心局限

### 1. Agent 能力受限

相比 Claude Code，Cursor 的 Agent 能力较弱：

- 不能执行复杂 Shell 命令
- 不能派生子代理
- 不能连接 MCP 工具

### 2. 绑定 IDE

必须使用 Cursor IDE，不能在终端或其他 IDE 中使用。

### 3. 中文支持一般

中文提示词效果不如英文。

## 与 Claude Code / Copilot 对比

| 维度 | Cursor | Claude Code | Copilot |
|------|--------|-------------|---------|
| **形态** | IDE | CLI | 插件 |
| **Agent 能力** | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| **多模型** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **学习曲线** | 中 | 高 | 低 |
| **价格** | $20-40/月 | $20-200/月 | $10-39/月 |
| **IDE 集成** | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |

## 适用场景

**最适合**：

- IDE 用户（习惯 VS Code）
- 多模型需求（不同任务用不同模型）
- 快速原型开发
- 前端开发（实时预览）

**不太适合**：

- 终端用户（Claude Code 更合适）
- CI/CD 集成（Claude Code 更强）
- 复杂 Agent 任务（Claude Code 更强）
- 预算有限（Copilot/Trae 更便宜）

## 规范与配置：.cursor/rules + AGENTS.md 双轨

Cursor 有两套规则文件机制，了解它才能和 Claude Code / Codex / Trae 团队协作：

### 规则文件加载链

```
~/.cursor/rules/              # 全局（用户级偏好）
├── 项目根/.cursor/rules/     # 项目级（团队共享，✅ 提交到 Git）
│   ├── always.md             # 始终生效
│   ├── *.md (glob)           # 按 glob 匹配生效
│   └── *.md (description)    # 按 AI 智能判断生效
├── 项目根/AGENTS.md          # 跨工具兼容（兼容读取）
└── 子目录/.cursor/rules/     # 目录级
```

### 路径作用域

Cursor 的 `.cursor/rules/` 支持 4 种生效方式：

| 方式 | 文件 | 生效条件 |
|------|------|---------|
| **始终生效** | `always.md` | 所有会话 |
| **Glob 匹配** | `*.md`（文件名含 glob） | 文件路径匹配时 |
| **智能判断** | `*.md`（description 字段） | AI 判断相关时 |
| **手动触发** | `*.md`（用户选择） | 用户手动 @引用 |

```
.cursor/rules/
├── always.md              # 始终生效（如"用中文回复"）
├── react-components.md    # glob: 匹配 src/components/**
└── api-conventions.md     # description: AI 智能判断
```

### 与 Claude Code / Codex / Trae 的兼容

| 场景 | 解法 |
|------|------|
| Codex 用户也要读 Cursor 的规则 | 把通用规范放 `AGENTS.md`，Codex 原生支持 |
| Claude Code 用户也要读 Cursor 的规则 | 把通用规范放 `AGENTS.md`，Claude Code 新版同时读取 |
| Trae 用户也要读 Cursor 的规则 | 把通用规范放 `AGENTS.md`，Trae 原生支持 |
| Cursor 专属配置（glob 规则） | 留在 `.cursor/rules/`，其他工具忽略 |

### Cursor 用户的跨工具最佳实践

- **通用规范写 AGENTS.md**：跨工具兼容的铁律、构建命令、代码风格
- **.cursor/rules/ 放 Cursor 专属**：glob 路径规则、AI 智能判断规则
- **避免在 .cursor/rules/ 写全局铁律**：Codex / Trae 不认这个路径
- **AGENTS.md 尽量短**：建议 ≤200 行，避免上下文膨胀

## 最佳实践

1. **用 @引用上下文**：@file、@function、@doc 让 AI 理解更多上下文
2. **选对模型**：简单任务用 Haiku，复杂任务用 Opus
3. **用 Composer 多文件编辑**：比逐个文件修改更高效
4. **配置 .cursorignore**：排除不需要索引的文件
5. **与 Codex / Claude Code 团队协作**：通用规范写 AGENTS.md

## 参考

- [Cursor 官方文档](https://docs.cursor.com)
- [AI Coding 工具全景](./overview)

## 下一步

- 深入 Copilot → [GitHub Copilot 评测](./copilot)
- 团队引入 → [团队 AI 工作流](../workflows/team)

## 如果你想

- 对比 Claude Code → [Claude Code 深度评测](./claude-code)
- 选型决策 → [AI Coding 工具全景](./overview)

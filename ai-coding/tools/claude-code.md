---
title: Claude Code 深度评测
description: Anthropic 官方 CLI 的能力边界、最佳实践与适用场景
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Claude Code 深度评测

> **TL;DR**：Agent 能力最强的 AI Coding 工具——MCP 生态、Subagent、Skills 让它不只写代码，还能"做事"。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- Claude Code 的核心优势与局限
- Agent 能力（MCP / Skills / Subagents）
- 与 Cursor / Copilot 的差异化
- 适用场景与不适用场景

## 核心优势

### 1. Agent 能力最强

Claude Code 不只是"写代码"，还能：

- **读写文件**：自动读取、修改、创建文件
- **执行命令**：运行测试、构建、部署
- **搜索代码**：Grep/Glob 定位代码
- **联网搜索**：WebFetch/WebSearch 获取信息
- **派生子代理**：并行处理多个任务

### 2. MCP 生态

MCP（Model Context Protocol）让 Claude Code 连接外部工具：

- GitHub / GitLab 集成
- 数据库查询
- API 调用
- 自定义工具

**MCP 是 Claude Code 的独特优势**——Cursor / Copilot 都没有类似生态。

### 3. Skills 可复用

Skills 是可复用的任务模板：

- 代码审查
- 文档生成
- 测试用例编写
- 自定义工作流

### 4. CLI 原生

- 不依赖 IDE
- 可脚本化
- 可 CI/CD 集成
- 终端用户友好

## 核心局限

### 1. 没有 GUI 预览

代码修改只能通过 diff 查看，没有实时预览。

### 2. 学习曲线较高

需要熟悉终端操作、CLAUDE.md 配置、MCP 设置。

### 3. 价格较高

$20-200/月，比 Copilot ($10/月) 贵。

### 4. 中文支持一般

中文提示词效果不如英文。

## 与 Cursor / Copilot 对比

| 维度 | Claude Code | Cursor | Copilot |
|------|-------------|--------|---------|
| **形态** | CLI | IDE | 插件 |
| **Agent 能力** | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **MCP 生态** | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **多模型** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **学习曲线** | 高 | 中 | 低 |
| **价格** | $20-200/月 | $20-40/月 | $10-39/月 |
| **CI 集成** | ⭐⭐⭐ | ⭐ | ⭐⭐ |

## 适用场景

**最适合**：

- 复杂代码重构（需要理解整个项目）
- 多文件修改（Agent 自动处理）
- CI/CD 集成（Headless 模式）
- 自定义工作流（Skills + MCP）
- 长任务自动化（Subagents）

**不太适合**：

- 简单代码补全（Copilot 更方便）
- IDE 用户（Cursor 更自然）
- 预算有限（Copilot/Trae 更便宜）

## 规范与配置：规则文件加载机制

Claude Code 的配置体系分三层，了解它才能和 Codex/Cursor/Trae 团队协作：

### 规则文件加载链

```
~/.claude/CLAUDE.md          # 全局（用户级偏好）
├── 项目根/CLAUDE.md          # 项目级（团队共享，✅ 提交到 Git）
├── 项目根/CLAUDE.local.md    # 项目级（个人覆盖，❌ 不提交）
├── 子目录/CLAUDE.md          # 目录级（子目录专属规则）
└── AGENTS.md                 # 跨工具兼容（新版同时读取）
```

**加载顺序**：全局 → 项目 → 子目录，逐级合并。`CLAUDE.md` 优先于 `AGENTS.md`。

### 路径作用域

Claude Code 通过**子目录 CLAUDE.md** 实现路径作用域：

```
src/pages/CLAUDE.md     # 仅 pages 相关文件被涉及时生效
src/common/CLAUDE.md    # 仅 common 相关文件被涉及时生效
```

早期版本用 `.claude/rules/*.md` 的 `---paths:` frontmatter，但这是 Claude 专属语法，Codex/Cursor 不认。**推荐用子目录 CLAUDE.md 替代**。

### 与 Codex/Cursor/Trae 的兼容

| 场景 | 解法 |
|------|------|
| Codex 用户也要读 Claude 的规则 | 把通用规范放 `AGENTS.md`，Codex 原生支持 |
| Cursor 用户也要读 Claude 的规则 | 把通用规范放 `AGENTS.md`，Cursor 兼容读取 |
| Trae 用户也要读 Claude 的规则 | 把通用规范放 `AGENTS.md`，Trae 原生支持 |
| Claude 专属配置（hooks/skills/MCP） | 留在 `CLAUDE.md` 或 `.claude/` 目录，其他工具忽略 |

### CLAUDE.md vs AGENTS.md：怎么选

- **CLAUDE.md**：Claude 专属深度配置（hooks、skills、MCP、superpower 映射）
- **AGENTS.md**：跨工具通用规范（构建命令、代码风格、目录结构、铁律）
- **推荐做法**：通用规范写 `AGENTS.md`，CLAUDE.md 薄引用 + 补充 Claude 专属内容

## 最佳实践

1. **用 CLAUDE.md 项目记忆**：把项目规范、常见命令写进去
2. **用 MCP 连接外部工具**：GitHub、数据库、API
3. **用 Skills 复用工作流**：代码审查、文档生成
4. **用 Subagent 并行处理**：大任务拆成小任务
5. **与 Codex/Cursor 团队协作**：通用规范写 AGENTS.md，CLAUDE.md 只放 Claude 专属

## 参考

- [Claude Code 官方文档](https://code.claude.com/docs)
- [Claude Code 精通](/claude-code/)
- [AI Coding 工具全景](./overview)

## 下一步

- 深入 Cursor → [Cursor 深度评测](./cursor)
- 团队引入 → [团队 AI 工作流](../workflows/team)
- 企业部署 → [企业部署指南](../enterprise/deployment)

## 如果你想

- 学习 Claude Code 使用 → [Claude Code 精通](/claude-code/)
- 看实战案例 → [Cookbook](/cookbook/)

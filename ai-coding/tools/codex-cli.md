---
title: Codex CLI 深度评测
description: OpenAI Codex CLI 工具评测——推理最强的终端 AI 编程助手
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-08-17
verifiedWith:
  sources:
    - name: OpenAI Codex
      url: https://openai.com/index/codex/
      accessedAt: 2026-08-17
---

# Codex CLI 深度评测

> **TL;DR**：推理最强但按 token 计费，适合数学/逻辑密集的编程任务。

⏱ 预计阅读时间：3 分钟

## 核心特点

- **OpenAI 官方 CLI**：类似 Claude Code 的终端工具
- **推理能力最强**：基于 o-series 模型
- **按 token 计费**：无订阅，用多少付多少

## 优势

- 推理能力业界最强（o3 模型）
- CLI 原生，可脚本化
- 支持复杂逻辑推理
- **AGENTS.md 原生支持**：跨工具兼容性最好

## 劣势

- 按 token 计费，成本不可预测
- Agent 能力不如 Claude Code
- MCP 生态不如 Claude Code
- 只认 AGENTS.md，不支持 CLAUDE.md / .cursor/rules

## 规范与配置：AGENTS.md 原生支持

Codex **只认 AGENTS.md**——这是它的规则文件机制，也是它跨工具兼容性最好的原因。

### 规则文件加载链

```
~/.agents/AGENTS.md           # 全局（用户级偏好）
├── 项目根/AGENTS.md          # 项目级（团队共享）
├── 项目根/AGENTS-{task}.md   # 任务级（如 AGENTS-refactor.md）
├── 项目根/AGENTS-{lang}.md   # 语言级（如 AGENTS-Python.md）
└── 子目录/AGENTS.md          # 目录级（天然路径作用域）
```

**加载顺序**：全局 → 项目 → 子目录，逐级合并。

### 路径作用域

Codex 通过**子目录 AGENTS.md** 实现路径作用域——这是最自然的方式：

```
src/pages/AGENTS.md     # 仅 pages 相关文件被涉及时生效
src/common/AGENTS.md    # 仅 common 相关文件被涉及时生效
```

无需 frontmatter 魔法，目录级 AGENTS.md 天然只作用于该目录树。

### 与 Claude Code / Cursor / Trae 的兼容

| 场景 | 解法 |
|------|------|
| Claude Code 用户也要读 Codex 的规则 | 把通用规范放 `AGENTS.md`，Claude Code 新版同时读取 |
| Cursor 用户也要读 Codex 的规则 | 把通用规范放 `AGENTS.md`，Cursor 兼容读取 |
| Trae 用户也要读 Codex 的规则 | 把通用规范放 `AGENTS.md`，Trae 原生支持 |
| Codex 专属配置 | 只认 `AGENTS.md`，不支持其他工具的规则文件 |

### Codex 用户的跨工具最佳实践

- **仓库根放 AGENTS.md**：通用规范（构建命令、代码风格、目录结构）
- **子目录放 AGENTS.md**：路径作用域规则
- **避免 CLAUDE.md / .cursor/rules**：Codex 不认这些文件
- **AGENTS.md 尽量短**：建议 ≤200 行，避免上下文膨胀

## 适用场景

- 数学/逻辑密集的编程任务
- 需要强推理的代码生成
- 成本不敏感的场景
- 与 Claude Code / Cursor / Trae 团队协作（AGENTS.md 通吃）

## 选型建议

| 需求 | 推荐 |
|------|------|
| 推理最强 | Codex CLI |
| CLI + Git 集成 | Aider |
| IDE + 多模型 | Continue |

## 参考

- [OpenAI Codex](https://openai.com/index/codex/)
- [AI Coding 工具全景](./overview)

## 下一步

- 团队引入 → [团队 AI 工作流](../workflows/team)
- 企业部署 → [企业部署指南](../enterprise/deployment)

## 如果你想

- 对比主流工具 → [AI Coding 工具全景](./overview)
- 选型决策 → [AI Coding 工具全景](./overview)

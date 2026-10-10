---
title: Cursor 深度评测
description: AI-native IDE 的优势、局限与适用场景
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-10
verifiedWith:
  sources:
    - name: Cursor 官方文档
      url: https://docs.cursor.com
      accessedAt: 2026-08-13
    - name: Meet the new Cursor（Cursor 官方博客）
      url: https://cursor.com/blog/cursor-3
      accessedAt: 2026-10-10
    - name: Cursor Changelog
      url: https://cursor.com/changelog
      accessedAt: 2026-10-10
---

# Cursor 深度评测

> **TL;DR**：从「VS Code 上的 AI 增强」变成了**从零重建的 agent 工作台**（Cursor 3）。多模型支持仍是核心差异化，但真正的变化是跨端任务编排 + 交付链路内建。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Cursor 3 相比旧版 Cursor 的实质变化
- 多模型与自研 Composer 模型
- 云端 agent、Origin 托管与跨端任务迁移
- 规则文件机制与跨工具协作

## Cursor 3 的实质变化

Cursor 早期基于 VS Code fork 起步（官方理由：so we could shape our own surface）。**Cursor 3 直接从零重建了界面，不再基于 VS Code**，并且原生支持多 repo 布局。

但旧 IDE **没有被删除**，变成「随时可切回」的兼容选项——不强制迁移，把迁移风险降到零。

> 📌 **2026-08 版说明**：本页早期版本称 Cursor 是「AI-native IDE」，这个定位已经过时。Cursor 官方现在自称 agent 工作台/构建平台，不是代码编辑器。形态与产品线的完整分析见 → [Agent 工作台的产品形态与设计取舍](./agent-workspace)

### 多端统一

所有 local 和 cloud agent 出现在同一个 sidebar，包括你从 mobile、web、Slack、GitHub、Linear 起的那些。

**会话可跨端迁移**：

- cloud → local：拉回本地改代码、跑测试
- local → cloud：转入后台继续跑（适合长任务，或你要离开电脑时）

### 内建交付链路

- **Origin 代码托管**（2026-08-17 起 beta）：代码仓库、PR、代码浏览、GitHub 同步。自己接上外部 SCM 不再必需
- **Self-testing agents**：agent 在自己的沙箱里测试改动，直到验证通过才提交 PR
- **Demos over diffs**：产出视频、截图、日志供审阅，而不是只给 diff
- **Projects + coordinator agent**：coordinator 不写代码，只做规划、派活、验收；每个 Project 维护一份跨机器同步的 shared context

### 多模型支持

支持 Claude、GPT、Grok 等主流模型，并可通过 API Key 接自定义模型。

另外 Cursor 有**自研模型**（Composer 系列），早期资料称 Composer 2 为 1.5T 参数——该数字来自第三方转述，官方未确认。

## 核心局限

- **模型锁定弱**：相较 Claude Code，扩展深度有限（hooks / skills / MCP 深度不如 Claude Code）
- **云端执行拿不到本地资源**：依赖本地数据库或 API 的测试，Cloud 跑不了（CLI 和桌面端可以）
- **闭源**：桌面端与 IDE 扩展不开源；代码托管与协作模型对平台有绑定

## 与 Claude Code / Copilot 对比

| 维度 | Cursor | Claude Code | Copilot |
|------|--------|-------------|---------|
| **形态** | Agent 工作台（保留 IDE 兼容） | CLI | 插件 |
| **Agent 能力** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| **多模型** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **云端常驻** | ✅ | ✅（Managed Agents） | ❌ |
| **跨端会话迁移** | ✅ | 部分 | ❌ |
| **学习曲线** | 中 | 高 | 低 |
| **价格** | $20-40/月 | $20-200/月 | $10-39/月 |

> 📌 对比数据中「Agent 能力 ⭐⭐」的旧结论已作废：Cursor 现在有 cloud agents、subagents（各自独立 VM）、custom modes、/goal、Automations，能力面显著扩大。

## 适用场景

**最适合**：

- IDE 用户（习惯 VS Code）但希望摆脱 IDE 限制
- 多模型需求（不同任务用不同模型）
- 快速原型开发、需要浏览器实时预览
- 需要 agent 在后台跑长任务

**不太适合**：

- 纯终端用户（Claude Code 更合适）
- CI/CD 深度集成（Claude Code 更强）
- 需要严格审计 agent 执行逻辑的企业（CLI 开源方案如 MiniMax Code 更合适）

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
2. **选对模型**：简单任务用轻量模型，复杂任务用强模型
3. **长任务用 cloud agent**：合盖继续跑，回来直接审 PR
4. **审阅看 artifacts 不只看 diff**：视频 / 截图 / 日志能暴露 diff 看不出的问题
5. **配置 .cursorignore**：排除不需要索引的文件
6. **与 Codex / Claude Code 团队协作**：通用规范写 AGENTS.md

## 参考

- [Cursor 官方文档](https://docs.cursor.com)
- [Meet the new Cursor](https://cursor.com/blog/cursor-3)
- [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- [AI 工具全景](./overview)

## 下一步

- 看形态与产品线的收敛逻辑 → [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- 深入 Copilot → [GitHub Copilot 评测](./copilot)
- 团队引入 → [团队 AI 工作流](/ai-harness/workflows/team)

## 如果你想

- 对比主流工具 → [AI 工具全景](./overview)
- 对比 Claude Code → [Claude Code 深度评测](./claude-code)
- 看跨角色协作 → [跨角色交付](./cross-role-delivery)

---
title: Code Review 自动化
description: 用 AI 辅助 Code Review 的实践与陷阱
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
---

# Code Review 自动化

> **TL;DR**：AI 辅助 Code Review 能发现 80% 的常见问题，但核心逻辑仍需人工审查。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- AI Code Review 的能力边界
- 常见审查场景
- 与人工审查的配合
- 避免的坑

## AI Code Review 能做什么

### 能做的

| 类型 | 示例 |
|------|------|
| **代码风格** | 命名规范、格式问题 |
| **常见 bug** | 空指针、数组越界、类型错误 |
| **安全问题** | SQL 注入、XSS、敏感信息泄露 |
| **性能问题** | 循环嵌套、内存泄漏 |
| **代码重复** | 重复逻辑、可提取的公共函数 |

### 不能做的

| 类型 | 原因 |
|------|------|
| **业务逻辑** | AI 不理解业务需求 |
| **架构设计** | AI 不理解系统全局 |
| **用户体验** | AI 不理解用户需求 |
| **性能瓶颈** | AI 不知道实际负载 |

## 审查流程

### 流程 1：AI 初审 + 人工终审

```
PR 提交 → AI 自动审查 → 人工确认 AI 建议 → 合并
```

**优点**：效率高，AI 过滤常见问题。

### 流程 2：人工初审 + AI 复审

```
PR 提交 → 人工审查 → AI 复审 → 合并
```

**优点**：AI 发现人工遗漏的问题。

### 流程 3：并行审查

```
PR 提交 → AI 审查 + 人工审查 → 合并建议 → 合并
```

**优点**：最全面，但耗时最长。

## Claude Code 审查示例

```bash
claude -p "审查这个 PR：
1. 代码风格是否符合项目规范
2. 是否有潜在的 bug
3. 是否有安全问题
4. 是否有性能问题" \
  --allowedTools "Read,Grep,Glob"
```

## 常见坑

**1. 不要完全信任 AI**

AI 可能误报（false positive）或漏报（false negative）。人工确认是必须的。

**2. 不要忽略上下文**

AI 可能不理解代码的业务上下文。人工需要补充。

**3. 不要过度审查**

不是所有 AI 建议都需要采纳。选择有价值的建议。

**4. 不要忽略学习**

AI 审查是学习机会。了解 AI 发现的问题类型，提升自己。

## 参考

- [Claude Code Skills](/claude-code/skills/what-is-a-skill)
- [Claude Code 官方文档](https://code.claude.com/docs)

## 下一步

- 常见模式 → [代码重构模式](../patterns/refactor)
- 测试生成 → [测试生成模式](../patterns/testing)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 团队工作流 → [团队 AI 工作流](./team)

---
title: 团队 AI 工作流
description: 多人协作场景下的 AI 编程工作流设计
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
---

# 团队 AI 工作流

> **TL;DR**：团队引入 AI 工具的关键是统一规范——CLAUDE.md / .cursorignore / 代码风格要先行。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 团队引入 AI 工具的步骤
- 统一规范的重要性
- 常见协作场景的工作流
- 避免的坑

## 引入步骤

### 第 1 步：选型

根据团队情况选工具（参考 [AI Coding 工具全景](../tools/overview)）。

### 第 2 步：统一规范

- **CLAUDE.md**：项目规范、常见命令、代码风格
- **.cursorignore**：排除敏感文件
- **.copilotignore**：排除敏感文件

### 第 3 步：试点

- 选 1-2 个项目试点
- 收集反馈
- 调整规范

### 第 4 步：推广

- 全团队培训
- 建立最佳实践文档
- 定期复盘

## 统一规范

### CLAUDE.md 示例

```markdown
# 项目规范

## 技术栈
- React 18 + TypeScript
- Vite + pnpm
- Tailwind CSS

## 代码风格
- 使用函数式组件
- 使用 hooks
- 避免 class 组件

## 常见命令
- pnpm dev: 启动开发服务器
- pnpm build: 构建
- pnpm test: 测试
```

### .cursorignore 示例

```
node_modules/
.env
.env.local
*.log
dist/
```

## 常见协作场景

### 场景 1：代码审查

**流程**：

1. 开发者提交 PR
2. AI 自动审查（安全、风格、逻辑）
3. 人工确认 AI 建议
4. 合并

**工具**：Claude Code Skills / Copilot Workspace

### 场景 2：文档生成

**流程**：

1. 开发者写代码
2. AI 自动生成文档（README、API 文档）
3. 人工审核
4. 提交

**工具**：Claude Code / Cursor

### 场景 3：测试生成

**流程**：

1. 开发者写函数
2. AI 自动生成测试用例
3. 人工审核测试覆盖
4. 提交

**工具**：Claude Code / Copilot

## 避免的坑

**1. 不要完全依赖 AI**

AI 是辅助，不是替代。核心设计、架构决策仍需人工。

**2. 不要忽略代码审查**

AI 生成的代码也需要审查。AI 可能生成有 bug 的代码。

**3. 不要泄露敏感信息**

配置 .cursorignore / .copilotignore，排除 .env、密钥等。

**4. 不要忽略培训**

团队成员需要学习如何有效使用 AI 工具。

## 参考

- [Claude Code 精通](/claude-code/)
- [AI Coding 工具全景](../tools/overview)

## 下一步

- CI/CD 集成 → [CI/CD 集成](./ci-cd)
- Code Review 自动化 → [Code Review 自动化](./code-review)

## 如果你想

- 企业部署 → [企业部署指南](../enterprise/deployment)
- 安全合规 → [安全与合规](../enterprise/security)

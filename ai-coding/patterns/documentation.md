---
title: 文档生成模式
description: AI 生成 API 文档、README、注释的最佳实践
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
---

# 文档生成模式

> **TL;DR**：AI 擅长生成"结构化"文档（API 文档、README），"叙述性"文档仍需人工润色。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- AI 擅长生成的文档类型
- 人工润色的文档类型
- 文档生成的最佳流程
- 常见坑

## AI 擅长的文档

### 1. API 文档

从函数签名自动生成 JSDoc / TSDoc：

```typescript
// AI 生成的 JSDoc
/**
 * 验证邮箱格式
 * @param email - 邮箱地址
 * @returns 是否有效
 * @example
 * validateEmail('test@example.com') // true
 * validateEmail('invalid') // false
 */
function validateEmail(email: string): boolean {
  // 验证逻辑
}
```

### 2. README

从代码结构自动生成 README：

- 项目简介
- 安装步骤
- 使用示例
- API 参考

### 3. 代码注释

为复杂逻辑添加注释：

```typescript
// AI 生成的注释
// 使用二分查找在有序数组中查找目标值
// 时间复杂度: O(log n)
// 空间复杂度: O(1)
function binarySearch(arr: number[], target: number): number {
  // 查找逻辑
}
```

### 4. Changelog

从 Git 提交自动生成 Changelog。

## 人工润色的文档

### 1. 架构文档

需要理解系统全局，AI 不知道设计决策。

### 2. 教程文档

需要理解用户水平，AI 不知道读者背景。

### 3. 故障排查

需要理解实际问题，AI 不知道生产环境。

## 最佳流程

### 第 1 步：AI 生成初稿

```bash
claude -p "为 src/utils.ts 生成 API 文档，使用 JSDoc 格式"
```

### 第 2 步：人工审核

检查 AI 生成的文档：

- 是否准确描述了函数行为
- 是否包含了所有参数
- 是否有遗漏的返回值

### 第 3 步：人工润色

补充 AI 遗漏的信息：

- 使用示例
- 注意事项
- 常见错误

### 第 4 步：持续更新

代码变更后，文档也需要更新。

## Claude Code 文档生成示例

```bash
# 生成 API 文档
claude -p "为 src/api/ 目录生成 OpenAPI 规范文档"

# 生成 README
claude -p "根据项目结构生成 README.md，包括安装、使用、API 参考"

# 更新文档
claude -p "更新 README.md，反映 src/ 目录的最新变化"
```

## 常见坑

**1. 不要完全信任 AI 生成的文档**

AI 可能生成不准确的描述。人工审核是必须的。

**2. 不要忽略文档质量**

AI 生成的文档可能只是"能读"，不一定"有用"。关注文档质量。

**3. 不要忽略文档维护**

代码变更后，文档也需要更新。

**4. 不要忽略文档风格**

统一文档风格（格式、术语、语气）。

## 参考

- [JSDoc 文档](https://jsdoc.app/)
- [OpenAPI 规范](https://swagger.io/specification/)
- [Claude Code 精通](/claude-code/)

## 下一步

- Code Review → [Code Review 自动化](../workflows/code-review)
- 团队工作流 → [团队 AI 工作流](../workflows/team)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 企业部署 → [企业部署指南](../enterprise/deployment)

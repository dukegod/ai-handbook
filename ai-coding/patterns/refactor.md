---
title: 代码重构模式
description: AI 辅助代码重构的最佳实践与常见模式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
---

# 代码重构模式

> **TL;DR**：AI 擅长"机械性"重构（提取函数、重命名、格式化），"逻辑性"重构仍需人工主导。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- AI 擅长的重构类型
- 人工主导的重构类型
- 重构的安全流程
- 常见坑

## AI 擅长的重构

### 1. 提取函数

```
// 重构前
function process(data) {
  // 100 行代码
}

// 重构后
function validate(data) { ... }
function transform(data) { ... }
function save(data) { ... }
function process(data) {
  const valid = validate(data);
  const transformed = transform(valid);
  save(transformed);
}
```

### 2. 重命名

批量重命名变量、函数、类。

### 3. 格式化

统一代码风格（缩进、空格、换行）。

### 4. 类型迁移

JavaScript → TypeScript 迁移。

### 5. 依赖更新

更新过时的依赖版本。

## 人工主导的重构

### 1. 架构重构

微服务拆分、模块重组。AI 不理解系统全局。

### 2. 数据库重构

表结构变更、索引优化。AI 不知道实际查询模式。

### 3. 性能重构

算法优化、缓存策略。AI 不知道实际负载。

## 安全流程

### 第 1 步：备份

```bash
git stash  # 或 git branch backup
```

### 第 2 步：小步重构

不要一次重构太多。每次只做一个小改动。

### 第 3 步：测试

每次重构后运行测试：

```bash
pnpm test
```

### 第 4 步：审查

AI 重构的代码也需要人工审查。

### 第 5 步：提交

确认无误后提交。

## Claude Code 重构示例

```bash
# 提取函数
claude -p "把 process 函数中的验证逻辑提取为独立函数"

# 重命名
claude -p "把所有 getData 改为 fetchData"

# TypeScript 迁移
claude -p "把 src/utils.js 迁移到 TypeScript"
```

## 常见坑

**1. 不要一次重构太多**

大范围重构容易引入 bug。小步快跑。

**2. 不要忽略测试**

没有测试的重构是危险的。先写测试，再重构。

**3. 不要完全信任 AI**

AI 重构可能改变逻辑。人工审查是必须的。

**4. 不要忽略版本控制**

每次重构都提交。出问题可以回滚。

## 参考

- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html)
- [Claude Code 精通](/claude-code/)

## 下一步

- 测试生成 → [测试生成模式](./testing)
- 文档生成 → [文档生成模式](./documentation)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 团队工作流 → [团队 AI 工作流](../workflows/team)

---
title: 测试生成模式
description: AI 生成单元测试、集成测试的技巧与边界
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
---

# 测试生成模式

> **TL;DR**：AI 擅长生成"机械性"单元测试，复杂场景测试仍需人工设计。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- AI 擅长生成的测试类型
- 人工设计的测试类型
- 测试生成的最佳流程
- 常见坑

## AI 擅长的测试

### 1. 单元测试

给定函数签名和预期行为，AI 可以生成完整的单元测试：

```typescript
// 原函数
function add(a: number, b: number): number {
  return a + b;
}

// AI 生成的测试
describe('add', () => {
  it('should add two positive numbers', () => {
    expect(add(1, 2)).toBe(3);
  });

  it('should add negative numbers', () => {
    expect(add(-1, -2)).toBe(-3);
  });

  it('should handle zero', () => {
    expect(add(0, 5)).toBe(5);
  });
});
```

### 2. 边界测试

AI 可以自动识别边界情况：

- 空值
- 零值
- 最大值
- 最小值
- 特殊字符

### 3. 快照测试

UI 组件的快照测试，AI 可以自动生成。

## 人工设计的测试

### 1. 集成测试

需要理解系统交互，AI 不知道实际调用链。

### 2. 端到端测试

需要理解用户流程，AI 不知道实际场景。

### 3. 性能测试

需要知道实际负载，AI 不知道生产环境。

### 4. 安全测试

需要理解攻击向量，AI 不知道威胁模型。

## 最佳流程

### 第 1 步：写函数

```typescript
function validateEmail(email: string): boolean {
  // 验证逻辑
}
```

### 第 2 步：AI 生成测试

```bash
claude -p "为 validateEmail 函数生成单元测试，覆盖正常情况、边界情况和异常情况"
```

### 第 3 步：人工审核

检查 AI 生成的测试：

- 是否覆盖了所有场景
- 是否有遗漏的边界情况
- 测试断言是否正确

### 第 4 步：补充测试

人工补充 AI 遗漏的测试。

## Claude Code 测试生成示例

```bash
# 生成单元测试
claude -p "为 src/utils.ts 中的 validateEmail 函数生成 Jest 单元测试"

# 生成集成测试
claude -p "为 src/api/users.ts 的用户注册接口生成集成测试"

# 补充测试用例
claude -p "分析现有测试覆盖率，补充缺失的测试用例"
```

## 常见坑

**1. 不要完全信任 AI 生成的测试**

AI 可能生成错误的测试断言。人工审核是必须的。

**2. 不要忽略测试质量**

AI 生成的测试可能只是"能跑"，不一定"有效"。关注测试质量。

**3. 不要忽略测试覆盖**

AI 可能遗漏重要的测试场景。人工补充是必要的。

**4. 不要忽略测试维护**

代码变更后，测试也需要更新。

## 参考

- [Jest 文档](https://jestjs.io/)
- [Claude Code 精通](/claude-code/)

## 下一步

- 文档生成 → [文档生成模式](./documentation)
- Code Review → [Code Review 自动化](../workflows/code-review)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 团队工作流 → [团队 AI 工作流](../workflows/team)

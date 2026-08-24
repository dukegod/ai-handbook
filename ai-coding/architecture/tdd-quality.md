---
title: TDD 质量保障
description: 如何用 TDD 收敛 AI 的概率性产出——RED→GREEN→REFACTOR 循环
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-19
---

# TDD 质量保障

> **TL;DR**：TDD 不是附属测试动作，而是 AI Native 的核心控制系统。测试用例是机器可执行的需求规约，可以把 AI 的不稳定输出收敛到确定行为。

## 你能在这里学到

- TDD 在 AI Native 中的角色
- RED→GREEN→REFACTOR 循环
- 测试作为 AI 执行目标
- 常见测试类型

## 前置知识

阅读本篇需要你先了解：

- [设计理念：人机分工](./design-philosophy)
- [测试生成模式](/ai-coding/patterns/testing)

## 一、TDD 在 AI Native 中的角色

AI 的输出是概率性的。测试用例是机器可执行的需求规约，可以把 AI 的不稳定输出收敛到确定行为。

```text
RED：先写失败测试，证明需求还没被满足
GREEN：写最小实现，让测试通过
REFACTOR：在测试保持绿色的前提下整理代码
```

它解决三个问题：

| 问题 | TDD 的作用 |
|------|------------|
| AI 输出不稳定 | 用测试结果给 AI 明确反馈 |
| 需求容易歧义 | 把需求转成机器可执行断言 |
| 回归难发现 | 把历史规则沉淀成长期保护网 |

## 二、RED→GREEN→REFACTOR 循环

### 第 1 步：RED——写失败测试

先写一个会失败的测试，证明需求还没被满足。

```typescript
// 搜索历史：写第 16 条时最老的被挤掉
it('should remove oldest when exceeding 15 items', () => {
  const history = new SearchHistory(maxItems: 15)
  // 添加 16 条记录
  for (let i = 0; i < 16; i++) {
    history.add(`keyword-${i}`)
  }
  // 第一条应该被移除
  expect(history.getAll()).not.toContain('keyword-0')
  expect(history.getAll()).toContain('keyword-15')
})
```

### 第 2 步：GREEN——写最小实现

写最小的代码让测试通过。

```typescript
class SearchHistory {
  private items: string[] = []
  private maxItems: number

  constructor(maxItems: number) {
    this.maxItems = maxItems
  }

  add(keyword: string) {
    this.items.push(keyword)
    if (this.items.length > this.maxItems) {
      this.items.shift() // 移除最老的
    }
  }

  getAll(): string[] {
    return [...this.items]
  }
}
```

### 第 3 步：REFACTOR——重构

在测试保持绿色的前提下整理代码。

```typescript
class SearchHistory {
  private items: string[] = []
  private readonly maxItems: number

  constructor(maxItems: number) {
    this.maxItems = maxItems
  }

  add(keyword: string): void {
    this.items.push(keyword)
    this.trimToLimit()
  }

  getAll(): readonly string[] {
    return this.items
  }

  private trimToLimit(): void {
    while (this.items.length > this.maxItems) {
      this.items.shift()
    }
  }
}
```

## 三、测试作为 AI 执行目标

在 AI Native 中，测试不是"写完代码后的补充"，而是 AI 执行任务前就应该存在的目标。

| 阶段 | 测试的作用 |
|------|------------|
| 任务开始前 | 测试作为需求规约，告诉 AI 要实现什么 |
| 任务执行中 | 测试结果给 AI 明确反馈（通过/失败） |
| 任务完成后 | 测试作为验收标准，确认 AI 完成了任务 |

## 四、常见测试类型

### 单元测试

给定函数签名和预期行为，AI 可以生成完整的单元测试。

```typescript
// AI 生成的测试
describe('add', () => {
  it('should add two positive numbers', () => {
    expect(add(1, 2)).toBe(3)
  })

  it('should handle negative numbers', () => {
    expect(add(-1, -2)).toBe(-3)
  })
})
```

### E2E 测试

需要理解用户流程，AI 不知道实际场景。人工设计为主。

```typescript
// 搜索历史 E2E 测试
test('search history persists across page reload', async () => {
  await page.goto('/search')
  await page.fill('#search-input', 'test keyword')
  await page.click('#search-button')
  
  // 重新加载页面
  await page.reload()
  
  // 验证历史记录保留
  await expect(page.locator('.search-history')).toContainText('test keyword')
})
```

### 集成测试

需要理解系统交互，AI 不知道实际调用链。人工设计为主。

## 五、最佳实践

### 1. 测试先行

先写测试，再让 AI 实现。测试作为 AI 的执行目标。

### 2. 测试就近放

单测和 E2E 就近放模块目录，方便 AI 找到上下文。

```text
<module-name>/
├── index.tsx
├── types.ts
├── store.ts
├── __tests__/        # 就近单测
└── e2e/              # 就近 E2E
```

### 3. 红绿灯验收

用测试结果作为确定性信号：

- 🟢 全部通过：任务完成
- 🔴 有失败：需要修复
- 🟡 部分通过：需要分析

## 参考

- [TDD 质量保障能力建设与复用手册](https://github.com/anthropics/claude-code) — TDD 实践（访问于 2026-08-19）

## 下一步

- 了解资产沉淀 → [资产飞轮机制](./asset-flywheel)
- 迁移到 AI Native → [迁移路径](./migration-guide)

## 如果你想

- 理解设计理念 → [设计理念：人机分工](./design-philosophy)
- 改造架构 → [三层架构与模块模板](./three-layer-architecture)
- 看工具对比 → [AI Coding 工具全景](/ai-coding/tools/overview)

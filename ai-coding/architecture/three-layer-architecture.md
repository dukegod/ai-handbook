---
title: 三层架构与模块模板
description: 如何让工程结构对 AI 友好——三层架构、模块 5 件套、显式状态契约
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-19
---

# 三层架构与模块模板

> **TL;DR**：把代码拆成边界清晰的模块，用三层架构分离关注点，让 AI 每次只处理一个小任务。

## 你能在这里学到

- 三层架构是什么，为什么对 AI 友好
- 模块 5 件套模板
- 显式状态契约（Store 三段式）
- 组件库选型原则

## 前置知识

阅读本篇需要你先了解：

- [设计理念：人机分工](./design-philosophy)

## 一、三层架构

除了按业务视角做横向的模块切分，还需要在代码实现层面做纵向的"架构分层"。推荐每个领域模块都严格划分三层：

| 层级 | 职责 | 对 AI 的价值 |
|------|------|--------------|
| **基础层** | 通用能力沉淀（网络请求、数据转换、常量枚举） | 标准化能力可转化为 Skills |
| **状态层** | 显式状态契约（Store 定义 State 和 Actions） | 对抗 AI 幻觉的静态护栏 |
| **视图层** | 纯渲染与事件派发 | AI 最擅长的"舒适区" |

### 为什么三层对 AI 友好

```text
传统"面条式"代码：网络请求 + 状态流转 + 组件渲染糅在一起
→ AI 推理能力瞬间过载

三层架构：基础层 / 状态层 / 视图层分离
→ AI 每次只关注一层，准确率大幅提升
```

## 二、模块 5 件套模板

推荐每个模块都采用统一的目录结构：

```text
<module-name>/
├── index.tsx         # 模块入口组件（仅组合 UI + 派发事件）
├── types.ts          # 数据类型定义（AI 生成代码的基石）
├── store.ts          # 状态契约与 actions（显式 Store）
├── services.ts       # 请求编排与数据转换
├── config.ts         # 静态配置（组件实例化、请求 URL）
├── components/       # 模块私有组件
├── __tests__/        # 模块级单测
└── docs/             # 模块规约
```

### 各文件职责

| 文件 | 职责 | AI 生成时的关注点 |
|------|------|-------------------|
| `types.ts` | 定义模块全部数据类型 | 必须最先写，作为后续 AI 生成的"地基" |
| `store.ts` | 显式状态契约 | 字段命名、类型必须准确 |
| `services.ts` | 请求编排、参数组装 | 请求参数来自公共参数和模块 Store |
| `config.ts` | 静态配置 | 优先复用公共配置常量 |
| `index.tsx` | 模块入口 | 只写渲染和事件派发 |

## 三、显式状态契约

AI 不擅长在代码静态上下文中感知到有哪些状态可被读取与修改。**核心原则**：状态契约要白纸黑字写在代码里，AI 一眼读懂。

### Store 三段式接口

```typescript
interface ModuleStore {
  /** 请求参数：所有入参和中间态 */
  query: {
    [field: string]: {
      value: unknown;       // 公开状态
      loading?: boolean;    // 私有状态：loading
      disabled?: boolean;   // 私有状态：禁用
    };
  };
  /** 响应数据：每个组件实例对应一份 */
  response: {
    [componentName: string]: {
      meta?: unknown[];           // 维度、筛选项等元数据
      dataSource?: unknown[];     // 列表数据
      status: 'idle' | 'loading' | 'error' | 'done';
      error?: string;
    };
  };
  /** 状态处理函数：支持异步 */
  actions: {
    updateQuery: (field: string, value: unknown) => void;
    fetchData: (componentName: string) => Promise<void>;
    reset: () => void;
  };
}
```

### 强约束

| 约束 | 说明 |
|------|------|
| 字段名精准 | AI 写代码时直接读 Store 类型，避免幻觉 |
| 结构正确 | 嵌套结构清晰，无凭空捏造 |
| 状态可推 | 所有依赖字段都在 Store 中显式声明 |
| Actions 完整 | 每个数据流对应明确的 action 函数 |

## 四、组件库选型原则

### 原则 1：优先选择 LLM 训练覆盖度高的开源框架

大模型在训练阶段经过了大量开源框架代码训练（React、Vue、Zustand、Redux Toolkit、Pinia 等），有非常好的开发质量和准确性。

**避免**：
- 深度封装的私有 DSL 配置化框架
- 私有 API（如私有的 `action.setState` 模式）
- 与开源范式差异过大的状态管理方案

**推荐**：

| 框架层 | 推荐选型 |
|--------|----------|
| 视图框架 | React / Vue（开源生态） |
| 状态管理 | Zustand + Immer / Redux Toolkit / Pinia |
| UI 组件 | Ant Design / Material UI / Element Plus |

### 原则 2：业务组件沉淀为可复用物料

将高频业务组件整理成标准物料：
- 明确**适用场景**、**核心 props**、**数据结构**、**禁用规则**
- 沉淀为组件文档和 Skill
- 让 AI 在生成代码时能直接查询

### 原则 3：避免业务黑盒

每个组件都应做到：

| 维度 | 要求 |
|------|------|
| 类型定义 | 完整的 TypeScript props 定义 |
| 状态可查 | 组件依赖的状态字段显式可见 |
| API 可文档化 | 通过 Skill 或文档描述组件用法 |
| 禁用可枚举 | 明确的禁用场景和 prop 互斥规则 |

## 五、不要让 AI 在巨石文件中挣扎

单文件堆积数千行的高耦合"巨石"代码，会让 AI 同时遇到两个致命问题：

- **上下文过长 → 注意力衰减**：AI 容易找错修改位置
- **高耦合 → 隐式依赖多**：修改大概率会意外破坏其他模块

```text
bad case: 一个 ReportAnalysis.tsx 3000 行
  → AI 找不到上下文边界

good case: 拆分为 FilterBar / MetricCards / TrendChart / PivotTable / DataExport
  → 每个模块独立可读、可测、可迭代
```

## 参考

- [AI Native 工程架构 Skills 使用手册](https://github.com/anthropics/claude-code) — 模块化实践（访问于 2026-08-19）

## 下一步

- 建立质量保障 → [TDD 质量保障](./tdd-quality)
- 了解资产沉淀 → [资产飞轮机制](./asset-flywheel)

## 如果你想

- 理解设计理念 → [设计理念：人机分工](./design-philosophy)
- 迁移到 AI Native → [迁移路径](./migration-guide)
- 看工具对比 → [AI Coding 工具全景](/ai-coding/tools/overview)

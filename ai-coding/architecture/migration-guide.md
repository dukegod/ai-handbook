---
title: 迁移路径
description: 如何从现有项目迁移到 AI Native——半天版/一周版/一个月版
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-19
---

# 迁移路径

> **TL;DR**：不要一步到位，分阶段迁移：半天版建立基本护栏，一周版形成团队能力，一个月版建设完整体系。

## 你能在这里学到

- 半天版：快速建立基本护栏
- 一周版：形成团队 AI 能力
- 一个月版：建设完整 AI Native 体系
- 每个阶段的验收标准

## 前置知识

阅读本篇需要你先了解：

- [设计理念：人机分工](./design-philosophy)
- [三层架构与模块模板](./three-layer-architecture)
- [TDD 质量保障](./tdd-quality)

## 一、半天版：快速建立基本护栏

适合快速把项目从"个人 AI 使用"升级到"团队有基本护栏"。

### 步骤

```text
1. 写 CLAUDE.md：命令、架构、测试、禁止项
2. 建 .claude/rules/naming.md
3. 建 .claude/rules/test-quality.md
4. 接入 Jest 或现有单测框架
5. 接入 Playwright smoke
6. 建 docs/code-reviews/
```

### CLAUDE.md 示例

```markdown
# 项目 AI 规则

## 构建命令
- 安装依赖：`pnpm install`
- 启动开发：`pnpm dev`
- 运行测试：`pnpm test`
- 构建产物：`pnpm build`

## 目录结构
- src/pages/ — 页面组件
- src/components/ — 公共组件
- src/utils/ — 工具函数
- __tests__/ — 单元测试

## 禁止项
- 不要修改 package.json 的依赖版本
- 不要删除 __tests__/ 目录
- 不要直接修改 .env 文件
```

### 验收标准

- [ ] AI 改测试文件时能自动知道模板
- [ ] AI 改页面时知道目录和命名
- [ ] 提测前能跑单测和 smoke

## 二、一周版：形成团队能力

适合正式推广到团队。

### 步骤

```text
1. 梳理标杆页面
2. 固化页面 / 模块目录结构
3. 建 create-page-structure Skill
4. 建 create-module-spec Skill
5. 建 create-module-code Skill
6. 建 code-review-expert Skill
7. 把业务组件文档 Skill 化
8. 建 SDD 文档归档规范
```

### 标杆页建设

选择一个结构清晰的页面作为标杆，固化其结构：

| 能力 | 可复制规则 |
|------|------------|
| 页面结构 | 页面根、common、redux、modules、docs、tests 固定 |
| 模块结构 | 模块 5 件套固定 |
| 状态管理 | store 注册和 widget 实例成对 |
| 文档 | 页面 docs 与模块 specs 就近放 |
| 测试 | 单测和 E2E 就近放 |

### 验收标准

- [ ] 一个新模块可以从 spec 到代码再到测试按流程生成
- [ ] CR 报告能稳定识别高影响变更

## 三、一个月版：建设完整体系

适合建设完整 AI Native 工程体系。

### 步骤

```text
1. 全量页面架构地图
2. 存量页面分组：新架构 / 旧架构 / 壳页 / 待清理
3. 每页 smoke 覆盖
4. 重点页面补核心交互 E2E
5. 组件库 API 文档和 demo 完整 Skill 化
6. SDD、TDD、CR、QA 纳入提交流程
7. 每次复盘沉淀到 rules / skills / docs
```

### 架构地图

建立全量页面的架构地图，方便 AI 快速定位：

```markdown
# 页面架构地图

## 新架构页面
- /industry/industrySummary — 行业大盘
- /product/detail — 商品详情

## 旧架构页面
- /legacy/report — 旧报表页面

## 壳页
- /app/ — 应用壳页
```

### 验收标准

- [ ] 新增模块 AI Native 覆盖率明显提升
- [ ] 存量迭代能通过架构地图和测试护栏稳定执行

## 四、迁移原则

| 原则 | 说明 |
|------|------|
| 渐进式 | 不要一步到位，分阶段迁移 |
| 标杆先行 | 先建一个标杆页，再推广到其他页面 |
| 测试兜底 | 每个阶段都要有测试保障 |
| 资产沉淀 | 每次迁移经验都要沉淀为资产 |

## 参考

- [跨项目迁移指南](https://github.com/anthropics/claude-code) — AI Native 迁移实践（访问于 2026-08-19）

## 下一步

- 理解设计理念 → [设计理念：人机分工](./design-philosophy)
- 改造架构 → [三层架构与模块模板](./three-layer-architecture)

## 如果你想

- 建立质量保障 → [TDD 质量保障](./tdd-quality)
- 了解资产沉淀 → [资产飞轮机制](./asset-flywheel)
- 看工具对比 → [AI Coding 工具全景](/ai-coding/tools/overview)

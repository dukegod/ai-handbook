---
title: 概念文模板
description: 用于写「什么是 X」「X 是什么」「X 的工作原理」这一类概念性文档的模板
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-23
---

# 概念文模板

> 当你要写「X 是什么」「X 怎么工作」「为什么要有 X」这类文档时，复制下面这份骨架。

**适用场景**：讲清楚一个概念、一个抽象、一种机制。读者读完能建立心智模型，但不一定会动手做什么。

**不适用场景**：手把手教读者做一件具体的事 → 用 [操作文模板](./template-howto)。

---

## 骨架

以下内容整块复制，改标题与占位符即可。

````markdown
---
title: 什么是 XXX
description: 一句话说明这篇讲什么、面向谁
audience: beginner        # beginner | intermediate | advanced
difficulty: 🟢            # 🟢 | 🟡 | 🔴
status: draft
lastUpdated: 2026-07-23
verifiedWith:
  claudeCode: 2.0.14
  model: claude-opus-4-8
---

# 什么是 XXX

> **TL;DR**：一句话总结（≤ 40 字），先给结论。读者只读这一句就能知道要不要往下看。

## 你能在这里学到

- XXX 是什么，解决什么问题
- XXX 与 YYY 的区别
- 什么时候该用、什么时候不该用
- 常见的坑

## 前置知识

阅读本篇需要你先了解：

- [某个基础概念](/link/to/prerequisite)
- （可选）[更进一步的相关概念](/link/to/related)

不了解也没关系，遇到不熟悉的术语可查 [术语表](/contributing/glossary)。

## 一、XXX 是什么

（先给一个简明定义，再展开。用类比或场景切入，避免开篇就抛术语。）

## 二、为什么需要 XXX

（说明它解决了什么问题；对比「没有 XXX 时怎么办 → 有了 XXX 之后怎样」。）

```mermaid
flowchart LR
  A[没有 XXX] -->|痛点| B[XXX] -->|解决| C[结果]
```

## 三、XXX 的工作机制

（用 1–2 张图 + 分步说明讲清楚流程。）

## 四、什么时候用 XXX

**适合的场景：**

- 场景 A
- 场景 B

**不适合的场景：**

- 场景 C（此时用 YYY 更好）

## 五、XXX 与相邻概念的边界

| 维度 | XXX | YYY | ZZZ |
| --- | --- | --- | --- |
| 触发方式 | ... | ... | ... |
| 作用域 | ... | ... | ... |
| 何时选它 | ... | ... | ... |

## 常见问题 FAQ

**Q：XXX 和 YYY 到底有什么区别？**

答：...

**Q：能不能同时用 XXX 和 YYY？**

答：...

## 参考

- [Anthropic 官方文档 · 相关章节](https://docs.claude.com/...)（访问于 2026-07-23）
- 补充阅读：[某篇博客](https://...) — 简述价值

## 下一步

- 想动手实操 → [如何写第一个 XXX](/link/to/howto)
- 继续读下一个概念 → [YYY 是什么](/link/to/next)

## 如果你想

- 深入原理 → [XXX 底层实现细节](/link/to/deep-dive)
- 换个视角 → [从工程角度看 XXX](/link/to/eng-view)
- 立刻用起来 → [XXX 十分钟上手](/link/to/quickstart)
````

---

## 写作建议

**开头「TL;DR」的力量：**

读者点进一篇文档的前三秒决定读不读下去。一句话说完，胜过三段铺垫。

**类比 > 术语：**

写「什么是 Skill」时，说「Skill 就像给 Claude 装了个 App」比说「Skill 是声明式的能力扩展单元」更好懂。类比出手后再补严格定义。

**图先于文字：**

概念文尤其吃图。能画流程/时序/边界的地方，先画图再写文字，读者理解速度快一个数量级。

**边界表：**

X 和 Y 长得像的时候，一张对比表价值远超三段文字描述。**先做表，再写章节。**

**"什么时候不该用"：**

比"什么时候该用"更值钱。因为读者搜到你这篇文档时，八成正犹豫要不要用它。

**避免的写法：**

- ❌ 把官方文档的段落直译一遍（读者能自己去官网看）
- ❌ 展开一大堆参数细节（那是参考文档的活）
- ❌ 用「大家都知道…」「显然…」开头（默认读者不知道）
- ❌ 只有理论没有例子（至少给一个最小可想象场景）

## 参考

- [Diátaxis · Explanation](https://diataxis.fr/explanation/) — 概念文的四象限定位（访问于 2026-07-23）

## 下一步

- 写操作型文档 → [操作文模板](./template-howto)
- 校对术语 → [术语表](./glossary)
- 提交前自检 → 回到 [写作规范 · PR 前 checklist](./style-guide#十、pr-前自检-checklist)

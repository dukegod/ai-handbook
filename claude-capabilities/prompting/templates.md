---
title: 常用模板
description: 12 个实战模板速查——code review / 数据提取 / 文档总结 / 翻译 / 客服 / 规划 / 调试
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  promptLibrary: 'https://docs.claude.com/en/prompt-library/library'
  accessedAt: 2026-08-07
---

# 常用模板

> **TL;DR**：12 个常用模板速查——code review / 数据提取 / 文档总结 / 翻译 / 客服 / 规划 / 调试 / 学习 / 写测试 / 写 commit / debug 报错 / 准备面试。每个模板「复制即用」，按需修改 `{占位符}`。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 12 个常用 prompt 模板（按场景分类）
- 模板的 `{占位符}` 替换约定
- 何时用模板 vs 自己写
- 与 [Cookbook](/cookbook/) 的分工（模板 = 片段，Cookbook = 端到端）

## 模板使用约定

- `{placeholder}` 标记需替换的内容
- `[可选内容]` 用方括号表示可选
- `// 注释` 标在 prompt 外（用 `# Claude:` 系统提示区分）

复制后**删注释行**——否则 Claude 会把它们当 prompt 解读。

---

## 1. Code Review

```text
请审查以下代码改动：
- 重点：{bug / 安全 / 性能 / 风格}
- 范围：{PR URL 或 diff}
- 输出：3 条最严重的问题 + 每条修复建议

代码：
{code}
```

**适用**：PR review、安全审计。

## 2. 数据提取（结构化输出）

```text
从以下文本提取结构化字段：

字段：
- {field_1}: {type + 说明}
- {field_2}: {type + 说明}
- {field_3}: {type + 说明}

输出格式：JSON

示例输入：{example_input}
示例输出：{example_output}

待提取文本：
{text}
```

详见 [Few-shot · 模式 2](/claude-capabilities/prompting/few-shot#模式-2数据提取) + [结构化输出](/claude-capabilities/api/structured-outputs)。

## 3. 文档总结

```text
把以下文档总结为：
- 1 段背景（{N} 字）
- {M} 个关键决策
- 1 段风险评估
- {K} 个 follow-up 问题

文档：
{document}
```

**适用**：RFC 评审、长文档摘要、读书笔记。

## 4. 翻译

```text
把以下 {source_lang} 翻译为 {target_lang}。
要求：
- 保留技术名词（如 React、TypeScript、Promise）
- 风格：{formal / casual / technical}
- 长度：原文 ± 10%

原文：
{text}
```

**反模式**：**整本书一次翻译**——会丢细节。**分章节翻译**。

## 5. 客服回复

```text
你是 {company} 客服助手。
- 风格：{friendly / professional / concise}
- 不编造公司没有的功能
- 不知道时承认 + 给转人工入口

客户问题：
{question}

回复：
```

**实战**：加上 `{company_not_to_discuss: [competitor list]}` 避免竞品讨论。

## 6. 任务规划

```text
我想做：{goal}。

请：
1. 拆成 {N} 步
2. 每步给预期时间
3. 标出可能的依赖 / 风险
4. 列出需要的资源 / 工具

最终给一个 {horizon} 内可执行的计划。
```

**适用**：项目启动、Sprint 规划、个人 OKR。

## 7. 调试 Bug

```text
我的代码有 bug：
- 报错：{error_message}
- 触发条件：{steps_to_reproduce}
- 已尝试：{what_i_tried}
- 期望行为：{expected}
- 实际行为：{actual}

请：
1. 列 3 个可能根因
2. 哪个最可能 + 为什么
3. 验证方法
4. 修复方案
```

**实战**：**带上 "已尝试"** —— 让 Claude 别重复低效方案。

## 8. 学习新概念

```text
我想学 {topic}。背景：{my_background}。

请：
1. 用一句话说清这是什么
2. 给我一个生活中的类比
3. 列 3 个核心概念
4. 给 1 个最小可运行示例
5. 列 2 个常见误解
6. 推荐 1 个进阶资源
```

**适用**：技术调研、新人 onboarding。

## 9. 写单元测试

```text
为以下函数生成单元测试：
- 测试框架：{pytest / vitest / jest / ...}
- 覆盖率目标：> {N}%
- 覆盖：正常路径 / 边界值 / 异常输入
- 断言粒度：每个 expect 必须验证具体值（禁止 toBeDefined / toBeTruthy）

函数：
{code}
```

详见 [代码能力 · 测试生成](/claude-capabilities/core/coding#五测试生成)。

## 10. 写 Commit Message

```text
把以下 diff 写成 1-3 句 commit message。
- 风格：{Conventional Commits / 自由}
- 包含：why > what > how

diff：
{diff}
```

**实战**：commit 之前批量 review。

## 11. 报错解读

```text
解释这个报错：
- 我做了什么：{context}
- 报错：{error_message}
- 我的环境：{language / version / OS}

请：
1. 报错含义（1 句话）
2. 最可能的 2 个原因
3. 排查步骤
4. 完整示例修复
```

**实战**：Stack Overflow 替代。

## 12. 准备技术面试

```text
我要面试 {role}，技术栈 {stack}。
请：
1. 出 {N} 道 {easy/medium/hard} 难度题
2. 标考察点
3. 给参考答案
4. 列出 2 个 follow-up 追问
5. 如果我卡住，给提示（不要直接给答案）
```

**实战**：**多轮**——先做、再追问、最后评分。

---

## 模板使用三原则

**1. 占位符必填**

`{placeholder}` 不替换 = Claude 不知道是模板。**实际用时全部替换**。

**2. 不要整段背诵**

模板是**起点**不是终点。**根据具体任务调整**——加约束、改输出格式、给反例。

**3. 模板越用越精**

```
v1: 复制模板
v2: 删无关部分
v3: 加项目特定约束
v4: 多次使用后形成"自家模板库"
```

## 与 Cookbook 的分工

| 维度 | 模板 | Cookbook |
| --- | --- | --- |
| **形式** | 短片段（10-30 行） | 端到端任务（多步） |
| **场景** | 单一动作 | 完整工作流 |
| **示例** | 占位符 + 1 个示例 | 多步截图 / 代码 |
| **适用** | 知道要做什么、想快 | 第一次做、想学 |

详见 [Cookbook 实战案例](/cookbook/)——比如 [第一个真实任务](/cookbook/first-real-task) 是端到端 Plan → Edit → Verify。

## 4 个常见坑

**1. 模板不替换占位符**

```text
# ❌ 复制了模板忘改
"为 {function} 写测试"

# ✅ 替换完
"为 src/auth/jwt.ts 写测试"
```

**2. 模板和任务不匹配**

```
# 任务：给新员工做培训
# 错模板：1. Code Review
# 对模板：8. 学习新概念
```

**3. 模板没改就发**

模板是**起手式**——根据具体上下文调整后再发。

**4. 模板越堆越多**

超过 20 个模板 = 没人用。**保留 5-10 个最常用的**。

## 参考

- [Anthropic Prompt Library](https://docs.claude.com/en/prompt-library/library)（访问于 2026-08-07）
- [Anthropic Docs · Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)（访问于 2026-08-07）
- [最佳实践](/claude-capabilities/prompting/best-practices)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)
- [Few-shot 示例](/claude-capabilities/prompting/few-shot)
- [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)
- [思维链](/claude-capabilities/prompting/chain-of-thought)
- [Cookbook 实战](/cookbook/)

## 下一步

- 端到端实战 → [Cookbook · 第一个真实任务](/cookbook/first-real-task)
- 切到 API → [Messages API](/claude-capabilities/api/messages)
- 继续学 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- 12 模板都用过的反馈调整 → [最佳实践](/claude-capabilities/prompting/best-practices)
- 自建模板库 → [Anthropic Prompt Library](https://docs.claude.com/en/prompt-library/library)
- Cookbook 端到端 → [Cookbook](/cookbook/)

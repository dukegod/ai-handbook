---
title: 最佳实践
description: Anthropic 官方 prompting 指南要点——8 条核心原则 + 好坏 prompt 对比 + 实战模式速查
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  promptEngineering: 'https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview'
  promptLibrary: 'https://docs.claude.com/en/prompt-library/library'
  accessedAt: 2026-08-07
---

# 最佳实践

> **TL;DR**：Anthropic 官方 prompting 指南浓缩成 **8 条核心原则**——清晰指令 / 用示例 / 让模型想 / 用 XML / 给角色 / 拆分任务 / 长 context 善用 / 验证。本页是**实战层**（如何写好 prompt），与 [推理能力](/claude-capabilities/core/reasoning)（何时让 Claude 想）分工。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Anthropic 官方 8 条核心 prompting 原则
- 好 prompt vs 坏 prompt 实战对比
- System prompt vs user prompt 的分工
- XML 标签、Few-shot、思维链的实战模式
- 常见 prompt 错误与怎么修
- 与 [推理能力](/claude-capabilities/core/reasoning)、[Messages API](/claude-capabilities/api/messages) 的关系

## 一、Anthropic 官方 8 条核心原则

参考 [Anthropic Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)（访问于 2026-08-07）：

### 原则 1：清晰直接

```text
# ❌ 模糊
帮我看看这段代码

# ✅ 清晰
请检查 src/auth/jwt.ts 里的 token 验证函数，找 3 个潜在安全漏洞，按严重性排序。
```

**核心动作**：动词具体（"检查" / "对比" / "找出"），对象具体（文件路径 / 函数名），输出格式具体（按严重性排序）。

### 原则 2：给示例（Few-shot）

```text
请把用户评论分类为「投诉」/「建议」/「表扬」。

示例：
- "App 崩了" → 投诉
- "希望加个夜间模式" → 建议
- "客服响应快" → 表扬

现在请分类："登录后白屏了"
```

详见 [Few-shot 示例](/claude-capabilities/prompting/few-shot)。

### 原则 3：让模型想

复杂任务显式让 Claude 写推理步骤——可参考 [推理能力 · 5 个模式](/claude-capabilities/core/reasoning#三5-个让-claude-想清楚再答的-prompt-模式)：

```text
请先想清楚 3 个反例再给方案。如果你能找到任何一个，就修订方案。
```

### 原则 4：用 XML 标签结构化

```xml
<context>
你正在重构 auth 模块，约束：所有函数 async、错误用 Result<T, E>。
</context>

<task>
把 src/auth/jwt.ts 改成 async + Result 类型，保留所有现有导出。
</task>

<constraints>
- 不改函数签名
- 加 timeout 5s
- 加单元测试
</constraints>
```

详见 [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)。

### 原则 5：给角色（System Prompt）

```python
system = "你是资深代码审查员，有 15 年 Python 经验，重点看边界条件、错误处理、性能。"
```

详见 [System Prompt 设计](/claude-capabilities/prompting/system-prompts)。

### 原则 6：拆分复杂任务（Chain Prompts）

```text
# ❌ 一步走
"请调研这 5 篇论文并写一份 3000 字综述"

# ✅ 拆 4 步
"步骤 1：先列每篇论文的核心观点（500 字内）
 步骤 2：对比 5 篇的方法论差异
 步骤 3：综合找 3 个共识和 3 个分歧
 步骤 4：基于上面写综述"
```

详见 [Anthropic Docs · Chain prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)。

### 原则 7：长 context 善用

Claude 1M context 装得下——**别让信息散落**，集中放：

```text
# 项目背景（2000 字）+ 代码（5000 字）+ 任务（100 字）
# 全部放在一个 prompt 里，不要分多次丢
```

详见 [长上下文](/claude-capabilities/core/long-context)。

### 原则 8：写完验证

```text
# 别只让 Claude 写
"写个排序函数"

# 强制验证
"写个排序函数。写完后自己跑 [3, 1, 2] 测试一下，并解释每步为什么这样排。"
```

**关键**：模型会**幻觉**执行结果——自己跑一遍，别信总结。详见 [第一个真实任务 · 跑测试、修红](/cookbook/first-real-task#第-5-步跑测试修红)。

## 二、好 prompt vs 坏 prompt 实战对比

| 任务 | 坏 prompt | 好 prompt |
| --- | --- | --- |
| 代码 review | "看看这个 PR" | "审查 PR #1234，重点找：并发问题、错误处理、SQL 注入风险；按严重性排序" |
| 文档总结 | "总结一下这份文档" | "把这份 50 页 RFC 文档总结为：3 段架构 + 5 个关键决策 + 1 段风险评估" |
| 数据提取 | "提取这个 PDF 的信息" | "从发票 PDF 提取：金额、日期、商家、发票号，输出 JSON 格式" |
| 调试 | "代码不工作" | "我的 Python 脚本在第 45 行抛 ConnectionResetError。脚本做的是... 已试过... 帮我定位" |
| 学习 | "教我 Docker" | "我要部署一个 FastAPI 应用到生产环境。请讲 Docker 在这个场景的核心概念：image / container / volume / network，每个给一个 FastAPI 例子" |

**3 个共同点**：
1. **具体动词**（审查 / 总结 / 提取 / 定位 / 教）
2. **明确对象**（PR #1234 / 50 页 RFC / 第 45 行 / FastAPI）
3. **规定输出格式**（按严重性排序 / 3 段 + 5 个 + 1 段 / JSON）

## 三、System Prompt vs User Prompt

| 维度 | System Prompt | User Prompt |
| --- | --- | --- |
| **作用** | 定角色、给规则、长期约束 | 当前任务、当前输入 |
| **改动频率** | 跨任务不变 | 每请求变 |
| **放哪** | API `system` 字段 | API `messages` 数组 |
| **cache 友好** | ✅ 适合 `cache_control` | ❌ 一般不 cache |
| **典型内容** | 角色、风格、规则、约束 | 任务描述、输入数据、问题 |

**实战分法**：

```python
# System：不变的部分
system = "你是资深 Python 工程师。代码风格遵循 PEP 8。回答用中文。"

# User：每次变
messages = [{"role": "user", "content": "..."}]
```

详见 [System Prompt 设计](/claude-capabilities/prompting/system-prompts)。

## 四、4 个常被忽略的细节

**1. 指令放对位置**

```text
# ❌ 指令埋在长 paragraph 里
"我最近在做一个项目，这个项目是 web 后端，主要用 Python，
有时候也用 Go。哦对了，记得用 TypeScript 的风格写。"

# ✅ 指令单独一段
"代码风格：用 TypeScript 风格（强类型、interface、async/await）。
任务：写一个 FastAPI 用户认证接口。"
```

**2. 否定句不如肯定句**

```text
# ❌ 否定
"不要写超过 100 行的代码"
"不要使用全局变量"
"不要解释过程"

# ✅ 改成肯定
"代码控制在 100 行以内"
"用模块级单例替代全局变量"
"直接给最终代码，不解释"
```

**3. 不要让模型"猜你想要"**

```text
# ❌ 模糊意图
"把代码写好"      # 什么叫写好？

# ✅ 明确意图
"代码要：1. 处理空输入 2. 跑 < 100ms 3. 单元测试覆盖 80% 以上"
```

**4. 长 prompt 里"标重点"**

```text
【关键】这里只改 auth.ts，别动 user.ts。
【重要】保持现有 export。
【输出】只给 diff，不给完整文件。
```

中文方括号 / 【】 / `<important>` XML 都能让 Claude 重点关注。

## 五、常见错误

**1. prompt 写完就提交**

模型可能没完全理解——**第一个响应先 review**，看是否符合预期；不符合就追加澄清。

**2. 期望 Claude 100% 一次成功**

复杂任务**几乎一定**要迭代。第一稿是起点不是终点。

**3. 忽视 system prompt**

把任务全塞 user prompt，system 留空 → Claude 风格不一致、容易跑偏。**永远用 system prompt 定基调**。

**4. 长 prompt 不结构化**

1000+ 字的 paragraph 让 Claude 抓不到重点。**用 XML 标签 / Markdown heading 分块**。

**5. 没给输出格式**

```text
# ❌ 默认输出散装
"提取发票信息"

# ✅ 强制 JSON
"提取发票信息，按 JSON 格式输出：{\"amount\": str, \"date\": str, \"merchant\": str}"
```

详见 [结构化输出](/claude-capabilities/api/structured-outputs)。

## 参考

- [Anthropic Docs · Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)（访问于 2026-08-07）
- [Anthropic Prompt Library](https://docs.claude.com/en/prompt-library/library)（访问于 2026-08-07）
- [Anthropic Docs · Chain prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)（访问于 2026-08-07）
- [推理能力 · 何时让 Claude 想](/claude-capabilities/core/reasoning)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)
- [Few-shot 示例](/claude-capabilities/prompting/few-shot)
- [思维链](/claude-capabilities/prompting/chain-of-thought)

## 下一步

- System prompt 实战 → [System Prompt 设计](/claude-capabilities/prompting/system-prompts)
- Few-shot 模式 → [Few-shot 示例](/claude-capabilities/prompting/few-shot)
- 思维链深入 → [思维链](/claude-capabilities/prompting/chain-of-thought)

## 如果你想

- XML 标签 / Prefill → [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)
- 速查模板 → [常用模板](/claude-capabilities/prompting/templates)
- 切到 API 调用 → [Messages API](/claude-capabilities/api/messages)

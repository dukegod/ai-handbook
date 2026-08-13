---
title: Prefill 与 XML 标签
description: API 视角的两大结构化技巧——XML 标签（5 个实战用法）+ Prefill 预填 response 开头（4 个限制）
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  xmlTagsDocs: 'https://docs.claude.com/en/docs/build-with-claude/use-xml-tags'
  prefillDocs: 'https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response'
  accessedAt: 2026-08-07
---

# Prefill 与 XML 标签

> **TL;DR**：**XML 标签**结构化长 prompt（5 个实战用法），**Prefill** 预填 response 开头强制输出格式（4 个限制）。两者都是"prompt 层结构化"——比纯文本更可控，但都比 Few-shot 抽象。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- XML 标签的本质与 5 个实战用法
- Prefill 的工作原理 + 4 个限制
- XML + Prefill 组合实战
- 与 [最佳实践 · 原则 4](/claude-capabilities/prompting/best-practices#原则-4用-xml-标签结构化) / [System Prompt](/claude-capabilities/prompting/system-prompts) 的分工
- 4 个常见坑

## 一、XML 标签的本质

**用结构化标签切分 prompt**——让 Claude 清楚区分"这是任务"、"这是上下文"、"这是约束"。

```xml
<context>
你正在重构 auth 模块。
技术栈：React 18 + TypeScript strict。
约束：所有函数 async，错误用 Result<T, E>。
</context>

<task>
把 src/auth/jwt.ts 改成 async + Result 类型，保留所有现有导出。
</task>

<output_format>
输出格式：
1. 变更摘要（3 句话）
2. 完整新代码
3. 验证步骤
</output_format>
```

**为什么有效**：
- Claude 训练数据中**大量 XML**（网页 / 文档 / API 响应）——熟悉结构
- 标签让 Claude **注意力精准定位**（找 `<task>` 段而不是全文 grep）
- 嵌套支持（`<task><step>...</step></task>`）

## 二、5 个实战用法

### 用法 1：分离"上下文 / 任务 / 约束"

```xml
<context>
[项目背景 / 既有代码 / 历史决策]
</context>

<task>
[当前任务]
</task>

<constraints>
[不能做什么 / 必须遵守的边界]
</constraints>
```

**适用**：长 prompt（> 500 字）的标准切分。

### 用法 2：标签化"示例"块

```xml
<examples>
<example>
<input>1+1=?</input>
<output>2</output>
</example>
<example>
<input>2+2=?</input>
<output>4</output>
</example>
</examples>
```

详见 [Few-shot · 3 类模式](/claude-capabilities/prompting/few-shot#四3-类实战模式)。

### 用法 3：嵌套结构（复杂任务）

```xml
<plan>
<step number="1">分析用户认证流程</step>
<step number="2">找出 3 个安全漏洞</step>
<step number="3">给修复方案
  <approach>优先改 jwt.ts</approach>
  <fallback>如改不动用 middleware 包一层</fallback>
</step>
</plan>
```

**实战**：标签嵌套 = 树形结构——适合多步任务、子任务有依赖。

### 用法 4：标签化"输出要求"

```xml
<output_requirements>
- 必须用 Markdown
- 代码块标语言
- 长度 < 500 字
- 不用 emoji
</output_requirements>
```

**实战**：把"风格"放 system，"输出要求"放 user（更具体）——避免污染 system cache。

### 用法 5：标签引用（变量）

```xml
你是 {{role}}，{{background}}。
当前任务：{{task}}。
```

**适用**：模板化 prompt（programmatically 替换 `{{role}}` 等变量）。

```python
template = open("prompt.xml").read()
prompt = template.replace("{{role}}", "Python 工程师")\
                  .replace("{{background}}", "10 年经验")\
                  .replace("{{task}}", "写个 JWT 验证")
```

## 三、Prefill 的本质

**预填 assistant 消息的开头**——强制 Claude 从指定位置继续输出。

```python
msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "分析这段代码：..."},
        {"role": "assistant", "content": "{"},   # ← Prefill 预填
    ],
)
# Claude 会在 '{' 后继续输出 JSON
```

**为什么有效**：模型从 `{` 继续生成 → 强制走 JSON 模式 → 不会有"以下是..."之类的客套。

## 四、4 个限制

### 限制 1：必须能"自然衔接"

```python
# ✅ 自然的开头
{"role": "assistant", "content": "{"}    # JSON
{"role": "assistant", "content": "分析如下：\n1. "}   # 编号列表
{"role": "assistant", "content": "<analysis>"}   # XML

# ❌ 不自然
{"role": "assistant", "content": "你好！"}   # Claude 不会从中间开始寒暄
```

**实战**：Prefill 内容**必须是 Claude 自然续写的位置**——开括号、XML 开标签、章节开头。

### 限制 2：不能与 system 矛盾

```python
# ❌ system 说"用 JSON 格式"
system = "请用 JSON 输出"
# 但 Prefill 不是 {
{"role": "assistant", "content": "好的，我来"}
→ Claude 困惑

# ✅ Prefill 与 system 一致
system = "请用 JSON 输出"
{"role": "assistant", "content": "{"}
→ Claude 从 { 继续，自然给 JSON
```

### 限制 3：Prefill 算 input token

```python
# Prefill 越长，input 越贵
{"role": "assistant", "content": "分析报告\n1. 现状："}   # 9 token
# 不算贵，但别滥用
```

### 限制 4：仅特定 API 支持

- ✅ Messages API 支持 Prefill
- ✅ 多轮对话中所有 assistant 消息都可 Prefill
- ❌ 部分 SDK 默认不暴露 Prefill 字段

## 五、5 个实战场景

### 场景 1：强制 JSON 输出

```python
messages=[
    {"role": "user", "content": "提取发票：金额、日期、商家"},
    {"role": "assistant", "content": "{"},
]
# → Claude 强制输出 {"amount": "...", "date": "...", ...}
```

### 场景 2：强制 XML 结构

```python
messages=[
    {"role": "user", "content": "分析这段代码"},
    {"role": "assistant", "content": "<analysis>"},
]
# → Claude 输出 <analysis>...</analysis> + 后续结构
```

### 场景 3：跳过客套

```python
# ❌ 不 Prefill
"请分析代码"
→ "好的！我来分析一下这段代码。首先..."（3 句客套）

# ✅ Prefill
{"role": "assistant", "content": "1. "}
→ "1. 第一个问题：..."
```

### 场景 4：强制章节顺序

```python
messages=[
    {"role": "user", "content": "写产品需求文档"},
    {"role": "assistant", "content": "## 背景\n"},
]
# → 先写 "## 背景" 章节、再续写其他
```

### 场景 5：多轮 Prefill（多步推理）

```python
# 第一轮 Prefill
{"role": "assistant", "content": "思考：\n"}

# 第二轮继续 Prefill
{"role": "assistant", "content": "思考：\n1. 根因\n2. 验证\n\n结论："}
```

## 六、XML + Prefill 组合

**组合实战**——XML 结构化 prompt + Prefill 强制输出结构：

```python
system = "你是数据提取助手。"

messages = [
    {
        "role": "user",
        "content": """
        <context>
        你需要从发票 OCR 文本中提取结构化字段。
        </context>

        <examples>
        <example>
        <input>发票号 INV-001，金额 ¥1000，日期 2024-01-15</input>
        <output>{"invoice_no": "INV-001", "amount": "1000", "date": "2024-01-15"}</output>
        </example>
        </examples>

        <task>
        提取：[新发票]
        </task>
        """,
    },
    {"role": "assistant", "content": "{"},   # Prefill
]
```

**实战效果**：
- XML 让 prompt 结构化（Claude 注意力精准）
- Few-shot 给模式（消除歧义）
- Prefill 强制 JSON 输出（无需提示词引导）

## 七、4 个常见坑

**1. XML 标签不闭合**

```xml
<!-- ❌ -->
<context>一些内容
<task>一些任务

<!-- ✅ -->
<context>一些内容</context>
<task>一些任务</task>
```

### 2. Prefill 太长

```python
# ❌ 50 字 Prefill
{"role": "assistant", "content": "以下是详细的分析报告，第一部分背景，第二部分方法..."}
# 浪费 input token、模型困惑

# ✅ 简短 Prefill
{"role": "assistant", "content": "## 背景\n"}
```

### 3. Prefill + system 矛盾

见 [限制 2](#限制-2不能与-system-矛盾)。

### 4. XML 标签混用大小写

```xml
<!-- ❌ -->
<Context>...</context>
<Task>...</task>

<!-- ✅ 一致 -->
<context>...</context>
<task>...</task>
```

## 参考

- [Anthropic Docs · Use XML tags](https://docs.claude.com/en/docs/build-with-claude/use-xml-tags)（访问于 2026-08-07）
- [Anthropic Docs · Prefill Claude's response](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response)（访问于 2026-08-07）
- [最佳实践 · 原则 4](/claude-capabilities/prompting/best-practices#原则-4用-xml-标签结构化)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)
- [Few-shot 示例](/claude-capabilities/prompting/few-shot)
- [结构化输出](/claude-capabilities/api/structured-outputs)

## 下一步

- 速查模板 → [常用模板](/claude-capabilities/prompting/templates)
- 结构化 JSON 输出 → [结构化输出](/claude-capabilities/api/structured-outputs)
- 切到 API → [Messages API](/claude-capabilities/api/messages)

## 如果你想

- 标签化模板 → [5 个实战用法](/claude-capabilities/prompting/prefill-and-xml#二5-个实战用法)
- Prefill 限制 → [4 个限制](/claude-capabilities/prompting/prefill-and-xml#四4-个限制)
- 风格转换 → [Few-shot · 模式 3](/claude-capabilities/prompting/few-shot#模式-3转换style-transfer)

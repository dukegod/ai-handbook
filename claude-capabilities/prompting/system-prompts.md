---
title: System Prompt 设计
description: API 视角的 system prompt 实战——5 个设计模式、5 类模板、与 user prompt 的分工
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  systemPromptDocs: 'https://docs.claude.com/en/docs/build-with-claude/system-prompts'
  promptEngineering: 'https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview'
  accessedAt: 2026-08-07
---

# System Prompt 设计

> **TL;DR**：System prompt 放 API 的 `system` 字段，是**跨任务不变的部分**——定角色、定规则、定风格、定约束。5 个设计模式（角色 / 规则 / 风格 / 约束 / 上下文）+ 4 类模板（通用 / 编程 / 写作 / 客服）能覆盖 80% 场景。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- System prompt 的本质（API 字段 + 不变部分）
- 5 个核心设计模式（角色 / 规则 / 风格 / 约束 / 上下文）
- 4 类模板（通用 / 编程 / 写作 / 客服）
- 与 [最佳实践](/claude-capabilities/prompting/best-practices) 的关系
- Prompt Caching 在 system prompt 上的实战（命中率 80%+）
- 5 个常见错误

## 一、System Prompt 的本质

**API 视角**：system prompt 是 `messages` 之外的 `system` 字段：

```python
msg = client.messages.create(
    model="claude-sonnet-5",
    system="你是资深 Python 工程师。代码风格遵循 PEP 8。",
    max_tokens=2048,
    messages=[{"role": "user", "content": "写个快速排序"}],
)
```

**两个关键认知**：

1. **跨任务不变**——system 改频率低（一次设好，跨多次请求复用）
2. **适合 cache**——`cache_control` 默认对 system 字段前 4 块生效

详见 [Sonnet 5 · Prompt Caching 5 错误](/claude-capabilities/models/sonnet#四prompt-caching-命中率优化)。

## 二、5 个设计模式

### 模式 1：定角色（Role）

```python
system = "你是资深代码审查员，有 15 年 Python 经验。"
```

**实战**：
- "你是 X 角色" → Claude 自动套用 X 角色的语气、视角、知识范围
- 给具体年限 / 公司 / 工具栈 → 更精准

**反例**：
```text
# ❌ 太宽
"你很厉害"

# ✅ 精准
"你是 Stripe 支付团队的前端工程师，专注 React + TypeScript，10 年经验"
```

### 模式 2：定规则（Rules）

```python
system = """
规则：
1. 代码必须用 async/await，不用 callback
2. 错误用 Result<T, E> 类型，不用 try/except
3. 函数不超过 50 行
4. 必须有单元测试
""".strip()
```

**实战**：
- 编号列出 → Claude 严格执行
- 反面规则 vs 正面规则——优先正面（"用 async/await" > "不用 callback"）

### 模式 3：定风格（Style）

```python
system = """
风格：
- 回答用中文
- 简短直接，不啰嗦
- 用 Markdown 格式输出
- 不用 emoji
- 技术名词保留英文（如 React、TypeScript、Promise）
""".strip()
```

**实战**：
- "回答用 X" 必带——Claude 默认会切语言
- 标点 / 段落长度 / emoji 都要明确

### 模式 4：定约束（Constraints）

```python
system = """
约束：
- 输出 < 500 字
- 不用 Markdown 表格（用 bullet list）
- 不引用外部 URL
- 不给 disclaimer / caveat
""".strip()
```

**实战**：
- 长度 / 格式 / 引用范围
- "不要 X" 列表容易让 Claude 过度删减——**优先写"要做 X"**

### 模式 5：定上下文（Context）

```python
system = """
项目上下文：
- 公司：跨境电商 SaaS
- 技术栈：React 18 + TypeScript + Node 20 + PostgreSQL
- 部署：AWS ECS + RDS
- CI：GitHub Actions
- 监控：Datadog

当前任务：用户认证模块重构
""".strip()
```

**实战**：
- 上下文信息放 system，让 model 一致化
- **适合 cache**——跨请求不变

## 三、5 个部分组合模板

实战中 5 个模式**常组合**：

```python
system = """
你是 Stripe 支付团队的资深前端工程师，10 年 React + TypeScript 经验。

规则：
1. 代码用 async/await + TypeScript strict mode
2. 错误用 Result<T, E> 类型
3. 函数不超过 50 行
4. 单元测试覆盖率 > 80%

风格：
- 回答用中文
- 简短直接
- 代码注释用英文（团队约定）

约束：
- 输出 < 500 字
- 不用 Markdown 表格
- 不用 emoji

项目上下文：
- SaaS 支付平台
- React 18 + TS 5 + Node 20
- 部署在 AWS ECS
""".strip()
```

**实战经验**：**前 50-100 字最重要**——Claude 注意力集中在 system 开头。

## 四、4 类模板速查

### 模板 1：通用助手

```python
system = "你是 helpful、harmless、honest 的助手。回答用中文。简短直接。"
```

### 模板 2：编程（最常用）

```python
system = """
你是 {language} 工程师，{years} 年经验，{domain} 背景。
代码风格：{style_conventions}
测试：覆盖率 > {coverage}%
错误处理：{error_pattern}
""".strip()
```

### 模板 3：写作（内容生成）

```python
system = """
你是 {role} 作家。风格：{style_description}。
读者：{audience}。长度：{word_count} 字 ± 10%。
输出格式：{format}。{tone}。
""".strip()
```

### 模板 4：客服 / 业务（角色扮演）

```python
system = """
你是 {company} 的客服助手。代表公司回应客户。
- 不编造公司没有的功能
- 不知道时承认 + 给转人工入口
- 语气：{tone}（默认专业友好）
- 不讨论竞品
""".strip()
```

## 五、何时用 system vs user

| 内容类型 | 放哪 | 理由 |
| --- | :---: | --- |
| 角色 / 风格 / 长期规则 | **system** | 跨任务不变 + cache 友好 |
| 当前任务描述 | user | 每请求变 |
| 用户输入数据 | user | 任务相关 |
| 短期约束（"这次回答 < 100 字"） | user | 当前任务专属 |
| 项目背景（跨多次请求一致） | system | 可 cache |

**反例**：

```python
# ❌ 把任务放 system
system = "请帮我写一个用户认证函数"     # 错——system 不变部分不该放任务

# ✅ 任务放 user
system = "你是 Python 工程师。代码遵循 PEP 8。"   # 长期规则
messages = [{"role": "user", "content": "写一个用户认证函数"}]   # 当前任务
```

## 六、常见坑

**1. system 太长（> 2000 字）**

Claude 注意力在 system 开头。**前 100 字定调**，后面的"参考材料"放 user 或文件附件。

**2. system 用否定句**

```text
# ❌
"不要用 try/except"

# ✅
"用 Result<T, E> 模式做错误处理"
```

详见 [最佳实践 · 4 个细节](/claude-capabilities/prompting/best-practices#四4-个常被忽略的细节)。

**3. system 不 cache**

```python
# ❌ 没 cache
system = "你是 Python 工程师..."

# ✅ cache（适合固定 system）
system = [
    {
        "type": "text",
        "text": "你是 Python 工程师...",
        "cache_control": {"type": "ephemeral"},
    }
]
```

cache 命中后**输入价格是基础价 10%**——长 system 必上 cache。详见 [Prompt Caching API](/claude-capabilities/api/prompt-caching)。

**4. 多个 system 块顺序乱**

```python
# ❌ 顺序变
system_1 = [角色块, 规则块]   # 今天
system_2 = [规则块, 角色块]   # 明天
# → cache 命中率掉到 0

# ✅ 顺序固定
system_template = [角色块, 规则块, 风格块, 约束块, 上下文块]
```

**5. system 与 user 矛盾**

```text
# system 写中文，user 写英文
# → Claude 选哪个？看哪个更具体。**保持一致**。
```

## 参考

- [Anthropic Docs · System prompts](https://docs.claude.com/en/docs/build-with-claude/system-prompts)（访问于 2026-08-07）
- [Anthropic Docs · Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)（访问于 2026-08-07）
- [最佳实践 · System Prompt vs User Prompt](/claude-capabilities/prompting/best-practices#三system-prompt-vs-user-prompt)
- [Sonnet 5 · Prompt Caching 5 错误](/claude-capabilities/models/sonnet#四prompt-caching-命中率优化)
- [Prompt Caching API](/claude-capabilities/api/prompt-caching)

## 下一步

- 思维链深入 → [思维链](/claude-capabilities/prompting/chain-of-thought)
- Few-shot 模式 → [Few-shot 示例](/claude-capabilities/prompting/few-shot)
- XML 标签 / Prefill → [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)

## 如果你想

- 实战速查 → [常用模板](/claude-capabilities/prompting/templates)
- 切到 API → [Messages API](/claude-capabilities/api/messages)
- 推理深入 → [推理能力](/claude-capabilities/core/reasoning)

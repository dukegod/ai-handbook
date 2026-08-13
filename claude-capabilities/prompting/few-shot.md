---
title: Few-shot 示例
description: 实战模式——给示例让 Claude 模仿；示例数量 / 选择 / 位置 / 反例 / 多样性的 5 个决策
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  promptEngineering: 'https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting'
  accessedAt: 2026-08-07
---

# Few-shot 示例

> **TL;DR**：Few-shot = 给 3-5 个示例让 Claude 模仿输出格式 / 风格 / 决策。**比 system prompt 的规则更具体、比 CoT 更结构化**。5 个决策（数量 / 选择 / 位置 / 反例 / 多样性）能覆盖 80% 场景。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Few-shot 的本质与何时该用
- 5 个核心决策（数量 / 选择 / 位置 / 反例 / 多样性）
- 3 类实战模式（分类 / 提取 / 转换）
- 与 [System Prompt 规则](/claude-capabilities/prompting/system-prompts) / [思维链](/claude-capabilities/prompting/chain-of-thought) 的边界
- 4 个常见坑

## 一、Few-shot 的本质

**给示例代替规则**——示例比抽象规则更容易被 Claude 模仿。

```text
# 规则式（抽象）
"把用户评论分类为「投诉」/「建议」/「表扬」"

# Few-shot 式（具体）
"评论分类：
- 'App 崩了' → 投诉
- '希望加个夜间模式' → 建议
- '客服响应快' → 表扬

现在分类：'登录后白屏了'
→ "
```

**为什么 Few-shot 有效**：
- 抽象规则有歧义（"建议"是什么？功能建议？性能建议？）
- 示例消除歧义（用户看到"希望加个夜间模式"就知道是功能建议）
- 多个示例 = **模式的边界**（覆盖"投诉"/"建议"/"表扬"3 类）

## 二、何时该用 Few-shot

| 场景 | 该用？ | 原因 |
| --- | :---: | --- |
| 简单分类（3 类以内） | ✅ | 示例消除歧义 |
| 复杂分类（10+ 类） | ✅ | 规则难写、示例直观 |
| 数据提取 | ✅ | 字段 + 格式 + 边界 case 一并示范 |
| 风格 / 语气模仿 | ✅ | 规则难描述、示例直观 |
| 代码生成（特定风格） | ✅ | 给出 2-3 个例子让 Claude 模仿 API 风格 |
| 长对话 / 复杂规划 | ❌ | 示例上下文太长、用 system prompt 规则 |
| 简单 Q&A | ❌ | 加示例拖时间 |
| **高准确率要求** | ✅ Self-Consistency | 多次采样取一致 |

**反直觉**：**Few-shot 适合"难描述的规则"**——能用一句话说清的（如"用 async/await"）直接 system 规则；说不清的（如"什么算投诉"）用示例。

## 三、5 个核心决策

### 决策 1：示例数量

```
0-shot（无示例）：通用任务、Claude 默认能处理
1-shot：1 个示例 + 简化边界
2-3 shot：标准 Few-shot，覆盖边界
4-5 shot：复杂任务、多种模式
> 5 shot：边际收益递减 + token 成本高
```

**实战经验**：**3-5 个示例**最有效——少于 3 个模式不全、多于 5 个模式重复。

### 决策 2：示例选择

```text
# ❌ 3 个示例都太相似
"1+1=2"
"2+2=4"
"3+3=6"
→ Claude 学到"加法"但学不到边界

# ✅ 3 个示例覆盖不同情况
"正常情况"（如 1+1=2）
"边界情况"（如 0+0=0）
"反例"（如 1+1 ≠ 3）
```

**实战**：**覆盖"正常 / 边界 / 反例"** 3 类——3 个示例就把模式说清。

### 决策 3：示例位置

```python
# system + user 模式
system = "你是文本分类器"
messages = [
    {
        "role": "user",
        "content": """
        分类示例：
        - 'App 崩了' → 投诉
        - '希望加夜间模式' → 建议
        - '客服响应快' → 表扬

        现在分类：'登录后白屏了'
        """,
    }
]
```

**实战**：
- **示例放 user 消息**（不用 system）——避免污染 system cache
- **当前任务紧跟示例**——避免"远隔效应"

### 决策 4：是否给反例

```text
# ❌ 只给正面
- 'App 崩了' → 投诉
- '希望加夜间模式' → 建议

# ✅ 给反例
- 'App 崩了' → 投诉
- '希望加夜间模式' → 建议
- 'App 经常崩' → ?   ← 模棱两可，看下面
- 'App 经常崩' → 投诉（如果表达负面体验）
- 'App 设计一般' → 不算投诉也不算建议
```

**实战**：**反例比正面更有价值**——告诉 Claude"什么不算"。但反例也别多，**1-2 个足够**。

### 决策 5：示例多样性

```text
# ❌ 3 个示例同模式
- 输入 A → 输出 X
- 输入 B → 输出 X
- 输入 C → 输出 X
→ Claude 只学到"输出 X"

# ✅ 3 个示例覆盖不同模式
- 输入 A → 输出 X
- 输入 B → 输出 Y
- 输入 C → 输出 Z
→ Claude 学到"模式 + 模式"
```

**实战**：**多输出 > 多输入**——输出模式多样性比输入变化更重要。

## 四、3 类实战模式

### 模式 1：分类

```text
把客户邮件分类为「紧急」/「一般」/「垃圾」。

紧急：
- "我的订单 #1234 还没收到，已等 3 天"
- "支付失败了，但扣款了"

一般：
- "如何申请退款？"
- "你们工作时间？"

垃圾：
- "恭喜您中奖 100 万！点击领取"
- "SEO 服务，联系 xxx"

现在分类：[新邮件]
```

### 模式 2：数据提取

```text
从发票文本提取结构化字段。

示例 1：
输入："发票号 INV-2024-001，金额 ¥1000，日期 2024-01-15"
输出：{"invoice_no": "INV-2024-001", "amount": "1000", "date": "2024-01-15"}

示例 2：
输入："Invoice No. INV-2024-002, Total: $500, Date: 2024-02-01"
输出：{"invoice_no": "INV-2024-002", "amount": "500", "currency": "USD", "date": "2024-02-01"}

现在提取：[新发票]
```

详见 [结构化输出](/claude-capabilities/api/structured-outputs)。

### 模式 3：转换（Style Transfer）

```text
把技术文档改写成面向 PM 的版本（去 jargon、加重业务影响）。

示例 1：
输入："P99 latency 从 200ms 降到 50ms"
输出："响应速度提升 4 倍，用户体验明显改善"

示例 2：
输入："数据库加了 read replica"
输出："数据库做了扩容，能撑更多用户同时访问"

现在改写：[新句子]
```

## 五、与 system 规则 / CoT 的边界

| 维度 | System 规则 | Few-shot | CoT |
| --- | --- | --- | --- |
| **抽象度** | 高（"用 async/await"） | 低（"看这个例子"） | 中（"先想再答"） |
| **覆盖** | 长期 / 跨任务 | 当前任务 | 当前任务 |
| **debug** | 难（不知道哪里错） | 易（看示例对比） | 中（看推理） |
| **token 成本** | 低（几十字） | 中（几百字） | 中（几百字） |
| **适用** | 通用规则 | 模式 / 边界 | 复杂推理 |

**组合实战**：

```python
system = "你是金融分析师"  # 角色（系统层）

messages = [{
    "role": "user",
    "content": """
    分析报告格式示例：
    - 输入：Q3 营收下降 5%
      输出：原因：宏观需求疲软 / 应对：聚焦高毛利产品
    
    - 输入：Q4 新用户增长 30%
      输出：原因：Q3 营销 ROI 兑现 / 应对：保持投放节奏

    现在分析：[新数据]
    """
}]
```

## 六、4 个常见坑

**1. 示例数量过多**

```text
# ❌ 8 个示例
8 个示例 × 200 字 = 1600 token 浪费

# ✅ 3-5 个
3 个示例 × 100 字 = 300 token，足够
```

### 2. 示例与任务风格不一致

```text
# ❌ 示例用正式语气，任务用随意语气
示例：'您好，我想咨询...'
任务：'Hey 能帮我看看...'
→ Claude 不知用哪个

# ✅ 风格一致
```

### 3. 示例缺乏"反例"

只有正面示例 → Claude 容易**误判边界**。至少 1 个反例。

### 4. Few-shot + CoT 同时用力

```text
# ❌ 给示例 + 强制逐步思考
"先看 3 个例子分类 → 然后想 3 步再分类"
→ Claude 不知道按哪个走

# ✅ 选一个
纯分类任务用 Few-shot
复杂推理用 CoT
```

## 参考

- [Anthropic Docs · Multishot prompting](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)（访问于 2026-08-07）
- [Anthropic Docs · Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)（访问于 2026-08-07）
- [最佳实践 · 原则 2](/claude-capabilities/prompting/best-practices#原则-2给示例few-shot)
- [System Prompt 设计 · 5 模式](/claude-capabilities/prompting/system-prompts#二5-个设计模式)
- [思维链 · 4 变体](/claude-capabilities/prompting/chain-of-thought#二4-种-cot-变体)

## 下一步

- XML 标签结构化 → [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)
- 速查模板 → [常用模板](/claude-capabilities/prompting/templates)
- 切到 API → [Messages API](/claude-capabilities/api/messages)

## 如果你想

- 风格转换实战 → [3 类实战模式](/claude-capabilities/prompting/few-shot#四3-类实战模式)
- 数据提取 → [结构化输出](/claude-capabilities/api/structured-outputs)
- 与 system 规则对比 → [System Prompt 设计](/claude-capabilities/prompting/system-prompts)

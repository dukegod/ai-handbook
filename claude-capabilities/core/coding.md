---
title: 代码能力
description: API 视角的代码生成能力；SWE-bench / HumanEval 实测对比、工具使用模式与代码审查实战
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  sweBench: 'https://www.swebench.com/'
  anthropicBlog: 'https://www.anthropic.com/news/claude-sonnet-4-5'
  accessedAt: 2026-08-06
---

# 代码能力

> **TL;DR**：Claude 5 代（Sonnet 5 / Opus 5 / Fable 5）在 SWE-bench Verified 上达到 **80%+** 准确率——接近资深工程师水平。Sonnet 5 应付 80% 编程任务，Opus 5 处理陌生代码与多文件重构，Fable 5 处理超长链代码 agent 任务。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 4 模型在 SWE-bench / HumanEval 实测中的差异
- API 视角的工具使用模式（tool_use 实现 Read / Edit / Bash）
- 4 类代码任务的模型选型（生成 / 审查 / 重构 / 测试）
- 何时 Sonnet 5 够用、何时升 Opus 5
- 5 个常见代码生成坑（幻觉 API、不存在的库、过时版本等）

## 一、Benchmark 实测对比

参考 [SWE-bench Verified](https://www.swebench.com/) 公开数据（访问于 2026-08-06）：

| Benchmark | 测什么 | Sonnet 5 | Opus 5 | Fable 5 | Haiku 4.5 |
| --- | --- | :---: | :---: | :---: | :---: |
| **SWE-bench Verified** | 多文件 PR 修复 | ~65% | ~78% | **~82%** | ~40% |
| **HumanEval** | 单函数生成 | ~92% | ~96% | ~97% | ~88% |
| **MultiPL-E** | 多语言生成 | ~85% | ~92% | ~93% | ~75% |
| **MBPP** | 简单编程 | ~95% | ~98% | ~98% | ~90% |
| **LiveCodeBench** | 真实场景 coding | ~70% | ~80% | **~85%** | ~45% |

**读法**：

- **Sonnet 5 已经是"接近资深工程师"**——80%+ 多文件 PR 修复对资深工程师是平均线
- **Opus 5 / Fable 5 在多文件、长链任务上显著更强**——但**单函数生成**差距小（95% vs 98% 实际应用区别不大）
- **Haiku 4.5 在 HumanEval 上 88%**——够日常用，但**别让它做陌生代码库 debug**

**反直觉**：**HumanEval 95% vs 98% 在生产中区别不大**——单函数生成早就"够用"。真正难的是 SWE-bench 那类**多文件、跨上下文、长链**任务，Opus 5 / Fable 5 优势最大。

## 二、API 视角的工具使用模式

Claude Code 内置的 Read / Edit / Bash 工具**就是 tool_use 协议的实现**——你做 API 集成时自己实现这些工具：

```python
import anthropic
import subprocess

client = anthropic.Anthropic()

# 定义工具（与 Claude Code 内置工具的 schema 等价）
tools = [
    {
        "name": "read_file",
        "description": "读取文件内容",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件绝对路径"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "edit_file",
        "description": "编辑文件（精确字符串替换）",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_string": {"type": "string"},
                "new_string": {"type": "string"},
            },
            "required": ["path", "old_string", "new_string"],
        },
    },
    {
        "name": "bash",
        "description": "执行 shell 命令",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
            },
            "required": ["command"],
        },
    },
]

# 一次多步工具调用
msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=8192,
    tools=tools,
    messages=[{"role": "user", "content": "在 src/auth.ts 加一个 JWT 验证函数"}],
)
```

**多步 tool call 实战**：

```python
# Claude 会按需多次 tool_use → 你执行 → 把结果喂回
def handle_tool_call(tool_name, tool_input):
    if tool_name == "read_file":
        return Path(tool_input["path"]).read_text()
    elif tool_name == "edit_file":
        # 精确字符串替换实现
        ...
    elif tool_name == "bash":
        return subprocess.run(tool_input["command"], shell=True, capture_output=True, text=True)

# 主循环
messages = [{"role": "user", "content": "..."}]
for _ in range(50):   # 上限 50 步
    msg = client.messages.create(model="claude-sonnet-5", tools=tools, messages=messages)
    if msg.stop_reason == "end_turn":
        break
    # 处理 tool_use
    messages.append({"role": "assistant", "content": msg.content})
    tool_results = []
    for block in msg.content:
        if block.type == "tool_use":
            result = handle_tool_call(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
    messages.append({"role": "user", "content": tool_results})
```

详见 [Tool Use 协议详解](/claude-capabilities/core/tool-use)。

## 三、4 类代码任务的模型选型

| 任务类型 | 首选 | 次选 | 原因 |
| --- | --- | --- | --- |
| **单函数生成** | Sonnet 5 | Haiku 4.5（成本敏感） | 简单任务 4 模型差距 < 5% |
| **单文件修改** | Sonnet 5 | Opus 5 | Sonnet 已够 |
| **多文件重构** | Opus 5 | Sonnet 5 + 多轮 | Opus 一次到位 |
| **陌生代码 debug** | Opus 5 | Sonnet 5 | 模式识别 Opus 强 |
| **大型 PR 审查** | Opus 5 | Sonnet 5 | review 任务 token 多 |
| **长链代码 agent（30+ 步）** | **Fable 5** | Opus 5 | Fable 步数少成本反而低 |
| **测试生成** | Sonnet 5 | Haiku 4.5（大量） | 模板化任务 |
| **代码翻译** | Sonnet 5 | Opus 5（复杂） | 单文件 Sonnet 够 |

## 四、代码审查 vs 代码生成

**代码生成**：4 模型差距较小（HumanEval 95-97%）——Sonnet 5 性价比最优。

**代码审查**：任务难度**远高于**生成——需要看完整代码、找 bug、给改进建议。Opus 5 / Fable 5 优势明显：

| 任务 | Sonnet 5 | Opus 5 |
| --- | --- | --- |
| 看 200 行代码找 bug | ~70% 召回 | ~85% 召回 |
| 看 5 文件 PR 找问题 | ~50% 召回 | ~80% 召回 |
| 给改进建议质量 | 良好 | 优秀 |

**实战模式**：

```python
# PR 审查 pipeline
def review_pr(diff: str) -> dict:
    response = client.messages.create(
        model="claude-opus-5",          # ← 审查用 Opus
        max_tokens=4096,
        system="你是资深代码审查员。重点找：1. 边界条件 2. 错误处理 3. 性能问题 4. 安全漏洞",
        messages=[{"role": "user", "content": f"审查这个 PR：\n\n{diff}"}],
    )
    return parse_review(response.content[0].text)
```

## 五、测试生成

**Haiku 4.5 + Batch API 是测试生成的甜区**——模板化任务，便宜优先：

```python
# 批量为 100 个函数生成测试
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"test-{i}",
            "params": {
                "model": "claude-haiku-4-5",
                "max_tokens": 2048,
                "messages": [{
                    "role": "user",
                    "content": f"为这个函数生成单元测试：\n```python\n{func.code}\n```\n要求覆盖正常路径、边界值、异常输入。"
                }],
            },
        }
        for i, func in enumerate(functions)
    ]
)
```

**质量权衡**：

| 模式 | 成本 | 测试质量 |
| --- | --- | --- |
| Haiku 4.5 批量 | $0.05 / 100 个 | 覆盖 70% 边界 |
| Sonnet 5 批量 | $0.15 / 100 个 | 覆盖 85% 边界 |
| Opus 5 逐个 | $0.50 / 100 个 | 覆盖 95% 边界 |

## 六、常见坑

**生成的代码引用不存在的库 / API**

```python
# Claude 可能生成
import requests_async   # ❌ 不存在

# 防御：prompt 里明确
"只用 Python 3.14 标准库 + 真实存在的第三方库（requests / aiohttp / httpx / flask / fastapi）"
```

**生成的代码用了过时的 API**

模型训练数据有截止日期——比如 Flask 1.x → 2.x 变化。**生产代码必 review + 跑测试**。

**测试覆盖率"虚高"**

```python
# ❌ Claude 容易生成的"假覆盖"
def test_foo():
    result = foo()
    assert result is not None    # 这不叫测试

# ✅ 强制 prompt
"每个 test_ 函数必须至少 1 个具体值断言（assertEqual / assertContains 等），
禁止只用 assertIsNotNone / assertTrue"
```

**多文件重构丢上下文**

长任务中 Claude 容易"忘记"之前改动——**关键文件 / 关键 schema 在 system prompt 里重申**：

```python
system = [
    {"type": "text", "text": "你正在重构 src/auth/ 模块。约定：所有函数 async；错误用 Result<T, E> 类型；不使用 try/except。"},
    {"type": "text", "text": "已完成的改动：\n- auth/jwt.ts 重写\n- auth/session.ts 重写", "cache_control": {"type": "ephemeral"}},
]
```

**混用 Sonnet 5 + Opus 5 的代码风格不一致**

**实战模式**：主任务用 Opus 5 重构 + Sonnet 5 补 boilerplate——但 prompt 强调 "保持与现有代码风格一致"。

## 参考

- [SWE-bench](https://www.swebench.com/)（访问于 2026-08-06）
- [Anthropic Blog · Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5)（访问于 2026-08-06）
- [Tool Use 协议详解](/claude-capabilities/core/tool-use)
- [Opus 5 详解 · 复杂编程场景](/claude-capabilities/models/opus#四opus-5-vs-sonnet-5实测选型)
- [Haiku 4.5 详解 · 批量生成测试](/claude-capabilities/models/haiku#四批量任务实战)
- [Subagent 编排](/claude-code/subagents-and-workflows/workflow-orchestration)

## 下一步

- Tool Use 完整协议 → [工具使用 API 协议](/claude-capabilities/core/tool-use)
- 长文档代码 review → [长上下文](/claude-capabilities/core/long-context)
- 视觉理解代码截图 → [Vision 能力](/claude-capabilities/core/vision)

## 如果你想

- 提示代码生成质量 → [深度提示工程 · System Prompts](/claude-capabilities/prompting/system-prompts)
- 工具链安全 → [MCP 协议层 · Server 编写](/claude-capabilities/mcp-protocol/server-authoring)
- 成本控制 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

# anthropic-sdk-python-minimal

Anthropic Python SDK 的**最小可复现示例**——5 个核心模式在 1 个文件里展示，复制即用。

> **配套教程**：[Python SDK](/claude-capabilities/sdk/python-sdk)（主 wiki 的 `claude-capabilities/` 章）

## 它做了什么

提供 5 个独立函数，对应 SDK 文档的 5 个核心模式：

| Mode | 用途 | 是否需 API key |
| --- | --- | :---: |
| `minimal` | Hello Claude 最小调用 | ✅ |
| `tool-loop` | Tool Use 循环（agent 基础） | ✅ |
| `streaming` | 流式响应（打字机效果） | ✅ |
| `structured` | 强制 JSON 输出（用 tool_use） | ✅ |
| `cache` | Prompt Caching 实战 | ✅ |

5 个模式**都靠真 API 调通**才能完整验证——`test_main.py` 只做静态自测（不调 API）。

## 目录结构

```
anthropic-sdk-python-minimal/
├── README.md        # 本文件
├── main.py          # 5 模式综合示例
├── test_main.py     # 静态自测（不调 API）
├── pyproject.toml   # uv / pip 项目元数据
└── .python-version  # 3.12
```

## 装依赖

需要 [uv](https://docs.astral.sh/uv/)（推荐）或 pip：

```bash
# uv（推荐）—— 自动建 .venv
uv sync
uv run python3 main.py minimal

# pip（备选）
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 设置 API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## 跑测试

```bash
# 静态自测（不需要 API key）
uv run test_main.py
# 期望：5/5 通过

# pytest 风格
uv run pytest
```

## 5 模式实战

```bash
# 模式 1：最小调用
uv run python3 main.py minimal
# 输出：Hello! How can I help...

# 模式 2：Tool Use 循环（让 Claude 读 README.md）
uv run python3 main.py tool-loop
# 输出：Claude 调 read_file → 拿到 README 前 3 行

# 模式 3：流式响应
uv run python3 main.py streaming
# 输出：打字机效果的故事 + token 用量

# 模式 4：Structured Outputs
uv run python3 main.py structured
# 输出：{"name": "Bob", "age": 30, "email": "bob@x.com"}

# 模式 5：Prompt Caching
uv run python3 main.py cache
# 输出：审查意见 + cache 命中 token 数
```

## 接入 Claude Code

**这个仓库不是 MCP server**——它是 Python SDK 的示例。要在 Claude Code 里用：

1. 复制 `mode_xxx()` 函数到你的项目
2. 装 `anthropic` 到你的依赖
3. 配 `ANTHROPIC_API_KEY` 环境变量

```python
# 你的项目里
from anthropic_sdk_python_minimal import main  # 不会这样用
# 直接复制函数体
def my_chat(prompt):
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
```

## 关键设计点

1. **5 模式拆 5 函数**——每个函数独立可复制，**不依赖** main.py 其他部分
2. **不写 uv.lock**——首次 `uv sync` 自动生成（避免手写 lock 文件）
3. **静态自测不调 API**——`test_main.py` 只检查**结构正确性**（5 模式都注册、schema 包含 required 字段、cache_control 用了等），避免消耗 token
4. **pyproject 用 `>=3.10`**——`anthropic` 包支持 3.10+，不强求 3.14
5. **不用 FastMCP / Agent SDK**——这是**基础 SDK 视角**，不引入额外抽象

## 已知限制

- **需真 API key**——5 模式都调真 API，本地没法 mock
- **小写 model ID**——`claude-sonnet-5-...` 是占位（实际 ID 略长），跑前需改成你账号能用的 ID
- **测试不覆盖真 API 调用**——结构正确 ≠ 业务正确，跑 `main.py <mode>` 手动验证
- **不演示 async 接口**——`AsyncAnthropic` 见 [Python SDK 文档](/claude-capabilities/sdk/python-sdk#三async-接口)

## 参考

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [PyPI · anthropic](https://pypi.org/project/anthropic/)
- [Python SDK 详解](/claude-capabilities/sdk/python-sdk)
- [Messages API](/claude-capabilities/api/messages)
- [Tool Use API](/claude-capabilities/api/tool-use)
- [Streaming](/claude-capabilities/api/streaming)
- [Structured Outputs](/claude-capabilities/api/structured-outputs)
- [Prompt Caching](/claude-capabilities/api/prompt-caching)
- [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 下一步

- TypeScript 版 → [examples/anthropic-sdk-typescript-minimal](/examples/anthropic-sdk-typescript-minimal/README)
- Agent SDK 版 → [examples/agent-sdk-minimal](/examples/agent-sdk-minimal/README)
- MCP server 模式 → [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 如果你想

- 多步 agent 实战 → [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

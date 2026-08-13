"""main.py —— anthropic SDK Python 最小可复现示例。

5 个核心模式在 1 个文件里展示：
1. 最小调用
2. Tool Use 循环
3. Streaming
4. Structured Outputs（用 tool_use 实现）
5. Prompt Caching

每个模式都是独立函数 —— 复制 [mode_name]() 就能直接用。

依赖：pip install anthropic
环境：export ANTHROPIC_API_KEY=sk-ant-...
"""
import json
import sys

import anthropic

# 5 个核心模式 ============================================================

def mode_minimal():
    """模式 1：最小调用 —— Hello Claude 风格。"""
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )
    print(msg.content[0].text)


def mode_tool_loop():
    """模式 2：Tool Use 循环 —— 让 Claude 调 bash 工具。"""
    import subprocess
    from pathlib import Path

    client = anthropic.Anthropic()
    tools = [{
        "name": "read_file",
        "description": "读取文件内容",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    }]

    def execute(name, tool_input):
        if name == "read_file":
            return Path(tool_input["path"]).read_text()
        return f"Unknown tool: {name}"

    messages = [{"role": "user", "content": "读 README.md 前 3 行"}]
    for _ in range(20):
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=4096,
            tools=tools,
            messages=messages,
        )
        if msg.stop_reason == "end_turn":
            return next(b.text for b in msg.content if b.type == "text")
        if msg.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": msg.content})
            results = []
            for block in msg.content:
                if block.type == "tool_use":
                    try:
                        result = execute(block.name, block.input)
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })
                    except Exception as e:
                        results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(e),
                            "is_error": True,
                        })
            messages.append({"role": "user", "content": results})
    return "Max turns exceeded"


def mode_streaming():
    """模式 3：Streaming —— 打字机效果。"""
    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-sonnet-5-...",
        max_tokens=1024,
        messages=[{"role": "user", "content": "讲个一句话故事"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print()
        final = stream.get_final_message()
        print(f"\n[input: {final.usage.input_tokens}, output: {final.usage.output_tokens}]")


def mode_structured():
    """模式 4：Structured Outputs —— 用 tool_use 强制 JSON。"""
    client = anthropic.Anthropic()
    tool = {
        "name": "extract_user",
        "description": "提取用户信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "email": {"type": "string"},
            },
            "required": ["name", "email"],
        },
    }
    msg = client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=512,
        tools=[tool],
        tool_choice={"type": "tool", "name": "extract_user"},
        messages=[{"role": "user", "content": "用户：Bob，30 岁，bob@x.com"}],
    )
    for block in msg.content:
        if block.type == "tool_use":
            return block.input
    return None


def mode_cache():
    """模式 5：Prompt Caching —— cache_control 实战。"""
    client = anthropic.Anthropic()
    system = [
        {
            "type": "text",
            "text": "你是 Python 审查员。代码风格：PEP 8 + async/await。",
            "cache_control": {"type": "ephemeral"},
        },
    ]
    msg = client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": "审查：def foo(): pass"}],
    )
    return {
        "text": msg.content[0].text,
        "input": msg.usage.input_tokens,
        "cache_read": msg.usage.cache_read_input_tokens,
    }


# 入口 ====================================================================

MODES = {
    "minimal": mode_minimal,
    "tool-loop": mode_tool_loop,
    "streaming": mode_streaming,
    "structured": mode_structured,
    "cache": mode_cache,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        print("用法：python3 main.py <mode>")
        print(f"可选 mode: {', '.join(MODES.keys())}")
        sys.exit(1)
    result = MODES[sys.argv[1]]()
    if result is not None:
        print(result)


if __name__ == "__main__":
    main()

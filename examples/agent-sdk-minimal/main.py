"""main.py —— 最小可复现的 Agent SDK 模式（基于 anthropic SDK 自实现）。

3 个核心模式：
1. 单 agent 跑多步任务（Tool Use 循环 + 简单 system prompt）
2. Supervisor 调度 sub-agent（主从模式）
3. 带 memory 的多轮对话（跨 session 持久化）

依赖：pip install anthropic
环境：export ANTHROPIC_API_KEY=sk-ant-...
"""
import json
import sys

import anthropic


# 模式 1：单 agent 跑多步任务 ===============================================

def mode_single_agent():
    """单 agent + 简单 system prompt + tool use 循环。"""
    client = anthropic.Anthropic()

    system = "你是研究助手。查资料 + 总结。回答用中文。"

    tools = [{
        "name": "web_search",
        "description": "查互联网信息（mock）",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    }]

    MOCK = {
        "transformer": "Transformer 是 2017 年 Google 提出的架构...",
        "注意力机制": "Self-attention 允许序列内任意位置交互...",
    }

    def execute(name, inp):
        return MOCK.get(inp.get("query", ""), "未找到相关资料")

    messages = [{"role": "user", "content": "研究 transformer 架构演进"}]
    for _ in range(20):
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=4096,
            system=system,
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
                    result = execute(block.name, block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": results})
    return "Max turns exceeded"


# 模式 2：Supervisor 调度 sub-agent =========================================

def mode_supervisor():
    """主 agent 调 sub-agent（researcher + writer）做端到端任务。

    实现要点：主 agent 通过 tool_use 调 sub-agent（每个 sub-agent
    是独立 function，模拟独立 agent 行为）。
    """
    client = anthropic.Anthropic()

    def run_researcher(query: str) -> str:
        """Sub-agent 1：研究员。"""
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=2048,
            system="你是研究员。给 3 个关键事实 + 一句话总结。",
            messages=[{"role": "user", "content": f"研究：{query}"}],
        )
        return next(b.text for b in msg.content if b.type == "text")

    def run_writer(research: str) -> str:
        """Sub-agent 2：写作者。"""
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=2048,
            system="你是技术写作者。基于素材写 200 字报告。",
            messages=[{"role": "user", "content": f"素材：\n{research}"}],
        )
        return next(b.text for b in msg.content if b.type == "text")

    # 主 agent 通过 tool 调 sub-agent
    sub_tools = [
        {
            "name": "call_researcher",
            "description": "调研究员 sub-agent 查资料",
            "input_schema": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
        {
            "name": "call_writer",
            "description": "调写作者 sub-agent 写报告",
            "input_schema": {
                "type": "object",
                "properties": {"research": {"type": "string"}},
                "required": ["research"],
            },
        },
    ]

    def execute(name, inp):
        if name == "call_researcher":
            return run_researcher(inp["query"])
        if name == "call_writer":
            return run_writer(inp["research"])
        return "Unknown"

    messages = [{"role": "user", "content": "研究 transformer 写 200 字报告"}]
    for _ in range(20):
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=4096,
            system="你是 supervisor。决定调 researcher 还是 writer。",
            tools=sub_tools,
            messages=messages,
        )
        if msg.stop_reason == "end_turn":
            return next(b.text for b in msg.content if b.type == "text")
        if msg.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": msg.content})
            results = []
            for block in msg.content:
                if block.type == "tool_use":
                    result = execute(block.name, block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": results})
    return "Max turns exceeded"


# 模式 3：带 memory 的多轮对话 ===============================================

def mode_memory():
    """跨 session 持久化 memory（用 JSON 文件存到磁盘）。"""
    import os
    from pathlib import Path

    MEMORY_PATH = Path("/tmp/agent_memory.json")

    def load_memory():
        if MEMORY_PATH.exists():
            return json.loads(MEMORY_PATH.read_text())
        return {"user_prefs": [], "history": []}

    def save_memory(mem):
        MEMORY_PATH.write_text(json.dumps(mem, ensure_ascii=False, indent=2))

    client = anthropic.Anthropic()
    mem = load_memory()

    # 第 1 轮：用户说偏好
    user_msg_1 = "我喜欢简洁的 Python 代码"
    mem["history"].append({"role": "user", "content": user_msg_1})

    msg_1 = client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=1024,
        messages=mem["history"],
    )
    response_1 = next(b.text for b in msg_1.content if b.type == "text")
    mem["history"].append({"role": "assistant", "content": response_1})
    mem["user_prefs"].append("简洁 Python")

    # 第 2 轮：新 session（模拟）—— 读 memory 后继续
    user_msg_2 = "写个 list comprehension 示例"
    mem["history"].append({"role": "user", "content": user_msg_2})

    prefs = "\n".join(f"- {p}" for p in mem["user_prefs"])
    msg_2 = client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=1024,
        system=f"用户偏好：\n{prefs}",
        messages=mem["history"],
    )
    response_2 = next(b.text for b in msg_2.content if b.type == "text")

    save_memory(mem)
    return {
        "round_1": response_1[:200],
        "round_2": response_2[:200],
        "memory_path": str(MEMORY_PATH),
        "user_prefs": mem["user_prefs"],
    }


# 入口 ====================================================================

MODES = {
    "single": mode_single_agent,
    "supervisor": mode_supervisor,
    "memory": mode_memory,
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

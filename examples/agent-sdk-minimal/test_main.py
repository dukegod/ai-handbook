#!/usr/bin/env python3
"""test_main.py —— Agent SDK 最小示例的静态自测。

5 个测试全部用 AST 解析 / 文本搜索 / subprocess，不 import main.py：
- 避免依赖 anthropic 安装
- 自测只验证代码结构，不验证业务行为
"""
import ast
import subprocess
import sys
from pathlib import Path

MAIN_PATH = Path(__file__).parent / "main.py"
SRC = MAIN_PATH.read_text(encoding="utf-8")
TREE = ast.parse(SRC)


def _find_modes_dict():
    for node in TREE.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "MODES":
                    return node.value
    return None


def test_modes_registered():
    """验证 3 个模式都注册到 MODES。"""
    modes_node = _find_modes_dict()
    assert modes_node is not None

    actual_keys = set()
    for k in modes_node.keys:
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            actual_keys.add(k.value)

    expected = {"single", "supervisor", "memory"}
    assert actual_keys == expected, f"模式不匹配：实际 {actual_keys}, 期望 {expected}"


def test_single_agent_uses_tool_loop():
    """验证 mode_single_agent 用 tool_use 循环模式。"""
    assert "mode_single_agent" in SRC
    assert "stop_reason" in SRC
    assert "tool_use" in SRC
    assert "tool_result" in SRC


def test_supervisor_uses_sub_agents():
    """验证 mode_supervisor 调 sub-agent（researcher + writer）。"""
    assert "mode_supervisor" in SRC
    assert "run_researcher" in SRC
    assert "run_writer" in SRC
    # 主 agent 通过 tool_use 调 sub
    assert "call_researcher" in SRC
    assert "call_writer" in SRC


def test_memory_uses_persistence():
    """验证 mode_memory 持久化到磁盘。"""
    assert "mode_memory" in SRC
    assert "MEMORY_PATH" in SRC
    assert "load_memory" in SRC
    assert "save_memory" in SRC
    assert "json" in SRC  # 用 json 序列化


def test_main_no_args_shows_usage():
    """验证 main() 无参时显示 usage 提示（兼容 anthropic 未装）。"""
    result = subprocess.run(
        [sys.executable, str(MAIN_PATH)],
        capture_output=True, text=True,
    )
    assert result.returncode == 1, f"期望 exit code 1，实际 {result.returncode}"

    if "用法" in result.stdout:
        assert "可选 mode" in result.stdout
        for mode in ["single", "supervisor", "memory"]:
            assert mode in result.stdout
        return

    # anthropic 未装
    assert "ModuleNotFoundError" in result.stderr
    assert "anthropic" in result.stderr


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✔ {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ✘ {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

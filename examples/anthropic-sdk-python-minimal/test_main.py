#!/usr/bin/env python3
"""test_main.py —— anthropic SDK Python 最小示例的静态自测。

**5 个测试全部用 AST 解析 / 文本搜索 / subprocess，不 import main.py**：
- 避免依赖 anthropic 安装（用户 clone 后没装也能跑）
- 自测只验证代码结构正确，不验证业务行为（业务靠 main.py <mode> 手动跑）

依赖：仅 Python 3.10+ 标准库
用法：python3 test_main.py
"""
import ast
import subprocess
import sys
from pathlib import Path

MAIN_PATH = Path(__file__).parent / "main.py"
SRC = MAIN_PATH.read_text(encoding="utf-8")
TREE = ast.parse(SRC)


def _find_modes_dict():
    """AST 找模块级 MODES = {...} 赋值。"""
    for node in TREE.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "MODES":
                    return node.value
    return None


def test_modes_registered():
    """验证 5 个模式都注册到 MODES dict。"""
    modes_node = _find_modes_dict()
    assert modes_node is not None, "未找到 MODES 顶层赋值"

    # 提取 dict 的所有 key（key 都是常量字符串）
    actual_keys = set()
    for k in modes_node.keys:
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            actual_keys.add(k.value)

    expected = {"minimal", "tool-loop", "streaming", "structured", "cache"}
    missing = expected - actual_keys
    extra = actual_keys - expected
    assert not missing, f"缺失模式: {missing}"
    assert not extra, f"多余模式: {extra}"


def test_all_modes_are_functions():
    """验证 MODES dict 的 value 都是函数定义。"""
    modes_node = _find_modes_dict()
    assert modes_node is not None

    for k, v in zip(modes_node.keys, modes_node.values):
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            assert isinstance(v, ast.Name), f"模式 {k.value!r} 不是直接函数引用"
            # 找该函数定义
            func_node = next(
                (n for n in TREE.body
                 if isinstance(n, ast.FunctionDef) and n.name == v.id),
                None,
            )
            assert func_node is not None, f"模式 {k.value!r} 引用 {v.id!r} 但找不到该函数定义"


def test_structured_uses_tool_choice():
    """验证 mode_structured 用了 tool_choice 强制 JSON。"""
    assert "tool_choice" in SRC
    assert '"tool"' in SRC
    assert '"name"' in SRC
    # 必须引用 extract_user
    assert "extract_user" in SRC


def test_cache_uses_cache_control():
    """验证 mode_cache 用了 cache_control + ephemeral + usage。"""
    assert "cache_control" in SRC
    assert "ephemeral" in SRC
    # 用了 usage.input_tokens / cache_read_input_tokens
    assert "cache_read_input_tokens" in SRC
    assert "input_tokens" in SRC


def test_main_no_args_shows_usage():
    """验证 main() 无参时显示 usage 提示。

    接受两种情况（兼容 anthropic 未装的环境）：
    1. anthropic 已装 → exit 1 + stdout 含"用法" + 5 模式
    2. anthropic 未装 → exit 1 + stderr 含 ModuleNotFoundError
    """
    result = subprocess.run(
        [sys.executable, str(MAIN_PATH)],
        capture_output=True, text=True,
    )
    # 退出码 1（无参或 import 失败都 exit 1）
    assert result.returncode == 1, f"期望 exit code 1，实际 {result.returncode}"

    # 情况 1：anthropic 已装，usage 提示
    if "用法" in result.stdout:
        assert "可选 mode" in result.stdout, f"stdout 缺'可选 mode': {result.stdout!r}"
        for mode in ["minimal", "tool-loop", "streaming", "structured", "cache"]:
            assert mode in result.stdout, f"stdout 缺模式 {mode}"
        return

    # 情况 2：anthropic 未装，import 失败
    assert "ModuleNotFoundError" in result.stderr, (
        f"既无'用法'提示也无 ModuleNotFoundError:\n"
        f"  stdout: {result.stdout!r}\n  stderr: {result.stderr!r}"
    )
    assert "anthropic" in result.stderr, f"stderr 应提及 anthropic: {result.stderr!r}"


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

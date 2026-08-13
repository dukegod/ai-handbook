/**
 * test_main.ts —— anthropic SDK TypeScript 最小示例的静态自测。
 *
 * 5 个测试全部用 AST 解析 / 文本搜索 / subprocess，不 import main.ts：
 * - 避免依赖 @anthropic-ai/sdk 安装
 * - 自测只验证代码结构正确，不验证业务行为
 *
 * 依赖：vitest
 * 用法：pnpm test
 */
import { describe, it, expect } from "vitest";
import { readFile } from "fs/promises";
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const MAIN_PATH = join(__dirname, "main.ts");

const SRC = await readFile(MAIN_PATH, "utf-8");

// 简单 AST：用正则匹配顶层 MODES 对象
function extractModeNames(): string[] {
  // 找 const MODES: Record<...> = { ... } 块的 keys
  const match = SRC.match(/const\s+MODES[^{]*\{([^}]*)\}/);
  if (!match) return [];
  const body = match[1];
  // 匹配 "key": func 形式
  const keys = [...body.matchAll(/["']([a-z-]+)["']\s*:\s*\w+/g)].map((m) => m[1]);
  return keys;
}

describe("anthropic-sdk-typescript-minimal", () => {
  it("5 模式都注册到 MODES", () => {
    const keys = extractModeNames();
    expect(keys.sort()).toEqual(["cache", "minimal", "streaming", "structured", "tool-loop"]);
  });

  it("5 模式都引用实际函数定义", () => {
    for (const name of ["minimal", "toolLoop", "streaming", "structured", "cache"]) {
      expect(SRC).toContain(`function ${name}`);
    }
  });

  it("modeStructured 用了 tool_choice 强制 JSON", () => {
    expect(SRC).toContain("tool_choice");
    expect(SRC).toContain('"tool"');
    expect(SRC).toContain("extract_user");
  });

  it("modeCache 用了 cache_control + ephemeral + usage.cache_read_input_tokens", () => {
    expect(SRC).toContain("cache_control");
    expect(SRC).toContain("ephemeral");
    expect(SRC).toContain("cache_read_input_tokens");
  });

  it("main 无参时显示 usage 提示（兼容 sdk 未装环境）", async () => {
    const result = await new Promise<{ code: number | null; stdout: string; stderr: string }>(
      (resolve) => {
        const child = spawn("npx", ["tsx", "main.ts"], { cwd: __dirname });
        let stdout = "";
        let stderr = "";
        child.stdout.on("data", (d) => stdout += d.toString());
        child.stderr.on("data", (d) => stderr += d.toString());
        child.on("close", (code) => resolve({ code, stdout, stderr }));
      },
    );
    // 退出码 1（无参 / import 失败）
    expect(result.code).toBe(1);
    // 情况 1：sdk 已装，usage 提示
    if (result.stdout.includes("用法")) {
      expect(result.stdout).toContain("可选 mode");
      for (const mode of ["minimal", "tool-loop", "streaming", "structured", "cache"]) {
        expect(result.stdout).toContain(mode);
      }
      return;
    }
    // 情况 2：sdk 未装，import 失败
    expect(result.stderr).toContain("Cannot find module");
  }, 30000);
});

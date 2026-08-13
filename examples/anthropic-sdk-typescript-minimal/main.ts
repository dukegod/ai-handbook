/**
 * main.ts —— anthropic SDK TypeScript 最小可复现示例。
 *
 * 5 个核心模式在 1 个文件里展示：
 * 1. 最小调用
 * 2. Tool Use 循环
 * 3. Streaming
 * 4. Structured Outputs（用 tool_use 实现）
 * 5. Prompt Caching
 *
 * 依赖：npm install
 * 环境：export ANTHROPIC_API_KEY=sk-ant-...
 */
import Anthropic from "@anthropic-ai/sdk";
import * as fs from "fs/promises";

// 5 个核心模式 ============================================================

async function modeMinimal(): Promise<string> {
  const client = new Anthropic();
  const msg = await client.messages.create({
    model: "claude-sonnet-5-...",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
  });
  const text = msg.content.find((b): b is Anthropic.TextBlock => b.type === "text");
  return text?.text ?? "";
}

async function modeToolLoop(): Promise<string> {
  const client = new Anthropic();
  const tools: Anthropic.Tool[] = [{
    name: "read_file",
    description: "读取文件内容",
    input_schema: {
      type: "object",
      properties: { path: { type: "string" } },
      required: ["path"],
    },
  }];

  async function execute(name: string, input: any): Promise<string> {
    if (name === "read_file") return await fs.readFile(input.path, "utf-8");
    return `Unknown tool: ${name}`;
  }

  const messages: Anthropic.MessageParam[] = [{ role: "user", content: "读 README.md 前 3 行" }];
  for (let i = 0; i < 20; i++) {
    const msg = await client.messages.create({
      model: "claude-sonnet-5-...",
      max_tokens: 4096,
      tools,
      messages,
    });
    if (msg.stop_reason === "end_turn") {
      const text = msg.content.find((b): b is Anthropic.TextBlock => b.type === "text");
      return text?.text ?? "";
    }
    if (msg.stop_reason === "tool_use") {
      messages.push({ role: "assistant", content: msg.content });
      const results: Anthropic.ToolResultBlockParam[] = [];
      for (const block of msg.content) {
        if (block.type === "tool_use") {
          try {
            const result = await execute(block.name, block.input);
            results.push({ type: "tool_result", tool_use_id: block.id, content: result });
          } catch (e) {
            results.push({
              type: "tool_result",
              tool_use_id: block.id,
              content: String(e),
              is_error: true,
            });
          }
        }
      }
      messages.push({ role: "user", content: results });
    }
  }
  return "Max turns exceeded";
}

async function modeStreaming(): Promise<void> {
  const client = new Anthropic();
  const stream = client.messages.stream({
    model: "claude-sonnet-5-...",
    max_tokens: 1024,
    messages: [{ role: "user", content: "讲个一句话故事" }],
  });
  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  process.stdout.write("\n");
  const final = await stream.finalMessage();
  console.log(`\n[input: ${final.usage.input_tokens}, output: ${final.usage.output_tokens}]`);
}

async function modeStructured(): Promise<any> {
  const client = new Anthropic();
  const tool: Anthropic.Tool = {
    name: "extract_user",
    description: "提取用户信息",
    input_schema: {
      type: "object",
      properties: {
        name: { type: "string" },
        age: { type: "integer" },
        email: { type: "string" },
      },
      required: ["name", "email"],
    },
  };
  const msg = await client.messages.create({
    model: "claude-sonnet-5-...",
    max_tokens: 512,
    tools: [tool],
    tool_choice: { type: "tool", name: "extract_user" },
    messages: [{ role: "user", content: "用户：Bob，30 岁，bob@x.com" }],
  });
  const toolUse = msg.content.find((b): b is Anthropic.ToolUseBlock => b.type === "tool_use");
  return toolUse ? toolUse.input : null;
}

async function modeCache(): Promise<{ text: string; cacheRead: number }> {
  const client = new Anthropic();
  const system: Anthropic.TextBlockParam[] = [
    {
      type: "text",
      text: "你是 TypeScript 审查员。代码风格：strict mode + async/await。",
      cache_control: { type: "ephemeral" },
    },
  ];
  const msg = await client.messages.create({
    model: "claude-sonnet-5-...",
    max_tokens: 2048,
    system,
    messages: [{ role: "user", content: "审查：const x = 1;" }],
  });
  const text = msg.content.find((b): b is Anthropic.TextBlock => b.type === "text");
  return { text: text?.text ?? "", cacheRead: msg.usage.cache_read_input_tokens };
}

// 入口 ====================================================================

type Mode = "minimal" | "tool-loop" | "streaming" | "structured" | "cache";

const MODES: Record<Mode, () => Promise<any>> = {
  "minimal": modeMinimal,
  "tool-loop": modeToolLoop,
  "streaming": modeStreaming,
  "structured": modeStructured,
  "cache": modeCache,
};

async function main() {
  const mode = process.argv[2] as Mode;
  if (!mode || !(mode in MODES)) {
    console.log("用法：pnpm start <mode>");
    console.log(`可选 mode: ${Object.keys(MODES).join(", ")}`);
    process.exit(1);
  }
  const result = await MODES[mode]();
  if (result !== undefined && result !== null) console.log(result);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

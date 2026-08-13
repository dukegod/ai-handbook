# anthropic-sdk-typescript-minimal

Anthropic TypeScript SDK 的**最小可复现示例**——5 个核心模式在 1 个文件里展示，复制即用。

> **配套教程**：[TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)（主 wiki）

## 它做了什么

提供 5 个独立 async 函数，对应 SDK 文档的 5 个核心模式：

| Mode | 用途 | 是否需 API key |
| --- | --- | :---: |
| `minimal` | Hello Claude 最小调用 | ✅ |
| `tool-loop` | Tool Use 循环（agent 基础） | ✅ |
| `streaming` | 流式响应（打字机效果） | ✅ |
| `structured` | 强制 JSON 输出（用 tool_use） | ✅ |
| `cache` | Prompt Caching 实战 | ✅ |

5 个模式**都靠真 API 调通**才能完整验证——`test_main.ts` 只做静态自测（不调 API）。

## 目录结构

```
anthropic-sdk-typescript-minimal/
├── README.md
├── main.ts          # 5 模式综合示例（async）
├── test_main.ts     # vitest 静态自测
├── package.json
├── tsconfig.json
└── .nvmrc           # 20
```

## 装依赖

需要 [Node.js 20+](https://nodejs.org/)（用 nvm 切版本）：

```bash
nvm use   # 自动用 .nvmrc 的 20
npm install
```

## 设置 API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## 跑测试

```bash
npm test
# 期望：5/5 通过（即使 SDK 未装也通过——自测不依赖 SDK）
```

## 5 模式实战

```bash
# 模式 1：最小调用
npx tsx main.ts minimal
# 输出：Hello! How can I help...

# 模式 2：Tool Use 循环
npx tsx main.ts tool-loop
# 输出：Claude 调 read_file → 拿到 README 前几行

# 模式 3：流式响应
npx tsx main.ts streaming
# 输出：打字机效果的故事 + token 用量

# 模式 4：Structured Outputs
npx tsx main.ts structured
# 输出：{ name: "Bob", age: 30, email: "bob@x.com" }

# 模式 5：Prompt Caching
npx tsx main.ts cache
# 输出：审查意见 + cache 命中 token 数
```

## 接入 Claude Code

**这个仓库不是 MCP server**——它是 TypeScript SDK 的示例。要在 Claude Code 里用：

1. 复制 `modeXxx()` 函数到你的项目
2. 装 `@anthropic-ai/sdk` 到你的依赖
3. 配 `ANTHROPIC_API_KEY` 环境变量

```typescript
// 你的项目里
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function myChat(prompt: string): Promise<string> {
  const msg = await client.messages.create({
    model: "claude-sonnet-5-...",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });
  const text = msg.content.find((b): b is Anthropic.TextBlock => b.type === "text");
  return text?.text ?? "";
}
```

## 关键设计点

1. **5 模式拆 5 async 函数**——每个独立可复制，**不依赖** main.ts 其他部分
2. **类型守卫** `(b): b is Anthropic.TextBlock => b.type === "text"`——TypeScript 5+ 强类型
3. **不锁定 lock 文件**——`package-lock.json` 在 `.gitignore`（避免手写错误；`npm install` 自动生成）
4. **静态自测不调 API**——`test_main.ts` 用 vitest + 文本搜索 / subprocess，**不依赖 SDK 安装**
5. **Node 20 LTS**——`.nvmrc` 锁版本

## 已知限制

- **需真 API key**——5 模式都调真 API
- **不演示 AnthropicAdmin**——那是管理端点，见 [Admin & Usage API](/claude-capabilities/api/admin-usage)
- **不演示 streaming + tool_use 组合**——见 [Tool Use API · 流式 tool_use](/claude-capabilities/api/tool-use#场景-3跳过客套)
- **测试不覆盖真 API 调用**——结构正确 ≠ 业务正确，跑 `main.ts <mode>` 手动验证

## 参考

- [Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [npm · @anthropic-ai/sdk](https://www.npmjs.com/package/@anthropic-ai/sdk)
- [TypeScript SDK 详解](/claude-capabilities/sdk/typescript-sdk)
- [Python 版仓库](/examples/anthropic-sdk-python-minimal/README)
- [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 下一步

- Agent SDK 版 → [examples/agent-sdk-minimal](/examples/agent-sdk-minimal/README)
- 多步 agent 实战 → [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

## 如果你想

- Node + Claude Code 集成 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)
- Python 对照 → [Python SDK 仓库](/examples/anthropic-sdk-python-minimal/README)

---
title: 操作文模板
description: 用于写「如何做 X」「X 快速上手」这一类操作型文档的模板
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-23
---

# 操作文模板

> 当你要写「如何做 X」「一步步教 X」「Y 快速上手」这类文档时，复制下面这份骨架。

**适用场景**：手把手教读者完成一件具体的事，读者跟着做能到达目标。

**不适用场景**：讲清楚一个概念或原理 → 用 [概念文模板](./template-concept)。

---

## 骨架

以下内容整块复制，改标题与占位符即可。

````markdown
---
title: 如何 XXX
description: 一句话说明本篇要完成什么任务、面向谁
audience: beginner
difficulty: 🟢
status: draft
lastUpdated: 2026-07-23
verifiedWith:
  claudeCode: 2.0.14
  model: claude-opus-4-8
  sdk: '@anthropic-ai/sdk@0.32.0'
---

# 如何 XXX

> **目标**：本篇结束后，你会得到一个可运行的 XXX。全程约 15 分钟。

## 你将做到

- ✅ 完成 A
- ✅ 完成 B
- ✅ 验证 C

## 前置检查清单

开始前请确保：

- [ ] Node.js ≥ 20 (`node -v`)
- [ ] 已安装 Claude Code (`claude --version`)
- [ ] 已在 [Anthropic Console](https://console.anthropic.com/) 拿到 API key
- [ ] 熟悉 [XXX 是什么](/link/to/concept)

## 第 1 步：准备工作目录

```bash
mkdir my-xxx-project && cd my-xxx-project
npm init -y
```

**预期输出：**

```
Wrote to /path/to/my-xxx-project/package.json:
...
```

## 第 2 步：安装依赖

```bash
npm install @anthropic-ai/sdk
```

## 第 3 步：写代码

新建 `index.mjs`：

```javascript
// Node 20+, @anthropic-ai/sdk@0.32+
// 最后验证 2026-07-23 with Claude Opus 4.8

import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,  // 敏感信息用环境变量
})

// 这次调用约 $0.003
const msg = await client.messages.create({
  model: 'claude-opus-4-8',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello, Claude' }],
})

console.log(msg.content[0].text)
```

## 第 4 步：运行

```bash
export ANTHROPIC_API_KEY=sk-ant-****
node index.mjs
```

**预期输出：**

```
Hello! How can I help you today?
```

## 第 5 步：验证

**验证点 1**：命令退出码是 `0`（`echo $?` 检查）
**验证点 2**：输出包含 assistant 的回复
**验证点 3**：Anthropic Console 的 Usage 页面能看到本次调用

## 常见错误

**报错 `401 Unauthorized`**

原因：API key 无效或未设置。

修复：
```bash
echo $ANTHROPIC_API_KEY  # 应输出 sk-ant-****
```

**报错 `Cannot find module '@anthropic-ai/sdk'`**

原因：忘了 `npm install` 或不在项目目录里。

修复：在项目根目录重新执行 `npm install @anthropic-ai/sdk`。

**响应很慢**

原因：可能命中了区域路由问题。

修复：检查网络到 `api.anthropic.com` 的延迟；企业用户考虑走 Bedrock/Vertex。

## 参考

- [Anthropic SDK · TypeScript](https://github.com/anthropics/anthropic-sdk-typescript)（访问于 2026-07-23）
- [Messages API 参考](https://docs.claude.com/en/api/messages)（访问于 2026-07-23）

## 下一步

- 让 XXX 使用工具 → [Tool Use 快速上手](/link/to/tool-use-howto)
- 优化成本 → [Prompt Caching 实操](/link/to/caching-howto)

## 如果你想

- 理解背后原理 → [XXX 是什么](/link/to/concept)
- 集成到已有项目 → [XXX 集成指南](/link/to/integration)
- 生产化部署 → [XXX 生产实践](/link/to/production)
````

---

## 写作建议

**每一步都能被"跑通验证"：**

操作文的核心是让读者复现你的步骤。每一步给出**预期输出**，读者对不上就能立即定位到问题所在的这一步。

**给成本估算：**

调用 API 时明确写"这次约 $x.xxx"。读者对成本有直觉，才敢放开手实验。

**「常见错误」是价值密度最高的段：**

你在验证过程中踩过的坑，就是读者会踩的坑。哪怕只有一条也要写下来，附上原因与修复。

**验证要具体：**

"应该能看到输出"是废话。"输出包含 `Hello`"、"文件行数为 42"、"exit code = 0"、"Console 里 Usage 有一条新记录"，才是能验证的验证。

**给"退出"路径：**

在结尾"如果你想"里给出多个方向，避免读者读完只能"再来一遍"。

**避免的写法：**

- ❌ 步骤太多而每步太简单（比如 15 步都是「点击某按钮」）
- ❌ 只给代码不给运行方法
- ❌ 「大家都知道 XX 环境准备好了」的假设
- ❌ 报错示例不完整，只有「会看到一个错」

## 参考

- [Diátaxis · How-to guides](https://diataxis.fr/how-to-guides/) — 操作文的四象限定位（访问于 2026-07-23）

## 下一步

- 写概念型文档 → [概念文模板](./template-concept)
- 校对术语 → [术语表](./glossary)
- 提交前自检 → 回到 [写作规范 · PR 前 checklist](./style-guide#十、pr-前自检-checklist)

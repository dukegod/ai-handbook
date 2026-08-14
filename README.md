# AI Handbook

> AI 知识体系、技术核心、产品动向与 Coding 落地（中文）

一份面向中文读者的 AI 全栈知识库，覆盖 AI 核心技术、Coding 落地、产品动向、LLM 厂商全景，以及 Claude 深度专项。

## 本地运行

前置：Node.js ≥ 18（推荐 20+）、pnpm ≥ 9。

```bash
pnpm install
pnpm dev          # 启动开发服务器，默认 http://localhost:5173
pnpm build        # 生成静态站点到 .vitepress/dist/
pnpm preview      # 本地预览构建产物
```

## 目录结构

```
.
├── CLAUDE.md                   项目上下文（Claude Code 自动加载）
├── AGENTS.md                   兼容其他平台（自动同步自 CLAUDE.md）
├── index.md                    首页
├── getting-started/            AI 入门（通用 AI 概念 + 工具选型）
├── ai-core/                    AI 核心技术
│   ├── fundamentals/             Transformer / 注意力 / 预训练 / RLHF
│   ├── model-arch/               Dense vs MoE / 长上下文 / 多模态
│   ├── training/                 数据工程 / 推理优化 / 量化蒸馏
│   └── eval/                     基准测试 / 评估方法论
├── ai-coding/                  AI Coding 落地
│   ├── tools/                    工具横评（Claude Code / Cursor / Copilot）
│   ├── workflows/                团队工作流 / CI/CD / Code Review
│   ├── patterns/                 重构 / 测试 / 文档生成模式
│   └── enterprise/               部署 / 安全 / 成本控制
├── ai-trends/                  AI 产品动向
│   ├── product-updates/          月度速报 / Claude / ChatGPT / 国内厂商
│   ├── research-highlights/      论文速递 / 开源推荐
│   └── industry/                 行业趋势 / 投融资
├── claude-code/                Claude Code CLI 精通（深度专项）
├── claude-capabilities/        Claude 全能力（API / SDK / MCP / Agentic）
├── ai-trends/vendors/          厂商档案（5 厂商对比）
├── reference/                  速查手册（含模型横向对比与选型决策树）
├── cookbook/                    实战案例
├── reference/                   速查手册
├── examples/                    示例仓库
├── scripts/                     工具脚本
└── contributing/                写作规范与路线图
```

## 内容路线图

见 [contributing/roadmap.md](./contributing/roadmap.md)。当前版本 **v0.2**：Claude 专项 107 篇 published，正在扩展为 AI 全栈知识体系。

## 贡献

写内容之前请先阅读：

- [写作规范](./contributing/style-guide.md)
- [术语表](./contributing/glossary.md)
- [概念文模板](./contributing/template-concept.md)
- [操作文模板](./contributing/template-howto.md)

如果你用 Claude Code 参与本项目：根目录 [CLAUDE.md](./CLAUDE.md) 会被自动加载为会话上下文，无需人工搬运。

## 许可

- 内容：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh)
- 代码（配置、脚本、组件）：MIT

## 声明

本项目与 Anthropic 无官方关联，是一份社区维护的中文学习资料。所有对 Anthropic 官方文档的引用均标注出处与访问日期。

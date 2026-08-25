# AI Handbook 项目上下文

> 这份文件是 Claude Code 每次会话自动加载的项目级记忆。目标是让任何一次新会话进来都能立刻理解项目定位、约束、常见坑与"下一步该做什么"。
>
> 保持精炼。不重复 [contributing/style-guide.md](./contributing/style-guide.md) 已细写的规范。

## 项目定位

**AI Handbook** 是一份面向中文读者、长期维护的 **AI 全栈知识库**，覆盖五个方向：

1. **AI 核心技术** —— Transformer / 注意力 / 预训练 / RLHF / MoE / 多模态
2. **AI Coding 落地** —— 工具横评 / 团队工作流 / 常见模式 / 企业部署
3. **产品动向** —— 月度速报 / 论文速递 / 开源推荐 / 行业趋势
4. **模型与厂商** —— 国外厂商（Anthropic / OpenAI / xAI）+ 国内厂商（DeepSeek / 字节豆包 / Moonshot / MiniMax / Zhipu / Qwen），横向对比与选型决策
5. **Claude 深度** —— Claude Code CLI 精通 + Claude API/SDK/MCP 全能力

当前版本 **v0.2**：Claude 专项 107 篇 published，正在扩展为 AI 全栈知识体系。按 [contributing/roadmap.md](./contributing/roadmap.md) 推进。

- **读者定位**：零基础 → 进阶全覆盖
- **协作模式**：个人主导
- **仓库**：`git@github.com:dukegod/ai-handbook.git`（默认分支 `main`）
- **线上站点**：[https://dukegod.github.io/ai-handbook/](https://dukegod.github.io/ai-handbook/)
- **本站与 Anthropic 无官方关联**

## 技术栈

- Node.js ≥ 20（本机 24），pnpm 10.28.1
- VitePress 1.6.4
- Mermaid 11.17 via `vitepress-plugin-mermaid` 2.0
- 无 TypeScript 检查、无 lint 工具（v0.4+ 再加）

## 常用命令

```bash
pnpm install        # 首次或更新依赖
pnpm dev            # 开发，http://localhost:5173，HMR
pnpm build          # 生成 .vitepress/dist/
pnpm preview        # 预览构建产物
```

停 dev / preview：`pkill -f 'vitepress'`。

## GitHub Pages 部署

已接入 GitHub Pages，当前线上地址：

- [https://dukegod.github.io/ai-handbook/](https://dukegod.github.io/ai-handbook/)

部署机制：

- GitHub Pages 发布来源是 `GitHub Actions`。
- Workflow 文件：`.github/workflows/deploy-pages.yml`。
- 推送到 `main` 自动触发；也可在 GitHub Actions 页面手动运行 `Deploy GitHub Pages`。
- Workflow 安装依赖后执行 `pnpm build`，发布 `.vitepress/dist/`。
- GitHub 项目站点挂在 `/ai-handbook/` 子路径下，因此 CI 设置 `VITEPRESS_BASE=/ai-handbook/`。
- `.vitepress/config.ts` 通过 `process.env.VITEPRESS_BASE ?? '/'` 设置 `base`，所以本地开发仍是根路径 `/`，不要把 `base` 写死成 `/ai-handbook/`。

GitHub Pages 费用与可见性：

- GitHub Free 可为公开仓库发布 Pages。
- 私有仓库发布 Pages 需要支持私有 Pages 的付费计划。
- 本仓库为了使用免费 Pages，已改为公开仓库。

部署排障记录：

- `pnpm-lock.yaml` 不能锁到公司内网 registry（例如 `registry.m.jd.com`），否则 GitHub runner 无法下载依赖。
- 如果 Actions 在 `Install dependencies` 卡住或报 socket timeout，先检查 `pnpm-lock.yaml` 是否包含内网 tarball。
- 处理方式：用公网 npm registry 重新生成 lockfile，并确保 workflow 里安装步骤显式使用 `--registry=https://registry.npmjs.org/`。
- Workflow 里的 `node-version` 当前为 `20`；GitHub Actions 可能提示 Node 20 deprecation warning，但当前不影响部署。
- 现有 `.github/workflows/lychee.yml` 死链检查可能失败，它和 Pages 部署是独立 workflow，不阻塞发布。

## 目录地图

```
.vitepress/         站点配置（config.ts 是 sidebar 的唯一真相源）
index.md            首页（layout: home）
getting-started/    AI 入门（通用 AI 概念 + 工具选型）
ai-core/            AI 核心技术（fundamentals / model-arch / training / eval）
ai-coding/          AI Coding 落地（tools / workflows / patterns / enterprise）
ai-trends/          产品动向
├── product-updates/   月度速报
├── vendors/           国外厂商（Anthropic / OpenAI / xAI）
│   └── anthropic/     Anthropic · Claude 全系（含动态）
│   └── openai/        OpenAI · GPT 全系（含动态）
│   └── grok/          xAI · Grok 全系
├── cn-vendors/        国内厂商（DeepSeek / 字节豆包 / Moonshot / MiniMax / Zhipu / Qwen）
│   └── deepseek/      DeepSeek
│   └── doubao/        字节豆包
│   └── moonshot/      Moonshot · Kimi 全系
│   └── minimax/       MiniMax 全系
│   └── zhipu/         Zhipu · 智谱 GLM 全系
│   └── qwen/          Qwen · 阿里通义千问全系
├── research-highlights/ 技术速递
└── industry/          行业观察
claude-code/        Claude Code CLI 精通（9 个子章 + reference 速查手册）
claude-capabilities/ Claude 能力全景（8 个子章，含模型 ID 速查）
cookbook/           实战案例
contributing/       写作规范五件套（本文重要参考）
```

任何一次结构调整必须**同步改** [.vitepress/config.ts](./.vitepress/config.ts) 里对应的 `sidebar` 数组，否则新页面显示不出来。

## 写作规范（红线摘要）

完整规范见 [contributing/style-guide.md](./contributing/style-guide.md)。以下是**必须坚守的最少约束**：

**术语规范**
- `Anthropic` = 公司，`Claude` = 模型，`Claude Code` = CLI 工具（三者禁止混用）
- `OpenAI` = 公司，`GPT` = 通用模型系列，`o 系列` = 推理模型
- `xAI` = 公司，`Grok` = 模型
- 国内厂商同理：公司名 ≠ 模型名

术语表见 [contributing/glossary.md](./contributing/glossary.md)。新术语先补表，再写正文。

**Frontmatter 强制字段**
```yaml
---
title: ...
description: ...
audience: beginner | intermediate | advanced
difficulty: 🟢 | 🟡 | 🔴
status: planned | draft | published
lastUpdated: YYYY-MM-DD
verifiedWith:              # published 时必填（Claude 相关页面）
  claudeCode: 2.x.x
  model: claude-opus-4-8
  sdk: '...'
---
```

**中英混排前后加半角空格**：`使用 Claude Code`，不是 `使用ClaudeCode`。

**每篇结尾两组引导**：`## 下一步`（线性）+ `## 如果你想`（横向跳转）。

## 内容开发工作流

**新写一篇 planned 页面**：

1. 决定这是概念文还是操作文
   - 讲"是什么 / 为什么" → 复制 [contributing/template-concept.md](./contributing/template-concept.md)
   - 讲"如何做" → 复制 [contributing/template-howto.md](./contributing/template-howto.md)
2. 覆盖对应的占位 md（保留 URL 路径）
3. 更新 frontmatter：`status: published`、填 `verifiedWith`、更新 `lastUpdated`
4. 术语与 glossary 对齐
5. 在 [.vitepress/config.ts](./.vitepress/config.ts) 的 sidebar 里去掉该条目的 🚧（把 `P('...')` 改为 `'...'` 字符串）
6. 跑 `pnpm build` 确认无报错；**跑 `pnpm check-links` 验死链**（v0.4.1 引入 lychee，详细见 [contributing/link-checking.md](./contributing/link-checking)）
7. 用 [style-guide 的 PR 前 checklist](./contributing/style-guide.md#十、pr-前自检-checklist) 逐项核对

**改老页面**：同步改 `lastUpdated` 与 `verifiedWith`；破坏性变更用引用块标注 `> ⚠️ 已废弃（Since Claude Code 2.x）`。

## 已知坑与对策

**YAML frontmatter 里 description 含反引号必须用单引号包裹**

反例（build 会报 `end of the stream or a document separator is expected`）：
```yaml
description: `anthropic` 官方 Python 包
```

正确：
```yaml
description: '`anthropic` 官方 Python 包'
```

只要值里有反引号、冒号、`{}[]#&*!|>%@` 任何 YAML 特殊字符，就用单引号包起来。

**Mermaid + pnpm strict = 页面空白（需 `.npmrc` 里 `shamefully-hoist=true`）**

Mermaid 11.x 的 ESM 通过裸模块名引用间接依赖：`dayjs` / `@braintree/sanitize-url` / `debug` / `cytoscape` / `cytoscape-cose-bilkent`。pnpm 默认严格模式把它们藏在 `node_modules/.pnpm/` 深层，浏览器加载 `dayjs` 时找不到 → Vue 应用 crash → 所有页面显示空白。

修复：项目根目录 `.npmrc` 里保留 `shamefully-hoist=true`。**不要删这行**。

DevTools 里典型现象：Sources 面板能看到 `mermaid.core` 的 chunk 尝试 `import dayjs from "/node_modules/.pnpm/dayjs@x.x.x/..."`，控制台报 module not found。

如果误删 `.npmrc` 后 dev / build 页面变空白，恢复 `.npmrc` 再 `CI=true pnpm install`（`CI=true` 避免 pnpm 因 TTY 交互中止 modules 重建）。

**GitHub Pages 构建不能依赖内网 npm registry**

GitHub Actions runner 访问不到公司内网 registry。`pnpm-lock.yaml` 里如果出现内网 tarball URL，会导致 Pages workflow 在安装依赖阶段超时或失败。

修复：用公网 npm registry 重新生成 lockfile，并保留 `.github/workflows/deploy-pages.yml` 里的：

```bash
pnpm install --frozen-lockfile --registry=https://registry.npmjs.org/
```

不要把 `.vitepress/config.ts` 的 `base` 写死。线上通过 `VITEPRESS_BASE=/ai-handbook/` 注入，本地默认 `/`。

**页面底部 `最后更新` 需要 git commit 后才显示**

VitePress 的 `lastUpdated` 从 git history 取。项目还没 commit 之前所有页面底部时间会为空——正常行为。

**Sidebar 里的 🚧 是 `P()` 函数加的**

看 [.vitepress/config.ts](./.vitepress/config.ts) 顶部：`const P = (text) => \`${text} 🚧\``。占位页用 `P('xxx')` 包裹，发布后改为 `'xxx'` 直接字符串。

## Fable 5 定位（已核实）

已在 [claude-code/basics/model-selection.md](./claude-code/basics/model-selection.md) 撰写时核实（2026-07-24），基于三个 Anthropic 官方一手来源：

- [code.claude.com/model-config](https://code.claude.com/docs/en/model-config#work-with-fable-5)
- [platform.claude.com/models/overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [claude.com/blog · Choosing a Claude model](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)

**关键事实**（写 [claude-capabilities/models/fable.md](./claude-capabilities/models/fable.md) 时直接引用）：

- `claude-fable-5`，"Next-generation intelligence for long-running agents"
- 2026-06-09 GA；Claude API / Bedrock / Vertex / Foundry 都支持
- Pricing：**$10 / $50 per MTok**（比 Opus 5 贵 2 倍）
- Context 1M，Max output 128k，adaptive thinking **always on**
- 官方比喻：**Fable = the specialist**（顶级专家），Opus = expert，Sonnet = generalist
- Claude Code 特殊行为：**不是默认**，需 `/model fable`；cybersecurity/biology 触发 fallback 到 Opus 5/4.8；zero data retention 环境不可用；需 v2.1.170+

**不要**再写「定位待核实」——若发现新信息，直接更新引用来源与日期。

## 内容边界（不做什么）

- **不重复官方 API schema 全表** → 只写"为什么用 / 何时用 / 踩坑"
- **不做纯翻译搬运** → 中文站的差异化在场景化案例、踩坑记录、中文语境技巧
- **Cookbook 案例入选门槛**：别处查不到 + 近 90 天可复现 + 有踩坑 + 有边界
- **每篇 ≤ 1500 汉字**，超过就拆

## 当前阶段的关键任务

- [x] Claude 专项 107 篇 published（v0.1 ~ v0.4.3）
- [x] 项目重命名为 AI Handbook，扩展为 AI 全栈知识体系（v0.2）
- [x] 新模块骨架：ai-core（12 stub）+ ai-coding（14 stub）+ ai-trends（8 stub）
- [ ] 填充 ai-coding/tools/ 横评（最高 ROI）
- [ ] 填充 ai-core/fundamentals/ 基础原理
- [x] GitHub Pages 部署
- [ ] 后续：i18n、Algolia 搜索

## 关键参考

- [contributing/style-guide.md](./contributing/style-guide.md) — 完整写作规范
- [contributing/glossary.md](./contributing/glossary.md) — 中英双语术语锁定
- [contributing/template-concept.md](./contributing/template-concept.md) — 概念文模板
- [contributing/template-howto.md](./contributing/template-howto.md) — 操作文模板
- [contributing/roadmap.md](./contributing/roadmap.md) — 分阶段路线图
- [.vitepress/config.ts](./.vitepress/config.ts) — sidebar 唯一真相源
- [Anthropic 官方文档](https://docs.claude.com/)
- [OpenAI 官方文档](https://platform.openai.com/docs)
- [AI 核心技术](/ai-core/) — Transformer / 注意力 / 预训练等基础知识
- [AI Coding 落地](/ai-coding/) — 工具横评与工作流

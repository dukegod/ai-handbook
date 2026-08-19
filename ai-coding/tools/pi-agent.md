---
title: PI-agent 深度评测
description: pi.dev 极简 Agent 框架深度评测——5 阶段 Loop + 统一 LLM API + 99.93% 缓存命中率
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-08-17
verifiedWith:
  sources:
    - name: pi.dev 官网
      url: https://pi.dev
      accessedAt: 2026-08-17
    - name: GitHub 仓库
      url: https://github.com/badlogic/pi-mono
      accessedAt: 2026-08-17
    - name: DeepSeek 官方中文文档
      url: https://github.com/deepseek-ai/awesome-deepseek-agent/blob/main/docs/pi_mono.zh-CN.md
      accessedAt: 2026-08-17
---

# PI-agent 深度评测

> **TL;DR**：Mario Zechner（libGDX 创始人）打造的极简 Agent 框架——5 阶段 Loop + 统一 LLM API，DeepSeek V4 上缓存命中率 99.93%，10 亿 tokens 成本仅 $2.65。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- PI-agent 的作者背景与设计哲学
- 5 阶段 Agent Loop 的架构优势
- 统一 LLM API + 缓存性能数据
- 与 Claude Code / Codex / DeepSeek Harness 的差异化
- 适用场景与最佳实践

## 作者与项目背景

### Mario Zechner（badlogic）

| 维度 | 信息 |
|------|------|
| **网名** | badlogic |
| **代表作 1** | **libGDX** —— Java 跨平台游戏框架，全球开发者使用 |
| **代表作 2** | **RoboVM** —— iOS 上的 Java 虚拟机（已被 Xamarin 收购） |
| **当前主业** | pi-mono 全职开发 |
| **风格** | 极简主义、性能优先、context 控制狂 |

Mario 的核心能力是**"造抽象层"**——libGDX 把 Java 跨平台，RoboVM 把 Java 跑在 iOS 上，pi 把任意 LLM 跑在统一抽象层上。

### 项目时间线

| 时间 | 里程碑 |
|------|--------|
| 2024 年中 | Mario 公开"想做一个极简 coding agent" |
| 2024 年底 | pi-mono 第一个 commit |
| 2026 年初 | NVIDIA 翻牌（基础设施层） |
| 2026 年 4 月 | DeepSeek V4 发布，pi 是第一个吃螃蟹的 harness |
| 2026 年 6 月 | v0.71.1，4 万 stars |
| 2026 年 8 月 | DeepSeek Harness 开源后，pi 仍是"模型无关"的中立 agent 框架 |

## 核心定位：框架，不是产品

PI-agent（pi.dev）核心哲学是 **"Adapt Pi to your workflows, not the other way around"**。它刻意不做成"开箱即用"的产品，而是提供一套**原语（primitives）**，让用户自己组装 AI 编程工作流。

| 维度 | PI-agent | Claude Code | Codex | Cursor |
|------|----------|-------------|-------|--------|
| **定位** | Agent 框架 | CLI 产品 | CLI 产品 | IDE 产品 |
| **开箱即用** | ⭐（需组装） | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **可扩展性** | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| **模型支持** | 15+ 提供商 | Anthropic | OpenAI | 多模型 |
| **定价** | 免费（MIT） | $20-200/月 | 按 token | $20-40/月 |

## 技术架构

### 5 阶段 Agent Loop（核心创新）

pi-agent-core 的 Agent Loop 分为 5 个阶段，这是 pi 区别于其他 harness 的核心设计：

```
┌─────────────────────────────────────────────────┐
│  pi-agent-core: Agent Loop（5 阶段）            │
├─────────────────────────────────────────────────┤
│                                                 │
│   1. Intake（输入接收）                          │
│      ↓                                          │
│   2. Context Assembly（上下文组装）              │
│      ↓                                          │
│   3. Model Inference（模型推理）                 │
│      ↓                                          │
│   4. Tool Execution（工具执行）                  │
│      ↓                                          │
│   5. Response（响应输出）                        │
│      ↓                                          │
│   （回到 2，继续下一轮）                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

**为什么 5 阶段设计很重要**：

| 优势 | 解释 |
|------|------|
| **system prompt 稳定** | 每个阶段调用 LLM 时 system prompt 结构一致 |
| **tools 定义稳定** | 工具 schema 在 Context Assembly 阶段注入，前缀不漂移 |
| **UI 与 LLM 调用解耦** | TUI/Web UI 不污染 LLM 请求前缀 |
| **缓存友好** | 前缀字节稳定 → DeepSeek prefix cache 命中率天然高 |

### 统一 LLM API（pi-ai）

pi-ai 是统一的 LLM API 抽象层，支持多厂商模型无缝切换：

```
pi-ai 抽象层
   ↓
   ├── OpenAI 兼容接口（OpenAI / DeepSeek / 国产大模型）
   ├── Anthropic Messages（Claude）
   ├── Google Generative AI（Gemini）
   └── vLLM 自定义推理（本地 GPU）
```

**关键设计**：

- ✅ 模型无关：换模型不改代码
- ✅ 配置驱动：`models.json` 声明供应商
- ✅ 流式支持：SSE / WebSocket 统一封装
- ✅ 工具调用统一：tool_calls schema 跨厂商标准化

**配置示例**（DeepSeek）：

```json
// ~/.pi/agent/models.json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "api": "openai-completions",
      "apiKey": "$DEEPSEEK_API_KEY",
      "models": [
        { "id": "deepseek-v4-pro" }
      ]
    }
  }
}
```

### 仓库结构（TypeScript monorepo）

```
pi-mono/
├── packages/
│   ├── pi-agent-core/       # 核心 Agent Loop
│   ├── pi-ai/               # 统一 LLM API 抽象
│   ├── pi-coding-agent/     # CLI 编码 agent
│   ├── pi-tui/              # 终端 UI
│   ├── pi-web-ui/           # Web UI
│   ├── pi-slack-bot/        # Slack bot 集成
│   ├── pi-vllm/             # vLLM 本地推理
│   └── ...（更多子包）
├── biome.json               # 代码风格配置
├── package.json
└── README.md
```

## 缓存性能：99.93% 命中率

pi 在 DeepSeek V4 Flash 上的缓存表现远超行业平均水平：

| 指标 | pi-mono | 其他 harness | 差距 |
|------|---------|-------------|------|
| **DeepSeek V4 Flash 缓存命中率** | **99.93%**（10 亿 tokens 实测） | 94-97% | +3-6pp |
| **10 亿 tokens 成本** | **$2.65** | ~$30 | -91% |
| **持续稳定性** | 99%+ | 90-97% | 更稳定 |

**为什么 pi 能做到 99.93%**：

1. **5 阶段 Loop 的 system prompt 稳定**——前缀字节不漂移
2. **统一 API 不引入额外字段污染 cache key**
3. **TUI / Web UI 独立渲染**，UI 层不污染 LLM 请求
4. **工具调用格式统一**（tool_calls schema 标准化）

→ 这 4 点都是**架构层面的 design by default**，不是后期优化。

## 核心优势

### 1. 极致可扩展：扩展 + Skills + 提示模板

- **扩展（Extensions）**：TypeScript 模块，可实现任意功能
- **Skills**：能力包，包含指令和工具
- **提示模板（Prompt Templates）**：可复用的 markdown 提示，通过 `/name` 展开
- **主题（Themes）**：UI 主题定制

**50+ 扩展示例**：子代理、Plan Mode、权限门控、沙箱、SSH 执行，甚至 DOOM 游戏扩展。

```bash
# 安装扩展
pi install @some-org/extension-name
# 或自己构建
pi build-extension my-tool
```

### 2. 15+ 模型提供商，数百个模型

| 提供商 | 模型示例 |
|--------|---------|
| Anthropic | Claude Opus / Sonnet / Haiku |
| OpenAI | GPT-4o / o3 / o4-mini |
| Google | Gemini Pro / Flash |
| Azure / Bedrock | 企业级部署 |
| DeepSeek | V4 Pro / V4 Flash |
| Mistral / Groq / Cerebras | 高性能推理 |
| xAI / Kimi / MiniMax | 新兴提供商 |
| Ollama / OpenRouter | 本地 / 聚合 |

**会话内切换模型**：`/model` 或 `Ctrl+L`，`Ctrl+P` 循环收藏模型。

### 3. AGENTS.md 原生支持

```
~/.agents/AGENTS.md           # 全局
├── 项目根/AGENTS.md          # 项目级
├── 项目根/SYSTEM.md          # 系统提示替换/追加
└── 子目录/AGENTS.md          # 目录级
```

### 4. 四种运行模式

| 模式 | 用途 | 示例 |
|------|------|------|
| **Interactive** | 完整终端 UI | `pi` |
| **Print/JSON** | 脚本化 + 事件流 | `pi -p "query"` / `--mode json` |
| **RPC** | JSON 协议（stdin/stdout） | 非 Node.js 集成 |
| **SDK** | 嵌入其他应用 | 程序化调用 |

### 5. 会话树 + 自修改

- **树状历史**：`/tree` 导航到任意历史节点并分支
- **书签 + 过滤 + 导出**：`/export` 导出 HTML，`/share` 上传 GitHub Gist
- **自修改**：让 Pi 构建自定义扩展，`/reload` 即时激活，无需重启

### 6. Steering 机制

Agent 工作时可以实时干预：

- `Enter`：**Steering 消息**——中断当前工具调用
- `Alt+Enter`：**Follow-up**——等当前任务完成再处理

## 生态背书

| 背书方 | 时间 | 含义 |
|--------|------|------|
| **NVIDIA** | 2026 上半年 | 把 pi 当 AI infra 标准件 |
| **DeepSeek 官方** | 2026-08 | 在 `awesome-deepseek-agent` 收录 pi 中文文档 |
| **OpenClaw** | 持续 | 把 pi 作为底层 agent 引擎 |

| 维度 | 数据 |
|------|------|
| **GitHub stars** | ~4 万 |
| **更新频率** | 高（每周多次 commit） |
| **Issue 响应** | 通常 1-3 天 |
| **协议** | MIT（核心） |

## 核心局限

### 1. 刻意缺失的功能

PI-agent 故意不内置这些功能，需要你自己装扩展：

| 缺失功能 | 替代方案 |
|----------|---------|
| 无 MCP（Model Context Protocol） | 扩展可添加 |
| 无子代理 | tmux 或扩展 |
| 无权限弹窗 | 容器运行或自建流程 |
| 无 Plan Mode | 扩展可添加 |
| 无内置 TODO | TODO.md 或扩展 |
| 无后台 bash | tmux |

### 2. 作者单点风险

Mario 是绝对核心 maintainer，bus factor = 1。

### 3. v0.x 阶段

API 仍在变化，breaking change 风险。企业级商业化路径不清晰。

### 4. DeepSeek Harness 竞争

DeepSeek 官方出了 Harness 后，pi 失去"中立模型供应商"的部分优势。

## 与 Claude Code / Codex / DeepSeek Harness 对比

| 维度 | PI-agent | Claude Code | Codex | DeepSeek Harness |
|------|----------|-------------|-------|-----------------|
| **形态** | CLI 框架 | CLI 产品 | CLI 产品 | Agent 框架 |
| **模型** | 15+ 提供商 | Anthropic | OpenAI | 插件扩展 |
| **内核** | 自研 | — | — | Cordis |
| **扩展** | ⭐⭐⭐（TypeScript） | ⭐⭐（MCP + Skills） | ⭐ | ⭐⭐⭐⭐（插件一切） |
| **缓存优化** | ⭐⭐⭐⭐（99.93%） | ⭐⭐ | ⭐ | ⭐⭐ |
| **可观测性** | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐（Trajectory） |
| **开箱即用** | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **定价** | 免费 MIT | $20-200/月 | 按 token | 免费 MIT |
| **AGENTS.md** | ✅ 原生 | ✅ 兼容 | ✅ 原生 | ✅ 原生 |

## 规范与配置：AGENTS.md + SYSTEM.md 双轨

### 规则文件加载链

```
~/.agents/AGENTS.md           # 全局（用户级偏好）
├── 项目根/AGENTS.md          # 项目级（团队共享）
├── 项目根/SYSTEM.md          # 系统提示替换/追加
├── 子目录/AGENTS.md          # 目录级（天然路径作用域）
└── Skills/                   # 按需加载能力包
```

### 路径作用域

通过**子目录 AGENTS.md** 实现：

```
src/pages/AGENTS.md     # 仅 pages 相关文件被涉及时生效
src/common/AGENTS.md    # 仅 common 相关文件被涉及时生效
```

### 与 Claude Code / Codex / Cursor / Trae 的兼容

| 场景 | 解法 |
|------|------|
| Codex 用户也要读 PI 的规则 | 把通用规范放 `AGENTS.md`，Codex 原生支持 |
| Claude Code 用户也要读 PI 的规则 | 把通用规范放 `AGENTS.md`，Claude Code 新版同时读取 |
| Cursor 用户也要读 PI 的规则 | 把通用规范放 `AGENTS.md`，Cursor 兼容读取 |
| Trae 用户也要读 PI 的规则 | 把通用规范放 `AGENTS.md`，Trae 原生支持 |
| PI 专属配置（SYSTEM.md / 扩展） | 留在 SYSTEM.md 或扩展目录，其他工具忽略 |

## 适用场景

| 用户类型 | 推荐度 | 理由 |
|---------|--------|------|
| **个人开发者**（想用 coding agent） | ⭐⭐⭐⭐⭐ | 直接用，免费 MIT |
| **创业团队**（搭 agent 产品） | ⭐⭐⭐⭐⭐ | 用 pi-agent-core 作为底层 |
| **企业研发**（私有化部署） | ⭐⭐⭐ | 观望，看商业版 |
| **大厂基础设施**（如 NVIDIA 案例） | ⭐⭐⭐⭐ | 已成事实标准 |

**不太适合**：

- 需要开箱即用体验的新手
- 依赖 MCP 生态的用户（需额外装扩展）
- 追求稳定 API 的生产环境（v0.x 阶段）

## 最佳实践

### 1. 从 models.json 开始配置

```json
// ~/.pi/agent/models.json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "api": "openai-completions",
      "apiKey": "$DEEPSEEK_API_KEY",
      "models": [{ "id": "deepseek-v4-pro" }]
    },
    "anthropic": {
      "api": "anthropic-messages",
      "apiKey": "$ANTHROPIC_API_KEY",
      "models": [{ "id": "claude-sonnet-5" }]
    }
  }
}
```

**经验法则**：优先用 DeepSeek V4 Flash——pi 的缓存优化在 DeepSeek 上效果最好（99.93% 命中率），成本是 Claude 的 1/10。

### 2. 渐进式扩展——Top 10 推荐

先用内置能力跑通基础流程，按优先级逐步安装扩展：

| 优先级 | 扩展 | 功能 | 安装 | 为什么需要 |
|--------|------|------|------|-----------|
| **P0** | **Plan Mode** | 任务拆解 + 分步执行 | `pi install plan-mode` | 复杂任务必备，避免一步到位的幻觉 |
| **P0** | **Sub-agents** | 派生子代理并行处理 | `pi install sub-agents` | 大任务拆分、并行执行的核心能力 |
| **P1** | **Permission Gates** | 自定义确认/审批流 | `pi install permission-gate` | 生产环境安全兜底，防止误操作 |
| **P1** | **Path Protection** | 保护指定文件不被修改 | `pi install protected-paths` | 守住配置文件、lock 文件等敏感路径 |
| **P1** | **MCP Integration** | 接入 Model Context Protocol | `pi install mcp-extension` | 连接 GitHub、数据库、API 等外部工具 |
| **P2** | **Custom Compaction** | 自定义上下文压缩策略 | `pi install compaction` | 长会话防上下文溢出，可选 topic-based / code-aware 摘要 |
| **P2** | **Sandboxing** | 沙箱隔离执行 | `pi install sandbox` | 不信任的代码在隔离环境运行 |
| **P2** | **SSH Execution** | 远程命令执行 | `pi install ssh` | 远程服务器部署、跨机器操作 |
| **P3** | **RAG / Memory** | 检索增强生成 + 长期记忆 | 自建扩展 | 项目知识库、历史决策记忆 |
| **P3** | **Dynamic Context** | 每轮注入动态上下文 | 自建扩展 | 根据文件变化、git 状态自动注入相关信息 |

**安装顺序建议**：

```bash
# 第一步：核心能力（Day 1）
pi install plan-mode
pi install sub-agents

# 第二步：安全兜底（Week 1）
pi install permission-gate
pi install protected-paths

# 第三步：外部连接（Week 2）
pi install mcp-extension

# 第四步：进阶优化（按需）
pi install compaction
pi install sandbox
pi install ssh
```

**经验法则**：P0 是"没它基本不能用"，P1 是"生产环境必须有"，P2 是"提升体验"，P3 是"深度定制"。先装 P0 跑通，再按需叠加。

### 3. 用 SYSTEM.md 控制系统提示

per-project 精细控制 AI 行为，不污染全局配置：

```markdown
<!-- SYSTEM.md -->
你是一个专业的 React 开发者。
使用 TypeScript，遵循 Airbnb 规范。
组件用函数式写法，不用 class。
```

### 4. 用 AGENTS.md 做跨工具规范

通用规范写 AGENTS.md，Claude Code / Codex / Cursor / Trae 都能读：

```markdown
<!-- AGENTS.md -->
## 项目铁律
- 构建命令：pnpm dev
- 测试命令：pnpm test
- Lint 命令：pnpm lint
```

### 5. 会话树管理复杂任务

用 `/tree` 在分支间导航，适合需要探索多种方案的场景：

```
/main-task
├── 方案 A（已放弃）
├── 方案 B（进行中）
│   ├── 子方案 B1
│   └── 子方案 B2 ← 当前位置
└── 方案 C（备用）
```

### 6. 利用 5 阶段 Loop 的缓存优势

pi 的 5 阶段设计让 system prompt 前缀稳定，搭配 DeepSeek 的 prefix cache 可以大幅降低成本。**不要频繁修改 SYSTEM.md**——每次修改都会导致缓存失效。

## 安装

```bash
# npm 安装
npm install -g @earendil-works/pi-coding-agent

# Linux/macOS 脚本安装
curl -fsSL https://pi.dev/install.sh | sh

# 验证
pi --version

# 启动
pi
```

## 参考

- [pi.dev 官网](https://pi.dev)
- [GitHub 仓库](https://github.com/badlogic/pi-mono)（4 万 Star）
- [DeepSeek 官方中文文档](https://github.com/deepseek-ai/awesome-deepseek-agent/blob/main/docs/pi_mono.zh-CN.md)
- [AI Coding 工具全景](./overview)
- [DeepSeek Harness 深度评测](./deepseek-harness)

## 下一步

- 对比 Claude Code → [Claude Code 深度评测](./claude-code)
- 对比 DeepSeek Harness → [DeepSeek Harness 深度评测](./deepseek-harness)
- 团队引入 → [团队 AI 工作流](../workflows/team)

## 如果你想

- 对比主流工具 → [AI Coding 工具全景](./overview)
- 选型决策 → [AI Coding 工具全景](./overview)

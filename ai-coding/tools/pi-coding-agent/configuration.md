---
title: 'Pi 配置文件详解（入门 → 进阶）'
description: 'Pi settings.json 全字段、auth.json 多 provider、trust.json 项目信任、.pi/settings.json 项目级覆盖，按入门到进阶递进'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-22
verifiedWith:
  piVersion: 0.86.1
  sources:
    - name: Pi 设置文档（settings.md）
      url: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md
      accessedAt: 2026-09-22
    - name: Pi Provider 文档（providers.md）
      url: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md
      accessedAt: 2026-09-22
    - name: Pi 包文档（packages.md）
      url: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md
      accessedAt: 2026-09-22
---

# Pi 配置文件详解（入门 → 进阶）

> **TL;DR**：Pi 的配置分两层——**全局**（`~/.pi/agent/settings.json`）和**项目**（`.pi/settings.json`）。项目覆盖全局，嵌套对象**合并而非替换**。5 分钟改 3 个字段就能用，深入后再碰 compaction / retry / cacheWarming。

⏱ 预计阅读时间：12 分钟

## 你能在这里学到

- 全局 vs 项目两个 scope 的优先级与合并规则
- 入门：`theme` / `defaultProvider` / `defaultModel` 三件套
- 进阶：`compaction` / `retry` / `cacheWarming` / `defaultThinkingLevel`
- 进阶：auth.json 多 provider 与 `/login` OAuth 流程
- 进阶：`trust.json` 与项目信任机制
- 进阶：三种资源加载方式（extensions / skills / packages）
- 进阶：环境变量、CLI flag、settings 之间的覆盖顺序

## 前置

- 已安装 Pi：`pi --version` 应输出 ≥ 0.86
- 已至少跑过一次：`pi` 命令能启动
- 熟悉 JSON 基础

## 一、两个 scope

| 位置 | Scope | 谁会用到 | git 提交？ |
|------|-------|---------|-----------|
| `~/.pi/agent/settings.json` | **全局**（所有项目） | 个人偏好、API key、主题 | ❌ gitignore |
| `.pi/settings.json` | **项目**（当前目录） | 团队共享的压缩/重试策略 | ✅ 提交 git |

**合并规则**：

- **标量字段**（字符串、数字、布尔）→ 高优先级**覆盖**低优先级
- **嵌套对象**（`compaction` / `retry`）→ **递归合并**，不是替换

```js
// ~/.pi/agent/settings.json（全局）
{
  "theme": "dark",
  "compaction": { "enabled": true, "reserveTokens": 16384 }
}

// .pi/settings.json（项目）
{
  "compaction": { "reserveTokens": 8192 }
}

// 合并结果（在项目目录下启动 pi 时）
{
  "theme": "dark",
  "compaction": { "enabled": true, "reserveTokens": 8192 }
}
```

`enabled: true` 来自全局（项目没写），`reserveTokens: 8192` 被项目覆盖。

> ⚠️ **数组字段不合并**——`defaultTools` / `enabledModels` / `packages` 项目值**整条替换**全局值。要保留全局某条的话，必须在项目里再写一遍。

---

## 二、入门：5 分钟改 3 个字段

第一次跑通 Pi 后，建议立刻改这三个：

### 1. `theme`

```json
{
  "theme": "light"
}
```

可选值：`"dark"`（默认）、`"light"`、或在 `themes` 字段加载的自定义主题名。

### 2. `defaultProvider` + `defaultModel`

```json
{
  "defaultProvider": "deepseek",
  "defaultModel": "deepseek-chat"
}
```

启动时自动选定的 provider 和模型。也可以在 `/model` 交互界面里按 Ctrl+S 保存。

**怎么看当前可选的 provider/model**：

```bash
pi -p "列出当前可用模型"  # 让 pi 自己打印
# 或直接读 ~/.pi/agent/models-store.json
```

### 3. `defaultThinkingLevel`

```json
{
  "defaultThinkingLevel": "medium"
}
```

可选值：`"off"` / `"minimal"` / `"low"` / `"medium"` / `"high"` / `"xhigh"` / `"max"`。也支持 `/thinking` 交互式设置后 Ctrl+S 保存。

> 💡 **为什么改这三个就够**：Pi 默认已经能用，**先跑起来**比一次配齐更重要。改完这三个，剩下的进阶配置等你真正用到再说。

**写到哪里**：

```bash
# 直接编辑
$EDITOR ~/.pi/agent/settings.json

# 或交互式（推荐新手）
pi
/settings     # 改 theme / defaultProvider / defaultModel
/model        # 选模型 + Ctrl+S 保存
```

---

## 三、`auth.json` 与多 Provider

凭据文件 `~/.pi/agent/auth.json` 控制 Pi 用哪些 provider 调用 LLM。两种方式：

### 方式 A：环境变量（适合临时/容器/CI）

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export DEEPSEEK_API_KEY=sk-...
pi
```

支持的常用环境变量：`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` / `GOOGLE_API_KEY` / `XAI_API_KEY` / `OPENROUTER_API_KEY` / `META_API_KEY` 等。

### 方式 B：`auth.json` 文件（适合本地日常）

**别手写**——用 `/login` 交互式填：

```bash
pi
/login          # 弹出菜单，选 provider
                #   - API key：直接粘贴
                #   - 订阅：走 OAuth 浏览器流程
```

支持的 OAuth 订阅：ChatGPT Plus/Pro、Claude Pro/Max、GitHub Copilot、xAI Grok、Meta Muse、OpenRouter、Radius。

OAuth token 自动刷新；OpenRouter 是用户级 API key，不过期。

**优先级**（高 → 低）：

1. **OAuth token**（`auth.json` 里订阅项）
2. **API key**（`auth.json` 里的 `provider` 项）
3. **环境变量**（`$PROVIDER_API_KEY`）
4. **报错**

> 💡 **安全提示**：`auth.json` 在 `~/.pi/agent/` 下，默认权限 600。**别把 `auth.json` 提交到 git**——它含明文 key。`~/.pi/` 整目录建议加入全局 `~/.gitignore`。

---

## 四、进阶：`compaction` 上下文压缩

长会话会撞上下文窗口上限。`compaction` 控制 Pi 自动总结历史消息的策略：

```json
{
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  }
}
```

| 字段 | 默认 | 含义 |
|------|------|------|
| `enabled` | `true` | 启用自动压缩 |
| `reserveTokens` | `16384` | 给 LLM 响应预留的 token |
| `keepRecentTokens` | `20000` | 保留不被压缩的最近 token |

**按模型微调**：

```json
{
  "compaction": {
    "modelOverrides": {
      "anthropic/claude-opus-4-8": { "reserveTokens": 400000 },
      "local/small-model":         { "reserveTokens": 2048, "keepRecentTokens": 4096 }
    }
  }
}
```

key 用 `"provider/modelId"`，大小写敏感、glob 不匹配。

**经验法则**：

- 大模型（Opus / Sonnet 5）→ `reserveTokens` 调大（400k+），给模型足够的"思考+输出"空间
- 小模型（Haiku / 本地 7B）→ 调小，避免提前压缩
- `keepRecentTokens: 0` 接受，但 `reserveTokens: 0` 会让响应没有余量

---

## 五、进阶：`retry` 重试与超时

```json
{
  "retry": {
    "enabled": true,
    "maxRetries": 3,
    "baseDelayMs": 2000,
    "maxAgentDelayMs": 60000,
    "provider": {
      "timeoutMs": 3600000,
      "maxRetries": 0,
      "maxRetryDelayMs": 60000
    }
  }
}
```

分两层：

| 层 | 字段 | 含义 |
|----|------|------|
| **Agent 层** | `maxRetries` / `baseDelayMs` / `maxAgentDelayMs` | Pi 自己重试（指数退避 2s→4s→8s…） |
| **Provider 层** | `timeoutMs` / `maxRetries` / `maxRetryDelayMs` | SDK 转发给 LLM 厂商的重试 |

**经验法则**：

- Agent 层重试是兜底，**保持默认**（3 次 + 60s 上限）即可
- Provider 层 `maxRetries` **保持 0**——除非你明确知道为什么需要
  - 设大了，SDK 重试可能让 Pi 在 quota 用尽时**阻塞**到下个账单周期
- `timeoutMs` 按最长任务设（默认 1 小时）：复杂重构时单次工具调用可能跑很久

---

## 六、进阶：`cacheWarming` 缓存预热

LLM provider 的 prompt cache 会**在闲置一段时间后失效**，下次请求重新付全价。`cacheWarming` 让 Pi 在 cache 到期前主动发一个最小请求续命：

```json
{
  "cacheWarming": "idle"
}
```

| 模式 | 行为 | 适合场景 |
|------|------|---------|
| `"off"` | 不预热 | 调试 / 隐私敏感环境 |
| `"streaming"`（默认） | 长工具执行期间保护前缀，agent 稳定后停止 | 大多数工作 |
| `"idle"` | 在等用户输入的空闲期也尝试预热（15% 续命概率） | 等人类回话时间长的场景 |

**Pi 自动决策条件**：

- 续命预期节省 ≥ $0.05 才发
- Active agent run 用 100% 续命概率
- 闲置 30 分钟 / active 60 分钟后停止
- 不在 budget-based thinking 的 Claude 模型上启用（key 冲突）
- 在 `models.json` 用 `promptCache` 字段声明自定义模型的缓存 TTL

**查看决策**：在 `/session` 里看下一时刻的续命概率与预期节省。

> 💡 **什么时候关掉**：如果你用 OpenAI o1/o3 这种 reasoning model，或者本地推理没有 prompt cache——关了省事。

---

## 七、进阶：模型与思考

```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-opus-4-8",
  "defaultThinkingLevel": "high",
  "modelThinkingLevels": {
    "anthropic/claude-opus-4-8": "max",
    "anthropic/claude-haiku-4-5": "low"
  },
  "hideThinkingBlock": false,
  "showCacheMissNotices": false,
  "thinkingBudgets": {
    "minimal": 1024,
    "low": 4096,
    "medium": 10240,
    "high": 32768
  },
  "enabledModels": ["claude-*", "gpt-4o", "gemini-2*"]
}
```

| 字段 | 用途 |
|------|------|
| `defaultThinkingLevel` | 启动时默认思考等级 |
| `modelThinkingLevels` | **按模型** 单独设置启动思考等级（覆盖全局） |
| `thinkingBudgets` | 自定义每个等级的 token 预算（Anthropic / Google / Bedrock 原生支持） |
| `enabledModels` | Ctrl+P 循环切换的模型白名单（glob） |
| `hideThinkingBlock` | 隐藏 thinking 块（调试时关） |
| `showCacheMissNotices` | 显示缓存未命中提示（成本排查时开） |

**为何要按模型设置思考等级**：

- Opus 4.8 配 `max` 思考 = 最强但最贵
- Haiku 4.5 配 `low` 思考 = 速度优先
- 切换模型时自动套用合适等级，省得手改

---

## 八、进阶：`trust.json` 与项目级配置

### 项目信任机制

Pi 启动时如果检测到当前目录有 `.pi/settings.json`、`.pi` 资源或项目级 `.agents/skills`，**会问你要不要信任**：

```
Project /Users/you/jd-projects/scm-gyl contains project-local settings.
Trust this project? [y/N]
```

信任后：

- 项目 `.pi/settings.json` 被加载
- 项目 `.pi` 资源被加载
- 缺失的项目 packages 自动安装
- 项目扩展被执行

**信任决策保存在** `~/.pi/agent/trust.json`：

```json
{
  "/Users/liuhui15/jd-projects/open-projects": true,
  "/Users/liuhui15/jd-projects/sz-fe": true
}
```

**交互模式**用 `/trust` 命令管理；**非交互模式**（`-p` / `--mode json` / `--mode rpc`）不弹提示，默认走 `defaultProjectTrust`：

| `defaultProjectTrust` | 行为 |
|----------------------|------|
| `"ask"`（默认） | 非交互模式直接忽略项目资源 |
| `"always"` | 非交互模式直接信任 |
| `"never"` | 非交互模式永远忽略 |

**单次覆盖**：

```bash
pi --approve          # 本次会话信任项目设置
pi --no-approve       # 本次会话忽略项目设置
pi config --approve   # pi config 命令一次信任
```

### 安全模型

> ⚠️ **信任项目 = 信任它能执行任意代码**。Pi 的 extensions、packages 都在你的系统权限下跑。**不熟的仓库先看 `.pi/` 里有什么**。

### 项目 `.pi/settings.json` 推荐放什么

| 放 | 不放 |
|----|------|
| 团队统一的 `compaction` / `retry` 策略 | API key（`auth.json` 是用户级） |
| 推荐的 `defaultProvider` / `defaultModel` | 个人主题偏好 |
| 项目级 `packages`（团队共享的扩展） | OAuth token |
| 项目级 `extensions` / `skills` / `prompts` | `auth.json` 里的任何东西 |

---

## 九、进阶：三种资源加载方式

Pi 把"如何加载扩展、技能、提示模板、主题"做成**三种独立机制**：

| 机制 | 加载对象 | 来源 | 配置文件字段 |
|------|---------|------|------------|
| **extensions** | TypeScript 扩展 | 本地文件/目录 | `~/.pi/agent/settings.json` 的 `extensions` |
| **skills** | Skill 目录 | 本地文件/目录 | `skills` |
| **packages** | npm/git 包 | 远程或本地路径 | `packages` |

### 1. `extensions`（本地扩展）

```json
{
  "extensions": ["./.pi/extensions/git-ai.ts"]
}
```

- 路径相对 `~/.pi/agent/`
- 支持 glob：`["./extensions/*.ts", "!./extensions/_draft.ts"]`
- `+path` 强制包含，`-path` 强制排除

### 2. `skills`（本地技能）

```json
{
  "skills": ["./skills/"],
  "enableSkillCommands": true
}
```

- `enableSkillCommands: true` 让 skill 可通过 `/skill:name` 调用

### 3. `packages`（npm/git 包）

```json
{
  "packages": [
    "pi-skills",
    "@org/my-extension",
    {
      "source": "pi-skills",
      "skills": ["brave-search", "transcribe"],
      "extensions": []
    }
  ]
}
```

- 字符串形式加载包内所有资源
- 对象形式可**过滤只加载部分资源**
- 用 `pi install npm:foo/bar@1.0.0` / `pi install git:github.com/u/r@v1` 安装
- `pi -l` 写到项目级 `.pi/settings.json`，未列的 packages 启动时自动安装

**真实示例**（你的 `settings.json`）：

```json
{
  "packages": [
    "npm:pi-web-access",
    "npm:pi-subagents",
    "npm:pi-deepseek-cache",
    "npm:context-mode"
  ]
}
```

> 💡 **三种怎么选**：
> - 团队共享 → `packages`（提交 `pi install` 命令到 README）
> - 个人长期用的 → `packages` 或 `extensions`
> - 一次性实验 → `pi -e npm:foo/bar`（临时目录，本 run 有效）

---

## 十、配置优先级（最终）

从高到低，**任何一项都能覆盖下一项**：

1. **CLI flag**（`pi --model xxx --thinking high`）—— 单次启动
2. **环境变量**（`PI_CACHE_RETENTION=long` 等）—— 单次进程
3. **`.pi/settings.json`**（项目级）—— 当前目录生效
4. **`~/.pi/agent/settings.json`**（全局）—— 所有项目
5. **Pi 内置默认值**

**常见环境变量**：

| 变量 | 作用 |
|------|------|
| `PI_CACHE_RETENTION=long` | 用 Anthropic 1h 缓存档 |
| `PI_SKIP_VERSION_CHECK=1` | 跳过版本更新检查 |
| `PI_OFFLINE=1` | 启动时完全断网 |
| `PI_EXPERIMENTAL=1` | 启用实验性功能 |
| `HTTP_PROXY` / `HTTPS_PROXY` | 代理（也可在 `httpProxy` 字段配） |

> ⚠️ **数组字段不合并**：项目级 `packages` 数组**整条替换**全局的，不是合并。要保留全局某条必须显式重写。

---

## 十一、常见坑

**坑 1：改了 settings.json 但没生效**

`settings.json` 是热更新的，但 `model` / `outputStyle` / `theme` 三类只在 session 启动时读。要么 `/model` 重选，要么重启 pi。

**坑 2：项目级 packages 启动了但我以为没装**

Pi 启动时会自动 `npm install` 项目级 `.pi/settings.json` 里声明的缺失 packages。看 `~/.pi/agent/npm/` 目录有没有新东西。

**坑 3：trust.json 加了目录但还是问**

`trust.json` key 是**目录绝对路径**，不是项目内的子路径。加 `/Users/you/jd-projects/scm-gyl`，不是 `/Users/you/jd-projects/scm-gyl/src`。

**坑 4：cache warming 一直在跑**

正常——Active agent run 用 100% 续命概率，长任务看起来"不停"。可以在 `/session` 里看预期节省与下次决策时间。

**坑 5：OAuth 订阅断网后登录失败**

远程 SSH 跑 `pi` + `/login openrouter` 时浏览器回调到 localhost 失败。**手动粘贴回调 URL 或 authorization code** 进提示框即可。

**坑 6：CI / Docker 里反复问信任**

设环境变量 `defaultProjectTrust: "always"`，或者 `pi --approve`，或者提前在 `trust.json` 里把容器工作目录加进去。

**坑 7：`compaction.modelOverrides` key 写错**

key 必须严格匹配 `"provider/modelId"`，**不支持 glob**。比如 `openrouter/anthropic/claude-sonnet-4` 整个串当 key，不是 `anthropic/*`。

**坑 8：`.pi/settings.json` 用 Windows 路径**

Windows 路径必须用正斜杠或转义反斜杠：

```json
{
  "shellPath": "C:/Program Files/Git/bin/bash.exe"
}
```

---

## 速查卡片

```json
{
  "$schema": "see https://github.com/earendil-works/pi/blob/main/docs/settings.md",

  // === 入门三件套 ===
  "theme": "dark",
  "defaultProvider": "deepseek",
  "defaultModel": "deepseek-chat",
  "defaultThinkingLevel": "medium",

  // === 上下文 ===
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  },

  // === 重试 / 超时 ===
  "retry": {
    "maxRetries": 3,
    "baseDelayMs": 2000,
    "provider": { "timeoutMs": 3600000, "maxRetries": 0 }
  },

  // === 缓存预热 ===
  "cacheWarming": "streaming",

  // === 资源加载 ===
  "packages": ["npm:pi-subagents", "npm:context-mode"],
  "extensions": [],
  "skills": [],

  // === 安全 ===
  "defaultProjectTrust": "ask"
}
```

---

## 参考

- [Pi 设置文档（settings.md）](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md) — 全字段权威参考
- [Pi Provider 文档（providers.md）](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md) — auth 与 OAuth 订阅
- [Pi 包文档（packages.md）](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md) — 包管理
- [PI-agent 深度评测](../pi-agent) — 架构视角

## 下一步

- 想理解 Pi 的架构与缓存优化 → [PI-agent 深度评测](../pi-agent)
- 想写 Pi 的 Skill → [Pi Coding Agent 总览](./)「章节地图」
- 想深入资源加载机制（扩展 / Skills / 包） → [Pi 进阶资源加载（扩展 / Skills / 包）](./resources)
- 想给团队配 Pi 流水线 → [团队 AI 工作流](/ai-harness/workflows/team)

## 如果你想

- 把 Pi 配置成 Claude Code 等价物 → 字段对照待补充（[PI-agent 深度评测](../pi-agent) 里有 AGENTS.md / CLAUDE.md 双轨部分）
- 排查诡异行为 → 翻回「十一、常见坑」
- 了解 Pi 与其他工具的取舍 → [AI 工具全景](../overview)

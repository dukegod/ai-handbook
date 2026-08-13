---
title: 术语表
description: Claude Handbook 中英双语术语锁定表；每篇文档的术语必须与本表对齐
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-23
---

# 术语表

> 中英双语锁定表。写作时若遇到本表未收录的术语，先补录到这里，再写正文。

## 阅读方式

- **首选写法**：正文里推荐的固定表达
- **中文括注**：仅在术语首次出现时使用，用于向新读者建立映射；后续文中直接用英文
- **禁止**：多种译法混用（比如「技能 / Skill」在同一篇里同时出现）

## Claude 与 Anthropic 家族

| 首选写法 | 说明 | 边界 |
| --- | --- | --- |
| **Anthropic** | Claude 系列模型与 Claude Code 的出品公司 | 不用「Claude 公司」 |
| **Claude** | 模型本身；家族含 Opus / Sonnet / Haiku / Fable | 不指公司也不指工具 |
| **Claude Code** | Anthropic 出品的命令行工具（CLI） | 首次出现建议加括注：`Claude Code（Anthropic 官方 CLI）` |
| **Claude.ai** | 网页/桌面/移动端聊天产品 | 与 Claude Code 是不同产品 |
| **Claude Agent SDK** | 用于构建自定义 Agent 的 SDK | 不同于 Anthropic SDK（HTTP 客户端） |
| **Claude Code SDK** | 从代码中程序化调用 Claude Code 的 SDK | 与 Claude Agent SDK 不同 |
| **Opus 4.8** | 最强推理模型；ID `claude-opus-4-8` | 别写 `Opus4.8`、`opus-4-8` |
| **Sonnet 5** | 平衡型；ID `claude-sonnet-5` | |
| **Haiku 4.5** | 快速轻量；ID `claude-haiku-4-5-20251001` | |
| **Fable 5** | ID `claude-fable-5`；专精长时运行 agent | 详见 [路线图](/contributing/roadmap) 风险项 |

## Claude Code 核心概念

| 首选写法 | 一句话定义 | 相关章节 |
| --- | --- | --- |
| **Session（会话）** | 一次 Claude Code 交互过程，含完整上下文与工具调用历史 | [/claude-code/basics/sessions](/claude-code/basics/sessions) |
| **Context（上下文）** | Claude 单次调用能看见的 token 总量；含系统提示、历史、工具结果 | [/claude-code/basics/context-window](/claude-code/basics/context-window) |
| **CLAUDE.md** | 项目/用户/企业级的持久化上下文文件，Claude Code 每次自动加载 | [/claude-code/basics/claude-md](/claude-code/basics/claude-md) |
| **Permission（权限）** | Claude Code 对工具调用的准入策略；分 `allow / deny / ask` | [/claude-code/basics/permissions](/claude-code/basics/permissions) |
| **Plan Mode** | 只读探索 + 计划审批模式；退出时才开始写文件 | [/claude-code/basics/plan-mode](/claude-code/basics/plan-mode) |
| **Tool（工具）** | Claude 可调用的能力单元（Read、Write、Bash、Grep …） | [/claude-code/tools/overview](/claude-code/tools/overview) |
| **Slash Command** | 用户输入 `/xxx` 触发的自定义快捷指令 | [/claude-code/customization/slash-commands](/claude-code/customization/slash-commands) |
| **Skill（技能）** | 声明式扩展；含 SKILL.md 与触发描述，Claude 根据 description 自动选用 | [/claude-code/skills/what-is-a-skill](/claude-code/skills/what-is-a-skill) |
| **Hook** | 在特定生命周期事件（工具前/后/停止/提交）自动执行的脚本 | [/claude-code/customization/hooks](/claude-code/customization/hooks) |
| **Subagent（子代理）** | 通过 Task 工具派生的独立 Agent；有自己的上下文与工具集 | [/claude-code/subagents-and-workflows/what-is-a-subagent](/claude-code/subagents-and-workflows/what-is-a-subagent) |
| **Workflow** | 用 JavaScript 编排多个 Subagent 的确定性脚本 | [/claude-code/subagents-and-workflows/workflow-orchestration](/claude-code/subagents-and-workflows/workflow-orchestration) |
| **Worktree** | Git 的多工作树能力；Claude Code 用它实现隔离改动 | [/claude-code/advanced/worktree](/claude-code/advanced/worktree) |
| **Memory（记忆）** | Claude Code 的持久化事实文件；不同于 CLAUDE.md，更细粒度 | [/claude-code/advanced/memory](/claude-code/advanced/memory) |
| **Headless / 非交互模式** | 用 `claude -p` 一次性输入输出，不进入 REPL | [/claude-code/advanced/headless](/claude-code/advanced/headless) |

## MCP 生态

| 首选写法 | 一句话定义 |
| --- | --- |
| **MCP（Model Context Protocol）** | 让 LLM 与外部工具/数据源通信的开放协议 |
| **MCP Server** | 提供工具/资源的服务端进程；可用 stdio / SSE / HTTP 传输 |
| **MCP Client** | 消费 MCP Server 的一方；Claude Code 内置 client |
| **MCP Transport** | 协议底层通道：stdio（本地进程）/ SSE（长连）/ HTTP（无状态） |
| **.mcp.json** | 项目级 MCP 配置文件 |

## API 与 SDK

| 首选写法 | 一句话定义 |
| --- | --- |
| **Messages API** | Anthropic HTTP API 的主入口，对话式请求 |
| **Tool Use** | Messages API 里让 Claude 调用外部工具的机制 |
| **Structured Outputs** | 强制 Claude 返回符合 schema 的 JSON |
| **Prompt Caching** | 对超长系统提示按 5min / 1h 缓存，最高节省 90% 输入成本 |
| **Message Batches** | 异步批量提交请求；50% 折扣，24h 窗口 |
| **Extended Thinking** | 让模型显式思考（消耗 thinking token） |
| **Vision** | 图片理解能力；直接传入 base64 或 URL |
| **Computer Use** | 让 Claude 通过 display/bash/text editor 工具操控计算机 |
| **Token Counting API** | 预估请求 token 消耗的独立端点 |
| **Files API** | 上传文件在多次请求间复用的能力 |
| **Batch API 折扣** | 提交后 24h 内异步取回，输入输出各 50% off |

## 提示工程

| 首选写法 | 一句话定义 |
| --- | --- |
| **System Prompt** | 请求头部的系统级指令；定义角色、目标、约束 |
| **Chain of Thought（CoT）** | 引导模型逐步推理的提示模式 |
| **Few-shot** | 通过示例演示期望格式 |
| **Prefill** | 预填 assistant 回复开头，锁定输出格式 |
| **XML Tags** | 用 `<example>` `<context>` 等标签结构化提示 |
| **Prompt Injection** | 通过外部数据篡改模型行为的攻击手法 |

## 常见易错

- ❌ `Claude 公司` → ✅ `Anthropic`
- ❌ `ClaudeCode` → ✅ `Claude Code`（中间有空格）
- ❌ `MCP 服务器` → ✅ `MCP Server`
- ❌ `技能` → ✅ `Skill` （若面向新手可加括注 `Skill（技能）`）
- ❌ `cluade` → ✅ `claude`
- ❌ `Opus4.8` → ✅ `Opus 4.8`
- ❌ 中英不加空格：`使用ClaudeCode完成` → ✅ `使用 Claude Code 完成`

## 参考

- [Anthropic 官方文档 · Model overview](https://docs.claude.com/en/docs/about-claude/models/overview)（访问于 2026-07-23）
- [Anthropic 官方术语](https://docs.claude.com/)（访问于 2026-07-23）

## 下一步

- 回到 [写作规范](/contributing/style-guide)
- 查看 [路线图](/contributing/roadmap) 了解各章节推进状态

## 如果你想

- 系统学习模型选型 → [模型选择](/claude-code/basics/model-selection)
- 理清 Skill vs Command vs Agent → [Skill vs Command vs Agent](/claude-code/skills/skills-vs-commands-vs-agents)

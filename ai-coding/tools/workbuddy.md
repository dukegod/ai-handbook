---
title: 腾讯 WorkBuddy 深度评测
description: 腾讯 WorkBuddy——带 Coding Mode 的桌面 AI 智能体(不是 IDE),与 ChatGPT Operator/Manus 同台
audience: intermediate
difficulty: 🟡
status: draft
lastUpdated: 2026-09-17
verifiedWith:
  sources:
    - name: WorkBuddy 产品概述
      url: https://www.codebuddy.cn/docs/enterprise/
      accessedAt: 2026-09-17
    - name: WorkBuddy 国际版
      url: https://www.workbuddy.ai/docs/workbuddy/Quickstart
      accessedAt: 2026-09-17
---

# 腾讯 WorkBuddy 深度评测

> **TL;DR**:WorkBuddy 不是 Claude Code / Cursor 那种"写代码工具"——它是**桌面 AI 智能体**(macOS / Windows 客户端),主打"一句话让 AI 自己规划并交付完整结果",**编程只是它 7-8 种场景之一**。与 ChatGPT Operator、Manus 同台竞争。

⏱ 预计阅读时间:4 分钟

## 它是什么 / 它不是什么

| 维度 | Claude Code / Cursor | WorkBuddy |
|------|---------------------|-----------|
| 形态 | IDE 插件 / CLI | **桌面 App**(macOS + Windows) |
| 主场景 | 在代码仓库里写代码 | 跨工具自动化(办公 / PPT / 数据 / 设计 / 编程) |
| 输入 | 选中代码 / 终端提示词 | 一句话自然语言任务 |
| 输出 | 代码 diff / 终端运行 | **完整可验收产物**(文档 / PPT / 网页 / 代码) |
| 起价 | Claude $20/月、Cursor $20/月 | Free / Pro $20/月 / Team $40/seat/月 |

**一句话区别**:Claude Code 帮你"写代码行";WorkBuddy 帮你"完成一件事",代码只是其中一种产物。

## 三场景(Coding Mode 只是其中之一)

### 1. Work Mode(默认,办公)

文档生成 / 数据分析 / PPT 报告 / 深度研究 / 邮件周报 / 批量文件处理。**它最强的地方不是编程,而是这些**。

### 2. Coding Mode(编程子集)

写代码 / 代码审查 / Bug 修复 / 重构 / 工程理解。**能用,但深度不如 Claude Code / Cursor**——没有 IDE 实时补全、没有 LSP、没有 subagent 编排。

### 3. Design Mode(设计)

原型设计 / 海报 / 品牌素材 / 交互稿生成。

> 编程时间预算:<25% —— 如果你 90% 时间在写代码,WorkBuddy 不是一个好选择。

## 关键差异化:Skills 与 Experts

- **Skills 市场**:SkillHub 全球 10.4 万+ Skills、5000 万+ 下载。装一个 Skill 等于给 Agent 加一条新能力
- **Experts**:把多个 Skills 组合成"虚拟团队成员"(运营专家 / 设计专家 / 数据专家),WorkBuddy 能**多 Expert 并行协作**
- **Connectors**:原生打通 GitHub / Notion / Jira / Slack / Telegram / 企业微信
- **自动化(Automation)**:周期任务,定时执行

## 适用场景

- **跨工具一键自动化**:"把这周的 Jira 报表做成 PPT 发到企微"(Jira + PPT + 企微 三件事一次完成)
- **本地文件批量处理**:重命名 / 转换格式 / 整理资料(可直接读写本地授权文件夹)
- **桌面级 Copilot**:不离开桌面,在 IM / Office / 浏览器里随时调用
- **团队级 AI 治理**:Admin Console / 共享 Credit 池 / 用量看板 / SSO / RBAC
- **手机远控**:在外用 IM(Slack / Telegram)下发任务,公司电脑 WorkBuddy 执行

## 不适用场景

- 主力写代码、需要 IDE 深度集成 → 用 Claude Code / Cursor / CodeBuddy
- 只要 CLI 体验 → 用 Claude Code / Codex CLI / CodeBuddy Code
- Linux 桌面用户 → **WorkBuddy 没有 Linux 版**(只有 macOS / Windows)
- 注重编程 Agent 能力(MCP / Subagent / Skills) → 用 Claude Code,WorkBuddy 的 Skills 偏办公

## 五种部署版本

| 版本 | 区域 / 部署 |
|------|------------|
| 海外版 | `codebuddy.ai`,`CODEBUDDY_INTERNET_ENVIRONMENT` 默认 |
| 国内版 | `copilot.tencent.com`,设置 `=internal` |
| iOA 版 | 腾讯 iOA 安全运营,`=ioa` |
| 专享版 | 企业专享 VPC,`=cloudhosted` |
| 私有化 | 客户机房,`=selfhosted` |

价格(海外):Free / Pro $20/月 / Team $40/seat/月。  
价格(国内):WorkBuddy Enterprise ¥198/人/月(含 CodeBuddy 套件)。

## 选型对比

| 需求 | 推荐 |
|------|------|
| 主力 IDE 写代码 | Claude Code / Cursor |
| CLI + 推理最强 | Codex CLI |
| 中文 + 国产化编程工具 | CodeBuddy |
| **跨工具一键自动化** | **WorkBuddy** |
| 桌面 App + Skills 生态 + 团队管理 | **WorkBuddy** |
| OpenAI Agent 同台替代品 | **WorkBuddy / Manus / Operator** |

## 参考

- [腾讯云 WorkBuddy 产品概述](https://www.codebuddy.cn/docs/enterprise/)(访问于 2026-09-17)
- [WorkBuddy 国际版文档](https://www.workbuddy.ai/docs/workbuddy/Quickstart)(访问于 2026-09-17)
- [AI 工具全景](./overview)

## 下一步

- 对比同门编程版 → [腾讯 CodeBuddy 深度评测](./codebuddy)
- 团队引入 → [团队 AI 工作流](/ai-harness/workflows/team)

## 如果你想

- 对比主流 AI 工具 → [工具全景](./overview)
- 看落地模式 → [AI Harness 工程](/ai-harness/)

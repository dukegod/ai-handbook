---
title: Web 应用
description: claude.ai 浏览器版——跨平台 + 移动适配 + 5 模式 + 4 坑
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  webApp: 'https://claude.ai'
  accessedAt: 2026-08-07
---

# Web 应用

> **TL;DR**：claude.ai 的浏览器版（[claude.ai](https://claude.ai)）——**无需安装、跨平台**（macOS / Windows / Linux / 移动浏览器）。**适合临时使用 / 公共电脑**。与 [桌面应用](/claude-capabilities/surfaces/desktop-app) 功能几乎一致——区别在"是否装客户端"。

⏱ 预计阅读时间：3 分钟

## 一、3 类入口

| 入口 | 平台 | 特点 |
| --- | --- | --- |
| **桌面浏览器** | Chrome / Safari / Firefox / Edge | 全功能 |
| **移动浏览器** | iOS Safari / Android Chrome | 触屏优化 |
| **PWA** | 任意浏览器 | "加到主屏幕" 离线访问 |

## 二、5 个核心能力

### 1. Chat（与桌面端一致）

详见 [Claude.ai · 5 模式](/claude-capabilities/surfaces/claude-ai#二5-个实战模式)。

### 2. Project + Knowledge base

跨对话保留 system + 知识库——Web 端完整支持。

### 3. Artifacts

独立窗口渲染代码 / SVG / Markdown——Web 端**最完整**（桌面 / 移动端稍弱）。

### 4. File Upload

```text
拖 PDF / 图片 / 代码到 claude.ai
→ 上传到 Anthropic 服务端
→ 作为 input
```

**注意**：Web 端上传的文件**30 天后自动删除**（同 [Files API 限制](/claude-capabilities/api/files)）。

### 5. 移动适配

```text
手机浏览器打开 claude.ai
→ 触屏优化界面
→ 支持语音输入（部分浏览器）
```

## 三、与桌面端对比

| 维度 | Web 端 | 桌面端 |
| --- | --- | --- |
| 安装 | 0 | 装客户端 |
| 跨平台 | ✅ | 单平台（按系统装） |
| 离线 | ❌（PWA 部分支持） | ❌ |
| 全局快捷键 | ❌ | ✅ |
| 性能 | 看网络 | 本地加载快 |
| 公共电脑 | ✅（用完即清） | 需手动登出 |
| Artifacts | ✅ 完整 | ✅ |

**何时用 Web 端**：
- 临时用（公共电脑 / 朋友电脑）
- 不想装客户端
- 跨平台（macOS / Win 切着用）

**何时用桌面端**：
- 全局快捷键是核心需求
- 高频使用

## 四、4 个常见坑

**1. 公共电脑忘登出**

```text
# 用完一定要登出
# 或直接关浏览器
```

**2. 移动端误操作**

```text
# 触屏容易误点
# 重要操作（删除 project）→ 用 desktop 端
```

**3. 浏览器缓存敏感对话**

```text
# 公司电脑 / 公共电脑
# → 用 private / incognito 模式
```

**4. 网络不稳时流式输出断**

```text
# 长对话流式断网 → 内容丢失
# → 用桌面端（重试更稳）
```

## 参考

- [claude.ai](https://claude.ai)
- [Claude.ai](/claude-capabilities/surfaces/claude-ai)
- [Artifacts](/claude-capabilities/surfaces/artifacts)
- [桌面应用](/claude-capabilities/surfaces/desktop-app)
- [Files API](/claude-capabilities/api/files)

## 下一步

- 移动端 → [Mobile](/claude-capabilities/surfaces/mobile)
- Slack 集成 → [Claude in Slack](/claude-capabilities/surfaces/claude-in-slack)
- 切到 API → [Messages API](/claude-capabilities/api/messages)

## 如果你想

- 团队 Workspace → [Claude.ai · 模式 4](/claude-capabilities/surfaces/claude-ai#模式-4团队协作)
- 安全 / 隐私 → [安全](/claude-capabilities/agentic/safety)

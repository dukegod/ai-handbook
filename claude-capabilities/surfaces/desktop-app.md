---
title: 桌面应用
description: Claude 桌面客户端——macOS / Windows / Linux 5 模式 + 与 Claude Code 对照
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  desktop: 'https://claude.ai/download'
  accessedAt: 2026-08-07
---

# 桌面应用

> **TL;DR**：Claude 桌面客户端（macOS / Windows / Linux）——**GUI 形态的 Claude**，带全局快捷键、跨应用菜单栏、桌面通知。**与 Claude Code（CLI）是平行产品**——终端派 vs GUI 派，**功能重叠但使用习惯不同**。

⏱ 预计阅读时间：3 分钟

## 一、3 平台支持

| 平台 | 包格式 | 状态 |
| --- | --- | --- |
| **macOS** | .dmg（Apple Silicon / Intel） | GA |
| **Windows** | .exe | GA |
| **Linux** | .deb / .AppImage | GA |

下载：[claude.ai/download](https://claude.ai/download)

## 二、5 个核心能力

### 1. 全局快捷键

```text
⌘ + Shift + Space（macOS）
Ctrl + Shift + Space（Win/Linux）
```

→ 任何应用里弹 Claude 浮窗提问。

### 2. 跨应用菜单栏

```text
macOS 菜单栏图标 → 选中文本 → 调 Claude
"总结这段"
"翻译成英文"
"找 bug"
```

### 3. 桌面通知

任务完成 / 长时间推理结束 → 系统通知。

### 4. 文件拖拽

```text
拖 PDF / 图片 / 代码文件到 Claude 窗口
→ 自动作为 input
```

### 5. 跨设备同步

对话历史 / project / knowledge base 跨 Mac / Win / Web 同步（账号登录）。

## 三、与 Claude Code 对照

| 维度 | 桌面应用 | Claude Code |
| --- | --- | --- |
| 入口 | GUI | 终端 |
| 改文件 | ❌ | ✅ |
| 跑命令 | ❌ | ✅ |
| 适合 | 临时 / 探索 / 跨应用 | 项目级编码 |
| 自动化 | ❌ | ✅（CI 集成） |
| 速度感知 | GUI 加载慢 | 终端快 |

**何时用哪个**：
- **桌面应用**：跨应用问答（聊天时翻译 / 总结）
- **Claude Code**：项目级编码、CI 自动化

## 四、4 个常见坑

**1. 期望"桌面应用能改文件"**

桌面应用**不能**直接改项目文件——它只是 GUI 包装。要改文件用 Claude Code。

**2. 通知轰炸**

长任务多 → 通知多。**设置里关非关键通知**。

**3. 跨平台同步冲突**

Mac / Win 同时改同一个 project → 冲突。**单设备活跃**。

**4. 全局快捷键被占用**

```text
⌘ + Shift + Space 跟其他 app 撞
→ 设置里改
```

## 参考

- [claude.ai/download](https://claude.ai/download)
- [Claude.ai](/claude-capabilities/surfaces/claude-ai)
- [Claude Code 入门](/getting-started/what-is-claude-code)

## 下一步

- 浏览器版 → [Web](/claude-capabilities/surfaces/web-app)
- 移动端 → [Mobile](/claude-capabilities/surfaces/mobile)
- 切到 Claude Code → [Claude Code 入门](/getting-started/what-is-claude-code)

## 如果你想

- 跨应用问答 → [Claude.ai · 5 模式](/claude-capabilities/surfaces/claude-ai#二5-个实战模式)
- 自动化 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

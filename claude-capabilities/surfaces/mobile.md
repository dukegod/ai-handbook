---
title: 移动端
description: iOS / Android Claude App——语音输入 / 移动端优化 / 5 模式 + 4 坑
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  ios: 'https://apps.apple.com/us/app/claude/id6443841246'
  android: 'https://play.google.com/store/apps/details?id=com.anthropic.claude'
  accessedAt: 2026-08-07
---

# 移动端

> **TL;DR**：Claude iOS / Android App——**触屏优化 + 语音输入 + 移动场景适配**。**适合通勤 / 临时提问 / 拍照提问**。功能与 Web 端**接近但弱于桌面 / Web**（Artifacts 受限、长对话不友好）。

⏱ 预计阅读时间：3 分钟

## 一、3 平台支持

| 平台 | 商店 | 特点 |
| --- | --- | --- |
| **iOS** | App Store | iPhone + iPad（通用） |
| **Android** | Google Play / 国内安卓市场 | 手机 + 平板 |
| **iPadOS** | 同 iOS App | 触屏 + 键盘优化 |

下载：
- [iOS](https://apps.apple.com/us/app/claude/id6443841246)
- [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)

## 二、5 个核心能力

### 1. 语音输入

```text
按 mic 按钮 → 说话 → 自动转文字
多语言（中 / 英 / 日 / ...）
```

**实战**：通勤时口述复杂问题。

### 2. 拍照提问

```text
拍照（菜单 / 文档 / 公式）→ 上传 → 问问题
```

**实战**：
- 餐厅菜单翻译
- 公式识别 + 解答
- 文档 OCR

### 3. 触屏优化

```text
- 大按钮（戴手套也能用）
- 滑动切换对话
- 触觉反馈
```

### 4. 跨设备同步

```text
Mac / iPhone / iPad / Android 共享：
- 对话历史
- Project + Knowledge base
- Artifacts（部分）
```

### 5. 离线消息查看

```text
飞行模式 / 弱网：
- 历史对话可读
- 新对话需要联网
```

## 三、4 个常见坑

**1. 移动端写长 prompt**

```text
# 手机打字慢
# → 复杂任务用桌面 / Web 端
```

**2. 移动端 Artifacts 受限**

```text
# 复杂 React 组件渲染
# → 用 Web 端
```

**3. 语音输入识别错**

```text
# 中英混合 / 专业术语识别率低
# → 文字 + 语音组合
```

**4. 后台被杀**

```text
# iOS / Android 后台限制
# 长对话别后台太久
```

## 四、与桌面 / Web 对比

| 维度 | 移动端 | 桌面端 | Web 端 |
| --- | --- | --- | --- |
| 安装 | 装 App | 装客户端 | 0 |
| 语音 | ✅ | ❌ | ❌ |
| 拍照 | ✅ | ❌ | ❌ |
| 触屏 | ✅ | ❌ | ❌ |
| 长对话 | 难 | 易 | 易 |
| 离线下查看 | ✅ | ✅ | ❌ |

**何时用移动端**：
- 通勤 / 出差
- 拍照 / 语音
- 临时快速提问

**何时不用**：
- 复杂 prompt
- 长对话
- 项目级编码（用 Claude Code）

## 参考

- [Claude iOS App](https://apps.apple.com/us/app/claude/id6443841246)
- [Claude Android App](https://play.google.com/store/apps/details?id=com.anthropic.claude)
- [Claude.ai](/claude-capabilities/surfaces/claude-ai)
- [桌面应用](/claude-capabilities/surfaces/desktop-app)
- [Web 应用](/claude-capabilities/surfaces/web-app)

## 下一步

- Slack 集成 → [Claude in Slack](/claude-capabilities/surfaces/claude-in-slack)
- 切到桌面 → [Desktop](/claude-capabilities/surfaces/desktop-app)
- 切到 API → [Messages API](/claude-capabilities/api/messages)

## 如果你想

- 团队协作 → [Claude.ai · 模式 4](/claude-capabilities/surfaces/claude-ai#模式-4团队协作)
- Vision 深入 → [Vision 能力](/claude-capabilities/core/vision)

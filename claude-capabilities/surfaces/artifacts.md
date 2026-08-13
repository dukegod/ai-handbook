---
title: Artifacts
description: 独立可分享的输出窗口——React / HTML / SVG / Mermaid / Markdown 4 类内容
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  artifacts: 'https://support.anthropic.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them'
  accessedAt: 2026-08-07
---

# Artifacts

> **TL;DR**：Artifacts 是 **claude.ai 里独立窗口的输出区域**——Claude 写的代码 / 文档 / 图表自动渲染在侧栏，**可下载 / 分享 / 二次编辑**。**4 类内容**：React 组件、HTML 页面、SVG 图表、Markdown 文档。

⏱ 预计阅读时间：3 分钟

## 一、4 类 Artifact

| 类型 | 用途 | 触发 |
| --- | --- | --- |
| **React 组件** | UI 草稿、可交互 demo | 写"做一个 React 组件..." |
| **HTML / CSS / JS** | 单页 demo | 写"做一个 HTML 页面..." |
| **SVG 图表** | 流程图、架构图、插图 | 写"画一个 SVG 示意图..." |
| **Markdown 文档** | 长文报告、README 草稿 | 写"写一份详细报告..." |

**Mermaid** 流程图也支持——Claude 用 ```mermaid 块自动渲染。

## 二、3 个实战模式

### 模式 1：UI 草稿

```text
用户：帮我做一个登录页的 React 组件，用 Tailwind
Claude：<artifact>React 组件</artifact>
       独立窗口渲染，可复制 / 下载
```

### 模式 2：可视化架构图

```text
用户：画一张微服务架构图
Claude：<artifact>SVG 图</artifact>
       实时渲染，可下载 SVG 文件
```

### 模式 3：长文报告

```text
用户：调研 transformer，写 3000 字综述
Claude：<artifact>Markdown 长文</artifact>
       侧栏渲染 + 目录 + 复制
```

## 三、Artifact 关键能力

| 能力 | 说明 |
| --- | --- |
| **实时渲染** | 写完立即看到效果 |
| **可编辑** | 二次修改 prompt 重新生成 |
| **可下载** | 复制 / 下载源文件 |
| **可分享** | 生成链接给团队 |
| **版本** | 同一对话里可对比多个版本 |

## 四、与 API 区别

| 维度 | Artifacts（claude.ai） | API |
| --- | --- | --- |
| 渲染 | 客户端自动 | 客户端自己实现 |
| 适合 | 临时 / 探索 | 生产 |
| 代码执行 | ❌ | ✅（你自己跑） |
| 部署 | ❌（独立窗口） | ✅（嵌入产品） |

## 五、4 个常见坑

**1. 期望"自动应用"代码**

```text
# ❌ 期望 artifacts 直接改文件
# ✅ Claude.ai 不能改文件——只生成代码
```

**2. 跨对话丢失**

artifacts 跟着对话走——对话结束**保留**但**不在新对话里**。

**3. 大输出 token 限制**

单 artifact 太大 → 生成截断。**控制在 5000 token 内**。

**4. SVG 复杂度过高**

```text
# ❌ 1000 个元素的 SVG
# ✅ 让 Claude 分块画
```

## 六、何时用 Artifacts vs API

| 场景 | 用 |
| --- | --- |
| 临时 UI 草稿 | **Artifacts** |
| 给团队分享 demo | **Artifacts** |
| 嵌入到产品 | **API** + 自渲染 |
| 自动化生成 | **API** |

详见 [Claude.ai](/claude-capabilities/surfaces/claude-ai) + [Messages API](/claude-capabilities/api/messages)。

## 参考

- [Anthropic Docs · Artifacts](https://support.anthropic.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them)（访问于 2026-08-07）
- [Claude.ai](/claude-capabilities/surfaces/claude-ai)
- [Messages API](/claude-capabilities/api/messages)

## 下一步

- 桌面应用 → [Desktop](/claude-capabilities/surfaces/desktop-app)
- 网页版 → [Web](/claude-capabilities/surfaces/web-app)
- 移动端 → [Mobile](/claude-capabilities/surfaces/mobile)

## 如果你想

- SVG 制作 → [深度提示工程 · 模板](/claude-capabilities/prompting/templates)
- 切到 API → [Messages API](/claude-capabilities/api/messages)

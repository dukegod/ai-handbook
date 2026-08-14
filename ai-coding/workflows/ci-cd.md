---
title: CI/CD 集成
description: AI 编程工具与 CI/CD 流水线的集成方案
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
---

# CI/CD 集成

> **TL;DR**：Claude Code 的 Headless 模式是 CI/CD 集成的最佳方案——无人值守、可脚本化、可监控。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Claude Code Headless 模式的用法
- GitHub Actions 集成方案
- 常见 CI/CD 场景
- 安全与权限控制

## Headless 模式

Claude Code 支持 Headless 模式——无人值守运行：

```bash
claude -p "审查 src/ 目录的安全问题" --output-format json
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| `-p` | 提示词 |
| `--output-format` | 输出格式（json/text/stream-json） |
| `--allowedTools` | 允许的工具 |
| `--disallowedTools` | 禁止的工具 |

## GitHub Actions 集成

### 自动代码审查

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "审查这个 PR 的代码质量和安全问题" \
            --output-format json \
            --allowedTools "Read,Grep,Glob"
```

### 自动生成文档

```yaml
name: Auto Docs
on:
  push:
    paths:
      - 'src/**'

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate Docs
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "更新 README.md，反映 src/ 目录的最新变化" \
            --allowedTools "Read,Write"
```

## 常见场景

### 1. 自动代码审查

PR 提交时自动审查，发现问题自动评论。

### 2. 自动生成文档

代码变更时自动更新文档。

### 3. 自动生成测试

新函数提交时自动生成测试用例。

### 4. 自动修复 lint

lint 错误时自动修复。

## 安全与权限控制

### 工具限制

```bash
claude -p "..." --allowedTools "Read,Grep,Glob" --disallowedTools "Bash,Write"
```

**只读操作**：Read、Grep、Glob、LSP
**写操作**：Edit、Write、Bash

### 密钥管理

- 使用 GitHub Secrets 存储 API Key
- 不要在代码中硬编码
- 使用最小权限原则

### 沙箱

Claude Code 的沙箱限制了危险操作。CI 环境中建议保持沙箱开启。

## 常见坑

**1. 超时**

CI 环境中 Claude Code 可能超时。设置合理的 timeout。

**2. 成本**

CI 中频繁调用 API 可能成本高。限制触发条件。

**3. 权限**

确保 CI 环境有足够权限（读写文件、执行命令）。

## 参考

- [Claude Code Headless 模式](/claude-code/advanced/headless)
- [Claude Code 官方文档](https://code.claude.com/docs)

## 下一步

- Code Review 自动化 → [Code Review 自动化](./code-review)
- 企业部署 → [企业部署指南](../enterprise/deployment)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 安全合规 → [安全与合规](../enterprise/security)

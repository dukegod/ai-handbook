---
title: 开源项目推荐
description: AI 开源项目筛选标准与分类推荐——推理引擎、应用框架、Agent 编排、RAG
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: vLLM
      url: https://github.com/vllm-project/vllm
      accessedAt: 2026-08-14
    - name: Ollama
      url: https://github.com/ollama/ollama
      accessedAt: 2026-08-14
    - name: Dify
      url: https://github.com/langgenius/dify
      accessedAt: 2026-08-14
---

# 开源项目推荐

> **TL;DR**：推荐标准不是「star 多」，是「工程可用 + 社区活跃 + 有明确边界」。本文给评估框架与分场景清单。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 评估开源项目健康的 5 个维度
- 按场景分类的成熟项目清单
- 避免「demo 陷阱」的检查清单

## 一、评估框架（5 个维度）

| 维度 | 看什么 | 红牌 |
| --- | --- | --- |
| 工程可用 | 文档、CLI、API 是否完整 | 只有 README 和演示视频 |
| 社区活跃 | commit 频率、issue 响应 | 三个月无 commit |
| 部署成本 | 依赖复杂度、硬件要求 | 需要 8 卡 A100 起步 |
| 许可协议 | 是否可商用 | 有传染性限制 |
| 演进方向 | roadmap 与你的需求是否一致 | 频繁破坏性变更 |

## 二、分类推荐（截至 2026-08）

**推理与部署**：

| 项目 | 定位 | 何时选它 |
| --- | --- | --- |
| vLLM | 高吞吐推理引擎 | 生产环境自建推理 |
| Ollama | 本机一键跑模型 | 本地开发 / 体验 |
| llama.cpp | 极致轻量（CPU 可跑） | 边缘设备 / 无 GPU |

**应用框架**：

| 项目 | 定位 | 何时选它 |
| --- | --- | --- |
| LangChain / LangGraph | 编排框架 + Agent 图 | 复杂多步 Agent |
| Dify | LLM 应用平台（含 UI） | 快速搭应用 / 非深度定制 |

**RAG 与知识库**：

| 项目 | 定位 | 何时选它 |
| --- | --- | --- |
| RAGFlow | 文档级 RAG | 企业知识库问答 |

> 详细对比见 [AI Coding · 工具全景](/ai-coding/tools/overview)。

## 三、demo 陷阱检查清单

看到「效果惊艳」的开源项目，先查：

- [ ] 有没有公开 benchmark / 复现说明，还是只有 gif 演示
- [ ] 有没有真实用户在跑（issue 区是提问还是吹捧）
- [ ] 能不能在我自己的数据上跑通（先跑通再评估效果）
- [ ] 文档有没有版本对应（README 与 release 是否脱节）

> **原则**：开源项目按「能不能立刻在我的机器上跑通」排序，而不是按 star 数排序。

## 四、如何跟踪

1. GitHub Trending（按语言过滤）、Hugging Face 模型榜
2. 关注你已选项目的 release notes——新版本可能改变选型
3. 中文社区：掘金 / 知乎的实践复盘比转发稿可信

## 参考

- [vLLM](https://github.com/vllm-project/vllm)（访问于 2026-08-14）
- [Ollama](https://github.com/ollama/ollama)（访问于 2026-08-14）
- [Dify](https://github.com/langgenius/dify)（访问于 2026-08-14）

## 下一步

- 看论文追前沿 → [重要论文速递](/ai-trends/research-highlights/papers)
- 落地到团队工作流 → [AI Coding 落地](/ai-coding/)

## 如果你想

- 选模型 → [模型选型决策树](/reference/model-selection-guide)
- 企业部署 → [AI Coding · 企业部署](/ai-coding/enterprise/deployment)
- 看真实案例 → [Cookbook](/cookbook/)

---
title: Zhipu · 智谱 GLM 全系
description: 'GLM-5.3 / GLM-5.3-Flash / GLM-5.2——清华系、1M 上下文、后训练 Scaling 旗舰、Agentic Coding'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: 智谱开放平台 API 定价
      url: https://docs.bigmodel.cn/cn/guide/start/pricing
      accessedAt: 2026-09-30
    - name: GLM-5.3 官方文档
      url: https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3
      accessedAt: 2026-09-30
    - name: 智谱模型与产品发布记录
      url: https://docs.bigmodel.cn/cn/update/new-releases
      accessedAt: 2026-09-30
---

# Zhipu · 智谱 GLM 全系

> 7 家厂商里**清华学术背景最深 + Agent 工具链最完整 + 全尺寸开源最彻底**。

## 一、公司背景

智谱 AI 由清华大学唐杰教授团队 2019 年孵化，总部北京。核心定位是**「学术 + 开源 + Agent」**——从 GLM-130B 开源起步，逐步商业化。商业模式：BigModel API + 企业 MaaS + 开源权重。是国内最早做大模型商业化的公司之一。

## 二、模型矩阵（截至 2026-09）

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **GLM-5.3** | 旗舰（2026-08-19 上线） | 1M | **常开**，`reasoning_effort` = low / high / max（默认 max） | Agentic Engineering / 复杂软件工程 |
| **GLM-5.3-Flash** | 原生多模态（2026-08-26 上线） | 1M | — | GUI Agent / Office 文档 / 金融研究 |
| **GLM-5.3-FlashX** | 多模态加速档 | 1M | — | 同上，低延迟 |
| **GLM-5.2** | 上一代旗舰（2026-06-16 上线） | 1M | — | Agentic Engineering / 通用 |
| **GLM-5.1** | 上一代（2026-04-07 上线） | 按输入长度分档 | — | 长程任务，单次可自主工作长达 8 小时 |
| **GLM-4.7-Flash** | 免费轻量（2026-01-19 上线） | 200K | — | 高并发 / 零成本调用 |

> **产品线逻辑**：`GLM-5.3` 是当前文本旗舰（**仅文本模态**，视觉能力由 `GLM-5.3-Flash` 承担），`GLM-5.2` 退居上一代，`GLM-4.7-Flash` 承担免费档。

> **关键洞察（官方已确认）**：`GLM-5.3` 与 `GLM-5.2` **使用相同的基础模型，所有提升均来自后训练**——这直接印证了「后训练 Scaling 是当前最大杠杆」的行业趋势。官方给出的口径是内部 Z.ai Code Bench 较 `GLM-5.2` **提升 50%**。

**官方公布的 `GLM-5.3` 相对 `GLM-5.2` 基准变化**：

| 基准 | GLM-5.2 | GLM-5.3 |
|------|---------|---------|
| Terminal-Bench 3.0 | 4.6 | **28.3** |
| DeepSWE v1.1 | 46.2 | **66.9** |
| Agents' Last Exam | 23.8 | **28.5** |
| Z.ai Code Bench（Max 档准确率） | 23.4% | **34.5%** |

> ⚠️ 原文表格中的「AA 智能分」一列在 2026-09 的官方文档中**未找到出处**，已移除，改用上表的官方基准数据。

## 三、技术架构

**MoE 路径** —— GLM-5 系列采用 MoE 架构，与行业趋势一致。

**混合注意力** —— `GLM-5.3-Flash` 采用**线性注意力 + 稀疏注意力混合架构**，官方披露总参 320B / 激活 18B，计算量与 KV 缓存较 `GLM-5.3` 大幅降低。`GLM-5` 曾首次集成 DeepSeek Sparse Attention。

**思考强制开启** —— `GLM-5.3` **始终启用思考**，且**不再支持 `thinking.type: "disabled"`**。从 `GLM-5.2` 迁移时必须先改为 `enabled` 并设置 `reasoning_effort`，否则请求失败。

**GLM 双向注意力** —— GLM 系列的独特设计：早期版本用双向注意力（Encoder-Decoder 风格），GLM-4 起转为自回归（Decoder-only）。**双向注意力在理解任务上有优势，但生成任务不如自回归**。

**多模态与语音** —— `GLM-OCR`（自研 CogViT 编码器-解码器）、`GLM-Image`（首个在国产芯片上完成全流程训练的 SOTA 多模态模型）、`GLM-TTS` / `GLM-ASR-2512` / `GLM-Realtime`。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Tool Use** | 函数调用 / 工具流式输出 | BigModel API |
| **思考控制** | `reasoning_effort` 三档（仅 GLM-5.3） | 常开，不可关闭 |
| **上下文缓存** | 缓存命中单独计费，存储限时免费 | BigModel API |
| **多模态** | `GLM-5.3-Flash` 原生视觉 | 图片 / 视频 / 文件输入 |
| **AllTools** | 搜索 + 计算 + 绘图组合 | BigModel 内置 |
| **协议兼容** | OpenAI Chat / Responses / Anthropic Message 三套端点 | `open.bigmodel.cn` |
| **Managed Agents** | Agent / Environment / Session / Deployment / Memory Store / Vault | 平台侧托管 Agent |

**AllTools 是智谱的差异化** —— 一个 API 调用同时支持搜索、计算、绘图、代码执行，类似 ChatGPT 的 Code Interpreter + Web Browsing 组合。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **BigModel API** | `open.bigmodel.cn` | 直接 API 调用 |
| **GLM Coding Plan** | 个人版 / 团队版 | Claude Code 等编码工具接入（2026-07-30 改版为积分制） |
| **Managed Agents** | 平台托管 | 定时 / 事件触发的长程 Agent 任务 |
| **GLM 开源权重** | HuggingFace / ModelScope | 私有部署 / 微调 |
| **MaaS 企业版** | 智谱云 | 企业私有化 |

**全尺寸开源是智谱优势** —— GLM 系列从 GLM-4 起全尺寸开放（Apache 2.0），是国内开源最彻底的大模型厂商。`GLM-4.7-Flash` 更是**完全免费**。

## 六、价格（截至 2026-09，官方定价，单位：元 / 百万 Tokens）

| 模型 | 上下文 | 输入 | 输出 | 缓存命中 |
|------|--------|------|------|----------|
| GLM-5.3 | 1M | ¥8 | ¥28 | ¥2 |
| GLM-5.3-Flash | 1M | ¥0.8 | ¥2.8 | ¥0.23 |
| GLM-5.3-FlashX | 1M | ¥2 | ¥7 | ¥0.57 |
| GLM-5.2 | 1M | ¥8 | ¥28 | ¥2 |
| GLM-4.7-Flash | 200K | 免费 | 免费 | 免费 |

**价格说明**：

- **智谱 BigModel 官方定价以人民币计价**（此前版本文档误记为美元，已按官方页更正）
- **缓存存储当前限时免费**——免费期结束后的标准价格官方暂未展示
- **Batch API 打 5 折**（标准调用价的 50%），适用于大规模非实时批处理
- 搜索工具按次计费：Search-Std ¥0.01 / 次、Search-Pro ¥0.03 / 次

**`GLM-5.3-Flash` 是价格利器** —— 1M 上下文 + 原生多模态，输入价仅为旗舰的 **1/10**。

## 七、适合场景 / 不适合场景

**适合**：
- 中文场景（中文基准领先，中文原生训练）
- 国产化替代（全尺寸开源，可完全私有部署）
- Agent 部署（`GLM-5.3` 常开思考 + `GLM-5.3-Flash` 原生多模态 + Managed Agents 平台）
- 多模态 GUI / Office 自动化（`GLM-5.3-Flash` 输入价 ¥0.8/M）
- 学术研究（清华背景，开源最彻底）

**不适合**：
- 英文为主的场景（Claude / GPT 英文更强）
- 极简单轮问答（`GLM-5.3` 强制常开思考，简单任务成本偏高——此时应改用免费档 `GLM-4.7-Flash`）
- 需要 2M 级超长上下文的场景（`GLM-5.3` 为 1M）

## 八、最新动态（2026-09）

**三条跟踪线**：

- **模型线**：`GLM-5.3` → `GLM-5.3-Flash` 迭代。核心看「旗舰是否换基座、是否强制思考、上下文是否再涨」
- **产品线**：GLM Coding Plan（个人版 / 团队版）。核心看配额机制与「非高峰时段折扣」这类直接影响成本的策略
- **平台线**：Managed Agents、知识库、Web Search / 网页阅读工具。核心看平台侧是否把 Agent 编排收进 API

**如何跟踪**：

1. **官方源**：[模型与产品发布记录](https://docs.bigmodel.cn/cn/update/new-releases)（带日期的完整发布流水，最权威）、[API 定价](https://docs.bigmodel.cn/cn/guide/start/pricing)、[GLM-5.3 模型页](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3)
2. **更新节奏**：旗舰约 2-3 个月一更（`GLM-5` 2026-02 → `5.1` 2026-04 → `5.2` 2026-06 → `5.3` 2026-08）
3. **判断原则**：智谱的换代**常常不动基座**——看到「小版本号 + 官方强调后训练」时，应预期能力涨、参数不变、价格不变，而不是重新做架构选型

**截至 2026-09 的具体动态**（均据官方源）：

- **2026-08-19 `GLM-5.3` 上线** —— 官方明确「与 `GLM-5.2` 使用相同的基础模型，所有提升均来自后训练」；内部 Z.ai Code Bench 较 `5.2` 提升 50%
- **2026-08-26 `GLM-5.3-Flash` 上线** —— 原生多模态，可「主动观察界面、渲染与交互反馈并持续迭代」；**线性 + 稀疏注意力混合架构，总参 320B / 激活 18B**；场景从 Coding 扩展到 Office 文档与金融研究工作流
- **`GLM-5.3` 强制思考** —— 三档 `reasoning_effort`（low / high / max，默认 max），**不再支持禁用思考**。这是对现有集成的破坏性变更，迁移需改参数
- **涌现的网络安全能力** —— 官方披露在 CyberGym 得分 **84.5%**（当前最佳，超过 Mythos 5 的 83.8%）；ExploitBench **54.4%**（`GLM-5.2` 为 24.4%）。与国内多家安全团队合作，在 **269 个项目中共发现 2436 个漏洞（1097 个中高危）**，并建立了 Z.ai 安全漏洞披露台账
- **2026-07-30 GLM Coding Plan 改版** —— 改为**基于积分的配额系统**；包括周末全天在内的非高峰时段，调用仅消耗标准积分的 **50%**
- **2026-05-29 GLM Coding Plan 团队版上线** —— 席位 / 权限 / 用量 / 预算统一管理，默认不使用代码、提示词和对话内容训练模型
- **平台侧新增 Managed Agents** —— 提供 Agent、Environment、Session、Deployment（cron 定时）、Memory Store、Skill、Vault（凭据）等完整 API

> ⚠️ **未能核实**：原文「GLM-5 为 744B 总参 / 40B 激活」的参数量在 2026-09 官方页未找到出处，已从表格移除；GLM-5.3 / GLM-5.2 的基座参数量官方同样未公开。

## 关键洞察

- **同基座换版本是智谱当前的主策略**——`GLM-5.3` 与 `GLM-5.2` 共享基座，能力提升纯靠后训练
- **全尺寸开源是最大优势**——全尺寸开放 + `GLM-4.7-Flash` 完全免费，私有部署最灵活
- **强制思考改变了成本模型**——`GLM-5.3` 不可关闭思考，简单任务必须换模型而不是换参数
- **GLM-5.3-Flash 是性价比断层**——1M 上下文 + 原生多模态，输入价 ¥0.8/M
- **Managed Agents 说明平台在往「Agent 运行时」走**——编排能力开始收进 API

## 参考

- [智谱模型与产品发布记录](https://docs.bigmodel.cn/cn/update/new-releases)（访问于 2026-09-30）
- [智谱 API 定价](https://docs.bigmodel.cn/cn/guide/start/pricing)（访问于 2026-09-30）
- [GLM-5.3 官方文档](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3)（访问于 2026-09-30）
- [智谱 BigModel 开放平台](https://open.bigmodel.cn/)
- [GLM-4 技术报告](https://github.com/THUDM/GLM-4)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 看另一家开源路线 → [Qwen · 阿里通义千问全系](../qwen/)
- 看横向对比表 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 看 MiniMax 档案 → [MiniMax 全系](/ai-trends/cn-vendors/minimax/)
- 看 Kimi 档案 → [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看国内厂商动态 → [国内厂商](/ai-trends/cn-vendors/)

---
title: OpenAI · GPT 全系
description: GPT-6 Astra / GPT-6.1 Sol / GPT-6 Luna——推理模型路线、部署与价格
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-08
verifiedWith:
  sources:
    - name: OpenAI 官方定价
      url: https://developers.openai.com/api/docs/pricing
      accessedAt: 2026-10-08
    - name: GPT-6 Astra 模型页
      url: https://developers.openai.com/api/docs/models/gpt-6-astra
      accessedAt: 2026-10-08
    - name: OpenAI API changelog
      url: https://developers.openai.com/api/docs/changelog
      accessedAt: 2026-10-08
    - name: OpenAI 模型目录
      url: https://developers.openai.com/api/docs/models
      accessedAt: 2026-10-08
---

# OpenAI · GPT 全系

> 7 家厂商里**最早商业化 + 最激进推理模型路线（o-series）+ 2026 年首次开源（GPT-OSS）**。

## 一、公司背景

OpenAI 2015 年成立，从非营利转型为"利润上限"结构。核心投资方 Microsoft（累计 $130 亿+）。商业模式：闭源 API + ChatGPT 订阅 + Azure OpenAI 企业部署。2026 年首次开源 GPT-OSS 20B/120B，标志策略转向。

## 二、模型矩阵（截至 2026-10）

| 模型 | 定位 | 价格（input / output） | 主要场景 |
|------|------|--------|----------|
| **GPT-6 Astra** | 旗舰（当前最强） | $10 / $50 | 复杂推理 / 编码 / computer use / 研究 |
| **GPT-6.1 Sol** | 主力（近 Astra 性能、更低成本） | $2 / $10 | 复杂编码 / 专业工作 / 多 agent（beta） |
| **GPT-6 Sol** | 复杂编码与 agent | $2 / $10 | 编码 / Agent 工作流 |
| **GPT-6 Luna** | 轻量 | $0.10 / $0.50 | 高并发 / 成本敏感 |
| **GPT-5.6 系列（Sol / Terra / Luna）** | 上一代 | $4/$20、$2/$12、$0.20/$1.20 | 存量负载 / 促销期内过渡 |
| **Daybreak 安全线（Cyber）** | 安全专精 | $12.50 / $75 | 网络安全（需单独审批） |
| **o 系列（o1 / o3 / o4-mini）** | 推理模型线 | o3 $2/$8、o4-mini $1.10/$4.40 | 数学 / 代码 / 逻辑 |

> **产品线逻辑**：主线已从 GPT-5.6 切到 **GPT-6**——Astra 打旗舰、6.1 Sol 打性价比主力、Sol / Luna 覆盖编码与高并发。Cyber 走 Daybreak 安全线（分 **Daybreak Blue** 通用模型档与 **Daybreak Red** 专用 Cyber 模型档，均需审批）。o 系列仍在定价表里，但官方已在模型目录注明 o3「被 GPT-5 取代」、o4-mini「被 GPT-5 Mini 取代」——**o 系列是存量与深研场景，不是新项目主线**。

> ⚠️ **上下文已到 1M**：GPT-6 Astra 上下文窗口 **1,050,000 token**（最大输入 922,000，最大输出 128,000）。计价按 **272K** 切长短档，不是按 1M 切。

> 📌 **10 月无型号变动**。模型目录（访问于 2026-10-08）里 GPT-6 家族仍是四个型号：`gpt-6-astra` / `gpt-6.1-sol` / `gpt-6-sol` / `gpt-6-luna`，**10 月的新动作全在 ChatGPT 端与平台端，不在模型矩阵**。更老的 `gpt-5.5` / `gpt-5.4` / `gpt-5.2` / `gpt-5.1` 仍在定价表里可调用，属于存量而非新线。

## 三、技术架构

**MoE 路径（推测）** —— GPT 系列采用 MoE 架构，具体专家数未公开。相比 Anthropic 的 dense 路线，MoE 让 OpenAI 在相同推理成本下堆更大参数量。（截至 2026-09 官方未公开 GPT-6 的架构细节，此处沿用 GPT-5 代的判断。）

**o-series 推理模型** —— OpenAI 的历史差异化。o1/o3 用 RLVR（Reinforcement Learning with Verifiable Rewards）训练：数学题答案对错、代码题单测通过率，完全可程序验证。**"多花时间想 = 准确率提升"** 是 o-series 的核心理念，这条路线已被整个行业继承（含 [DeepSeek-R1](/ai-trends/cn-vendors/)）。**但 o 系列自身已让位**：官方模型目录直接标注 o3 被 GPT-5 取代、o4-mini 被 GPT-5 Mini 取代，o1 / o3 / o4-mini 目前是存量与深研场景的选择。

**推理档位已成体系** —— GPT-6 Astra 的 `reasoning.effort` 支持 `low` / `medium` / `high` / `xhigh` / `max`，并可在会话中途改档而不破坏缓存前缀。⚠️ Astra **不支持** `none` 档，也不支持自定义 `temperature` / `top_p` / `logprobs`。

**开源动态（GPT-OSS）** —— OpenAI 仍是"闭源 + 开源"双轨，`gpt-oss-120b` / `gpt-oss-20b` 仍在模型目录中。⚠️ 但官方正在**下线微调平台**：不再对新用户开放，已有用户可在未来几个月内继续创建训练任务；已训练模型在基座下线前仍可推理。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Function Calling** | JSON Schema 函数调用 | Responses / Chat Completions API |
| **Structured Outputs** | 强制 JSON 输出格式 | 响应格式参数 |
| **Vision** | 图片理解 + OCR | 全部最新 GPT 模型原生 |
| **Agents API** | 托管 agent 会话（public beta） | 2026-09-10 发布，Codex harness |
| **Async Tool Calling** | 应用侧执行工具，模型继续跑 | Responses API |
| **Mid-turn Steering** | 生成中追加指令纠偏 | WebSocket |
| **Web Search** | 服务端检索 | $10 / 1k 次 |
| **File Search** | RAG 检索增强 | Responses API |
| **Code Interpreter** | 沙箱内执行代码 | 容器按分钟计费 |

**Function Calling 是 OpenAI 首创** —— 2023 年 6 月推出，现已成为行业标准。Claude 的 Tool Use、Qwen 的 Tool Use 都是跟进。

> ⚠️ **Assistants API 已于 2026-08-26 关停**。文档中若还出现 Assistants 相关能力，一律迁移到 **Responses API + Conversations API**。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **OpenAI API** | `platform.openai.com` | 直接 API 调用 |
| **Azure OpenAI** | Azure 云 | 企业合规 / 私有 VPC |
| **Amazon Bedrock** | OpenAI 兼容 Responses 端点（2026-06） | AWS 侧采购与合规 |
| **GPT-OSS** | HuggingFace / 自部署 | 私有化 / 微调 |
| **ChatGPT** | Web/Desktop/Mobile | 终端用户产品 |

**云厂商采购路径在变多** —— 除 Azure OpenAI 外，**2026-06 起 OpenAI 模型也上了 Amazon Bedrock**（走 OpenAI 兼容的 Responses API 端点，支持模型随 Region 变化）。选型时"能不能走既有云合同"正在变成一个实际的决策维度。

## 六、价格（截至 2026-10，官方定价）

> ✅ **2026-10 全表复核无调价**。下表每一行（input / cached / cache write / output）均与 2026-10-08 抓取的官方定价页逐项核对一致，10 月没有任何型号提价或降价。GPT-6 家族四档价格自 2026-09 发布以来未动。

短上下文 = ≤272K 输入 token；长上下文 = >272K 输入 token。

| 模型 | Input | Output | 缓存读 | 缓存写 | 备注 |
|------|-------|--------|--------|--------|------|
| GPT-6 Astra | $10 / MTok | $50 / MTok | $1.00 | $12.50 | 长上下文档：$20 / $75 |
| GPT-6.1 Sol | $2 / MTok | $10 / MTok | $0.10 | $2.50 | 长上下文档：$4 / $15 |
| GPT-6 Sol | $2 / MTok | $10 / MTok | $0.20 | $2.50 | 2026-09-22 发布 |
| GPT-6 Luna | $0.10 / MTok | $0.50 / MTok | $0.01 | $0.125 | 2026-09-22 发布 |
| GPT-5.6 Sol | $4 / MTok | $20 / MTok | $0.40 | $5.00 | 促销价，至少到 2026-11-21 |
| GPT-5.6 Terra | $2 / MTok | $12 / MTok | $0.20 | $2.50 | 2026-07-30 降价 20% |
| GPT-5.6 Luna | $0.20 / MTok | $1.20 / MTok | $0.02 | $0.25 | 2026-07-30 降价 80% |
| GPT-5.6 Cyber | $12.50 / MTok | $75 / MTok | $1.25 | $15.625 | Daybreak 安全线 |

**价格梯度**：GPT-6 Luna < GPT-6 Sol ≈ GPT-6.1 Sol < GPT-5.6 Terra < GPT-5.6 Sol < **GPT-6 Astra**。**最贵的不是上一代旗舰而是新旗舰**——Astra 的 $10 / $50 已高于 Cyber 之外的任何型号，跨代选型时别默认"新一代更便宜"。

**长上下文不是简单 2x**：Astra 超过 272K 输入后，**input 与缓存按 2x、output 按 1.5x** 计费（$20 / $75）。

**处理档位（service tier）**：

| 档位 | 倍率 | 说明 |
| --- | --- | --- |
| Standard | 1x | 基准 |
| Batch | 0.5x | 异步，不计速率限制 |
| Flex | 0.5x | 与 Batch 同价 |
| Fast | 2x | 2026-07-30 起取代原 Priority Processing |
| Ultrafast | 6x | 仅 `gpt-6-astra`，2026-09-29 新增 |

**缓存写入是独立计价项**（基准 input 的 1.25x），别只按"缓存读便宜"估算总账。另注意：区域处理（data residency）端点与 FedRAMP 端点均加价 10%（适用于 2026-03-05 及之后发布的型号）。

**GPT-5.6 Sol 的促销价有明确期限**——官方写明促销定价**至少持续到 2026-11-21**。引用这个价格时必须带上期限，否则跨月会失真。

> ⚠️ **"档位"有两个，别混**：上表是**处理档位（service tier）**，决定价格倍率与延迟；官方另有**用量档位（usage tier）**，决定速率限制。2026-10-06 用量档位从五档**简化为 Build / Launch / Grow 三档**，按累计 credit 采购额自动升级，与价格倍率无关。

> 📌 **10 月新增计费项：GPT-Rosalind**。`gpt-rosalind-research`（生命科学推理）走 trusted-access 计划开放，**2026-10-05 起开始计费**，$5 / $0.50 / $25 per MTok，且**不适用缓存写入计价**。

## 七、适合场景 / 不适合场景

**适合**：
- 通用对话（GPT-6.1 Sol / GPT-6 Luna 性价比高）
- 数学 / 代码 / 逻辑推理（o 系列仍是深研场景的标杆）
- 多模态（Vision + Realtime API）
- 企业合规（Azure OpenAI / Bedrock 双云路径）

**不适合**：
- 超低成本边缘场景（GPT-6 Luna 之外仍偏贵）
- 极简单轮问答（杀鸡用牛刀）
- 国内直接使用（需走 Azure 或代理）

## 八、最新动态（2026-10）

**三层产品线跟踪**：

- **产品层 — ChatGPT**：面向终端用户的对话产品，功能更新频繁（工具调用、多模态、Agent 能力）
- **模型层 — GPT 系列 / o 系列**：
  - **GPT 系列**：通用对话与生成，主打综合能力（当前主线是 GPT-6）
  - **o 系列**：推理模型，回答前「思考」更久，擅长数学、编程、逻辑（o1、o3 等，现已让位 GPT-5 / GPT-6）
- **开发者层 — Platform API**：模型 API、Agents API、批处理端点。价格与限额变化对工程师最直接

> 关键认知：2024 年起 OpenAI 把「快速应答」与「慢速推理」分成两条模型线，o 系列确立了**推理时计算（inference-time compute）**路线——这也影响了后来的整个行业，包括 [DeepSeek-R1](/ai-trends/cn-vendors/)。**2026-09 起这条双线收敛了**：GPT-6 自身就带 `reasoning.effort` 档位，不再需要靠"换个模型系列"来实现慢思考。

**已核实的历史锚点**：

| 时间 | 事件 | 意义 |
| --- | --- | --- |
| 2022-11 | ChatGPT 发布 | 对话式 AI 进入大众视野 |
| 2023-03 | GPT-4 发布 | 多模态（图像输入）与更强推理 |
| 2024-05 | GPT-4o 发布 | 实时语音对话；免费开放 |
| 2024-09 | o1 发布 | 推理时计算路线确立，推理模型品类诞生 |
| 2026-07-09 | GPT-5.6 系列推出 | Sol / Terra / Luna 三档，GPT-5.6 铺开 |
| 2026-09-03 | **GPT-6 Astra 发布** | 新旗舰，$10 / $50，1.05M 上下文 |
| 2026-09-22 | **GPT-6 Sol / Luna 发布** | 主力与轻量档，$2/$10 与 $0.10/$0.50 |
| 2026-09-29 | **GPT-6.1 Sol 发布** | 近 Astra 性能、$2 / $10，**GPT-6 家族三周内连发三个型号** |
| 2026-10-07 | **GPT-6 与 Intelligent UI 在 ChatGPT 上线** | GPT-6 从 API 走向全体 ChatGPT 用户，见下表 |

**2026-10 的事件**（日期与内容取自官方 [changelog](https://developers.openai.com/api/docs/changelog)，访问于 2026-10-08）：

| 日期 | 事件 | 影响 |
| --- | --- | --- |
| 2026-10-07 | **GPT-6 与 Intelligent UI 在 ChatGPT 上线** | Plus / Pro / Business / Enterprise 用 **GPT-6 Sol**，Free / Go 用 **GPT-6 Luna**（次日 10-08 起扩展）；Enterprise 取决于管理员设置 |
| 2026-10-07 | `chat-latest` 快照更新 | API 侧同步指向 ChatGPT 付费档的最新模型，官方同时建议生产环境直接用 GPT-6 家族 |
| 2026-10-06 | **Decisions API 公测**，首发 `gpt-6-luna` | 把文本 / 图片转成结构化答案，官方称比 Responses API 快 10x |
| 2026-10-06 | 用量档位从五档简化为 **Build / Launch / Grow** | 按累计 credit 采购额自动升级，只影响速率限制 |
| 2026-10-05 | 组织设置内新增 **HIPAA 合规**开通流程 | 符合条件的管理员可签署 BAA 并为组织启用 |
| 2026-10-05 | **GPT-Rosalind 开始计费** | `gpt-rosalind-research` 从 GA 转入计费，$5 / $0.50 / $25 |

**GPT-6 在 ChatGPT 的三个例外**（易踩坑）：

- **Pro 的推理选项仍走 GPT-6 Astra，且不支持 Intelligent UI**——想要 Intelligent UI 就不能选 Pro 推理档
- **ChatGPT Work 与 Codex 所用模型本次不变**，跟随 GPT-6 的只有通用对话面
- Intelligent UI 覆盖 Instant 到 Extra High 推理档，不是全档位通吃

> ⚠️ **官方基准数字尚无独立验证**。GPT-6 Instant 在联网检索任务中首次响应比 GPT-5.6 Instant 快 44%、Extra High 起步速度≈GPT-5.6 Medium 而最终得分更高——这些均来自官方自述，**不要当成独立测评结论引用**。

**2026-09 的重要平台变更**（均见 [changelog](https://developers.openai.com/api/docs/changelog)）：

| 日期 | 事件 | 影响 |
| --- | --- | --- |
| 2026-09-29 | Agents API 加入 computer use | agent 可在 OpenAI 托管浏览器里干活，登录由你的应用处理 |
| 2026-09-29 | Astra 支持 Ultrafast 档 | 6x 价格换更低 token 间隔 |
| 2026-09-10 | **Agents API 公测** | 托管 Codex harness，负责会话编排、上下文压缩与恢复 |
| 2026-09-08 | Prompt Cache Diagnostics 转正 | 可定位缓存未命中的原因（Anthropic 同期也做了同类能力） |
| 2026-09-08 | GPT-Image 2.5 Sunburst / Flare | 图像生成编辑双线 |
| 2026-08-26 | **Assistants API 关停** | 必须迁到 Responses / Conversations API |
| 2026-08-21 | GPT-5.6 Sol 降价 | input −20%、output −33%（促销价至 2026-11-21） |

> ⚠️ 锚点截至 2026-10-08 已核实。**引用价格务必带版本号 + 日期**：GPT-5.6 Sol 的 $4 / $20 是有期限的促销价，GPT-6 Astra 又是全系最贵——两代"旗舰"的价格关系在两个月内反转过一次。
>
> ⚠️ 10 月的 ChatGPT 侧细节（GPT-6 Sol / Luna 分档、Intelligent UI 范围、Pro 例外）依据官方 release notes 与 OpenAI Research 页，其中 **10-07 的"ChatGPT 已切换到 GPT-6"一事另由 API changelog 当日 `chat-latest` 条目独立佐证**。Help Center 的 ChatGPT release notes 页面本轮返回 Cloudflare 人机校验、未能直接抓取，故上表 ChatGPT 行未逐条回链到该页。

**如何跟踪**：

1. **官方源**：[OpenAI Blog](https://openai.com/blog)（产品与模型）、[API changelog](https://developers.openai.com/api/docs/changelog)（最准的开发者侧信源）、[模型目录](https://developers.openai.com/api/docs/models)、[Status](https://status.openai.com)（服务可用性）
2. **关注信号**：模型降价 / 提价与促销期限、上下文长度变化、新端点、端点或模型的**关停公告**（Assistants 就是这么没的）
3. **中文二手**：机器之心、量子位聚合快，但价格等数字以官方为准

## 关键洞察

- **o 系列是推理标杆，但已交棒** —— RLVR 训练让"想得更久 = 答得更准"成为现实，这个理念如今长在 GPT-6 的 `effort` 档位里
- **换代节奏在加快** —— 2026-09 三周连发 Astra / Sol / Luna / 6.1 Sol 四个型号，"旗舰=最强=最贵"的假设已失效
- **Function Calling 是行业标准** —— Claude / Kimi / Qwen 都兼容 OpenAI 格式
- **平台关停风险要纳入选型** —— Assistants API 已于 2026-08-26 关停；云路径也从单一 Azure 扩到 Azure + Bedrock

## 参考

- [OpenAI 平台文档](https://platform.openai.com/docs)
- [OpenAI API changelog](https://developers.openai.com/api/docs/changelog)（访问于 2026-10-08）
- [OpenAI 定价](https://developers.openai.com/api/docs/pricing)（访问于 2026-10-08）
- [OpenAI 模型目录](https://developers.openai.com/api/docs/models)（访问于 2026-10-08）
- [Anthropic Claude 对比](../anthropic/)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 看国内厂商路线 → [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看横向对比表 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 看 xAI 路线 → [xAI · Grok 全系](../grok/)
- 看推理时计算的技术原理 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 看 Agent 工程实践 → [Anthropic · Claude 全系](../anthropic/)

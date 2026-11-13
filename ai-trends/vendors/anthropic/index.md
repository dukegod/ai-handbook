---
title: Anthropic · Claude 全系
description: 'Opus 5.5 / Sonnet 5.5 / Haiku 5.5 / Fable 5.2——技术架构、Constitutional AI 训练、能力与部署'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核了在售四型号的 Model ID、定价、缓存倍率、批量与快速模式、生命周期、Claude Code 侧 alias 与最低版本；示例未在本机重跑（本机 Claude Code 2.1.319 低于 Fable 5.2 所需的 v2.1.321）'
  sources:
    - name: Anthropic 模型总览
      url: https://platform.claude.com/docs/en/about-claude/models/overview
      accessedAt: 2026-11-13
    - name: Claude 定价文档
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-11-13
    - name: Claude Platform release notes
      url: https://platform.claude.com/docs/en/release-notes/overview
      accessedAt: 2026-11-13
    - name: Claude 模型退役与生命周期
      url: https://platform.claude.com/docs/en/about-claude/model-deprecations
      accessedAt: 2026-11-13
    - name: Claude Model IDs and versioning
      url: https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions
      accessedAt: 2026-11-13
    - name: Claude Code 模型配置
      url: https://code.claude.com/docs/en/model-config
      accessedAt: 2026-11-13
    - name: Claude Fable 5.2 模型页
      url: https://platform.claude.com/docs/en/models/fable-5-2/overview
      accessedAt: 2026-11-13
---

# Anthropic · Claude 全系

> 7 家厂商里**最坚持 dense 架构** + 唯一公开推 RLAIF 训练方法 + 把 Agent / Computer Use 当一等公民。

## 一、公司背景

Anthropic 是 2021 年由前 OpenAI 核心成员 Dario Amodei 与 Daniela Amodei 兄妹创办的 AI 安全公司，总部旧金山。核心定位是**"安全 + 可解释 + 可控"**——不卷规模上限，专注**可调度的工程化 AI**。商业模式 100% 闭源：按 token 计费 API + 订阅制产品（Claude.ai）+ Claude Code 终端 + 企业部署（AWS Bedrock / GCP Vertex）。

## 二、模型矩阵（截至 2026-10）

在售阵容与价格**截至 2026-11-13**。

| 模型 | Model ID | 定位 | 上下文 | 思考模式 | 发布 | 主要场景 |
| --- | --- | --- | --- | --- | --- | --- |
| **Fable 5.2** | `claude-fable-5-2` | 长 Agent 专精 | 1M | adaptive thinking（始终开启） | 2026-11-09 | 长任务 / 长 Agent / 大仓库 |
| **Opus 5.5** | `claude-opus-5-5` | 旗舰推理 | 1M | adaptive thinking（始终开启） | 2026-09-22 | 复杂推理 / 编码 / Agent |
| **Sonnet 5.5** | `claude-sonnet-5-5` | 主力 | 1M | adaptive thinking | 2026-09-28 | 编码 / 通用对话 / 工具调用 |
| **Haiku 5.5** | `claude-haiku-5-5` | 高并发 / 延迟敏感 | 1M | adaptive thinking | 2026-10-07 | 分类 / 提取 / 路由 / subagent |
| **Mythos 5.2** | `claude-mythos-5-2` | 安全专精 | 1M | adaptive thinking | 2026-11-09 | 网络安全 / 生物（limited availability） |
| Fable 5.1 / Fable 5 | `claude-fable-5-1` / `claude-fable-5` | 上一代 | 1M | adaptive thinking | 2026-09-01 / 更早 | 存量负载（legacy，仍可调用） |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | 上一代轻量档 | 200K | extended thinking | 2025-10-15 | 存量负载（仍可调用） |

> **产品线逻辑**：4 个主流型号覆盖"质量/速度/成本"三角，Fable 5.2 是"长 Agent"专属赛道，**不是 Opus 的替代**，是补位。官方选型指引是：绝大多数负载从 **Opus 5.5** 起步；提高 effort 后仍不够，再上 **Fable 5.2**。Mythos 5.2 状态 Active 但属**受限可用**——需通过 Anthropic 验证计划（如 Cyber Verification Program）认证。

> ⚠️ **2026-11 换代提醒**：**Fable 5.2 于 2026-11-09 发布**，四条主流线（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）全部换代完毕。**Fable 5.1 与 Fable 5 退居 legacy 档**——官方 [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 划入 "Legacy models"，但 [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) 状态列仍是 **Active**（能否调用看后者，该不该用看前者）。Haiku 4.5 亦仍是 Active，退役承诺「不早于 2026-10-15」未变。Mythos 5.2 与 Fable 5.2 同日发布、同价同规格。

## 三、技术架构

**dense 模型路径**（推测）—— 7 家厂商里 Anthropic 是少数仍坚持 dense 的（多数走 MoE）。代价是训练成本更高、参数总量受限；收益是**推理行为更稳定、不需要路由调优**。

**Constitutional AI（RLAIF）** —— Anthropic 主推的训练方法：用 AI 而非人类做偏好标注，先用"宪法"原则（helpful / harmless / honest）让模型自评，再用 RLAIF 训练。**核心差异**：与 OpenAI 的 RLHF / DeepSeek 的 GRPO 不同，它把"价值观"显式编码进训练流程，更适合做安全可控的助手。

**长上下文实现** —— Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5 均为 1M 上下文，Haiku 4.5 为 200K。1M 上下文在 4.6 及之后的模型上**按标准价计费**（官方举例：90 万 token 与 9 千 token 单价相同）——**唯一例外是 Haiku 5.5**：按 prompt 长度分档，超过 10 万 token 走更贵的一档。官方披露的工程细节是**分词器换代**——Claude 4.7 及之后的模型换用新分词器，同样文本约多出 30% token（更早型号沿用旧分词器）；当前分词器下 1M token ≈ 555k 词 ≈ 250 万字符，旧分词器下 1M ≈ 750k 词。

## 四、核心能力

| 能力 | 描述 | 落地 |
| --- | --- | --- |
| **Tool Use** | 函数调用 / JSON Schema 校验 | Messages API 原生 |
| **Prompt Caching** | 5 分钟 + 1 小时双档缓存 | 读 0.1x（Fable 5.2 / Mythos 5.2 / Fable 5.1 / Mythos 5.1 为 0.025x、Opus 5.5 与 Sonnet 5.5 为 0.05x） |
| **Computer Use** | 截图 + 操作 GUI（鼠标键盘） | `computer_toolset_20260801` 已 GA（2026-08-19） |
| **Browser Use** | 应用自托管浏览器内驱动 | `browser_toolset_20260801`（2026-08-19 新增） |
| **Agent SDK** | 多 agent 编排 / Subagent 派生 | Claude Code / SDK 同源 |
| **Files API** | 客户端文件直传 | 已 GA（2026-08-19） |
| **Agent Skills** | Skills 打包进容器 | Skills API 已 GA（2026-08-19） |
| **Managed Agents** | 托管会话 + 预算 / 审批 / 记忆 | $0.08 / 会话小时 |
| **Message Batches** | 24h 异步批处理（50% 折扣） | Messages API |

**Agent 能力是 Anthropic 的核心壁垒**——Computer Use 让你"操作电脑"，Browser Use 让你"操作浏览器"，Agent SDK 让你"派生 subagent"，组合起来能做**长任务自动化**（hooks + skills + subagents 就是它的工程化封装）。

## 五、部署形态

| 部署 | 平台 | 适合 |
| --- | --- | --- |
| **Claude API** | `platform.claude.com` | 直接 API 调用 |
| **Claude Code** | CLI / VS Code / JetBrains | 本地 CLI 工作流 |
| **AWS Bedrock** | `aws.amazon.com/bedrock` | AWS 集成 / 私有化 |
| **GCP Vertex AI** | `cloud.google.com/vertex-ai` | GCP 集成 / 私有化 |
| **Claude Platform on AWS** | AWS Marketplace（CCU 计费） | Anthropic 官方运维 + AWS 采购 |
| **Claude in Microsoft Foundry** | Azure Marketplace（CCU 计费） | Azure 企业采购路径 |
| **Claude.ai** | Web/Desktop/Mobile | 终端用户产品 |

**云厂商是企业部署的多条腿**——大客户不直接接 Anthropic，走 marketplace 计费 + 私有 VPC。两条计费口径要分清：**Bedrock / Vertex 是云厂商自己开票**；**Claude Platform on AWS / Claude in Microsoft Foundry 是 Anthropic 定价后折算成 CCU（$0.01 / CCU）由云厂商转收**。

## 六、价格（截至 2026-11，官方定价）

价格与生命周期**截至 2026-11-13**。

| 模型 | Input | Output | 缓存读 | 退役承诺 | 备注 |
| --- | --- | --- | --- | --- | --- |
| Haiku 5.5（prompt ≤ 100k） | $0.10 / MTok | $0.50 / MTok | $0.01 / MTok | 不早于 2027-10-07 | 全系最便宜 |
| Haiku 5.5（prompt > 100k） | $0.50 / MTok | $2.50 / MTok | $0.05 / MTok | 不早于 2027-10-07 | **按 prompt 长度分档**，全系唯一 |
| Haiku 4.5 | $1 / MTok | $5 / MTok | $0.10 / MTok | 不早于 2026-10-15 | 上一代；仍为 Active |
| Sonnet 5.5 | $2 / MTok | $10 / MTok | $0.10 / MTok | 不早于 2027-09-28 | 2026-10-07 起缓存读从 $0.20 降到 $0.10 |
| Opus 5.5 | $4 / MTok | $20 / MTok | $0.20 / MTok | 不早于 2027-09-22 | 比 Opus 5 降 20% |
| **Fable 5.2** | **$8 / MTok** | **$40 / MTok** | **$0.20 / MTok** | **不早于 2027-11-09** | 比 Fable 5.1 降 20%；缓存读 0.025x |
| Mythos 5.2 | $8 / MTok | $40 / MTok | $0.20 / MTok | 不早于 2027-11-09 | 受限可用（需 Anthropic 验证计划认证） |
| Fable 5.1 / Mythos 5.1（legacy） | $10 / MTok | $50 / MTok | $0.25 / MTok | 不早于 2027-09-01 | 上一代 Fable |
| Fable 5 / Mythos 5（legacy） | $10 / MTok | $50 / MTok | $1 / MTok | 不早于 2027-06-09 | 更早一代 |

**价格梯度**：Haiku 5.5 < Haiku 4.5 < Sonnet 5.5 < Opus 5.5 < Fable 5.2 = Mythos 5.2 < Fable 5.1 = Mythos 5.1 = Fable 5 = Mythos 5。**Fable 5.2 是现售最贵档**——$8 是 Opus 5.5 的 **2 倍**、Sonnet 5.5 的 4 倍；上一代 Fable 5.1 的 $10 才是"2.5 倍 Opus 5.5"，5.2 降价后**相对倍数反而更小**。legacy 档更贵，但已不推荐新项目使用。

> ⚠️ **Haiku 5.5 是唯一按 prompt 长度分档计费的型号**——同样 1M 上下文窗口，官方对 > 10 万 token 的 prompt 收 5 倍价（输入 $0.50 vs $0.10）；批处理同样分档（≤ 100k 为 $0.05 / $0.25，> 100k 为 $0.25 / $1.25）。做超长上下文摘要别默认按短 prompt 的价估预算。

**缓存折扣已不再统一**——读取命中价按模型分档：**Fable 5.2 / Mythos 5.2 / Fable 5.1 / Mythos 5.1 为 0.025x**、**Opus 5.5 / Sonnet 5.5 为 0.05x**、其余为 0.1x。写入侧是 5 分钟档 1.25x、1 小时档 2x。**长 prompt + 多轮对话场景必开缓存**（具体折扣以官方定价页为准）。

**其他计价维度**：Batch API 一律 5 折（Fable 5.2 → $4 / $20，Opus 5.5 → $2 / $10，Sonnet 5.5 → $1 / $5）；`inference_geo: "us"` 数据驻留为 1.1x；**Fast mode** Fable 5.2 为 $16 / $80、Opus 5.5 为 $8 / $40、Opus 5 与 Opus 4.8 为 $10 / $50，且不与 Batch 叠加。

> ⚠️ **Batch 输出 300k 是 beta**（`anthropic-beta: output-300k-2026-03-24`），官方点名支持的型号是 Opus 5.5 / Opus 5 / Sonnet 5.5 / Sonnet 5 / Haiku 5.5 / Opus 4.8 / 4.7 / 4.6 / Sonnet 4.6——**Fable 不在其中**；同步 Messages API 的 max output 上限仍是 128K。

## 七、适合场景 / 不适合场景

**适合**：
- 编码 + 工具调用（Sonnet 5.5 + Tool Use 是业界标杆）
- 长文档处理（四个主力型号都是 1M）
- Agent 任务（Computer Use + Browser Use + Agent SDK + Subagent 组合）
- 重视安全可控（Constitutional AI）

**不适合**：
- 超低成本场景（Haiku 5.5 起价已降到 $0.10 / MTok，但仍比 Qwen / GLM 同尺寸贵）
- 国内合规（需走 Bedrock / Vertex 等海外渠道，或等国内合作）
- 极简单轮问答（杀鸡用牛刀）

## 八、最新动态（2026-10）

**三条跟踪线**：

- **模型线**：Claude 家族的发布与定价——哪个模型在哪个价位、定位是什么
- **工具线**：Claude Code、Claude Agent SDK、Claude.ai 产品功能，对开发者比模型线更常变化
- **协议线**：MCP 的演进。已开源为开放标准，生态变化影响所有工具

**本轮核实的 2026-11 事件**（均见 [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)）：

| 日期 | 事件 | 影响 |
| --- | --- | --- |
| 2026-11-12 | **自托管 Claude Managed Agents** 开放 | 整套托管 agent 服务可跑在自有基础设施上 |
| 2026-11-09 | 发布 **Claude Fable 5.2**（`claude-fable-5-2`），$8 / $40 | 比 Fable 5.1 降价 20%；1M context / 128k output / adaptive thinking 总是开 / 默认 effort `high`；强制 30 天数据留存；Dreams 也已支持 |
| 2026-11-09 | 同日发布 **Claude Mythos 5.2**（`claude-mythos-5-2`），$8 / $40 | 规格同 Fable 5.2，但需通过 Anthropic 验证计划的组织才能调用 |
| 2026-11-09 | **Fable 5.2 fast mode** 上线：$16 / $80 | 输出速度最高 2.5 倍；不与 Batch 叠加 |
| 2026-11-05 | Compliance API 新增 security posture 端点（Enterprise beta）、Console 上线 IP allowlisting beta、Admin API 支持全端登出 | 企业治理面又扩一轮 |
| 2026-11-03 | **Claude Mythos 5 / Opus 4.7 / Sonnet 4.6 文本带水印** | 水印范围扩大，注意合规口径 |
| 2026-11-02 | Messages API 上线 **message threads** beta（`anthropic-beta: message-threads-2026-08-12`） | 服务端保存会话、只发增量；线程在最后一次请求后 5 分钟过期 |

**上一轮核实的 2026-10 事件**：

| 日期 | 事件 | 影响 |
| --- | --- | --- |
| 2026-10-30 | Claude Opus 4.8 的 fast mode 废弃 | 2026-11-30 移除 |
| 2026-10-08 | Compliance API 的 chat 端点可返回「统一 Claude 体验」的对话（Enterprise 组织 beta） | 审计链路要跟着扩 |
| 2026-10-07 | 发布 **Claude Haiku 5.5**（`claude-haiku-5-5`） | 四条主流线全部换代完毕；1M context / 128k output / adaptive thinking（默认 effort `medium`）/ 延迟最快档 |
| 2026-10-07 | **Sonnet 5.5 缓存读降价**：$0.20 → $0.10 / MTok（0.05x 取代 0.1x） | 写侧与其他价格不变；长 prompt 场景成本直接减半 |
| 2026-10-07 | Max / Team 计划新增每月 API 额度 | 订阅用户可把额度打到 API 侧 |
| 2026-10-07 | Python / TypeScript SDK 新增 browser use 与 computer use 工具集的 beta 类 | 工具循环交给 SDK 跑 |
| 2026-10-06 | Models API 新增 `capabilities.server_tools` | 可编程判断某模型是否接受 web search / code execution |
| 2026-10-05 | Models API 新增 `capabilities.thinking.types.disabled` | 可编程判断某模型是否接受 `thinking: {"type":"disabled"}` |
| 2026-10-01 | Dreams（research preview）支持 Opus 5.5 / Fable 5.1 / Sonnet 5.5 | — |

**再往前的 2026-09 事件**：

| 日期 | 事件 | 影响 |
| --- | --- | --- |
| 2026-09-30 | **Claude Sonnet 4.5 正式进入 Deprecated** | 2026-11-30 退役，官方推荐迁移到 Sonnet 5.5 |
| 2026-09-28 | 发布 **Claude Sonnet 5.5**（`claude-sonnet-5-5`），$2 / $10 | 主力位换代；强制 `tool_choice` 返回 400 |
| 2026-09-22 | 发布 **Claude Opus 5.5**（`claude-opus-5-5`），$4 / $20 | 旗舰降价 20%；思考不可关闭，深度改由 `effort` 控制（默认 `medium`） |
| 2026-09-22 | Fast mode（research preview）开放给 Opus 5.5 | $8 / $40 |
| 2026-09-14 | 会话按需压缩（compaction on demand）进 beta | 长会话可主动折叠，保留近期轮次原文 |
| 2026-09-10 | `ant` CLI 1.32.0 可直连 Managed Agents 会话 | 终端里审批 / 跟踪 agent |
| 2026-09-01 | 发布 **Fable 5.1** + **Mythos 5.1** | 缓存读砍到 0.025x（$0.25 / MTok）；Fable 5.1 文本带水印，且强制 30 天数据留存 |
| 2026-08-19 | Computer Use 转正、新增 Browser Use、Files API / Skills 转正 | 一批 beta header 可以摘掉了 |
| 2026-08-10 | Sonnet 5 的 $2 / $10 转正价，原定 9-01 涨到 $3 / $15 **不执行** | 主力价长期锁定 |

> ⚠️ **换代伴随的迁移风险**：**Opus 5.5 / Fable 5.2 / Mythos 5.2 的思考完全不可关闭**——`thinking: {"type": "disabled"}` 与 `{"type": "enabled", ...}` 一律返回 400，只能省略 `thinking` 字段、改用 `effort`。**Sonnet 5.5 是个例外**：它支持 `thinking: {"type": "between_tools"}` 关掉「前置思考」，但仅限 `high` 及以下 effort。`tool_choice` 的 `any` / `tool` 在 Opus 5.5 / Fable 5.2 / Sonnet 5.5 上同样返回 400。**Fable 5.2 还新增前缀校验**：改动 `system` / `tools` / 早期消息后重放 5.2 thinking block 直接 400；且只有 5.2 自身能读 5.2 的 thinking block。**Haiku 4.5 的代码搬到 Haiku 5.5 会直接坏**——`budget_tokens` 形式的手动 extended thinking 返 400，新分词器也让同样文本多约 30% token。**API version `2026-10-21` 起 `temperature` / `top_p` / `top_k` 被移除**，传了返回 400。

**如何跟踪**：

1. **官方源**：[Anthropic News](https://www.anthropic.com/news)、[Claude 模型总览](https://platform.claude.com/docs/en/about-claude/models/overview)、[Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)、[模型退役页](https://platform.claude.com/docs/en/about-claude/model-deprecations)、[Claude Code docs](https://code.claude.com/docs)
2. **更新节奏**：模型大版本约半年一更，2026-09 到 11 月三个月连发五个（5.1 / 5.5 / 5.5 / 5.5 / 5.2）；Claude Code 几乎每周迭代
3. **判断原则**：模型更新看「价格 / 能力 / 上下文」三要素；工具更新看「对现有工作流的破坏性」，破坏性变更优先跟进

## 关键洞察

- **dense 路径在 2026 是少数派**——但 Anthropic 靠"行为稳定 + 安全可控"差异化
- **Agent 是核心壁垒**——Computer Use / Browser Use / Agent SDK / Skills / Hooks 别的厂商没整合好
- **缓存折扣是价格利器**——长 prompt 场景必开，新一代把读取打到 0.025x，Sonnet 5.5 又降到 0.05x
- **Fable 5.2 是补位不是替代**——专门做"长 Agent"赛道；Opus 5.5 是性价比首选
- **换代在加速，破坏性变更在变多**——思考不可关闭、换分词器、Fable 前缀校验都是迁移门槛
- **定价开始分维度**——Haiku 5.5 按 prompt 长度分档，"单一 MTok 单价"这个假设本身在松动

## 参考

- [Anthropic 平台文档](https://platform.claude.com/docs/en/intro)
- [Claude 定价](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)（访问于 2026-11-13）
- [Claude 模型退役与生命周期](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-11-13）
- [Claude Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)（访问于 2026-11-13）
- [Claude Code 模型配置](https://code.claude.com/docs/en/model-config)（访问于 2026-11-13）
- [Claude 产品总览](https://claude.com/product/overview)

- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Claude 模型 · claude-capabilities](/claude-capabilities/models/overview)
- [模型 ID 与定价速查](/claude-capabilities/models/model-ids)
- [Claude Code 精通](/claude-code/)
- [architecture review](/contributing/architecture-review-2026-08-10)

## 下一步

- 看 OpenAI 路线对比 → [OpenAI · GPT 全系](../openai/)
- 看技术架构对比 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 选模型 → [模型选择](/claude-code/basics/model-selection)
- 了解 Fable 5.2 → [Fable 5.2 深度解读](/claude-capabilities/models/fable)
- 对比八家厂商 → [8 厂商横向对比](/ai-trends/model-selection/model-comparison)

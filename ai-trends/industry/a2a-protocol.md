---
title: A2A 协议行业深度调研
description: Agent2Agent 协议截至 2026-10 的规范现状、治理归属、行业采纳、竞品格局、能力缺口与落地建议
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-19
verifiedWith:
  sources:
    - name: A2A Protocol Specification（官方规范一手来源）
      url: https://a2a-protocol.org/latest/specification/
      accessedAt: 2026-10-19
    - name: A2A Protocol 官方文档站
      url: https://a2a-protocol.org/
      accessedAt: 2026-10-19
    - name: Agentic Commerce Protocol（AP2）
      url: https://agenticcommerceprotocol.info/standards/ap2
      accessedAt: 2026-10-19
---

# A2A 协议行业深度调研

> **TL;DR**：A2A 已经拿下了「Agent 之间怎么说话」的**事实标准**地位——Linux Foundation 治理、150+ 组织背书、六语言官方 SDK、三家云厂商产品化。但它的采纳是**平台层热、开发者层冷**：几乎没有任何 coding harness 或 agent 框架原生支持，安全审计也在持续暴露结构性缺陷。真正的行业共识不是「A2A 赢了」，而是「A2A 是底座协议，上面还要叠支付、信任、行业域协议三层」。

⏱ 预计阅读时间：18 分钟

## 你能在这里学到

- A2A 的规范现状：核心对象、五状态任务机、v1.0 的破坏性变更到底改了什么
- 治理与时间线：从 Google 项目到 Agentic AI Foundation（AAIF）的完整脉络
- 采纳的真实分布：哪些厂商真做了、哪些只是挂名，以及开发者层的采纳空白
- 竞品全景：MCP / ANP / ACP / AG-UI / AP2 / A2A-T / ACT 各自占哪一层，为什么是叠加不是替代
- 能力缺口与安全风险：Agent Card 信任链、人审语义、不透明执行
- 企业侧落地的分层策略与常见工期预期的现实评估

## 前置知识

- 了解 [MCP（Model Context Protocol）](./trends) 的基本定位即可，本文不重复讲工具调用层
- 不需要读过 A2A 规范原文，关键定义本文都会给

---

## 一、五个核心判断

先给结论，后面逐条展开。

### 判断 1：标准之争已经结束，但赢家不是「一统」

Google 2025-04 发布、2025-06 捐给 Linux Foundation；IBM 在 2025-08 放弃了自家的 Agent Communication Protocol 并把工程师并入 A2A 的技术指导委员会。**一年之内，主要竞争者选择了合并而不是对打。** [来源: Agent2Agent (A2A) Protocol | Tom Rochette | tomrochette.com | 2026-09-13]

到 2026-08-27，A2A 作为 Growth Stage 项目进入 AAIF，与 MCP、goose、AGENTS.md 同门治理。这意味着 A2A 在「谁来定义 Agent 互操作」这个问题上已经没有了体制内的对手。

### 判断 2：采纳集中在平台层，开发者层几乎空白

支持度高度集中在**企业套件与云平台**：Microsoft（Azure AI Foundry、Copilot Studio）、AWS（Bedrock AgentCore Runtime）、Google（Gemini Enterprise）、Salesforce（Agentforce）、IBM（watsonx Orchestrate）、SAP（Joule）。

但反过来看：**在主流 coding harness / agent 工具里，没有一个原生说 A2A**，最接近的接触点只是 Gemini CLI 上社区拼装的远程 A2A agent 接入。[来源: Agent2Agent Protocol (A2A) | Tom Rochette | tomrochette.com | 2026-09-13]

这是理解 A2A 现状最重要的一条：**A2A 是「平台之间」的协议，不是「开发者之间」的协议。**

### 判断 3：国内跑的是并行的另一套，不是开源 A2A

中国厂商没有把宝押在开源 A2A 上，而是各自做了协议层：

| 协议 | 主导方 | 定位 |
| --- | --- | --- |
| **A2A-T**（Agent-to-Agent for Telecom） | 华为 + 中国移动 + Orange + AIS | 电信自智网络域的 Agent 协同，已进 TM Forum 标准体系 |
| **AHA**（Agent Hub Access） | 支付宝 | 跨终端（手机 / 车机 / 眼镜）多智能体互联 |
| **ACT**（Agentic Commerce Trust Protocol） | 支付宝 + IIFAA 联盟 | 智能体支付与信任，已出 2.0 |
| **APASS** | 蚂蚁集团 | 智能体商业活动的信任基础设施 |
| **OpenAN** | 中国移动 + 华为 + 中兴（LFN） | A2A-T 的开源实现与增强，2026-06 发布 |

这些协议普遍**兼容或引用 MCP / A2A**，但语义层是自研的。[来源: 支付宝发布国内首个智能体商业底座 | 中证网 | 2026-08-17；华为 A2A-T 开源计划 | 中国通信新闻网 | 2026-03-01]

### 判断 4：最大的风险不在协议设计，在信任链和安全实现

v1.0 之前 Agent Card 默认**无签名**，任何人可以伪造一张名片把对端 agent 引导到恶意端点。v1.0 加入 JWS 签名缓解了这一点，但下游实现的安全性并不随规范自动获得。

已有安全机构对 A2A 做专项审计并列出 10 个缺陷，Red Hat、Palo Alto、Semgrep、Trustwave 四家独立确认；v1.0 发布后不久，官方 A2A 示例项目被曝出 9.8 分 CRITICAL 的远程代码执行漏洞（CVE-2026-47391）。[来源: AI 之间开始"打电话"了，但没人装防盗门——A2A 协议安全的深度解剖 | 2048ai.net | 2026；可信度中——二手中文分析，未逐条回溯原始审计报告]

### 判断 5：企业侧的正确姿势是「域内自建统一 + 对外兼容 A2A」

A2A 的协议覆盖面不足以独立支撑一套多 Agent 体系（详见第七节）。但它的 **Agent Card 自描述 + JSON-RPC over HTTP(S) + Task 状态机**这三件套是值得直接借鉴的抽象。**先按这三个抽象做域内统一，再把对外边界做成 A2A 兼容层**，比一上来就全量对齐开源协议成本低得多。

---

## 二、A2A 是什么：把规范读薄

A2A 是一个**应用层协议**，跑在已有的 Web 技术栈上（HTTP / JSON-RPC 2.0 / SSE / Webhook / TLS）。它没有重造传输，这是它能快速落地的原因——一个 Agent 协议如果自己造一套可靠传输，等于退回 1980 年重写 TCP。

> [!info] 官方规范一手核对（2026-10-19 访问 https://a2a-protocol.org/latest/specification/）
> 许可 Apache-2.0，版权方 The Linux Foundation；官方 SDK 覆盖 **Python / Go / Java / JavaScript / .NET / Rust** 六种语言；发现地址为 `.well-known/agent-card.json`；版本协商走 HTTP Header `A2A-Version`（格式 `Major.Minor`，不支持时返回 `VersionNotSupportedError`）；扩展协商走 `A2A-Extensions`（逗号分隔的扩展 URI）。

### 2.1 五个核心对象

| 对象 | 作用 | 关键字段 |
| --- | --- | --- |
| **Agent Card** | 智能体的自描述名片，声明「我能做什么、怎么调我」 | `name`、`description`、`version`、`skills[]`、`capabilities`、`securitySchemes`、`supportedInterfaces[]` |
| **Task** | 被委派的工作单元，有完整生命周期 | `id`、`contextId`、`status`、`artifacts[]`、`history[]` |
| **Message** | 一次通信的内容载体 | `role`、`parts[]`、`taskId`、`contextId` |
| **Part** | 消息的内容片段 | v1.0 后 text / data / file 三种，靠 **JSON 成员名本身**做判别 |
| **Artifact** | 任务产出的结果，可增量追加 | `artifactId`、`parts[]`、`name` |

Agent Card 的 `supportedInterfaces` 数组声明支持的协议绑定与服务地址，**数组第一项为首选**——调用方拿到名片就知道该往哪个地址、用什么方式、以什么身份发任务。

### 2.2 五状态任务机

```
submitted → working → completed
                 ↓        ↘
          input-required   failed
                 ↓
              （补充输入后回到 working）
```

`input-required` 是「需要补充信息时暂停、等人类介入」的状态。**这个状态是 A2A 里唯一的人审钩子，也是最大的语义缺口**（见第七节）。

### 2.3 三种传输绑定

| 绑定 | 用途 |
| --- | --- |
| **JSON-RPC 2.0 over HTTPS** | 默认主通道 |
| **gRPC** | 企业级低延迟场景（v0.3 引入） |
| **HTTP + JSON / REST** | 对已有 REST 生态最友好 |

另有三种结果投递方式：SSE 流式推送、Webhook 异步回调（分钟到天级长任务）、轮询 `tasks/get`。

### 2.4 v1.0 改了什么（对已有实现影响最大）

> [!warning] v1.0 的 `kind` 判别符移除是**破坏性变更**
> v0.3.x 用内联 `kind` 字段做多态判别：
> ```json
> { "kind": "text", "text": "Hello" }
> { "kind": "file", "file": { "name": "a.png", "mimeType": "image/png", "fileWithBytes": "iVBOR..." } }
> ```
> v1.0 改为**用 JSON 成员名本身做判别符**：
> ```json
> { "text": "Hello" }
> { "raw": "iVBOR...", "filename": "a.png", "mediaType": "image/png" }
> ```
> 受影响的还有 `DataPart`（`{"data": {...}, "mediaType": "application/json"}`）和两个流式事件类型（`statusUpdate` / `artifactUpdate` 包装）。规范给出的迁移策略是：客户端**立即**用新名字，服务端在过渡期**可以**同时接受两种形态、响应只发新形态。[来源: A2A Protocol Specification, Appendix A.2.1 | 2026-10-19]

v1.0 的其他关键变化：

- **应用层与传输映射分离**，JSON-RPC 与 gRPC 表示更贴近
- **签名 Agent Card**：JWS（RFC 7515）+ JSON Canonicalization（RFC 8785），对应 `AgentCardSignature` 对象
- **多租户**：一个端点承载多个逻辑 Agent，SaaS 场景刚需
- **`tasks/list`**：支持游标分页与过滤
- **OAuth 2.0 现代化**：移除 implicit / password 流程，加入 device code 与 PKCE
- **扩展机制**：可通过 `A2A-Extensions` 声明新增数据、需求、RPC 方法与状态机

规范同时保留了 Appendix A 的迁移映射表，并明确要求所有 legacy 名称与文档锚点在声明的最早移除版本之前保持可解析——这一点比很多协议做得好。

---

## 三、治理与时间线

| 日期 | 事件 |
| --- | --- |
| 2025-04-09 | Google 在 Cloud Next '25 发布 A2A，宣布 50+ 合作伙伴（Atlassian、Box、Cohere、Intuit、LangChain、MongoDB、PayPal、Salesforce、SAP、ServiceNow、UKG、Workday + Accenture / BCG / 麦肯锡等集成商） |
| 2025-06-23 | 捐赠给 Linux Foundation（Open Source Summit NA, Denver）；创始成员 AWS、Cisco、Microsoft、Salesforce、SAP、ServiceNow |
| 2025-07-30 | 规范 v0.3.0：发现地址从 `agent.json` 改为 `agent-card.json`，加入 Agent Card 签名 |
| 2025-08 | **IBM 放弃 ACP，工程师并入 A2A 的 TSC** |
| 2025-09-16 | Google 发布 AP2 支付协议（60+ 组织共建），设计为 A2A + MCP 的扩展 |
| 2025-12-09 | Linux Foundation 成立 **Agentic AI Foundation（AAIF）**，创始项目为 MCP、goose、AGENTS.md——**A2A 此时尚未入库** |
| 2026-03-12 | 规范 v1.0.0 发布（GitHub release 记录） |
| 2026-04 | Linux Foundation 周年数据：支持组织从 2025-04 的 50+ 涨到 **150+** |
| 2026-04-28 | AP2 所有权移交 **FIDO Alliance**，保持平台中立 |
| 2026-05-28 | 规范 v1.0.1（HTTP binding 与规范修复，无新特性） |
| 2026-08-27 | **A2A 正式加入 AAIF**，与 MCP 同门治理 |

> [!info] v1.0.0 日期存在来源冲突
> 第三方页面（thirdbrain.tech、tomrochette.com）标注为 **2026-03-12**，理由是「已对照 GitHub release 确认」；而 alicelabs.ai、replyant.com 等页面标注为 **2026-04**（replyant 更精确到 04-23）。两者相差约六周。本文采信 03-12（有一手 release 记录的说法更可信），但**建议实际引用前到 [GitHub Releases](https://github.com/a2aproject/A2A/releases) 再核一次**。[待验证]

治理主体是来自 AWS、Cisco、Google、IBM Research、Microsoft、Salesforce、SAP、ServiceNow 八家的技术指导委员会（TSC）。AAIF 的加入意味着 A2A 的规范演进从此与 MCP 在同一个基金会框架下并行——**这意味着未来 A2A 与 MCP 的边界会持续被重新讨论，而不是各管一层互不干涉。**

GitHub 主仓库 star 数在 2026 年内的量级：约 21.9k（2026-03）→ 25.7k（2026-09）→ 约 26k（2026-10）。作为对照，MCP 的量级约为 A2A 的 2.4 倍——**MCP 赢下了工具调用层，A2A 正在赢它上面那层**。[来源: Agent2Agent Protocol v1 2026 | spillwave.com；Agent2Agent (A2A) Protocol | tomrochette.com | 2026-09-13]

---

## 四、行业采纳：平台层热，开发者层冷

### 4.1 国际厂商

| 厂商 | 产品 / 集成 | 性质 |
| --- | --- | --- |
| Microsoft | Azure AI Foundry、Copilot Studio | 平台级产品化 |
| AWS | Amazon Bedrock AgentCore Runtime | 运行时 |
| Google | Gemini Enterprise、ADK（原生支持，与 A2A 共同开发） | 平台 + SDK |
| Salesforce | Agentforce | 企业套件 |
| IBM | watsonx Orchestrate | 企业套件 |
| SAP | Joule | 企业套件 |

⚠️ 注意：Linux Foundation 的 150+ 组织数据里，**没有区分 GA 与 Preview**，也没有区分「产品集成」与「联合发布声明」。这个数字适合用来说明势能，不适合用来说明生产环境部署量。[来源: thirdbrain.tech 对 LF 周年发布稿的核对]

### 4.2 生态规模的一个参照

第三方统计口径：A2A 相关 agent 约 **180+**（2026-08），而 MCP server 约 **4200+**。同一口径下 MCP 的成熟度被评估为 production-ready，A2A 仍处于「v1.0 刚落地、试点为主」的阶段。[来源: archparse.com | 可信度中——数据来源未披露，量级可参考，具体数字不宜引用]

### 4.3 国内厂商（另起炉灶）

**支付宝 / 蚂蚁**是最激进的一个。2026-08-17 AI 生态合作伙伴大会上发布：

- **AHA（Agent Hub Access）** 多智能体跨端互联协议体系，含智能交互协议（Skills Interface Standards）、智能体互联协议、设备感知与执行协议（X User Interface）三层
- 联合千问、华为、OPPO、vivo、小米、荣耀、比亚迪、吉利、理想、蔚来、阶跃星辰、Rokid 等 20 余家共建互联生态
- 落地数据：与 5 家主流手机厂商打通跨端协同（合作厂商份额超 70%），车端覆盖 16 家车企品牌，与 60 余家车企达成定点；OPPO 接入后支付宝在 OPPO 手机活跃度新增 200 多万
- 平台层面明确基于 **MCP + A2A** 推出 AHA 方案，同时自建 **ACT 2.0**（智能体商业信任协议，IIFAA 联盟）
- 「阿宝」已完成万余项服务智能化适配，覆盖出行、餐饮、文旅、政务民生八大场景

**荣耀 YOYO × 支付宝阿宝**是一个具体的跨端调用样本：用户在 YOYO 上说「查一下公积金缴存明细」，YOYO 识别意图后唤起阿宝，在支付宝侧完成查询并以服务卡片回呈。[来源: 智能体走向互联，协作如何更可靠？ | 中国通信新闻网 | 2026-10-15]

**华为 / 中国移动（A2A-T）**走的是垂直行业标准路线，落地数据最实：

- 2026-02-06 由华为、中国移动、Orange、AIS 等在 TM Forum Accelerate Week 联合发布，含 IG1453 beta 版及增强版提示词元模型 IG1453A
- MWC 2026 期间启动配套软件开源：SDK + 注册中心（认证、寻址、技能管理）+ 编排中心（低代码/无代码工作流编排）
- 中国移动福建移动现网试点：故障诊断场景下**无线工单数量压降 30%，平均修复时间从 3 小时缩短至 2.03 小时**
- 2026-06 中国移动携手华为、中兴在 LFN 发布 OpenAN，A2A-T 的开源实现与增强

A2A-T 的设计动机值得一提：Fierce Network 提出的「**混沌智能体理论**」——成千上万分属不同供应商、分辖无线/传输/云/安全/能源的专业智能体共处一张网络，各自行为合理但相互作用易形成反馈回路与不可预知的涌现行为。A2A-T 被类比为「智能体决策间的 CSMA/CD」。[来源: 从"定义能力"到"定义协作"，A2A-T 有望成为自智网络通用语言 | 中国通信新闻网 | 2026-07-13]

---

## 五、竞品与相邻协议全景

**核心认知：这些协议是叠加关系，不是替代关系。** 按层看会清楚很多。

```
┌─────────────────────────────────────────────┐
│  前端交互层    AG-UI（CopilotKit）             │  agent ↔ UI 流式
├─────────────────────────────────────────────┤
│  协作层        A2A ★                          │  agent ↔ agent 任务委派
│                A2A-T（电信域）/ AHA（跨端）    │  垂直域变体
├─────────────────────────────────────────────┤
│  身份层        ANP / APASS                    │  跨组织去中心化身份
├─────────────────────────────────────────────┤
│  能力层        MCP ★                         │  agent ↔ 工具/数据
├─────────────────────────────────────────────┤
│  支付层        AP2 / ACT                      │  agent ↔ 交易
└─────────────────────────────────────────────┘
```

### 5.1 五协议对照

| 维度 | MCP | A2A | ANP | ACP | AG-UI |
| --- | --- | --- | --- | --- | --- |
| 发起方 | Anthropic | Google | ANP Working Group（社区） | IBM / BeeAI | CopilotKit |
| 时间 | 2024-11 | 2025-04 | 2025 | 2025 | 2025 |
| 核心目标 | agent ↔ 工具 | agent ↔ agent 任务委派 | 跨组织去中心化身份 | 带状态的多 agent 协作 | agent ↔ 前端流式 |
| 传输 | stdio / Streamable HTTP | HTTP + JSON-RPC 2.0 | HTTP / P2P + JSON-LD | HTTP + JSON | HTTP/SSE、WebSocket |
| 发现 | server manifest | Agent Card | DID 解析 | agent descriptor | 嵌入，无独立发现 |
| 治理 | Linux Foundation | Linux Foundation（AAIF） | 社区 | **已并入 A2A** | 社区 |

> [!note] MCP 传输的一个易错点
> MCP 早期有独立的「HTTP+SSE」传输（客户端单向收 SSE），现行 spec 已被 **Streamable HTTP** 取代——单次 POST + 可选请求作用域内的 SSE 流。说「MCP 用 SSE 传输」不准确，SSE 只是回传增量结果的一种承载方式。[来源: 我在理解智能体通信协议时，发现了 MCP 的关键作用 | 51CTO | 2026]

**ACP 的合并是这段历史里最重要的一条**：IBM 放弃自有协议并把工程师送进 A2A 的 TSC，等于承认「Agent 通信协议」这个位置只有一个。剩下的是**分层**，不是**竞争**。

### 5.2 支付层：AP2 与 ACT

| 协议 | 发起方 | 治理 | 关键设计 |
| --- | --- | --- | --- |
| **AP2**（Agent Payments Protocol） | Google（2025-09-16，60+ 组织含 Mastercard / PayPal / Amex / Adyen / Coinbase） | **2026-04-28 移交 FIDO Alliance** | 设计为 A2A + MCP 的扩展；可验证凭证（mandates）承载用户意图；覆盖卡 / 稳定币 / 实时银行转账；加密支付走 A2A 的 x402 扩展；v0.2 增加 Human Not Present 支付 |
| **ACT**（Agentic Commerce Trust Protocol） | 支付宝 + IIFAA 联盟等 20 余家 | 国内联盟 | 2.0 已发布；构建智能体支付能力框架与信任机制 |

AP2 移交 FIDO 是个信号：**支付协议必须脱离单一厂商，否则跨网络就走不通。**

### 5.3 一句话结论

> MCP 标准化 agent 怎么用工具，A2A 标准化 agent 怎么把活派给另一个 agent，ANP 标准化不同组织的 agent 在没有共享 broker 的情况下怎么互认身份。
> **三者会同时跑，按需分层叠加。** 你几乎不会「选一个协议而不是另一个」。[来源: How to Choose Between MCP, A2A, and ANP | Atlan | 2026]

---

## 六、开源生态支持度：这是最大的短板

这是很多选型调研低估的一块。**「协议统一了」不等于「生态支持了」。**

### 6.1 支持度分级

| 框架 | A2A 支持形态 | 等级 |
| --- | --- | --- |
| **Google ADK** | 原生。A2A 共同开发产物：agent 可直接暴露为 A2A server、提供 A2A client 工具、Agent Card 从 ADK 配置自动生成，支持流式 / 多轮 / push notification | ✅ 原生 |
| **LangGraph / LangChain** | 需 adapter。`invoke`/`stream` 映射到 `message/send`/`message/stream`，graph state 映射到 task state，**LangGraph 的 interrupt 映射到 A2A 的 `input-required`** | ⚠️ 适配 |
| **CrewAI** | 需包装。可把单个 crew member 暴露为 A2A agent，或把整个 crew 包成一个 | ⚠️ 适配 |
| **Microsoft AutoGen** | **进入维护模式**，功能并入 Microsoft Agent Framework 1.0（2026-04-03 发布） | ⚠️ 迁移中 |
| **OpenAI Agents SDK** | 未见原生 A2A server 暴露 | ❓ 未确认 |
| **先于 A2A 出现的项目**（OpenClaw 等） | 需第三方网关 | ❌ 需桥接 |

[来源: A2A Framework Integration | GitHub（OrcaQubits/agentic-commerce-skills-plugins）；Microsoft Agent Framework 1.0 发布信息 | spillwave.com | 2026]

以 OpenClaw 为例，社区提供的 A2A 接入方式是 `win4r/openclaw-a2a-gateway` 这类独立网关项目，需要自行 clone、安装、配置 `a2a.config.json`、在每个 agent 侧装 a2a-client SDK、手写能力声明——**官方文档自己给的耗时估算是 45–90 分钟**，且明确列出了「未声明能力」「循环委派」等常见故障。[来源: OpenClaw A2A Gateway | aiagentspedia.org | 可信度中——第三方集成站，描述的是社区项目而非官方支持]

### 6.2 为什么会这样

A2A 是 2025-04 才出现的东西，而今天主流的 agent 框架、harness、编排工具大多在这之前就已经有了自己的多 agent 通信方式。**协议晚于生态，就得反向适配生态**，而 A2A 官方能提供的只有 SDK 和 sample，没有「一键接入」。

这条结论对企业落地的直接含义：**不要指望「支持 A2A」能成为一个开源项目的加分项去推动生态，先假设所有东西都需要你写适配层。**

---

## 七、能力缺口与风险

这一节是本次调研最有价值的部分。

### 7.1 信任链薄弱：Agent Card 默认无签名

Agent Card 是整个发现机制的根。它的安全问题会沿着整条链路放大：

- 没有 `AgentCardSignature` 验证 → 任何人都能发布一张声称自己是任意 agent 的名片，把对端引导到恶意端点（**冒充**）
- 卡片描述进入对端 agent 的上下文 → 恶意描述即提示注入载体（**上下文投毒**）
- 无重放保护 → 截获的调用可重复执行（**重放攻击**）

v1.0 加了 JWS 签名解决「谁签发的」，但规范本身的措辞是 **SHOULD** 而非 **MUST**：

> "Clients **SHOULD** verify signatures when present to ensure the Agent Card has not been tampered with" —— A2A Protocol Specification §14.3

**「存在时」才验证** = 不签名也不违规。加上 Extended Agent Card 走认证端点、含更多敏感信息，信任模型实际上是分裂的。

### 7.2 安全审计与已知漏洞

- **审计**：v1.0 发布前一个月，安全机构 Grith 的首次重大审查给出 **10 个缺陷**，Red Hat、Palo Alto、Semgrep、Trustwave 四家公司独立确认
- **官方示例 RCE**：v1.0 发布后不久，一个官方 A2A 示例被曝出 **9.8 分 CRITICAL 的远程代码执行漏洞**（CVE-2026-47391）

⚠️ 上述两条来自二手中文技术分析文章，**未逐条回溯原始审计报告与 CVE 记录**。[待验证——如需在正式材料中引用，请直接核对 Grith 原始报告与 NVD]

安全设计上的结构性问题可归纳为三条：

1. **不透明执行（Opaque Execution）**——委派出去后看不到对方到底怎么干的，无法观测、无法审计
2. **无内容监控**——协议层没有任何机制能检测或阻止恶意行为
3. **无人在环确认**——协议本身没有「您确定要执行吗」这一环的强制语义

### 7.3 人审语义缺失（你说的那个点，展开讲）

A2A 里唯一的人审钩子是任务状态 `input-required`。但规范只定义了这个**状态**，没有定义围绕它的**语义**：

- 谁是人？`input-required` 之后是人直接回复，还是回到调用方 agent 的模型让它决定？
- 人确认的是什么？如果确认发生在 UI 层，执行发生在 agent 层，**「审批对象」和「执行对象」之间就存在一个可被替换的缝隙**

这个缝隙不是理论问题。2026-09-17 一篇 arXiv 论文（Loopjacking: Hijacking Human-in-the-Loop Approval）做了实验：

- 在 Agno AgentOS 上，管理员审批了一笔 **20 单位**的转账，随后工具实际收到并执行了 **2000 单位**的转账——**屏幕上是 20，实际执行是 2000，倍数 100，使用的是管理员的授权**
- 论文报告在 Agno 7 个已发布版本（至 3.0.9）、每个版本 5 次攻击全部成功（35/35）；LangGraph Agent Server 上 12 个版本（至 0.14.0）同样复现

⚠️ **必须说明的边界条件**：这是实验室结果，受测产品是刻意挑选的，账本是 mock，凭据是合成的，流量未离开 loopback，「人」是脚本。作者明确表示结果**不能估算生态普遍性**。LangGraph 的结果还依赖一个「允许非审批者编辑待审批线程」的授权策略——**这是配置问题，不是协议问题**。目前没有来源报告该攻击被用于真实部署。[来源: Loopjacking: an approval for 20 units released 2,000 | pk-sharma.com | 2026-09-17]

**这个案例真正的意义不是「有漏洞」，而是揭示了一个设计原则**：

> 人审按钮保护的是「你批准的那个动作」，而不是「最终执行的动作」。**如果这两者之间没有不可篡改的绑定，人审在架构上就是无效的。**

### 7.4 其他覆盖不全的场景

| 场景 | A2A 现状 |
| --- | --- |
| 幂等性 | 协议未强制。调用方需自行处理重试与去重 |
| 任务取消 | `tasks/cancel` 存在，但被调用方是否遵守、正在执行的动作能否中断，未定义 |
| 跨任务上下文共享 | `contextId` 提供关联，但无共享记忆语义（设计上是刻意的：不透明执行） |
| 成本 / 计费 | 完全在协议之外（交给 AP2 / ACT） |
| 多 agent 协商与冲突消解 | 无。A2A-T 补的正是这块（见第四节） |
| 可观测性 | 兼容 OpenTelemetry / W3C Trace Context 需自行接入，规范未强制 |

---

## 八、企业侧落地的建议

结合前面七节，给出一套通用的可执行判断。

### 8.1 分层策略

```
对外边界层  ── A2A 兼容（Agent Card + JSON-RPC + Task 状态机）
                ↑ 只在「跨系统、跨团队、跨组织」边界暴露，同域内不强制
域内编排层  ── 自建统一抽象（调用语义、上下文、错误模型）
                ↓
工具接入层  ── MCP 兼容
```

**理由**：A2A 的价值在跨信任边界；同一信任域内的多 Agent 之间属于同一责任主体，用 A2A 会付出「不透明执行」的成本却拿不到收益（因为你本来就可以直接看域内状态）。

### 8.2 借鉴 A2A 的三个抽象（无论用不用 A2A 都值得抄）

1. **Agent Card 自描述**——把「我能做什么、输入输出模态、鉴权方式、版本」结构化成一份可被机器读取的契约。这条在域内同样有效。
2. **Task 五状态机**——把「派活」和「干活」解耦，状态显式化。特别是 `input-required` 的存在本身。
3. **应用层 / 传输层分离**——协议版本与绑定解耦，JSON-RPC / gRPC / REST 可换。这条决定了未来的迁移成本。

### 8.3 必须自己补的四件事（A2A 不管）

| 补什么 | 为什么 A2A 不管 | 建议 |
| --- | --- | --- |
| **人审的强绑定** | 协议只定义状态不定义语义 | 审批票据必须携带被审批动作的不可篡改摘要（参数 hash），执行侧强校验，不匹配即拒 |
| **可观测性** | 不透明执行是设计原则 | 至少贯通 traceId 贯穿委派链路；跨信任边界时明确记录「委派给了谁、何时、什么参数」 |
| **幂等与补偿** | 协议未强制 | 调用侧生成幂等键；跨系统副作用操作走「预留—确认—释放」而非直接执行 |
| **协议版本协商与灰度** | 有 `A2A-Version` 但无迁移治理 | 对外暴露时明确支持版本矩阵，平台侧 SDK 与对外适配层解耦 |

### 8.4 关于「两周 MVP」的工期预期

业界常见「两周出一个能跑的 A2A 接入」的承诺。这个预期是否成立，取决于把范围切在哪。以下判断供参考：

**两周可信的范围**：
- 单个对外端点暴露（JSON-RPC + Agent Card 静态托管）
- Agent 注册与发现（自建注册中心，或直接依赖 Agent Card 直连）
- 基本的鉴权透传（Bearer token）
- `send` + `get` 两个核心方法

**两周不可信的范围**：
- 完整三绑定（JSON-RPC + gRPC + REST）
- 流式（SSE）+ 长任务 webhook + 断线重连
- 签名 Agent Card 的签发与校验链路
- 人审闭环（这是最容易被低估的一块）
- 与外部存量系统完成真实联调

建议把对外承诺拆成**「可发现 + 可调用 + 可鉴权」**三档，先交第一档。

---

## 九、信息缺口与待验证

本次调研未解决、建议后续补齐的问题：

| # | 缺口 | 建议动作 |
| --- | --- | --- |
| 1 | **企业内部自建 A2A 变体的具体定义**（协议形态、覆盖场景、与开源 A2A 的差异） | 需组织内部信息源访谈，本报告完全无法覆盖 |
| 2 | v1.0.0 精确发布日期（03-12 vs 04-23 来源冲突） | 核对 [GitHub Releases](https://github.com/a2aproject/A2A/releases) |
| 3 | Grith 审计 10 个缺陷的原始清单与逐条状态 | 查阅 Grith 原始报告 |
| 4 | CVE-2026-47391 的官方通告与影响范围 | 查 NVD / GitHub Advisory |
| 5 | OpenAI Agents SDK、CrewAI 等对 A2A 的**官方**支持状态 | 查各框架官方文档站（当前仅有第三方集成站信息） |
| 6 | 150+ 组织中 GA / Preview 的分布 | 需逐个查厂商发布说明 |
| 7 | AGNTCY Agent Directory（基于 OASF）在发现层的实际使用率 | 查 Cisco 侧项目状态 |
| 8 | 国内厂商（支付宝 / 华为）与开源 A2A 的**协议级**兼容程度 | 需读 AHA / A2A-T 规范原文 |
| 9 | A2A 与 MCP 在 AAIF 同门治理后的边界演变 | 持续跟踪 TSC 会议记录 |

---

## 参考

**一手来源**

- [A2A Protocol Specification（官方规范）](https://a2a-protocol.org/latest/specification/)（访问于 2026-10-19）
- [A2A Protocol 官方文档站](https://a2a-protocol.org/)（访问于 2026-10-19）
- [a2aproject/A2A GitHub 仓库](https://github.com/a2aproject/A2A)（访问于 2026-10-19）
- [What is the Agent Payments Protocol (AP2)?](https://agenticcommerceprotocol.info/standards/ap2)（访问于 2026-10-19）

**二手分析与对照**

- [Agent2Agent (A2A) Protocol](https://tomrochette.com/agents/a2a) | Tom Rochette | 2026-09-13 —— 事实核对型页面，可信度较高
- [Agent2Agent (A2A) protocol](https://www.thirdbrain.tech/KB-AI/ai-agentic-systems/protocols-and-standards/a2a-protocol) | 2026-10-10 —— 含 LF 周年数据核对
- [A2A Protocol Guide 2026](https://alicelabs.ai/en/insights/a2a-protocol-guide-2026) | Alice Labs | 2026-09-18
- [2026年AI智能体互操作协议大比拼：MCP、A2A、ANP、ACP谁主沉浮？](https://devpress.csdn.net/awstech/6a7c7ac110ee7a33f29a02f2.html) | CSDN DevPress
- [Survey: Agent Communication Protocols in 2026](https://openstandardagents.org/research/agent-communication-protocol-survey/) | OSSA
- [A2A Protocol v1 2026: How AI Agents Actually Talk to Each Other](https://spillwave.com/writing/a2a-protocol-v1-2026-how-ai-agents-actually-talk-to-each-other) | Spillwave
- [Loopjacking: an approval for 20 units released 2,000](https://www.pk-sharma.com/briefing/loopjacking-human-approval-binding) | 2026-09-17 —— 明确标注了实验边界条件，可信度较高
- [AI 之间开始"打电话"了，但没人装防盗门——A2A 协议安全的深度解剖](https://2048ai.net/6a8d5043662f9a54cba045a4.html) | 2048ai.net | **可信度中——未回溯原始审计报告**

**国内产业报道**

- [智能体走向互联，协作如何更可靠？](https://www.cnii.com.cn/rmydb/202610/t20261015_764403.html) | 中国通信新闻网 | 2026-10-15
- [从"定义能力"到"定义协作"，A2A-T有望成为自智网络通用语言](https://www.cnii.com.cn/rmydb/202607/t20260713_748572.html) | 中国通信新闻网 | 2026-07-13
- [MWC 2026丨华为将宣布A2A-T软件开源计划](https://www.cnii.com.cn/rmydb/202603/t20260301_722508.html) | 中国通信新闻网 | 2026-03-01
- [支付宝发布国内首个智能体商业底座](https://jnzstatic.cs.com.cn/zzb/htmlInfo/130283.html) | 中证网 | 2026-08-17
- [技术加速赋能实体经济 支付宝AI开放平台推动智能体商业落地](http://tech.ce.cn/xx/202607/t20260707_3073548.shtml) | 中国经济网 | 2026-07-07

## 下一步

- 看趋势分析框架 → [行业趋势](./trends)
- 看生态层面的其他动向 → [投融资动态](./funding)
- 看 AI Native 研发范式 → [AI Native 三层架构](../../ai-harness/three-layer-architecture)

---
title: Moonshot · Kimi 全系
description: Kimi K3 / K2.7 Code / K2.6——2.8T MoE 架构、1M 长上下文、中文长文档分析
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: Kimi 开放平台 · 官方定价
      url: https://platform.moonshot.cn/docs/pricing/chat
      accessedAt: 2026-09-30
    - name: Kimi 开放平台 · 平台新功能发布记录
      url: https://platform.moonshot.cn/docs/changelog/index
      accessedAt: 2026-09-30
    - name: Kimi K3 官方模型文档
      url: https://platform.moonshot.cn/docs/guide/kimi-k3-quickstart
      accessedAt: 2026-09-30
---

# Moonshot · Kimi 全系

> 7 家厂商里**开源权重规模最激进（K3 为 2.8T，全球首个 3 万亿级开源模型）+ 中文长文档分析标杆**；当前旗舰上下文为 1M。

## 一、公司背景

Moonshot AI（月之暗面）2023 年由清华系创业者杨植麟创办，总部北京。核心定位是**"长上下文 + 中文场景"**——从 128K 起步，一路扩到千万 token 级别，是中文用户处理长文档 / 长视频的首选。商业模式：Kimi Web/App 免费 + API 付费 + 企业定制。

## 二、模型矩阵

官方定价页当前只列四个在售模型名（截至 2026-09-30）：

| 模型 | 时间 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **Kimi K3** | 2026-07 上线 | 旗舰 | 1M（1,048,576） | `reasoning_effort` low / high / max | 长程编程 / 知识工作 / 深度推理 / **视觉理解** |
| **Kimi K2.7 Code** | 2026-06 上线（含高速版） | 编程 / 多模态专精 | 256K | 思考模式 | 编程、工具调用 |
| **Kimi K2.6** | 2026-04 上线 | 上一代通用 | 256K | 思考模式 | 文本 / 图片 / 视频理解 |
| ~~Kimi K2.5~~ | — | **已全平台下线** | — | — | 2026-08 国内外下线，调用返回 404，需迁移 K3 |
| ~~Kimi K2 全系列~~ | — | **已正式下线** | — | — | 2026-05 停止维护 |

> **产品线逻辑**：K3 做旗舰（2026-07 上线开放平台 API，2.8T 参数，权重已发布），K2.7 Code 做编程专精，K2.6 做便宜的通用档。K2.5 与 K2 全系已先后退出，**不要再按「K2.5 是上一代」来规划**——它已经调不通了。

## 三、技术架构

**MoE 架构** —— K3 在 896 个专家中激活 16 个（Stable LatentMoE 框架），是当前在售模型里专家数最多的。官方称相比 K2 整体扩展效率提升约 2.5 倍。

> ⚠️ 旧版 K2 系列的「384 专家 / 激活 8」为历史口径，K2 已于 2026-05 下线，且该数字本次未从官方文档复核。

**KDA 混合线性注意力** —— K3 基于 **KDA（Kimi Delta Attention）混合线性注意力 + 注意力残差（Attention Residuals）** 构建，这是与 K2 最大的架构差异，目标是让信息在更长序列和更深模型中流动更顺畅。K3 官方技术报告截至 2026-09-30 尚未随模型页公布。

**1M 长上下文** —— 当前旗舰 K3 为 100 万 token。K2-0905 曾扩到 2M token（当时是 7 家厂商中最长），但**该档位随 K2 全系于 2026-05 下线**，目前无法调用。

**K2 Thinking（RLVR）** —— 和 OpenAI o-series 同路线：用可验证奖励（数学答案对错、代码单测通过率）训练推理能力。**K2 Thinking 在中文数学 / 代码基准上追平 o1**（历史结论，K2 Thinking 亦已下线；当前对应能力由 K3 的 `reasoning_effort` 承担）。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Tool Use** | 函数调用 / JSON Schema | Kimi API |
| **Deep Research** | 多步搜索 + 长文档分析 | Kimi Web 内置 |
| **文件解析** | PDF / Word / PPT 直接解析 | Kimi Web + API |
| **多模态** | 图片 / 视频理解 | **K3 原生**、K2.6 原生 |
| **长视频** | 视频理解 | K2.6；K3 支持视觉理解 |

**文件解析是 Kimi 差异化** —— 直接上传 PDF/Office 文件，Kimi 解析后在 1M context 内分析。Claude 需要先用 Files API 上传，GPT 需要 Code Interpreter。

> ⚠️ 2026-08 Files API 有破坏性变更：文件 ID 统一加 `file_` 前缀；**不再对图片做 OCR 文本提取**，图片理解需改用 `purpose=image` 上传。依赖旧行为的流程需要改。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **Kimi API** | `api.moonshot.cn/v1` | 直接 API 调用 |
| **Kimi Web/App** | 网页 / 移动端 | 终端用户产品 |
| **K3 权重** | 已开源 | 私有部署 / 微调 |
| **K2 权重** | 已下线 | 历史，Apache 2.0 |

**K3 已开源** —— 官方模型页称「完整模型权重已发布」，是月之暗面最新开源旗舰，也是全球首个达到 2.8 万亿参数规模的开源模型。

> ⚠️ 调用 K3 有门槛：开放平台需**累计充值最低 10 元**才解锁；新用户注册赠送的 15 元代金券**不可用于 K3**。

## 六、价格（截至 2026-09，官方定价，人民币）

官方以**人民币**计价，单位为每 100 万 tokens：

| 模型 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 上下文 |
|------|-------|--------|---------|--------|
| **Kimi K3** | ¥2.00 | ¥20.00 | **¥100.00** | 1,048,576 |
| **Kimi K2.7 Code** | ¥1.30 | ¥6.50 | ¥27.00 | 262,144 |
| **Kimi K2.7 Code 高速版** | ¥2.60 | ¥13.00 | ¥54.00 | 262,144 |
| **Kimi K2.6** | ¥1.10 | ¥6.50 | ¥27.00 | 262,144 |

**K3 独有「缓存写入」计费** —— K3 按 TTL 分两档单独计费：5min 档 ¥20.00 / MTok，1h 档 ¥40.00 / MTok；不指定 TTL 时默认按 5min 档。命中缓存后自动续期且**不再重复收缓存写入费**。长会话场景要留意这一项。

**文件接口限时免费** —— 文件内容抽取 / 文件存储接口本身当前不产生费用。

**K3 定价参考** —— 输出价是 K2.7 Code 的约 3.7 倍、2.6 档的约 3.7 倍，长输出场景成本敏感的话，K2.7 Code / K2.6 更划算。

## 七、适合场景 / 不适合场景

**适合**：
- 长文档分析（PDF / 合同 / 论文，1M 上下文）
- 中文场景（中文基准领先，中文文件解析原生支持）
- 办公自动化（Deep Research + 文件解析组合）
- 中文数学 / 代码推理（K3 的 `reasoning_effort`）
- 需要开源自部署的大规模场景（K3 权重已发布）

**不适合**：
- 英文为主的场景（Claude / GPT 英文更强）
- 极低成本场景（K3 输出价远高于国产同档位）
- 海外部署（Kimi API 主要面向国内）

## 八、最新动态（2026-09）

**三条跟踪线**：

- **模型线**：K3 / K2.7 Code / K2.6 三档。核心看「哪一档是当前旗舰、上下文多长、是否原生多模态」
- **下线线**：**下线比上线更值得盯**。K2.5、K2、`moonshot-v1` 都在 2026 年内彻底退场，迁移成本常被低估
- **产品线**：联网搜索 API、托管智能体（Hosted Agents）、文件与视觉接口的行为变更

**如何跟踪**：

1. **官方源**：[平台新功能发布记录](https://platform.moonshot.cn/docs/changelog/index)（按月归档，最权威）、[官方定价](https://platform.moonshot.cn/docs/pricing/chat)、[Kimi K3 模型页](https://platform.moonshot.cn/docs/guide/kimi-k3-quickstart)
2. **更新节奏**：Kimi 是国产厂商里 changelog 维护最规范的，**按月归档、带日期标签**，排查问题直接翻
3. **判断原则**：先看「下线」再看「上线」。国内厂商里 Kimi 的旧模型退役最激进，生产环境务必锁死 `model` 名并订阅 changelog

**截至 2026-09-30 的具体动态**：

| 时间 | 事件 | 意义 |
| --- | --- | --- |
| 2026-09 | **Kimi 托管智能体（Hosted Agents）Beta 上线** | 基于 Kimi Durable Harness 的 7×24 全托管 Agent 运行环境，沙箱 / 会话 / 失败恢复 / 超时重试全托管；支持控制台、API、`hakimi` 三种用法；多智能体编排、技能与凭据库、跨会话持久记忆。**Beta 当前面向国内企业认证用户** |
| 2026-09 | **联网搜索 API** | `/v1/tools/search` 与 `/v1/tools/search_pro`，返回结构化结果，可自行编排搜索逻辑 |
| 2026-09 | **计费方式调整** | 账户消耗按现金、代金券各 50% 扣除；一类用尽后全额从另一类扣 |
| 2026-08 | **`kimi-k2.5` 与 `moonshot-v1` 全系列全平台下线** | 国内外均下线，调用返回 404，需迁移到 K3 |
| 2026-08 | **Files API 破坏性变更** | 文件 ID 加 `file_` 前缀；文档解析增强；**图片不再做 OCR 提取**，需用 `purpose=image` |
| 2026-07 | **Kimi K3 上线开放平台 API** | 1M 上下文，原生视觉；同期 K2.5 与 `moonshot-v1` 停止向新注册用户开放 |
| 2026-06 | **Kimi K2.7 Code 上线**，随后推出高速版 | 补上编程 / 多模态专精档 |
| 2026-05 | **`kimi-k2` 全系列正式下线** | 含 `k2-0905-preview`、`k2-0711-preview`、`k2-turbo-preview`、`k2-thinking` 等 |
| 2026-04 | Batch API 全量开放；**Kimi K2.6 发布** | 大批量异步推理更便宜 |

> 📌 **两个容易踩的坑**：① 还在用 `kimi-k2.5` / `kimi-k2` / `moonshot-v1` 的代码在 2026 年内会陆续开始报 404，**现在就该排查**；② K3 的「缓存写入」是新计费项，长会话若不规划 TTL，账单会比预期高一截——重复前缀多的场景优先用 1h 档。

## 关键洞察

- **开源规模是核心壁垒** —— K3 的 2.8T / 896 专家是当前开源模型的天花板，权重已发布
- **1M 上下文 + 中文长文档是护城河** —— 中文 OCR、长上下文、文件解析的组合，Claude / GPT 都不如；但**别再引用 2M**，那属于已下线的 K2-0905
- **文件解析是差异化** —— 直接上传 Office / PDF，无需预处理
- **下线节奏比上线更值得跟踪** —— 一年内连砍 K2.5 / K2 / `moonshot-v1` 三条线，迁移要提前做

## 参考

- [Kimi 开放平台 · 官方定价](https://platform.moonshot.cn/docs/pricing/chat)（访问于 2026-09-30）
- [Kimi 开放平台 · 平台新功能发布记录](https://platform.moonshot.cn/docs/changelog/index)（访问于 2026-09-30）
- [Kimi K3 官方模型文档](https://platform.moonshot.cn/docs/guide/kimi-k3-quickstart)（访问于 2026-09-30）
- [Kimi 开放平台文档首页](https://platform.moonshot.cn/docs)
- [Kimi K2 技术报告](https://moonshotai.github.io/Kimi-K2/)（历史，K2 已下线）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Anthropic Claude 对比](/ai-trends/vendors/anthropic/)

## 下一步

- 看国内另一家路线 → [Zhipu · 智谱 GLM 全系](../zhipu/)
- 看横向对比表 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 看长上下文竞品 → [DeepSeek](/ai-trends/cn-vendors/deepseek/)（1M 上下文 + 峰谷定价）
- 看闭源对手 → [字节豆包](/ai-trends/cn-vendors/doubao/)
- 看国外长上下文做法 → [Anthropic · Claude 全系](/ai-trends/vendors/anthropic/)

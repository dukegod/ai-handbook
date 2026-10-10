---
title: 视频生成模型对比
description: 主流 AI 视频生成模型全景——Runway / Kling / Pika / Vidu / 即梦 / MiniMax H3 / CogVideoX / HunyuanVideo 对比与选型（Sora 2 已于 2026-09-24 下线）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-09
verifiedWith:
  sources:
    - name: OpenAI API 废弃说明
      url: https://developers.openai.com/api/docs/deprecations
      accessedAt: 2026-10-08
    - name: OpenAI 视频生成指南(Sora 2)
      url: https://developers.openai.com/api/docs/guides/video-generation
      accessedAt: 2026-10-08
    - name: Runway Dev 官方模型目录
      url: https://docs.dev.runwayml.com/guides/models
      accessedAt: 2026-10-08
    - name: HuggingFace MiniMax-H3 模型卡
      url: https://huggingface.co/MiniMaxAI/MiniMax-H3
      accessedAt: 2026-10-08
    - name: HuggingFace HunyuanVideo-1.5
      url: https://huggingface.co/tencent/HunyuanVideo-1.5
      accessedAt: 2026-10-08
    - name: MiniMax H3 官方页面
      url: https://platform.minimax.io/
      accessedAt: 2026-08-23
    - name: CogVideoX GitHub
      url: https://github.com/zai-org/CogVideo
      accessedAt: 2026-08-23
    - name: HunyuanVideo GitHub
      url: https://github.com/Tencent-Hunyuan/HunyuanVideo
      accessedAt: 2026-08-23
    - name: Unite.AI Best AI Video Generators
      url: https://www.unite.ai/best-ai-video-generators/
      accessedAt: 2026-08-23
---

# 视频生成模型对比

> **TL;DR**：OpenAI Sora 已于 2026-09-24 整体下线且**没有替代 API**，闭源看效果选 Runway / Kling，国内选 Kling / 即梦；开源看规模选 MiniMax H3（33B）/ HunyuanVideo-1.5，看性价比选 CogVideoX。

> **本次核实范围(2026-10-08)**：已复核 OpenAI Sora 生命周期、Runway 自有模型线、MiniMax H3、腾讯 HunyuanVideo 这几条。Kling / Vidu / 即梦 / Pika / Veo / PixVerse 的版本与时长，以及 HunyuanVideo 13B、CogVideoX 2B/5B 参数与全文 GitHub ⭐ 数，本次**未从可访问的官方源复核**，沿用上一版取值。

## 你能在这里学到

- 主流视频生成模型全景（闭源 + 开源）
- 各模型的核心参数与能力对比
- 按场景选型建议
- 个人创作者/团队/企业的推荐

## 前置知识

阅读本篇需要你先了解：

- [模型选型指南](./model-selection-guide)
- [文本模型对比](./model-comparison)

## 一、模型全景（截至 2026-10）

### 闭源商业模型

| 模型 | 厂商 | 时长 | 分辨率 | 特色 | 开源 |
|------|------|------|--------|------|------|
| **Gen-4.5 / Gen-4 Turbo** | Runway | 4-16s | 1080P | 30+ AI 工具组合 | ❌ |
| **Veo 3** | Google DeepMind | 8s | 4K | 高保真、物理一致 | ❌ |
| **Kling（可灵）** | 快手 | 分钟级 | 1080P | 国内领先、中文优化 | ❌ |
| **Pika** | Pika Labs | 短片 | 1080P | 操作最简、上手快 | ❌ |
| **Vidu** | 生数科技 | 短片 | 1080P | 一致性最强、多参考物 | ❌ |
| **即梦（Jimeng）** | 字节跳动 | 短片 | 1080P | 抖音生态、创作模板多 | ❌ |
| **Seedance** | 字节跳动 | 短片 | 1080P | 多平台集成 | ❌ |
| **PixVerse V6** | 爱诗科技（AIsphere） | 短片 | 待官方公布 | 全球化 SaaS、效果模板生态、高性价比 | ❌ |
| **PixVerse C1** | 爱诗科技（AIsphere） | 短片 | 待官方公布 | **多宫格分镜叙事**、影视级打斗/特效 | ❌ |

> ⚠️ **Sora 已经不是 OpenAI 的视频选项了(2026-09-24)**。`sora-2` / `sora-2-pro` 及其全部快照、连同整个 **Videos API**,已在 **2026-09-24 正式下线**(2026-03-24 发布的废弃通知),OpenAI 官方明确写了 **没有一对一的替代 API**。任何仍把 Sora 列为"闭源第一梯队"或按 Sora 排期做技术选型的文档都已经失效——API 集成路线需要重新选型。
>
> Runway 自有模型线已推进到 **Gen-4.5**(`gen4.5`)与 **Gen-4 Turbo**(`gen4_turbo`),上一版的 "Runway Gen-3" 落后了两代;同门还有视频编辑模型 **Aleph 2.0**(`aleph2`)。图片侧 Runway 走 **Gen-4 Image** / **Gen-4 Image Turbo**。另外 Runway Dev 已转型为**多模型路由平台**,其官方目录里同时收录了 Seedance 2.5/2.0、Veo 3.1、WAN 3.0、MiniMax H3(`hailuo3`)与 H3 Max(`h3_max`)、Grok Imagine Video 1.5 等第三方模型——想接多家视频模型可以考虑走这类聚合 API,但注意那是 Runway 的转售目录,不等同于各厂商自己的首发口径。

### 开源模型

| 模型 | 厂商 | 参数 | 时长 | 分辨率 | GitHub ⭐ |
|------|------|------|------|--------|-----------|
| **MiniMax H3** | MiniMax | **33B** | 4-15s | **768P/2K** | HuggingFace 3.6M+ 下载 |
| **HunyuanVideo** | 腾讯混元 | 13B | 短片 | 1080P | 12,444 |
| **CogVideoX** | 智谱 AI | 2B/5B | 6s | 720P | 12,964 |
| **HunyuanVideo-1.5** | 腾讯混元 | 轻量版 | 短片 | 1080P | 4,529 |
| **Mochi** | Genmo | — | 5.4s | 480P | 3,709 |
| **Vidu-S1** | 生数科技 | — | 实时 | — | 245 |

> ⚠️ 截至 2026-10-08 未从可访问的官方源复核此项:Kling、Vidu、即梦、Pika、Veo 3、PixVerse 的时长与分辨率，以及 HunyuanVideo 13B / CogVideoX 2B·5B 参数与本表 GitHub ⭐ 数，均仍为上一版取值。GitHub REST API 当时返回限流，未能取到新的 star 数。腾讯侧可核实的是：**HunyuanVideo-1.5 仍是官方最新开源视频权重**(2025-11-18 上线,`tencent-hunyuan-community` 许可,提供 480p/720p 与 1080p 超分蒸馏变体),未发现 2026-08-23 ~ 10-08 窗口内更新的官方 HunyuanVideo 版本。

## 二、MiniMax H3 深度评测（重点）

### 核心参数（已校验）

| 参数 | 数值 |
|------|------|
| 参数规模 | **33B**（330 亿，dense 单流 Transformer） |
| 分辨率 | **768P（短边默认）/ 2K** |
| 时长 | **4-15 秒** |
| 帧率 | 24 fps |
| 音频 | **原生立体声**（一体生成，32 kHz） |
| 发布日期 | 2026-07-28（HuggingFace 上线） |
| 开源 | ✅ 权重公开（仅 H3-Base） |

> ⚠️ **三个模块名要按官方模型卡改过来**。上一版写的 "H3-Contextual Omni Representation"、"H3-VAE"、"H3-In-context Regeneration" 三个名字在官方模型卡里对不上，正确叫法与开源边界是:
>
> | 组件 | 官方名 | 是否开源 |
> |------|--------|----------|
> | 上下文解析 | **H3-Context-IR**（Context Intermediate Representation） | ❌ 托管式预处理，开源版需自建或调 API |
> | 主力生成 | **H3-Base**（H3-Omni-Transformer） | ✅ 权重已发布（FL2VA / Ref2VA 两档） |
> | 2K 重生成 | **H3-Regenerate-2K** | ❌ 官方称「准备就绪后另行发布」 |

### 架构特点

| 组件 | 说明 |
|------|------|
| **H3-Omni-Transformer** | 33B dense 单流 Transformer，联合预测视频与音频 latent；约 13B 参数在 AdaLN 分支（推理时可预计算缓存，不必加载） |
| **H3-Encoder** | 文本编码用 Qwen3-VL-32B 完整预训练权重，取第 50 层 hidden states |
| **H3-VisualVAE** | f16t4d24：空间 16×、时间 4× 压缩，24 latent 通道 |
| **H3-AudioVAE** | 32 kHz → 40 Hz latent，左右声道独立编解码再合成 |
| **H3-Regenerate-2K** | 不用超分模块，让 H3 带着原上下文把 768p 结果上下文内重生成 2K |

### 生态热度

| 指标 | 数值 |
|------|------|
| HuggingFace 官方下载 | 3.59M（近 30 天滚动） |
| HuggingFace 点赞 | 5,978 |
| ComfyUI 集成下载 | 16.3M |
| ComfyUI 节点项目 | 10+ 个 |

> 下载量为 HuggingFace `downloads` 字段（近 30 天滚动窗口），访问于 2026-10-08。
> ⚠️ 截至 2026-10-08 未从可访问的官方源复核此项:ComfyUI 集成下载 16.3M 与节点项目数仍为上一版取值。另外 2026-08-23 ~ 10-08 窗口内，HuggingFace 上 `MiniMaxAI` 组织**未出现新的视频模型**（该组织同期新增的是 MiniMax-Music3 音乐模型与 MiniMax-M3 文本/多模态模型，均非视频线）。

## 三、场景选型

### 个人创作者

| 场景 | 首选 | 理由 |
|------|------|------|
| **零基础入门** | **Pika** | 界面友好，操作最简 |
| **国内用户** | **Kling / 即梦** | 访问稳定，中文支持好 |
| **高质量短片** | **Runway Gen-4.5** | 工具最全，效果专业 |
| **图生视频** | **Vidu** | 一致性最强，角色稳定 |
| **抖音创作** | **即梦** | 字节生态打通 |
| **影视级分镜叙事** | **PixVerse C1** | 多宫格分镜、打斗/特效专精 |
| **社交/效果模板** | **PixVerse V6** | 效果模板生态、海外用户友好 |
| **本地部署 / 开源** | **MiniMax H3** | 33B 参数、原生音频 |
| **预算极低** | **CogVideoX** | 5B 参数可本地跑 |

### 团队 / 企业

| 场景 | 首选 | 理由 |
|------|------|------|
| **企业级本地部署** | **HunyuanVideo-1.5 / MiniMax H3** | 开源、可私有化 |
| **API 集成** | **Kling / Runway** | 稳定 API，商用可靠 |
| **多语言营销** | **HeyGen / Synthesia** | 160+ 语言，数字人 |
| **成本敏感批量生成** | **MiniMax H3 / CogVideoX** | 本地跑，无 API 费用 |

## 四、效果 vs 成本对比

| 模型 | 视频质量 | 易用性 | 价格 | 开源 | 推荐指数 |
|------|----------|--------|------|------|----------|
| **Runway Gen-4.5** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| **Kling** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| **Pika** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| **Vidu** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ |
| **即梦** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ |
| **PixVerse V6/C1** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ |
| **MiniMax H3** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **HunyuanVideo-1.5** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **CogVideoX** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐ |

> Sora 已从本表移除：2026-09-24 起 Sora 2 与 Videos API 在 OpenAI 侧全部下线且无替代 API（见 §一）。

## 五、关键洞察

### 1. 闭源效果领先，开源快速追赶

Runway **Gen-4.5** 仍是效果第一梯队，但 **MiniMax H3（33B）** 已经把开源推到接近闭源的水平——尤其是**原生音频**和 **2K 分辨率**是开源第一次达到的能力。

> 上一版这里的第一梯队写着 "Sora / Runway"。Sora 2 与 Videos API 已于 2026-09-24 下线且无替代 API，因此 2026-10 的闭源第一梯队只剩 Runway 一家（以及本表里未复核的 Kling / Vidu 等）。

### 2. 国内厂商差异化路线

- **Kling**：长时长（分钟级），国内领先
- **即梦**：抖音生态，创作模板丰富
- **Vidu**：一致性最强，图生视频首选
- **PixVerse**：全球化 SaaS、效果模板生态；**C1 主打多宫格分镜叙事**
- **MiniMax H3**：全模态统一、开源可用
- **HunyuanVideo-1.5**：企业级本地部署首选

### 3. 时长仍是瓶颈

除了 Kling（分钟级），大多数模型仍在 **15 秒以内**（MiniMax H3 为 4-15 秒）。长视频生成是下一战场。

### 4. 音频同步成新标准

**MiniMax H3** 是第一个原生支持立体声的开源模型，Runway 等闭源模型也在跟进。未来视频 + 音频一体生成会成标配。

## 六、上手建议

### 完全零基础

```text
第 1 步：注册 Pika（免费额度）
第 2 步：输入一段文字提示词
第 3 步：生成 4 秒视频
第 4 步：满意后升级付费或试试 Kling
```

### 有一定基础

```text
第 1 步：Runway Gen-4.5 做主力（效果最好）
第 2 步：Vidu 做角色一致性视频
第 3 步：Kling 做长时长视频
```

### 开发者 / 本地部署

```text
第 1 步：MiniMax H3 部署到本地（33B，需 A100）
第 2 步：HunyuanVideo-1.5 做轻量版备选
第 3 步：CogVideoX-5B 做极致成本控制
```

## 参考

- [OpenAI API 废弃说明](https://developers.openai.com/api/docs/deprecations)（访问于 2026-10-08）——Sora 2 与 Videos API 2026-09-24 下线、无替代 API
- [OpenAI 视频生成指南（Sora 2）](https://developers.openai.com/api/docs/guides/video-generation)（访问于 2026-10-08）——官方标注为历史存档
- [Runway Dev 官方模型目录](https://docs.dev.runwayml.com/guides/models)（访问于 2026-10-08）——Gen-4.5 / Gen-4 Turbo / Aleph 2.0
- [HuggingFace MiniMax-H3 模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3)（访问于 2026-10-08）——模块名、参数、开源边界
- [HuggingFace HunyuanVideo-1.5](https://huggingface.co/tencent/HunyuanVideo-1.5)（访问于 2026-10-08）
- [MiniMax H3 官方页面](https://platform.minimax.io/)（访问于 2026-08-23）
- [CogVideoX GitHub](https://github.com/zai-org/CogVideo)（访问于 2026-08-23）
- [HunyuanVideo GitHub](https://github.com/Tencent-Hunyuan/HunyuanVideo)（访问于 2026-08-23）
- [Unite.AI Best AI Video Generators](https://www.unite.ai/best-ai-video-generators/)（访问于 2026-08-23）

## 下一步

- 看图片模型对比 → [图片模型对比](./image-model-comparison)
- 看文本模型对比 → [模型对比](./model-comparison)
- 按场景选型 → [模型选型决策树](./model-selection-guide)
- 看厂商档案 → [国内厂商](/ai-trends/cn-vendors/)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- AI Native 架构 → [AI Native](/ai-harness/)
- AI 工具 → [AI 工具全景](/ai-coding/tools/overview)

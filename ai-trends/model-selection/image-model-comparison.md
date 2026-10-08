---
title: 图片生成模型对比
description: 主流 AI 图片生成模型全景——Midjourney / DALL-E / Imagen / Firefly / Ideogram / 即梦 / Flux / SD / HunyuanImage / CogView 对比与选型
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-08
verifiedWith:
  sources:
    - name: OpenAI API Changelog
      url: https://developers.openai.com/api/docs/changelog
      accessedAt: 2026-10-08
    - name: OpenAI API 模型目录
      url: https://developers.openai.com/api/docs/models
      accessedAt: 2026-10-08
    - name: OpenAI API 废弃说明
      url: https://developers.openai.com/api/docs/deprecations
      accessedAt: 2026-10-08
    - name: Midjourney Version 官方文档
      url: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
      accessedAt: 2026-10-08
    - name: HuggingFace FLUX.2-dev
      url: https://huggingface.co/black-forest-labs/FLUX.2-dev
      accessedAt: 2026-10-08
    - name: HuggingFace FLUX.1-dev
      url: https://huggingface.co/black-forest-labs/FLUX.1-dev
      accessedAt: 2026-10-08
    - name: HuggingFace FLUX.1-schnell
      url: https://huggingface.co/black-forest-labs/FLUX.1-schnell
      accessedAt: 2026-10-08
    - name: HuggingFace HunyuanImage 3.0
      url: https://huggingface.co/tencent/HunyuanImage-3.0
      accessedAt: 2026-10-08
    - name: HuggingFace CogView4-6B
      url: https://huggingface.co/zai-org/CogView4-6B
      accessedAt: 2026-10-08
    - name: HuggingFace SD 3.5 Large
      url: https://huggingface.co/stabilityai/stable-diffusion-3.5-large
      accessedAt: 2026-08-24
    - name: HuggingFace Kolors
      url: https://huggingface.co/Kwai-Kolors/Kolors
      accessedAt: 2026-08-24
    - name: Midjourney 官方
      url: https://www.midjourney.com/
      accessedAt: 2026-08-24
    - name: Black Forest Labs
      url: https://bfl.ai/
      accessedAt: 2026-08-24
---

# 图片生成模型对比

> **TL;DR**:闭源看效果选 Midjourney V8.2 / GPT-Image 2.5 / Imagen;文字排版选 Ideogram;开源看质量选 Flux.2-dev / HunyuanImage 3.0(80B MoE),看性价比选 FLUX.2-klein-4B / Flux.1-schnell / CogView4-6B。

> **本次核实范围(2026-10-08)**:已复核 OpenAI、Midjourney、Black Forest Labs、腾讯 HunyuanImage、智谱 CogView 这几条线的版本与参数。Imagen / Firefly / Ideogram / Recraft / 即梦 / 通义万相 / 文心一格 / Stability / Kolors / PixArt 这几行本次**未从可访问的官方源复核**,数值沿用上一版,参考文末 ⚠️ 标注。

## 你能在这里学到

- 主流图片生成模型全景(闭源商业 + 国内闭源 + 开源)
- 各模型的核心参数、License、生态热度
- 按场景选型建议(个人 / 团队 / 企业)
- 开源模型本地部署门槛与推荐

## 前置知识

阅读本篇需要你先了解:

- [模型选型指南](./model-selection-guide)
- [视频生成模型对比](./video-model-comparison)

## 一、模型全景(截至 2026-10)

### 闭源商业模型

| 模型 | 厂商 | 最新版本 | 分辨率 | 特色 | 开源 |
|------|------|----------|--------|------|------|
| **Midjourney V8.2** | Midjourney | V8.2(2026-07-24) | 2K(HD) | 美学质量第一梯队、艺术风格丰富 | ❌ |
| **GPT-Image 2.5** | OpenAI | Sunburst / Flare(2026-09-08) | 高保真 | ChatGPT/API 集成、多轮迭代、文字排版强 | ❌ |
| **Imagen 4** | Google DeepMind | Imagen 4(2025) | 2K+ | Gemini/Vertex 集成、细节保真 | ❌ |
| **Firefly Image 4** | Adobe | 2025 | 商用友好 | 训练数据合规、PS/AI 深度集成 | ❌ |
| **Ideogram 3.0** | Ideogram | 3.0(2025) | 高保真 | **文字排版最强**、Logo/海报专精 | ❌ |
| **Recraft V3** | Recraft | V3(2025) | 高保真 | 设计场景专精、SVG 输出、品牌一致性 | ❌ |

**闭源两条已核实的版本变化**:

- **Midjourney 默认版本已从 V7 变成 V8.2**(2026-07-24 起为默认)。V8.1 于 2026-04-14 发布、2026-06-10 至 07-23 担任默认,首次提供 2048px 的 HD 出图(SD 转 HD 需 1.3 分钟 GPU 时间,SD 为 0.8)。V7 是 2025-04-03 发布、2026-06-09 卸任默认。V8.2 引入 Edit Model,取代 Omni Reference、Character Reference 与 Retexture。另有专攻东方/动漫风格的 **Niji 7**(2026-01-09)。
- **OpenAI 图片线在 6 周内换代**。2026-04-21 发布 **GPT-Image 2**(灵活尺寸、高保真输入、token 计费、Batch 5 折);2026-09-08 发布 **GPT-Image 2.5 Sunburst / Flare**,同时支持图像生成与编辑,新增 `xhigh` 与 `max` 质量档,沿用 GPT-Image 2 的 token 费率——官方定位是 **Sunburst 偏编辑精度、Flare 偏日常高质量快速出图**。

> ⚠️ 截至 2026-10-08,`DALL·E 2` 与 `DALL·E 3` 已于 2026-05-12 从 OpenAI API 下线,官方推荐迁移到 `gpt-image-2` / `gpt-image-1` / `gpt-image-1-mini`。同期 `gpt-image-1` 已进入废弃流程(2026-10-23 移除),`gpt-image-1-mini`、`gpt-image-1.5`、`chatgpt-image-latest` 将于 2026-12-01 移除,官方指定替代均为 `gpt-image-2.5-sunburst` 或 `gpt-image-2.5-flare`。**再用 DALL·E 或只盯 GPT-Image-1 做选型会踩空。**

> ⚠️ 截至 2026-10-08 未从可访问的官方源复核此项:Imagen 4、Firefly Image 4、Ideogram 3.0、Recraft V3 的版本号与分辨率仍为上一版取值。

### 国内闭源模型

| 模型 | 厂商 | 最新版本 | 分辨率 | 特色 | 开源 |
|------|------|----------|--------|------|------|
| **即梦(Jimeng)** | 字节跳动 | 3.x(2025) | 高保真 | 抖音/剪映生态、创作模板丰富 | ❌ |
| **通义万相(Wanx)** | 阿里 | 2.x(2025) | 高保真 | 中文语义强、电商设计场景 | ❌ |
| **可灵图像(Kolors)** | 快手 | 1.x | 1024+ | 已开源基座权重,商用需授权 | 🟡 |
| **文心一格** | 百度 | ERNIE-ViLG(2025) | 高保真 | 百度生态、中文语义 | ❌ |

> ⚠️ 截至 2026-10-08 未从可访问的官方源复核此项:即梦、通义万相、可灵图像、文心一格的版本号与分辨率仍为上一版取值,本次未找到四家在 2026-08-24 ~ 10-08 窗口内的可核实官方发布记录。

### 开源模型

| 模型 | 厂商 | 参数规模 | License | HF 下载 | HF 点赞 | 发布 |
|------|------|----------|---------|---------|---------|------|
| **Flux.2-dev** | Black Forest Labs | ~32B | Non-Commercial | 495 万+ | 2,385 | 2025-11-22 |
| **FLUX.2-klein-4B** | Black Forest Labs | 4B | ⚠️ 见下 | 40.6 万 | 1,011 | 2026-01-14 |
| **Flux.1-dev** | Black Forest Labs | 11.9B | Non-Commercial | 70 万+ | 15,437 | 2024-07-31 |
| **Flux.1-schnell** | Black Forest Labs | 11.9B | Apache 2.0 | 65.7 万 | 6,166 | 2024-07-31 |
| **HunyuanImage 3.0** | 腾讯混元 | **80B MoE**(64 experts) | 自定义(非商) | 3,401 | 1,136 | 2025-09-25 |
| **SD 3.5 Large** | Stability AI | 8B | Community(非商) | 7.7 万 | 3,717 | 2024-10 |
| **SDXL Base 1.0** | Stability AI | 3.5B | Open RAIL++ | 158 万 | 8,067 | 2023-07 |
| **CogView4-6B** | 智谱 AI | 6.37B | Apache 2.0 | 4,365 | 258 | 2025-03-03 |
| **HunyuanDiT** | 腾讯混元 | 1.5B | Tencent(可商用) | 18.6 万 | 17 | 2024-05 |
| **Kolors** | 快手 | 未公开 | 需授权 | 9,045+ | 114 | 2024-07 |
| **PixArt-Σ** | 华为 & 港大 | 0.6B | AGPL 3.0 | 10,638 | 105 | 2024-04 |

> 上表的 HF 下载量为该仓库 `downloadsAllTime`(累计下载)与 `likes` 快照,取自 HuggingFace 官方 API,访问于 2026-10-08;旧版文档里的下载数口径为近 30 天滚动值,两者不可直接比较。
>
> ⚠️ 截至 2026-10-08 未从可访问的官方源复核此项:SD 3.5 Large、SDXL Base 1.0、HunyuanDiT、Kolors、PixArt-Σ 的参数与下载/点赞数据仍为上一版取值。`FLUX.2-klein-4B` 的 License 字段在 HuggingFace 仓库标签上**未标注 license**,需打开仓库内 LICENSE 文件确认后才能判断能否商用,本次未能读到该文件。

## 二、Flux 家族深度评测(开源标杆)

Black Forest Labs(前 Stability AI 核心团队)已成为**开源图像模型第一梯队**。

### Flux 三档定位

| 版本 | 参数 | License | 适用场景 | 生成速度 |
|------|------|---------|----------|----------|
| **Flux.1-Pro** | 12B | 闭源 API | 商业最高质量 | 中 |
| **Flux.1-dev** | 11.9B | 非商用 | 研究/个人开发 | 中 |
| **Flux.1-schnell** | 11.9B | Apache 2.0 | 商用友好、快速 | **1-4 步蒸馏** |
| **Flux.1-Kontext** | 12B | 非商用 | **图像编辑专精** | 中 |
| **Flux.2-dev** | ~32B | 非商用 | 新一代基座 | 中 |
| **FLUX.2-klein-4B / 9B** | 4B / 9B | ⚠️ 见文末注 | 轻量基座、体积优先 | 中 |

### 生态热度

- **Flux.1-dev**:HuggingFace 15,437 点赞,是**开源图像模型点赞第一**
- **Flux.2-dev**:2025-11-22 上线,累计下载已超 495 万
- **ComfyUI 生态**:官方 workflow 完善,LoRA/ControlNet 极丰富
- **License 差异**:dev/Pro 商用受限,**只有 schnell 是 Apache 2.0**(商业可放心用)

> ⚠️ 上一版把 Flux.2-dev 记作「~12B」是错的。HuggingFace 官方 API 对该仓库的 safetensors 权重统计为 **32,223,281,152 个 BF16 参数(约 32B)**,量级是 Flux.1 系列的近三倍。`black-forest-labs/FLUX.2-dev` 模型卡为 gated 状态、未登录无法读取 README,因此这个数字取自 HuggingFace 的权重元数据而非厂商自述的模型卡参数表。同理 `Flux.1-dev` 官方权重统计为 11,901,408,320(约 11.9B),`Flux.1-schnell` 为 11,891,178,560。
>
> ⚠️ 截至 2026-10-08 未从可访问的官方源复核此项:`FLUX.2-klein-4B` / `FLUX.2-klein-9B` 的 License——HuggingFace 仓库标签上 `FLUX.2-klein-4B` 未声明 license,同批的 `FLUX.2-klein-9B` 与 `FLUX.2-klein-base-9B` 标记为 `license:other`,商用前必须逐个仓库打开 LICENSE 确认,不要按「klein 属于 Flux.2 就一定可商用」推断。

## 三、HunyuanImage 3.0 深度评测(国产旗舰)

腾讯混元 2025-09 发布,是**中文场景开源模型天花板**。

### 核心参数(已校验)

| 参数 | 数值 |
|------|------|
| 架构 | **MoE Transformer**(64 experts) |
| 总参数 | **~80B**(BF16 权重) |
| 激活参数 | 约 12-15B(推理时) |
| 分辨率 | 1024+ |
| 中文提示词 | **原生支持** |
| License | 非商用(自定义) |
| 发布 | 2025-09-25 |

> HF 权重统计复核:BF16 **81,748,524,512** + F32 **1,260,674,947** = 合计约 **83.0B** 参数,`config.json` 确认 `num_experts: 64`,与上文「80B MoE」的说法一致。论文见 arXiv:2509.23951。HuggingFace 点赞 1,136。License 标识为 `tencent-hunyuan-community`(腾讯混元社区许可,非商用)。

### 部署门槛

- **完整权重**:80B BF16 需要 **160GB+ 显存**(需 2×A100 80G 或 4×A6000)
- **量化版本**:社区提供 NF4/GGUF 量化,单卡 40G 可跑
- **推荐用途**:企业本地部署、需要中文能力的场景

## 四、场景选型

### 个人创作者

| 场景 | 首选 | 理由 |
|------|------|------|
| **零基础入门** | **即梦 / Midjourney V8.2** | 界面友好,创作模板多 |
| **国内用户** | **即梦 / 通义万相** | 访问稳定,中文支持好 |
| **艺术创作** | **Midjourney V8.2** | 美学质量最高、风格丰富 |
| **文字/海报** | **Ideogram 3.0** | 文字排版能力最强 |
| **多轮迭代** | **GPT-Image 2.5** | ChatGPT 对话式编辑 |
| **本地部署** | **Flux.1-dev / Flux.2-dev** | 12B / 32B 开源、社区生态最好 |
| **商用免版权** | **Flux.1-schnell / SDXL** | Apache 2.0 / RAIL++ 可商用 |
| **中文场景本地跑** | **HunyuanImage 3.0**(量化) | 中文语义原生 |
| **极致性价比** | **CogView4-6B** | 6.37B、Apache 2.0、单卡可跑 |

### 团队 / 企业

| 场景 | 首选 | 理由 |
|------|------|------|
| **API 集成生产** | **GPT-Image 2.5 / Imagen / Midjourney API** | 稳定 API、SLA 保障 |
| **商用版权敏感** | **Adobe Firefly** | 训练数据合规 |
| **设计流程集成** | **Firefly / Recraft** | PS/AI/Figma 集成 |
| **企业本地部署** | **HunyuanImage 3.0 / Flux.1-schnell** | 开源可私有化 |
| **电商/中文** | **通义万相 / 即梦** | 中文语义、场景模板 |
| **批量成本敏感** | **Flux.1-schnell / SDXL** | 本地跑,无 API 费用 |

## 五、效果 vs 成本对比

| 模型 | 图像质量 | 易用性 | 价格 | 商用友好 | 开源 | 推荐指数 |
|------|----------|--------|------|----------|------|----------|
| **Midjourney V8.2** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **GPT-Image 2.5** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **Imagen 4** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **Ideogram 3.0** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **Firefly Image 4** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅✅(数据合规) | ❌ | ⭐⭐⭐⭐ |
| **即梦** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **通义万相** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ❌ | ⭐⭐⭐⭐ |
| **Flux.2-dev** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ 非商 | ✅ | ⭐⭐⭐⭐⭐ |
| **FLUX.2-klein-4B** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ 见文末注 | ✅ | ⭐⭐⭐⭐ |
| **Flux.1-dev** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ 非商 | ✅ | ⭐⭐⭐⭐⭐ |
| **Flux.1-schnell** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅(Apache) | ✅ | ⭐⭐⭐⭐⭐ |
| **HunyuanImage 3.0** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⚠️ 非商 | ✅ | ⭐⭐⭐⭐ |
| **SD 3.5 Large** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ 需协议 | ✅ | ⭐⭐⭐⭐ |
| **SDXL** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅(RAIL++) | ✅ | ⭐⭐⭐⭐ |
| **CogView4-6B** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅(Apache) | ✅ | ⭐⭐⭐⭐ |
| **HunyuanDiT** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐ |

## 六、关键洞察

### 1. 商业闭源仍是效果第一梯队

**Midjourney V8.2 / GPT-Image 2.5 / Imagen 4** 在美学、语义理解、复杂构图上仍领先。特别是 **GPT-Image 2.5**——ChatGPT 集成让"对话式修图"成为主流交互,2026-09-08 又把这条线拆成"编辑精度优先的 Sunburst"与"日常高质量的 Flare"两档。

### 2. Flux 家族成为开源基座事实标准

**Flux.1-dev**(HuggingFace 15K+ 点赞)已是**开源图像模型点赞第一**,超越所有 Stable Diffusion 版本。**Flux.2-dev**(2025-11-22)延续这个势头,参数量也从 12B 档跃升到 32B 档。

关键差异化:
- **Flux.1-schnell**——Apache 2.0,商用友好,1-4 步蒸馏推理快
- **Flux.1-Kontext**——图像编辑(inpaint/change)专精
- **Flux.2-dev**——新一代基座,32B 权重
- **FLUX.2-klein-4B/9B**——2026-01-14 发布的轻量档,给显存紧张的本地部署用

### 3. 中文场景国产模型领先

- **闭源**:即梦(抖音生态)、通义万相(电商)、文心一格(百度)
- **开源**:HunyuanImage 3.0(80B MoE,中文原生)、CogView4-6B(6.4B、Apache)

**HunyuanImage 3.0** 是**首个 80B 级别开源图像模型**,采用 MoE 架构(64 experts)。中文语义理解优势明显,但部署门槛高(需 160GB+ 显存跑全量)。

### 4. 文字排版成为分水岭

大多数模型在文字生成(招牌、Logo、海报文字)上仍有瑕疵。**Ideogram 3.0** 是文字排版最强,**GPT-Image 2.5** 紧随其后,而多数开源模型在这个维度仍偏弱。

### 5. License 是商用最大陷阱

**必须注意的 License 边界**:

| License | 可商用? | 代表模型 |
|---------|----------|----------|
| **Apache 2.0** | ✅ 完全自由 | Flux.1-schnell、CogView4-6B、PixArt |
| **Open RAIL++** | ✅ 有使用限制 | SDXL |
| **SD Community** | ⚠️ 年收入 <100 万美元免费 | SD 3.5 |
| **Flux Non-Commercial** | ❌ 需授权 | Flux.1-dev、Flux.2-dev |
| **Tencent Custom** | ❌ 需授权 | HunyuanImage 3.0 |

商用前**必须**核对 License,不能因为"开源"就直接用于商业产品。

### 6. 生成速度分化

- **蒸馏模型**(Flux.1-schnell、SDXL Turbo):1-4 步、毫秒级
- **标准扩散**(Flux.1-dev、SDXL、SD 3.5):20-30 步、秒级
- **大模型**(HunyuanImage 3.0):秒到十秒级

批量生产选蒸馏版,质量优先选标准版。

## 七、上手建议

### 完全零基础

```text
第 1 步:注册 Midjourney(Discord)或即梦(网页版)
第 2 步:输入英文提示词(Midjourney)或中文(即梦)
第 3 步:生成 4 张变体,选一张 Upscale
第 4 步:满意后升级付费,或试 Ideogram 做文字设计
```

### 有一定基础

```text
第 1 步:GPT-Image 2.5 做多轮迭代主力(对话修图)
第 2 步:Ideogram 做文字海报
第 3 步:Firefly 做商用版权敏感场景
第 4 步:即梦/通义 做中文场景
```

### 开发者 / 本地部署

```text
第 1 步:ComfyUI + Flux.1-dev(11.9B,需 24G+ 显存);显存够再上 Flux.2-dev(~32B)
第 2 步:LoRA 微调(个人风格/角色)
第 3 步:ControlNet 做精准控制(pose/depth/canny)
第 4 步:批量生产切 Flux.1-schnell(Apache 商用)
第 5 步:中文场景切 HunyuanImage 3.0 量化版或 CogView4-6B
```

### 企业本地部署

```text
第 1 步:评估 License 边界(商用/非商用)
第 2 步:硬件规划(HunyuanImage 3.0 需 160G+,Flux.1 24-48G,Flux.2-dev 按 32B 另算)
第 3 步:私有化部署 Flux.1-schnell(Apache)或 SDXL
第 4 步:LoRA 训练品牌资产(风格/字体/角色)
第 5 步:接入 CDN 与审核链路
```

## 参考

- [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)(访问于 2026-10-08)——GPT-Image 2 / GPT-Image 2.5 发布记录
- [OpenAI API 模型目录](https://developers.openai.com/api/docs/models)(访问于 2026-10-08)
- [OpenAI API 废弃说明](https://developers.openai.com/api/docs/deprecations)(访问于 2026-10-08)——DALL·E 下线、gpt-image-1 移除时间表
- [Midjourney Version 官方文档](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)(访问于 2026-10-08)——V8.2 / V8.1 / V7 / Niji 7 版本沿革
- [HuggingFace FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev)(访问于 2026-10-08)
- [HuggingFace FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)(访问于 2026-10-08)
- [HuggingFace FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell)(访问于 2026-10-08)
- [HuggingFace HunyuanImage 3.0](https://huggingface.co/tencent/HunyuanImage-3.0)(访问于 2026-10-08)
- [HuggingFace CogView4-6B](https://huggingface.co/zai-org/CogView4-6B)(访问于 2026-10-08)
- [HuggingFace SD 3.5 Large](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)(访问于 2026-08-24)
- [HuggingFace Kolors](https://huggingface.co/Kwai-Kolors/Kolors)(访问于 2026-08-24)
- [Black Forest Labs 官方](https://bfl.ai/)(访问于 2026-08-24)
- [Midjourney 官方](https://www.midjourney.com/)(访问于 2026-08-24)

## 下一步

- 看视频模型对比 → [视频模型对比](./video-model-comparison)
- 看文本模型对比 → [模型对比](./model-comparison)
- 按场景选型 → [模型选型决策树](./model-selection-guide)
- 看厂商档案 → [国内厂商](/ai-trends/cn-vendors/)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- AI Native 架构 → [AI Harness 工程](/ai-harness/)
- AI 工具 → [AI 工具全景](/ai-coding/tools/overview)

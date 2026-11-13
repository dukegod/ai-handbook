---
title: 视觉能力
description: API 视角的图片 / PDF 处理；支持的格式、image block 怎么写、token 计算与多图实战
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 订正模型 ID、vision 支持范围与 token 估算口径（官方文档于当日重新核对）：当前四型号 claude-fable-5-2 / claude-opus-5-5 / claude-sonnet-5-5 / claude-haiku-5-5 全部支持图片与 PDF、均为 1M context；图片 token 改为按 28×28 patch 计（⌈w/28⌉×⌈h/28⌉），当前型号属高分辨率档（最长边 2576 px、visual token 上限 4784），旧的 (w×h)/750 与 1600 上限已废弃；PDF 官方口径为每页文本 1500~3000 token，每页再按图片计一次；单图上限 Claude API 10 MB / Bedrock 5 MB，单请求 128 MB、1M context 型号最多 600 张图；CLI 相关断言沿用 2026-08 的记录（当时基于 Claude Code 2.1.220），示例未在本机重跑'
  claudeCode: 2.1.220
  model: claude-opus-5-5
  visionDocs: 'https://platform.claude.com/docs/en/build-with-claude/vision'
  pdfDocs: 'https://platform.claude.com/docs/en/build-with-claude/pdf-support'
  tokenCounting: 'https://platform.claude.com/docs/en/build-with-claude/token-counting'
  accessedAt: 2026-08-06
---

# 视觉能力

> **TL;DR**：当前四型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）**全部支持 vision**，context 均为 1M——支持 PNG / JPEG / GIF / WebP / PDF。**图片按 28×28 patch 算 token**（不按内容），**PDF 按页数 + 内容**算。API 视角通过 `image` block 传图（base64 或 URL），与 text block 混排。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 当前 4 型号 vision 支持矩阵
- `image` block 的两种形式（base64 / URL）
- 图片 token 计算规则（按 28×28 patch）
- PDF 传法与 token 计算
- 多图实战（多张图混排、对比、OCR）
- 何时该用 vision vs 不该用
- 5 个常见坑（体积与 token 代价、PDF token 爆炸、base64 vs URL、动画 GIF、ZDR 隐私）

## 一、4 模型 vision 支持

| 模型 | 图片（PNG/JPEG/GIF/WebP） | PDF | 视频帧 | Context | 单图上限 |
| --- | :---: | :---: | :---: | --- | --- |
| **Fable 5.2** | ✅ | ✅ | ❌ | 1M | 10 MB |
| **Opus 5.5** | ✅ | ✅ | ❌ | 1M | 10 MB |
| **Sonnet 5.5** | ✅ | ✅ | ❌ | 1M | 10 MB |
| **Haiku 5.5** | ✅ | ✅ | ❌ | 1M | 10 MB |

**注意**：
- Claude 4 代起 vision 走**原生多模态**——不是 OCR 后丢给文本模型
- **不支持视频流**——视频需先抽帧（按秒抽）再传
- **单张上限 10 MB**（base64 编码后，Claude API / claude.ai；Bedrock 是 5 MB）；单边最大 8000×8000 px
- **单次请求最多 600 张图**（1M context 型号；200k context 型号是 100 张），整个请求体上限 128 MB
- **一次超过 20 张图时单图尺寸限制更严**——要么每边不超过 3000 px，要么控制在 20 张以内

## 二、最小调用示例

**Base64 内嵌（图片 < 10 MB）**：

```python
import anthropic
import base64

client = anthropic.Anthropic()

with open("chart.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "这张图里 Y 轴的单位是什么？最高的数据点是多少？",
                },
            ],
        }
    ],
)
print(msg.content[0].text)
```

**URL 引用（图片公网可达）**：

```python
msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/chart.png",
                    },
                },
                {"type": "text", "text": "描述这张图的趋势"},
            ],
        }
    ],
)
```

**URL 限制**：
- 必须是**公网可访问**（内网需用 base64）
- Anthropic 会**下载并存储**图片到服务端（与 Prompt Caching 兼容）
- 如果图片更新，要给不同 URL 避免缓存

## 三、Token 计算

**图片按 patch 算 token，不按内容**——同一张图不管多复杂，token 数只由分辨率决定。Claude 按 28×28 像素切块，每块算 1 个 visual token：

```
Token 计算公式（image）：
  tokens = ⌈width / 28⌉ × ⌈height / 28⌉
```

**两档分辨率**：

| 档位 | 适用型号 | 最长边上限 | visual token 上限 |
| --- | --- | --- | --- |
| **高分辨率** | Claude 4.7 及以后（含当前四型号） | 2576 px | 4784 |
| 标准 | 其余型号 | 1568 px | 1568 |

高分辨率档**自动生效**——不需要 beta header，也不用客户端开关。

**常见尺寸**（当前四型号 = 高分辨率档）：

| 尺寸 | 处理 | visual token |
| --- | --- | --- |
| 200×200（图标） | 不缩放 | 64 |
| 1000×1000 | 不缩放 | 1296 |
| 1092×1092 | 不缩放 | 1521 |
| 1920×1080 | 不缩放 | 2691 |
| 2000×1500 | 不缩放 | 3888 |
| 3840×2160（4K） | 缩到 2576×1449 | 4784 |

**反直觉**：同一张 4K 图，标准档缩到 1456×819 只花 **1560** token，高分辨率档却要 **4784**——**当前型号比老型号贵 3 倍左右**。不需要高保真就先降采样。

**PDF Token 计算**：PDF 每页会**同时**按图片和文本两路计费：

```
Token 计算公式（PDF，官方口径）：
  文本部分：每页约 1500 ~ 3000 token（按内容密度）
  图片部分：每页转成一张图，再按上面的公式算一遍
```

**反直觉**：PDF 成本按**页**叠加——10 页 PDF 的**文本部分**就 **1.5 万 ~ 3 万 token**，加上每页的图片开销，整体在 **3 万 ~ 8 万 token** 量级，比 1 张图片贵一个数量级。

> **别复用旧估算**：Claude 4.7 世代起换了 tokenizer，同样文本**约多 30% token**。换型号后请用 [`messages/count_tokens`](https://platform.claude.com/docs/en/build-with-claude/token-counting) 重新量，别拿老模型的数字套。

## 四、多图实战

**多张图混排**（对比、识别）：

```python
msg = client.messages.create(
    model="claude-opus-5-5",          # 复杂视觉任务用 Opus
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "对比这两张 UI 截图，列出 3 个主要差异："},
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img1}},
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img2}},
        ],
    }],
)
```

**OCR + 结构化提取**：

```python
# 发票 OCR
msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system="你是发票 OCR 助手。按 JSON 格式输出：金额、日期、发票号、商家。",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": invoice}},
            {"type": "text", "text": "提取这张发票的信息"},
        ],
    }],
)
```

**PDF 文档问答**：

```python
import base64

with open("contract.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

msg = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data,
                },
            },
            {"type": "text", "text": "这份合同里违约责任是怎么规定的？"},
        ],
    }],
)
```

**排版顺序**：官方建议**图片放在文字前面**——和长文档 prompt 的最佳实践一致（先给上下文，再给问题）。混排也能用，但图先、问后效果更稳。

## 五、何时该用 vision

| 场景 | 该用 vision？ | 替代方案 |
| --- | :---: | --- |
| UI 截图理解 | ✅ | — |
| 图表数据提取 | ✅ | — |
| 文档 OCR（发票 / 合同） | ✅ | — |
| 长 PDF 文档问答 | ✅（用 Opus 5.5） | 先 PDF 转文本 + text 提问 |
| 视频内容理解 | ❌ | 先抽帧 + 传图 |
| 验证码识别 | ⚠️ | Anthropic 禁止 |
| 隐私敏感图片 | ❌ | 走 [ZDR 模式](#六、常见坑) |

## 六、常见坑

**1. 体积上限，以及大图的 3 倍 token 代价**

```python
# ❌ 超过 10 MB（base64 编码后）会被拒；单边也不得超过 8000 px
with open("4k.png", "rb") as f:    # 20 MB
    data = base64.b64encode(f.read()).decode()

# ✅ 先降到当前型号的长边上限以内
from PIL import Image
img = Image.open("4k.png")
img.thumbnail((2576, 2576))
img.save("4k_resized.png", optimize=True)
```

**注意**：大图通常**不会报错，只会被悄悄缩放**——但当前型号是高分辨率档，4K 图要 4784 visual token，约为标准档的 3 倍。不需要高保真就先降采样。

**2. PDF token 爆炸**

100 页 PDF 光**文本**就 **15 万 ~ 30 万 token**——1M context 型号一次提问就吃掉 15%~30% 窗口。**实战做法**：

- 长 PDF 先用 [Long Context](/claude-capabilities/core/long-context) 切片策略
- 关键页 only（PDF reader 抽 5-10 页关键内容）
- 单次请求最多 600 页（context 小于 1M 的型号是 100 页）——但密集排版的 PDF 往往先撑爆 context，先到上限的不是页数

**3. base64 vs URL 选择**

| 场景 | 推荐 |
| --- | --- |
| **小图（< 100 KB）+ 临时** | base64（一次请求搞定） |
| **大图（> 1 MB）** | base64（避免 URL 下载失败） |
| **同一图多次复用** | URL（走 Anthropic 缓存） |
| **公网可达 + 长期** | URL |
| **内网 / 隐私** | base64（不走外网） |

**4. 动画 GIF 只取第一帧**

```python
# ❌ 传动画 GIF 期待"理解动作"
with open("animation.gif", "rb") as f:
    data = base64.b64encode(f.read()).decode()
# 实际只识别第一帧

# ✅ 抽关键帧 + 拼接
from PIL import Image
gif = Image.open("animation.gif")
frames = [gif.seek(i) or gif.copy() for i in range(gif.n_frames)]
# 拼成一张大图 / 多张图传
```

**5. ZDR 模式 + 图片**

Zero Data Retention 模式下，URL 图片**仍会**被 Anthropic 下载存储——**隐私敏感图片走 base64 + 确认 ZDR 启用**。

## 参考

- [Anthropic Docs · Vision](https://platform.claude.com/docs/en/build-with-claude/vision)（访问于 2026-11-13）
- [Anthropic Docs · PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)（访问于 2026-11-13）
- [Anthropic Docs · Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)（访问于 2026-11-13）
- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-11-13）
- [Opus 5.5 详解 · 视觉任务](/claude-capabilities/models/opus#四、opus-5-5-vs-sonnet-5-5-实测选型)
- [长上下文 · 文档处理策略](/claude-capabilities/core/long-context)
- [成本与 Token 管理 · 计费模型](/claude-code/basics/cost-and-tokens)

## 下一步

- 长 PDF 处理 → [长上下文](/claude-capabilities/core/long-context)
- 视觉推理 → [推理能力](/claude-capabilities/core/reasoning)
- 文档问答 Pipeline → [Tool Use 协议](/claude-capabilities/core/tool-use)

## 如果你想

- 图片安全 / 隐私 → [Anthropic Acceptable Use Policy](https://www.anthropic.com/legal/aup)
- ZDR 模式 → [模型概览 · 按数据驻留](/claude-capabilities/models/overview#按数据驻留-zdr)
- PDF 文本提取替代 → [Long Context · PDF 策略](/claude-capabilities/core/long-context)

---
title: 视觉能力
description: API 视角的图片 / PDF 处理；支持的格式、image block 怎么写、token 计算与多图实战
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  visionDocs: 'https://platform.claude.com/docs/en/build-with-claude/vision'
  accessedAt: 2026-08-06
---

# 视觉能力

> **TL;DR**：Claude 5 全系支持 vision（Opus 5 / Sonnet 5 / Haiku 4.5 / Fable 5）——支持 PNG / JPEG / GIF / WebP / PDF。**图片按尺寸算 token**（不按内容），**PDF 按页数 + 内容**算。API 视角通过 `image` block 传图（base64 或 URL），与 text block 混排。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 4 模型 vision 支持矩阵
- `image` block 的两种形式（base64 / URL）
- 图片 token 计算规则（按尺寸）
- PDF 传法与 token 计算
- 多图实战（多张图混排、对比、OCR）
- 何时该用 vision vs 不该用
- 5 个常见坑（token 爆炸、OCR 误读、隐私、base64 vs URL、动画 GIF）

## 一、4 模型 vision 支持

| 模型 | 图片（PNG/JPEG/GIF/WebP） | PDF | 视频帧 | 最大尺寸 |
| --- | :---: | :---: | :---: | --- |
| **Opus 5** | ✅ | ✅ | ❌ | 5 MB / 张 |
| **Sonnet 5** | ✅ | ✅ | ❌ | 5 MB / 张 |
| **Fable 5** | ✅ | ✅ | ❌ | 5 MB / 张 |
| **Haiku 4.5** | ✅ | ✅ | ❌ | 5 MB / 张 |

**注意**：
- Claude 4 代起 vision 走**原生多模态**——不是 OCR 后丢给文本模型
- **不支持视频流**——视频需先抽帧（按秒抽）再传
- **单张上限 5 MB**——超大会被 SDK 拒；超 1568×1568 px 会自动 resize

## 二、最小调用示例

**Base64 内嵌（图片 < 5 MB）**：

```python
import anthropic
import base64

client = anthropic.Anthropic()

with open("chart.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

msg = client.messages.create(
    model="claude-sonnet-5",
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
    model="claude-sonnet-5",
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

**图片按尺寸算 token，不按内容**——同一张图不管多复杂，token 数是固定的：

```
Token 计算公式（image）：
  tokens = (width × height) / 750
  最小 100 tokens，最大 1600 tokens
```

**常见尺寸**：

| 尺寸 | Token |
| --- | --- |
| 200×200 (图标) | 100 |
| 800×600 (普通图) | 640 |
| 1568×1568 (大图，会 resize) | 1600 |
| 4K (3840×2160，会 resize 到 1568) | 1600 |

**反直觉**：**4K 图和 1568×1568 图 token 数一样**——超大会 resize。

**PDF Token 计算**：

```
Token 计算公式（PDF）：
  tokens = ceil(页数 × 705) + max(0, 文本长度)
```

**反直觉**：PDF 一页约 **705 token base** + 实际文本——一张 10 页 PDF 可能 **7000+ token**，比 1 张图片贵 5-10 倍。

## 四、多图实战

**多张图混排**（对比、识别）：

```python
msg = client.messages.create(
    model="claude-opus-5",          # 复杂视觉任务用 Opus
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
    model="claude-sonnet-5",
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
    model="claude-opus-5",
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

## 五、何时该用 vision

| 场景 | 该用 vision？ | 替代方案 |
| --- | :---: | --- |
| UI 截图理解 | ✅ | — |
| 图表数据提取 | ✅ | — |
| 文档 OCR（发票 / 合同） | ✅ | — |
| 长 PDF 文档问答 | ✅（用 Opus 5） | 先 PDF 转文本 + text 提问 |
| 视频内容理解 | ❌ | 先抽帧 + 传图 |
| 验证码识别 | ⚠️ | Anthropic 禁止 |
| 隐私敏感图片 | ❌ | 走 [ZDR 模式](#六常见坑) |

## 六、常见坑

**1. 5 MB / 1568×1568 上限**

```python
# ❌ 一张 4K 图直接传
with open("4k.png", "rb") as f:    # 20 MB
    data = base64.b64encode(f.read()).decode()

# ✅ 先压缩
from PIL import Image
img = Image.open("4k.png")
img.thumbnail((1568, 1568))
img.save("4k_resized.png", optimize=True)
```

**2. PDF token 爆炸**

100 页 PDF ≈ **70,000 token**——一次提问就吃掉 70k context。**实战做法**：

- 长 PDF 先用 [Long Context](/claude-capabilities/core/long-context) 切片策略
- 关键页 only（PDF reader 抽 5-10 页关键内容）

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

- [Anthropic Docs · Vision](https://platform.claude.com/docs/en/build-with-claude/vision)（访问于 2026-08-06）
- [Anthropic Docs · PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)（访问于 2026-08-06）
- [Opus 5 详解 · 视觉任务](/claude-capabilities/models/opus#四opus-5-vs-sonnet-5实测选型)
- [长上下文 · 文档处理策略](/claude-capabilities/core/long-context)
- [成本与 Token 管理 · 图片 token 计算](/claude-code/basics/cost-and-tokens)

## 下一步

- 长 PDF 处理 → [长上下文](/claude-capabilities/core/long-context)
- 视觉推理 → [推理能力](/claude-capabilities/core/reasoning)
- 文档问答 Pipeline → [Tool Use 协议](/claude-capabilities/core/tool-use)

## 如果你想

- 图片安全 / 隐私 → [Anthropic Acceptable Use Policy](https://www.anthropic.com/legal/aup)
- ZDR 模式 → [模型概览 · 按数据驻留](/claude-capabilities/models/overview#按数据驻留zdr)
- PDF 文本提取替代 → [Long Context · PDF 策略](/claude-capabilities/core/long-context)

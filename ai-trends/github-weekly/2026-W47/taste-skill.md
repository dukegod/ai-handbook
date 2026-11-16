---
title: 'Leonxlnx/taste-skill：把「品味」写成在真实浏览器里跑的 checker'
description: taste-skill 深度解读——发给编码 Agent 的设计品味 skill、五道脚本流程、headless Chrome 多视口一致性检查与 finish gate、11 种 hero 布局发牌机制，以及「没有可执行 checker 的设计规范只是又一套 prompt」
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-16
---

# Leonxlnx/taste-skill：把「品味」写成在真实浏览器里跑的 checker

> **TL;DR**：116,318 star，**本月涨星 +19,546，涨星占存量 16.8%**（本周未进周榜，月榜第 6）。MIT 协议，JavaScript，仓库建于 **2026-02-19**，最新版本 **tasteskill v2.5.1（2026-11-07）**，最近一次提交 2026-11-07。**8 个 open issue、2 个 open PR**——对 11 万 star 的项目来说异常干净。目标一句话：让编码 Agent 做出的公司官网达到 figma.com 和 x.ai 的水准，而不是拼一个通用落地页。

📅 数据窗口：2026-11-10 ~ 2026-11-16 ｜ 🏷️ Agent 工具链 / 设计质量门 ｜ 本月涨星 +19,546 ｜ 总 star 116,318

## 是什么

[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) 是一个 Agent Skill，名字直白：给编码 Agent 装上「品味」。它的核心不是提示词模板，而是一整套**可执行的构建流水线**——先给 Agent 定规矩，再在真实浏览器里验收。

README 把自己定义为一个有具体约束的系统：普通文案、一套设计系统、一屏一段、左右边距对齐、**真实照片**（客户没有就用有授权的替代）、真实品牌图标与真实产品 UI、每页一个 hero 进场加一到两个「dealt moment」、安静的微交互；**shader 效果与滚动场景严格限定给科技 / 游戏 / 软件页**。最后一句是关键：**由一个 checker 和一个 finish gate 在真实浏览器里验证这些规则**。

五步流程：

1. **发牌（deal）**——`scripts/start.mjs` 按业务类型发一套配色和一组 Google Fonts 搭配（`library/palettes.json`、`library/type.json`）；`assets/layout/deal.mjs` 再发一种 hero 布局，**共 11 种**（split、centred、product、photo、place、collage、editorial、word、film、statement、triptych）。
2. **从一套系统起步**——`assets/starter.html` + `system.css` + `layout.css` 强制「一屏一段」（桌面基准 1440×900）、左右内容边距等宽、固定导航栏、单屏收尾页脚。
3. **真实产品 UI 与真实照片**——软件 / 科技页用重写过的 HTML UI 片段和节点连线图（`assets/ui/`、`assets/diagrams/`），品牌图标由 `scripts/icons.mjs` 解析成本地 SVG；门店 / 酒店 / 零售等页面以**策展过的真实照片**打头（`scripts/photos.mjs`），来源在页脚一行署名，**图下不加说明文字**。
4. **效果只给该给的页面**——shader 底、滚动场景、程序化 3D 打印**只发**给 software / tech / gaming 三类页面，且限制在 **4 个 WebGL 上下文**以内，手机与 `prefers-reduced-motion` 有静态回退。
5. **在真实浏览器里过 HTTP 检查**——`scripts/consistency.mjs` 等脚本用 headless Chrome 按 **1440、1024、768、390** 四个视口渲染，**逐条输出 PASS / WARN / FAIL**；`scripts/gate.mjs` 是 finish gate，**最多修三轮**，没有可修的 FAIL 就不放行。

## 技术亮点

**第一，它把「审美」翻译成了可判定的失败条件，而不是形容词。** README 列出的检查项包括：空画面、坏掉的 shader、对比度下降、列错位、section 高度漂移、占位文案、**编造的街道门牌号**、慢网络下的图片空隙。**「编造的街道门牌号」这种检查只有真的在渲染页面才能发现**——这正是它和「在提示词里写『不要编造地址』」的区别。

**第二，效果按业务类型发放，是一条反直觉但正确的规则。** README 写得很清楚：cafes、hotels、shops、studios、services **只拿照片和排版类的 moment，WebGL 数量为零**；shader 和 3D 只发给 software / tech / gaming。**「所有页面都炫」是 AI 生成站点最典型的病，而这里的修法是按业务类型限制，而不是按效果强度限制。**

**第三，它连「没有照片」这个真实约束都处理了。** 照片来自 Wikimedia Commons 等开放档案并署名，`photos.mjs` 会**限制图片体积**。这意味着 skill 在**客户确实没有素材**时仍能跑完，而不是卡在等素材。

**第四，它对安装环境的要求非常具体。** Node 22+、已安装的 **Chrome / Edge / Chromium**（非标准路径要设 `CHROME_PATH`）、可选 ffmpeg（用于 WebP 输出和 hero 照片的手机裁切）。**「它自己什么都不装、不需要任何 API key」**——这是个重要约束：**整套东西是确定性的，没有模型调用，所以结果可复现。**

**第五，它已经把 skill 变成桌面应用。** README 顶部主推 **TasteCode**——「Taste Skill as a desktop app, with a design agent built in」，免费开源。**skill 到产品的这一步通常发生在流量之后，这里是反过来的：先有可用的 CLI 与脚本，再包应用。**

## 后续发展建议

**最重要的判断是：任何「反 AI 味」「设计规范」类项目，值不值得用的唯一判据是有没有可执行的 checker。** 四个判断：

- **「没有 checker 的品味 skill，只是又一套 prompt」。** 这条判据可以直接用在选型上：读 README，看它**有没有列出能被自动判定为失败的规则**。taste-skill 的规则列表（对比度下降、列错位、占位文案、编造门牌号、图片空隙）本身就是一份可验收清单；反过来，只有「要有高级感」「避免千篇一律」这类描述的项目，**产出质量完全取决于模型当次的发挥**。

- **「多视口 + 真实渲染 + 明确 PASS / WARN / FAIL」这个组合可以直接抄成内部前端质量门。** 内部平台的 CI 里如果要做 UI 回归，**至少要有三个视口和一份机器可读的结果**，而不是让评审人肉眼看截图。**注意 WARN 的存在——它意味着规则分硬门（FAIL 必须修）和软门（WARN 提示），这个分级比全硬门更实用。**

- **「finish gate 最多修三轮」是一个值得抄的收敛策略。** Agent 反复自我修正容易无限循环；**给定最大轮次、每轮产出机器可读结果、超过上限就失败上报**——这是一条能直接写进 Agent 执行协议的规则，比「请最多尝试三次」这种提示词可靠。

- **技术选型上它的最大优点是确定性。** 没有模型调用、没有 API key，结果只取决于脚本和浏览器版本，**这让它适合放进 CI 而不是只适合本地试玩**。内部平台如果要建自己的「UI 质量门」，建议沿这条思路：**能确定判定的交给脚本，不能确定的交给模型评审**。

**风险与局限**：**最后提交是 2026-11-07，距本周窗口有 9 天**，更新频率比本周榜上多数项目低；**8 个 issue / 2 个 PR 几乎为零**，一方面说明质量稳定，另一方面也说明**外部反馈还没进来，口味是否真的被广泛认可还没被验证**；README 里写明照片与图标「需要网络访问」，**离线场景只有内置素材可用**；依赖 headless Chrome 与 Node 22+，**在 CI 里需要显式装浏览器**；skill 名叫 `design-taste-frontend`，定位是**公司官网与落地页**，不是通用产品 UI——**拿它做后台系统会水土不服**；最后，它把设计判断固化成了一组具体数字（一屏一段、4 个 WebGL 上下文、11 种 hero 布局），**这些是作者 taste 的量化，不是客观标准**——适合当起点，不适合当终局。

## 下一步

- 想看同一层问题的组件级方案 → [astryx 深度解读（本期同期项目）](./astryx.md)
- 想看「约束先行」的工程纪律版本 → [agent-skills 深度解读（本期同期项目）](./agent-skills.md)

## 如果你想

- 想理解设计与实现怎么分工 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看 Agent 工具全景 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)

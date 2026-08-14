---
title: 死链检查
description: v0.4.2 工程项——lychee 0.24 schema + 修真 3 处 URL + 排除 ~20 类 false positive；防 sidebar 🚧 漏修 / 内部链接错位 / 外部 404
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-10
---

# 死链检查

> **背景**：v0.3.1 收尾时发现 sidebar 多处 `P('xxx')` 占位 🚧 漏去掉——手动同步机制不可靠。**v0.4.1 引入 lychee 死链检查**——v0.4.2 升级到 0.24 schema + 真跑过、修过 3 处 URL + 排除 ~20 类 false positive，**139 个 .md 文件 0 错通过**。

## 一、为什么需要

Claude Handbook 当前 113+ 篇 published，跨段引用频繁（v0.3 共 46 篇就触发过 3 次死链事故）：

| 事故 | 原因 | 损失 |
| --- | --- | --- |
| v0.3.1 收尾 | 12 处 sidebar 🚧 漏修 | 1 个 fix commit 修复 |
| v0.3.2.2 messages | `./sonnet` 相对路径 VitePress 解析失败 | 1 处链接改绝对路径 |
| v0.3.3 claude-ai | `/surfaces/desktop` 错文件名（应是 `desktop-app`） | 1 处链接修复 |
| v0.4.2 message-batches | `messages-batches` 拼错（无 `/`） | 3 处 URL 修真 |

**v0.4.1 之前**：每次发布靠**手动 `pnpm build` 看死链警告**——耗时、易漏。
**v0.4.2 之后**：本地 + CI 自动跑 + `failMode=error`——死链 = merge block。

## 二、3 个交付物

| 文件 | 作用 |
| --- | --- |
| `lychee.toml`（项目根） | lychee 配置（接受状态码 / 排除规则 / 缓存 / fallback 扩展） |
| `scripts/check-links.sh`（项目根） | 本地命令包装（`bash scripts/check-links.sh`） |
| [`.github/workflows/lychee.yml`](/.github/workflows/lychee.yml) | CI workflow（push + PR 触发，failMode=error） |

## 三、3 种安装方式

**macOS**（推荐）：
```bash
brew install lychee
```

**Cargo**（任何平台）：
```bash
cargo install lychee --locked
```

**Docker**（无需安装）：
```bash
docker run --rm -v $(pwd):/input lycheeverse/lychee /input
```

## 四、3 种使用方式

### 1. 本地快速跑

```bash
pnpm check-links
# 等价于 bash scripts/check-links.sh
```

**v0.4.2 行为**：

- 扫描 139 个 .md 文件
- 用 `--files-from` 显式传文件列表（避免 lychee 0.24.2 CLI 多 glob 解析 bug）
- 用 `--root-dir "$(pwd)"` 解析 VitePress root-relative 链接
- 输出到 `./scripts/.lychee-out` 详细报告
- **0 错** 退出 0；有错退出 2

### 2. 本地直接调 lychee

```bash
# v0.4.2 推荐：单文件列表 + root_dir
lychee --config lychee.toml --root-dir "$(pwd)" --files-from <(find . -name "*.md" -not -path "./node_modules/*")

# 离线模式（只查本地 + 锚点，快）
lychee --offline --config lychee.toml --root-dir "$(pwd)" "claude-code/basics/claude-md.md"

# 排除 generated 内容（靠 lychee.toml 的 exclude_path，无需 CLI 传）
lychee --config lychee.toml --root-dir "$(pwd)" "claude-code/basics/claude-md.md"
```

### 3. CI 自动跑

push 到 `main` / `content/**` / `fix/**` / `infra/**` 分支 + 每个 PR → GitHub Action 自动跑。

**v0.4.2 升级**：`failMode: error`（v0.4.1 阶段用 warning 让 PR 不卡发版，v0.4.2 升级为 error 死链 = merge block）。

## 五、配置速查（`lychee.toml`）

### v0.4.2 新增 / 升级字段

```toml
# verbose 0.24+ 改字符串（v0.4.1 用 bool 错）
verbose = "warn"  # error / warn / info / debug / trace

# accept 数组（v0.4.1 用数字 OK，0.24 数组形式更标准）
accept = [200, 203, 206, 301, 302, 303, 304, 307, 308]

# 排除路径（生成产物）—— v0.4.2 改用正则字符串
exclude_path = [
    "(^|/)node_modules",
    "(^|/)\\.vitepress",
    "(^|/)public",
    "(^|/)assets",
    "(^|/)\\.lycheecache",
]

# Fallback 扩展（无扩展名链接尝试 .md / .html）
fallback_extensions = ["md", "html"]

# 排除 URL —— v0.4.2 加 ~20 类 false positive
exclude = [
    "^http://localhost",          # 本地 dev
    "^mailto:",                    # 邮箱
    "^https?://coding\\.jd\\.com", # 公司内 Git（CI runner 访问不到）
    "^https?://(www\\.)?claude\\.ai",  # 拒绝 lychee 爬虫
    "^https?://aws\\.amazon\\.com/bedrock",  # 超时
    "logo\\.svg$",                 # VitePress public 资源
    "hero\\.svg$",
    "favicon\\.svg$",
    "favicon\\.ico$",
    "^https?://docs\\.claude\\.com/en/docs/",  # 平台迁移中
    "^https?://code\\.claude\\.com/docs/en/commit$",  # 文档已迁
    "^https?://(www\\.)?npmjs\\.com/package/",  # npmjs 反爬
    "^https?://slack\\.com/apps/.*-claude$",  # marketplace 迁移
    # ... 详见 lychee.toml
]

# 超时 / 重试
timeout = 20
max_retries = 3
retry_wait_time = 2
```

完整配置见 `lychee.toml`。

详见 [lychee 0.24 官方文档](https://lychee.cli.rs/)。

## 六、5 个实战场景

### 场景 1：sidebar 🚧 漏修检测

```text
场景：刚 published 一篇，没改 sidebar
lychee 输出：
  ✘ 404  /claude-code/foo  .vitepress/config.ts
       → 提示：sidebar 链到未 published 占位
```

**修复**：参考 [v0.3.1 收尾 · sidebar 同步](/contributing/roadmap#v031-收尾修复-2-处)，把 `P('xxx')` 改成 `'xxx'` 直接字符串。

### 场景 2：内部链接文件名错位

```text
lychee 输出：
  ✘ 404  /claude-capabilities/surfaces/desktop  /surfaces/desktop.md
       → 实际是 desktop-app.md
```

**修复**：把链接改成 `/claude-capabilities/surfaces/desktop-app`。

### 场景 3：外部 URL 拼错（v0.4.2 真修过）

```text
lychee 输出：
  ✘ 404  https://platform.claude.com/docs/en/api/messages-batches  3 处
       → 真实 URL 应是 https://platform.claude.com/docs/en/api/messages/batches（带 /）
```

**修复**：用 `sed` 批量替换或手动改 3 处 md 文件。本例修改了 `claude-capabilities/models/{choosing-model,haiku}.md` 和 `claude-capabilities/api/message-batches.md`。

### 场景 4：平台迁移中（v0.4.2 加 exclude）

```text
lychee 输出：
  ✘ 404  https://docs.claude.com/en/docs/build-with-claude/system-prompts  2 处
       → 实际是 redirect 到 platform.claude.com/en/docs/build-with-claude/system-prompts
       → 但 platform 上对应 URL 也 404（平台迁移中）
```

**修复**：把 `https://docs.claude.com/en/docs/` 整段加到 `lychee.toml` 的 `exclude` 列表——平台迁移完成后再清。

### 场景 5：反爬 / 限流（v0.4.2 加 exclude）

```text
lychee 输出：
  ✘ 403  https://www.npmjs.com/package/@anthropic-ai/sdk  3 处
       → npmjs 拒绝 lychee User-Agent
  ✘ 403  https://claude.ai/  2 处
       → claude.ai 拒绝爬虫
```

**修复**：把 `^https?://(www\\.)?npmjs\\.com/package/` 和 `^https?://(www\\.)?claude\\.ai` 加到 `exclude`。

## 七、CODING 平移（公司内 Git）

本仓库用 **coding.jd.com**（不是 GitHub），需要平移 lychee workflow：

```yaml
# coding 流水线（.coding/pipeline.yml 风格）
steps:
  - name: Checkout
    command: git clone ...
  - name: Run Lychee
    image: lycheeverse/lychee:latest
    command: |
      lychee \
        --config lychee.toml \
        --root-dir "$(pwd)" \
        --files-from <(find . -name "*.md" -not -path "./node_modules/*") \
        --format detailed \
        --no-progress
```

**v0.4.2 升级**：CI 阶段 `failMode: error`——平移到 CODING 时也保持 error，不要回退到 warning。

## 八、5 个常见坑

**1. lychee 0.24+ verbose 字段改字符串**

```bash
# v0.4.1 写法（0.24 之前 OK）
verbose = false
# 0.24+ 报 invalid verbosity value

# v0.4.2 写法
verbose = "warn"  # error / warn / info / debug / trace
```

**2. lychee 0.24.2 CLI 多 glob 解析有 bug**

```bash
# 报错：recursive wildcards must form a single path component
lychee "**/*.md" "!**/node_modules/**"

# v0.4.2 解法：用 --files-from + find 显式列文件
find . -name "*.md" -not -path "./node_modules/*" > /tmp/files.txt
lychee --files-from /tmp/files.txt
```

**3. root-relative 链接不解析**

```text
lychee 输出：Cannot resolve root-relative link '/claude-code/xxx': provide a root dir
```

**v0.4.2 解法**：所有调用都加 `--root-dir "$(pwd)"`（本地）或 `--root-dir $&#123;&#123; github.workspace &#125;&#125;`（CI）。

**4. `.lycheecache` 误提交**

```bash
# 已在 .gitignore
.lycheecache
scripts/.lychee-out
```

**5. CI 跑太慢（> 5 min）**

139 篇 + 外链，**典型 30-60 秒**。CI 设 `timeout-minutes: 10` 足够。**v0.4.2 实测**：本地 22 秒（带缓存）。

## 九、已知限制（v0.4.2 阶段）

**中文锚点不被检查**——VitePress 用自己的 slug 算法（"一、Session 是什么" → `#一session-是什么`），lychee 用 GFM 算法（可能 → `#1-session-是什么`），**两者不一致**。`include_fragments` 在 v0.4.2 暂不开启，避免 false positive。

**VitePress 内部资源**——`/logo.svg` / `/hero.svg` / `/favicon.svg` 在 VitePress 解析时映射到 `public/*.svg`，lychee 不知道映射，需手动 `exclude`。

**平台迁移中**——`docs.claude.com` 全部 URL 暂 exclude，等 platform.claude.com 上对应页面 200 后再清 exclude。

## 十、调试

```bash
# 跑 debug 模式看每个请求详情
lychee --config lychee.toml --root-dir "$(pwd)" --files-from <(find . -name "*.md" -not -path "./node_modules/*") --verbose debug

# 单链接测试
lychee --offline --config lychee.toml --root-dir "$(pwd)" "claude-code/basics/claude-md.md"

# 看 .lycheecache（缓存命中加速）
cat .lycheecache 2>/dev/null | head -20

# 清缓存重跑
rm -rf .lycheecache scripts/.lychee-out
pnpm check-links
```

## 参考

- [lychee 0.24 官方文档](https://lychee.cli.rs/)
- [lycheeverse/lychee GitHub](https://github.com/lycheeverse/lychee)
- [lycheeverse/lychee-action](https://github.com/lycheeverse/lychee-action)
- CLAUDE.md · 内容开发工作流第 6 步（"无死链" 升级为 lychee 自动验证）
- [CLAUDE.md](/)

## 下一步

- 切到 CI 部署升级 → [v0.4.2 · CI 部署](/contributing/roadmap#v04-精修与工程化)
- 切到术语 lint → [v0.4+ · 术语 lint](/contributing/roadmap#v04-精修与工程化)
- 切到 Algolia 搜索 → [v0.4+ · Algolia 搜索增强](/contributing/roadmap#v04-精修与工程化)

## 如果你想

- 实战场景细节 → [5 个实战场景](#六5-个实战场景)
- CODING 平台平移 → [CODING 平移](#七coding-平移公司内-git)
- 已知限制与 workaround → [已知限制](#九已知限制v042-阶段)
- 死链事故复盘 → [为什么需要](#一为什么需要)

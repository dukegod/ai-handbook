---
title: CLAUDE.md 项目记忆
description: 四级 CLAUDE.md（Managed / User / Project / Local）的加载规则、结构建议、/init 与 @import，以及 Auto Memory 的边界
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-08
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/memory'
  accessedAt: 2026-08-08
---

# CLAUDE.md 项目记忆

> **TL;DR**：CLAUDE.md 是**每次会话自动加载**的项目 / 用户 / 企业级记忆。**四级继承**（Managed → User → Project → Local）+ `@import` 导入其他文件 + `/init` 自动生成 + `/memory` 交互编辑。建议 < 200 行、写具体规则、别指望它是硬约束（要硬约束用 Hook）。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- CLAUDE.md 是什么、什么时候被加载
- **四级继承**的路径与加载顺序（Managed / User / Project / Local）
- `/init` 与 `/memory` 两个必须掌握的命令
- `@import` 语法、AGENTS.md 兼容、跨 worktree 分享
- CLAUDE.md vs Auto Memory 的边界
- 写作建议 + 常见排查

## 前置

- 装好 Claude Code
- 已读 [心智模型 · 上下文里有什么](/getting-started/mental-model#三上下文里有什么) 建立对「每次会话开头加载什么」的直觉

## 一、CLAUDE.md 是什么

**你写、Claude 每次会话开头自动加载**的 markdown 文件——用来沉淀 Claude 每次都应该知道的项目事实：build 命令、目录约定、编码规范、「总是做 X」的规则。

⚠️ 它**不是硬约束**——Claude Code 把它作为 user message 注入，Claude 读完尽量遵守但不保证。想要硬约束用 [Hook](/claude-code/customization/hooks)。

**什么时候加进去？** 官方建议：

- Claude 第二次犯同样错误
- Code review 抓住 Claude 应该知道的项目细节
- 你在两次会话里输入同一条 correction
- 新同事要靠这段 context 才能上手

## 二、四级继承：从广到窄

四层**都会加载**，按下表顺序拼接进 context——**越靠后越 specific，冲突时叶胜**：

| 层级 | 路径 | 用途 | 共享范围 |
| --- | --- | --- | --- |
| **Managed policy**（企业） | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />Linux/WSL: `/etc/claude-code/CLAUDE.md`<br />Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | 全组织规范 | 组织所有用户 |
| **User instructions** | `~/.claude/CLAUDE.md` | 个人偏好（跨项目） | 只你自己 |
| **Project instructions** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享项目规范 | 团队（通过 git） |
| **Local instructions** | `./CLAUDE.local.md` | 个人级项目偏好 | 只你自己（**记得 `.gitignore`**） |

**Walk-up 目录树**：Claude Code 从当前目录一层层向上找 `CLAUDE.md` 与 `CLAUDE.local.md`——在 `foo/bar/` 启动会加载 `foo/bar/CLAUDE.md`、`foo/CLAUDE.md`、以及各自旁边的 `.local.md`。**子目录**里的 CLAUDE.md 启动时**不加载**，Claude 读到那个目录里的文件才按需加载。

**跨 worktree 分享个人偏好**：`CLAUDE.local.md` 是 gitignore 的、每个 worktree 独立。想跨 worktree 共享 personal instructions，用 `@` 导入 home 目录里的文件：

```markdown
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

## 三、`/init`：自动生成

```text
/init
```

Claude 扫你的代码库，生成 starting CLAUDE.md（含 build 命令、测试指令、约定）。**已有 CLAUDE.md 时它会建议改进而不覆盖**。

`/init` 还会读你项目里其他 AI 工具的规则文件并整合：

- Cursor：`.cursor/rules/` / `.cursorrules`
- Copilot：`.github/copilot-instructions.md`
- 新版（设 `CLAUDE_CODE_NEW_INIT=1`）还读：`AGENTS.md` / `.devin/rules/` / `.windsurf/rules/` / `.clinerules`

## 四、`@import`：导入其他文件

CLAUDE.md 支持 `@path/to/file` 语法引入其他 markdown 文件（也可导入 README、package.json 等）：

```markdown
See @README for overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

- 相对 / 绝对路径都行；递归最多 **4 层**深度
- Code span 与 fenced code block 里的 `@` 不解析（想文档里提路径又不导入，用反引号包）
- **外部导入**（超出工作目录）首次触发 approval dialog

**AGENTS.md 兼容**：Claude Code 只读 `CLAUDE.md`。已有 `AGENTS.md` 的仓库用 `@AGENTS.md` 导入或 `ln -s AGENTS.md CLAUDE.md` 符号链接即可。

## 五、`/memory`：查看与编辑

```text
/memory
```

列出所有 memory 文件（CLAUDE.md / CLAUDE.local.md / auto memory），可以：

- 打开任意文件编辑
- 切换 Auto Memory 开关
- 打开 auto memory 目录

查**实际加载了什么**用 `/context`（列出 Memory files 段）。

## 六、CLAUDE.md vs Auto Memory

Claude Code 有两套 memory 机制，互补：

| | CLAUDE.md | Auto Memory |
| --- | --- | --- |
| **谁写** | 你 | Claude 自己 |
| **写什么** | 规则与约束 | Claude 发现的模式与偏好 |
| **作用域** | 项目 / 用户 / 组织 | 每 repo 一份（跨 worktree 共享） |
| **加载** | 全文，每次会话开头 | 只加载 `MEMORY.md` 前 200 行 / 25 KB |
| **适合** | 编码标准、workflow、架构决策 | build 命令、debug 心得、Claude 学到的偏好 |

Auto Memory 默认开启，存 `~/.claude/projects/<project>/memory/`。让 Claude "记住 API tests 需要本地 Redis"，它自动写 auto memory；**想写进 CLAUDE.md** 就明确说「添加到 CLAUDE.md」。

关闭 Auto Memory：`settings.json` 里 `autoMemoryEnabled: false` 或环境变量 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`。

## 七、写作建议

- **大小**：目标每份 CLAUDE.md **< 200 行**。太长挤 context、且 Claude 遵守率降低。需要更细粒度时用 [`.claude/rules/`](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) 做 path-scoped
- **结构**：用 markdown headers 与 bullets 分组。Claude 和人一样读结构
- **具体性**：写可验证的规则。「用 2-space 缩进」比「格式化代码」好；「commit 前跑 `npm test`」比「测试改动」好；「API handler 在 `src/api/handlers/`」比「文件保持整齐」好
- **一致性**：定期核查——两处矛盾时 Claude 可能随机选一个
- **HTML 注释**：`<!-- 给人看的注释 -->` 会被剥离，**不进 context**（省 token 的好办法）

## 八、path-scoped rules 实战补充

第七节提了 path-scoped 思路——这一节展开**怎么用、什么时候不灵**。

### 8.1 两条核心规则

| Rule 文件 | 加载时机 | 适用场景 |
| --- | --- | --- |
| 无 `paths:` | **全局生效**，每次会话开头加载 | 整个项目通用规则（类似原 CLAUDE.md 内容） |
| 带 `paths:` | **路径作用域**：`Read` 匹配文件时按需注入 | 大 CLAUDE.md 上下文爆炸的拆分解药 |

### 8.2 YAML frontmatter 正确写法

```markdown
---
paths:
  - "src/app/**/*.tsx"          # Next.js App Router 页面
  - "src/components/**/*.tsx"   # 所有 UI 组件
  - "**/*.test.{ts,tsx}"        # 测试文件
---

# UI/UX Rules（仅在处理以上文件时生效）

- 必须基于 shadcn/ui + Radix 构建
- 支持深色模式（dark: 前缀）
- 所有交互元素必须有 aria-label
```

**要点**：YAML 数组（`- "path"`），不要逗号分隔；路径加双引号；可放子目录但匹配按项目根算。

### 8.3 实际效果

让 Claude 编辑：

- `src/components/ui/button.tsx` → 自动加载 `ui-ux.md` + `code-style.md`
- `src/app/api/knowledge/route.ts` → 自动加载 `api-design.md` + `security.md`
- `src/lib/utils.ts`（不匹配任何 scoped rule）→ 只加载全局规则

上下文更干净，响应更快。配合 [Hooks 路径感知](/claude-code/customization/hooks#92-路径感知matcher--脚本判断--rules-联动) 用效果最佳——rule 限定范围，hook 只在命中路径上跑检查。

### 8.4 已知问题与调试（2026.3 状态）

- **加载时机**：主要依赖 `Read`。`Write` / `Edit` 支持仍在优化，部分版本 Write 时不立即加载，需先 Read 或重启
- **调试**：
  - `/debug rules` 或 `/context` 查看当前已加载的 rules
  - 想强制触发可先 `/read src/components/button.tsx`
  - VS Code 插件行为与 CLI 一致，但有时需重启扩展
- **与 CLAUDE.md 的关系**：全局规则放 CLAUDE.md 或无 `paths:` 的 rule 文件；路径特定规则**必须**拆到 `.claude/rules/`

## 常见坑

**Claude 不遵守 CLAUDE.md**

CLAUDE.md 是**建议不是硬约束**。排查：

1. `/context` 确认 Memory files 段里列出了你的文件
2. 具体度不够？改成可验证形式（见「写作建议」）
3. 检查跨文件是否有冲突
4. **必须硬约束**用 [Hook](/claude-code/customization/hooks)

**`CLAUDE.local.md` 被 commit**

`CLAUDE.local.md` 是**约定 gitignore** 的。创建时立刻加进 `.gitignore`——`/init` 交互式模式选个人选项会自动做这个。

**Compact 后 CLAUDE.md 指令好像丢了**

**项目根 CLAUDE.md 会在 compact 后被自动 re-inject**，但**子目录级 CLAUDE.md 不会**（下次读那个目录里的文件才 reload）。想让某条指令跨 compact 稳定生效，写在**项目根**。

**CLAUDE.md 太长**

`/doctor` 提供 trim 建议：砍能从代码库推导的内容（目录树 / 依赖列表 / 架构概述），保留 pitfalls / 与 tool 默认不同的约定。

## 本项目的 CLAUDE.md（活样本）

Claude Handbook 自己在根目录维护 [CLAUDE.md](https://coding.jd.com/sz-fe/claude-wiki/blob/main/CLAUDE.md)——一个真实项目的 CLAUDE.md 长什么样，直接看这个即可。它遵循本页的所有建议：< 200 行、分组清晰、术语约束、已知坑、当前阶段任务。

## 参考

- [Anthropic Docs · Memory & CLAUDE.md](https://code.claude.com/docs/en/memory)（访问于 2026-07-28）
- [Anthropic Docs · Context window](https://code.claude.com/docs/en/context-window)（访问于 2026-07-28）
- [Anthropic Docs · Settings · claudeMd 键](https://code.claude.com/docs/en/settings)（访问于 2026-07-28）

## 下一步

- 学控制 Claude 能做什么 → [权限系统](./permissions)

## 如果你想

- 硬约束某个行为 → [Hooks](/claude-code/customization/hooks)
- 大项目组织多份规则 → [官方 `.claude/rules/` 指南](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)
- 让稳定能力包被 Claude 自动选用 → [什么是 Skill](/claude-code/skills/what-is-a-skill)
- 查所有会话 slash 命令 → [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)

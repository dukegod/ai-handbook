---
title: 键位配置
description: 'Claude Code 键位定制——常用默认快捷键速查、~/.claude/keybindings.json 自定义格式、20 个 context 与 namespace:action、Vim 模式与 vimInsertModeRemaps'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  interactiveDocs: 'https://code.claude.com/docs/en/interactive-mode'
  keybindingsDocs: 'https://code.claude.com/docs/en/keybindings'
  accessedAt: 2026-08-04
---

# 键位配置

> **TL;DR**：Claude Code 的默认快捷键够用 80% 场景。想改就编辑 `~/.claude/keybindings.json`——按 context 分组，把键映射到 `namespace:action`，设 `null` 解绑。Vim 党可开 `editorMode: vim` + `vimInsertModeRemaps` 把 `jj` 映射成 Esc。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- 默认快捷键速查（通用 / 文本编辑 / 快速命令）
- `~/.claude/keybindings.json` 自定义格式
- 20 个 context 与 `namespace:action` 命名
- Vim 模式与 `vimInsertModeRemaps`
- 保留键与终端冲突

## 前置

- Claude Code v2.1.220 交互式模式

## 一、默认快捷键速查

### 通用控制

| 键 | 作用 |
| --- | --- |
| `Ctrl+C` | 中断运行；空 prompt 时第一次清输入、第二次退出 |
| `Ctrl+D` | 退出 Claude Code（800ms 内按两次确认） |
| `Ctrl+L` | 重绘屏幕；fullscreen 模式连按两次 = `/clear` |
| `Ctrl+O` | 切换 transcript 查看器（看 tool 调用细节） |
| `Ctrl+R` | 反向搜索命令历史 |
| `Ctrl+T` | 切换 Claude 的 to-do checklist 显示 |
| `Ctrl+S` | 暂存/恢复 prompt（有文本时暂存，空 prompt 时恢复） |
| `Ctrl+B` | 把运行中的任务转后台（tmux 用户按两次） |
| `Ctrl+G` / `Ctrl+X Ctrl+E` | 在外部编辑器编辑 prompt |
| `Esc` | 中断 Claude 或关对话框 |
| `Esc Esc` | 清输入草稿 / 空 prompt 时开 rewind 菜单 |
| `Shift+Tab` | 循环切换 permission mode |
| `Option+P` / `Alt+P` | 切换模型 |
| `Option+T` / `Alt+T` | 切换 extended thinking |
| `Option+O` / `Alt+O` | 切换 fast mode |

### 文本编辑（readline 风格）

| 键 | 作用 |
| --- | --- |
| `Ctrl+A` / `Ctrl+E` | 行首 / 行尾 |
| `Ctrl+K` / `Ctrl+U` | 删到行尾 / 删到行首 |
| `Ctrl+W` | 删前一个词 |
| `Ctrl+Y` | 粘贴删掉的文本 |
| `Alt+B` / `Alt+F` | 按词左移 / 右移 |
| `Ctrl+_` / `Ctrl+Shift+-` | 撤销输入编辑 |

**macOS 注意**：`Alt+B` / `Alt+F` / `Alt+Y` / `Alt+P` 需在终端配 Option 为 Meta——iTerm2: Profiles → Keys → 设 Left/Right Option 为 "Esc+"；VS Code: `terminal.integrated.macOptionIsMeta: true`。

### 快速命令（行首输入）

| 前缀 | 作用 |
| --- | --- |
| `/` | 命令或 skill |
| `!` | Shell 模式——跑命令并让 Claude 响应输出 |
| `@` | 文件路径补全 |
| `:` | Emoji shortcode（v2.1.217+） |
| `?`（空输入时） | 切换快捷键帮助面板 |

### 多行输入

| 方式 | 适用 |
| --- | --- |
| `\` + `Enter` | 所有终端 |
| `Shift+Enter` | iTerm2 / WezTerm / Ghostty / Kitty / Warp / Apple Terminal / Windows Terminal 原生支持 |
| `Ctrl+J` | 任何终端 |
| `Option+Enter` | macOS 配 Option as Meta 后 |

VS Code / Cursor / Alacritty / Zed 需跑 `/terminal-setup` 装 Shift+Enter 绑定。

## 二、自定义 keybindings.json

敲 `/keybindings` 创建或打开 `~/.claude/keybindings.json`：

```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

**结构**：

- `bindings` 数组，每块指定一个 `context` + 键映射
- 键 = 击键序列，值 = `namespace:action`（或 `null` 解绑）
- **改完自动生效**，无需重启

### 20 个 Context

| Context | 场景 |
| --- | --- |
| `Global` | 全局 |
| `Chat` | 主输入框 |
| `Autocomplete` | 补全菜单 |
| `Confirmation` | 权限确认对话框 |
| `Transcript` | transcript 查看器 |
| `HistorySearch` | Ctrl+R 历史搜索 |
| `Task` | 后台任务运行中 |
| `ThemePicker` / `ModelPicker` | 选择器 |
| `Tabs` / `Footer` / `Select` | 导航组件 |
| `DiffDialog` | diff 查看器 |
| `MessageSelector` | rewind 消息选择 |
| `Scroll` | fullscreen 滚动 |
| `Plugin` / `Settings` / `Help` | 各自面板 |

### 常用 Action

| Action | 默认 | 作用 |
| --- | --- | --- |
| `chat:submit` | Enter | 提交 |
| `chat:newline` | Ctrl+J | 换行不提交 |
| `chat:externalEditor` | Ctrl+G | 外部编辑器 |
| `chat:cycleMode` | Shift+Tab | 切 permission mode |
| `chat:modelPicker` | Meta+P | 模型选择 |
| `app:toggleTodos` | Ctrl+T | 显示 to-do |
| `app:toggleTranscript` | Ctrl+O | 显示 transcript |
| `history:search` | Ctrl+R | 历史搜索 |
| `task:background` | Ctrl+B | 转后台 |

## 三、击键语法

**修饰键**（`+` 连接）：

```text
ctrl+k          Ctrl + K
shift+tab       Shift + Tab
meta+p          Option/Alt + P
ctrl+shift+c    多修饰键
```

`cmd` 只在支持 Kitty keyboard protocol 的终端能检测——多数终端不发，想跨终端通用用 `ctrl` 或 `meta`。

**大写字母**：单独大写字母隐含 Shift（`K` = `shift+k`）；带修饰键的大写是风格性的（`ctrl+K` = `ctrl+k`，不隐含 Shift）。

**Chord（序列）**：空格分隔

```text
ctrl+x ctrl+k   先 Ctrl+X，松开，再 Ctrl+K
```

**特殊键**：`escape` / `enter` / `tab` / `space` / `up` `down` `left` `right` / `backspace` `delete`。

## 四、解绑与保留键

**解绑**：值设 `null`

```json
{ "context": "Chat", "bindings": { "ctrl+s": null } }
```

要回收 chord 前缀（如想让 `ctrl+x` 单键生效），必须解绑所有以它开头的 chord。

**保留键（不可重绑）**：

| 键 | 原因 |
| --- | --- |
| `Ctrl+C` | 硬编码中断 |
| `Ctrl+D` | 硬编码退出 |
| `Ctrl+M` | 终端里等同 Enter |
| `Caps Lock` | 不送达终端 |

**终端冲突**：`Ctrl+B`（tmux prefix）/ `Ctrl+A`（GNU screen）/ `Ctrl+Z`（SIGTSTP）。

## 五、Vim 模式

`/config` → Editor mode → `vim`，或 settings.json：

```json
{ "editorMode": "vim" }
```

支持 NORMAL / INSERT / VISUAL 模式，常用 motion（`hjkl` / `w` / `e` / `b` / `0` / `$` / `gg` / `G` / `f` / `t`）、text object（`iw` / `i"` / `i(`）、操作符（`d` / `c` / `y` / `p`）。

**`jj` 映射成 Esc**（v2.1.208+）：

```json
{
  "editorMode": "vim",
  "vimInsertModeRemaps": { "jj": "<Esc>" }
}
```

**仅从 user settings / `--settings` / managed settings 读取**——项目级 settings 里的 `vimInsertModeRemaps` 被忽略（防仓库重映射你的键）。

**Vim 与 keybindings 独立**：vim 管 text input 层，keybindings 管组件层。Vim 的 Esc 切 INSERT→NORMAL，不触发 `chat:cancel`。Vim 键不能通过 keybindings 文件改——用 `vimInsertModeRemaps`。

## 六、验证与调试

Claude Code 自动验证 keybindings，告警：

- JSON / 结构解析错
- 无效 context 名
- 保留键冲突
- 终端 multiplexer 冲突
- 同 context 内重复绑定

加载时显示告警，写入 debug log。`claude --debug` 看详情。

## 常见坑

**macOS Alt 快捷键不生效**——终端没配 Option as Meta。iTerm2 / Apple Terminal / VS Code 各有配置位置（见上文）。

**改了 keybindings 没生效**——正常应该自动生效。检查 JSON 语法、context 名拼写。`claude --debug` 看加载告警。

**Vim 模式下 `?` 不出帮助面板**——vim NORMAL 模式 `?` 是 vim 行为（反向搜索）。想用 Claude 的帮助面板先 `i` 回 INSERT。

**`Ctrl+X` 单键想用但被 chord 占**——必须解绑所有 `ctrl+x` 开头的 chord（`ctrl+x ctrl+k` / `ctrl+x ctrl+e` / `ctrl+x ctrl+b`）才能回收前缀。

**把 `vimInsertModeRemaps` 写进项目 settings**——被忽略。只能写 `~/.claude/settings.json` 或 managed settings。

## 参考

- [Anthropic · Interactive mode](https://code.claude.com/docs/en/interactive-mode)（访问于 2026-08-04）—— 默认快捷键全表 + Vim 模式
- [Anthropic · Customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings)（访问于 2026-08-04）—— keybindings.json 完整参考

## 下一步

- 回顾 settings 全貌 → [Settings 配置文件](./settings)
- 看权限模式切换 → [权限系统](../basics/permissions)
- 配 Hooks 自动化 → [Hooks](./hooks)

## 如果你想

- 看 Vim 完整 motion 表 → [Anthropic · Interactive mode · Vim](https://code.claude.com/docs/en/interactive-mode#vim-editor-mode)
- 理解 transcript 查看器 → 敲 `Ctrl+O` 试用
- 终端配置（Option as Meta 等） → [Anthropic · Terminal configuration](https://code.claude.com/docs/en/terminal-config)

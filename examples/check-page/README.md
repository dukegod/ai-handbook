# check-page Skill

一个最小可复现的 Claude Code Skill 示例——按 [style-guide](../../contributing/style-guide) 第十节「PR 前自检 checklist」给仓库里任意一篇 md 做写作规范体检，输出脚本能自动判断的那部分问题。

> **配套教程**：[写你的第一个 Skill](../../cookbook/build-first-skill)（位于主 wiki 的 `cookbook/`）

## 它做了什么

触发后会自动跑 `scripts/check_page.py`，对指定文件做 4 类体检：

1. **frontmatter 必填字段**：`title` / `description` / `audience` / `difficulty` / `status` / `lastUpdated` 缺一即报
2. **汉字数上限**（1500）：超出建议拆篇
3. **术语易错对照**：命中 `claude` 拼写、术语对齐、型号名空格等规则
4. **中英间距**：中文与英文/数字紧贴无空格即报（带白名单：`第1步`、emoji 前缀等合法紧贴）
5. **published 缺 `verifiedWith`**：章导读与 `contributing/` 元文档豁免，其余要补

脚本的边界写在 `scripts/check_page.py` 顶上的 docstring 里——**只报"脚本能判断的"**，内容正确性、逻辑错误仍需人读。

## 目录结构

```
check-page/
├── SKILL.md                # Skill 定义（frontmatter + 触发词 + Instructions）
└── scripts/
    └── check_page.py       # 体检脚本（标准库，无依赖）
```

## 装上 Skill

把整个 `examples/check-page/` 目录软链或拷贝到 Claude Code 能发现的位置：

```bash
# 个人级（所有项目生效）
ln -s "$(pwd)/examples/check-page" ~/.claude/skills/check-page

# 项目级（只当前项目生效，写进仓库）
# 在 .claude/settings.json 里加：
#   "skills": ["./examples/check-page"]
```

重启 Claude Code 生效。

## 怎么用

在 Claude Code 对话里说：

```text
帮我检查一下 getting-started/installation.md
```

或

```text
过一遍 style-guide，看 claude-code/basics/ 这几篇过没过
```

Skill 会调 `scripts/check_page.py` 对指定文件跑一遍，把命中问题列成清单，**不会自动改**——按问题人工决定改不改（脚本有误报空间，见下）。

## 验证一次

在仓库根手动跑：

```bash
python3 examples/check-page/scripts/check_page.py getting-started/what-is-claude-code.md
# 预期：未发现问题（或少量合法紧贴的提示）

python3 examples/check-page/scripts/check_page.py claude-code/advanced/memory.md
# 预期：可能命中 0~2 条术语 / 间距问题
```

## 关键设计点

1. **Skill body 跑 `!`指令**——SKILL.md 头部那行 `!\`python3 ${CLAUDE_SKILL_DIR}/scripts/check_page.py $ARGUMENTS\`` 是 Skill SDK 的"Bash 注入"语法：渲染 Skill 时把命令输出嵌入到对话里。`${CLAUDE_SKILL_DIR}` 是 SDK 注入的环境变量，自动指向 Skill 根目录，避免写死绝对路径。
2. **`argument-hint` 引导参数**——` <file.md> [file2.md ...]` 在 `/skill` 命令激活时显示在输入框里，避免用户不知道传什么。
3. **`allowed-tools` 白名单**——只放行调 `check_page.py` 的 Bash，其他工具（Edit / Write / Read）都不给，**就算恶意 prompt 注入也改不了文件**——这是 Skill 的安全护栏。
4. **Instructions 不自动改文件**——Instructions 里明确说"逐条处理"和"先分类再动手"，但绝不主动 Edit 文档；这是 wiki 项目反复打磨出的安全姿态。

## 已知限制

- **纯规则匹配**：术语易错只能看字面（"ClaudeCode"），不能看语境（"我说的是英文翻译不是错别字"）。
- **不带拼音 / OCR**：汉字数靠 `re` 匹配 `[\u4e00-\u9fff]`，标点和 emoji 都不计入。
- **不解析 VitePress 组件**：`<DifficultyBadge />` 这种自定义组件被当普通文本处理，可能在间距 / 字符数上误报。
- **规则更新靠手改脚本**：本 Skill 是"一次性体检"，不是 watch 模式；想 CI 自动化要在 GitHub Actions 里另接。

## 参考

- [Claude Code Skill 规范](../../claude-code/skills/skill-md-spec)
- [如何写好触发词](../../claude-code/skills/writing-triggers)
- [Claude Handbook 写作规范](../../contributing/style-guide)

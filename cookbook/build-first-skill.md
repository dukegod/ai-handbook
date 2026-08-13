---
title: 写你的第一个 Skill
description: 从 SKILL.md 到本地装好到对话里能用，30 分钟；以仓库内 check-page Skill 为实例
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  skillSpec: 'https://code.claude.com/docs/en/skills'
  accessedAt: 2026-08-06
---

# 写你的第一个 Skill

> **目标**：跟着做完，你会在本仓库里 `examples/check-page/` 之外另写一个自己的 Skill，从写 `SKILL.md` 到对话里触发成功跑一次，全程约 30 分钟。

⏱ 预计阅读时间：7 分钟 · 动手 30 分钟

## 你将做到

- ✅ 写一个能跑的 `SKILL.md`（frontmatter + Bash 注入 + Instructions）
- ✅ 用 `allowed-tools` 限定权限边界
- ✅ 把它装到本机 / 项目级，软链或 `settings.json` 二选一
- ✅ 在 Claude Code 对话里说触发词，验证 Skill 真被加载

## 前置检查清单

- [ ] 装好 Claude Code v2.1.x：`claude --version`
- [ ] 有一个**没在前台跑服务**的小目录当 Skill 根（避免命令污染）
- [ ] 会写一点点 Bash / Python（或你常用的脚本语言）

## 第 1 步：起 Skill 目录与 SKILL.md

```bash
mkdir -p ~/projects/my-skills/weather-poke && cd ~/projects/my-skills/weather-poke
```

新建 `SKILL.md`：

```markdown
---
description: 查某个城市的当前天气（mock 数据，不真请求天气 API），把结果嵌进对话。
argument-hint: <城市>
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/weather.py *)
---

## 天气结果

!`python3 ${CLAUDE_SKILL_DIR}/scripts/weather.py $ARGUMENTS`

## Instructions

1. 上面那段是 weather.py 对指定城市的输出（mock 数据）。
2. 用一两句自然语言总结：现在多少度、是否适合出门。
3. 如果用户问「明天」/「下周」——本 Skill 不支持，告知并建议改用 [Cookbook: 真实天气 API 接入](#)。
```

**注意 3 件事**：

- `description` 是触发器核心——Claude Code 决定要不要用本 Skill **全靠这段**。模糊的 `description` 永远不会被触发
- `argument-hint` 在用户主动 `/skill weather-poke` 时显示在输入框里，避免他不知道传什么
- `allowed-tools` **只放行调 `weather.py` 的 Bash**——Edit / Write / Read 都不给，**就算 prompt 注入也改不了文件**

## 第 2 步：写脚本

```bash
mkdir scripts && cat > scripts/weather.py <<'EOF'
#!/usr/bin/env python3
import sys

MOCK = {
    "北京": "晴 18°C 北风 3 级",
    "上海": "多云 22°C 东南风 2 级",
    "深圳": "雷阵雨 28°C 东南风 4 级",
}

def main():
    city = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "北京"
    print(MOCK.get(city, f"暂无 {city} 的 mock 数据（仅支持：北京/上海/深圳）"))

if __name__ == "__main__":
    main()
EOF
chmod +x scripts/weather.py
```

**先在 Skill 目录外**手动跑一次确认脚本没坏：

```bash
python3 scripts/weather.py 北京
# 预期：晴 18°C 北风 3 级
```

## 第 3 步：装上 Skill

个人级（所有项目生效）：

```bash
ln -s ~/projects/my-skills/weather-poke ~/.claude/skills/weather-poke
```

项目级（只当前项目生效，配合 `examples/check-page` 这种「在仓库里维护的 Skill」用）——在项目 `.claude/settings.json` 加：

```json
{
  "skills": ["./examples/check-page", "~/projects/my-skills/weather-poke"]
}
```

**重启 Claude Code**（`/exit` 再 `claude`）让新 Skill 进注册表。

## 第 4 步：触发 + 验证

新开一个 `claude` 会话：

```text
帮我看下上海今天天气
```

预期对话里出现：

1. Claude 主动说「我用 weather-poke 查一下」或类似措辞
2. 渲染结果里出现 `多云 22°C 东南风 2 级`
3. Claude 接着用自然语言总结

**怎么判断 Skill 真被加载了**：

- `/skills` 命令能列出 `weather-poke`
- 触发时控制台有 `[Skill loaded: weather-poke]` 之类的日志（v2.1+ 才有）

## 第 5 步：迭代

第一次触发大概率 description 没写对——Claude 不加载、或加载了但没用对场景。**不要重写整个 SKILL.md**，先调 description 的一句话：

| 现象 | 改哪 |
| --- | --- |
| 完全不加载 | description 太抽象 / 没出现触发关键词 |
| 加载了但乱用 | 加 `instructions` 限定"只在用户问 X 时用" |
| 加载对了但参数传错 | 检查 `argument-hint` 是不是和 `$ARGUMENTS` 用法对得上 |

## 常见错误

**description 写得太长**

Claude 拿 description 跟当前对话匹配，长度 > 200 字符基本等于"什么都像又什么都不像"。**保持在 1-2 句话、出现 2-3 个用户真的会说的关键词**。

**allowed-tools 漏配 → Bash 跑不了**

忘了写 `allowed-tools: Bash(...)` 会导致 Skill body 里的 `!` 指令被安全策略拒。**每个要用到的工具都在 frontmatter 列出来**——`Bash`、`Read`、`Edit` 各自一行。

**Instructions 让 Claude 自动改文件**

Instructions 里写了"修一下 xxx"——Skill 加载后 Claude 会**用 Edit 工具直接改**。本项目所有 Skill 的姿态是**只体检不自动改**——这是边界，不是 bug。明确写"只报告、不修改"。

**`${CLAUDE_SKILL_DIR}` 写错位置**

这个变量**只有 Skill body 里的 `!` 指令展开时**有值，SKILL.md 之外（比如 Instructions 的自然语言段）展开成空串。把脚本路径写死在 Instructions 里就等着换机器崩吧。

## 参考

- [Claude Code Skill 规范](/claude-code/skills/skill-md-spec)
- [如何写好触发词](/claude-code/skills/writing-triggers)
- [Skill 与 Commands / Agents 的取舍](/claude-code/skills/skills-vs-commands-vs-agents)
- 实战示例：[`examples/check-page`](/examples/check-page/README)（仓库内相对路径）

## 下一步

- 学写第一个 MCP Server → [写你的第一个 MCP Server](./build-first-mcp-server)
- 想写可复用的工作流 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

## 如果你想

- 看 Skill 写好后的发布渠道 → [Plugins 与 Marketplace](/claude-code/skills/plugins-marketplace)
- 对比 Skills / Commands / Subagents 选型 → [三者对比](/claude-code/skills/skills-vs-commands-vs-agents)

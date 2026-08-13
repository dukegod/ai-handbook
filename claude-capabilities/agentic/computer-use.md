---
title: Computer Use
description: Claude 操作电脑的能力——截图 / 鼠标 / 键盘 / 5 个实战场景 + 4 个坑
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  computerUse: 'https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool'
  accessedAt: 2026-08-07
---

# Computer Use

> **TL;DR**：Computer Use 让 Claude **直接操作 GUI**（截图 + 鼠标 + 键盘）——能看到屏幕、能点按钮、能填表、能跨应用。**适合 GUI 自动化测试 / 浏览器爬虫 / 跨应用工作流**。⚠️ 风险大：sandbox 必须严密。

⏱ 预计阅读时间：5 分钟

## 一、核心能力

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5-...",
    max_tokens=4096,
    tools=[
        {
            "type": "computer_20250124",   # Computer Use tool
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
        },
    ],
    messages=[{
        "role": "user",
        "content": "在浏览器里打开 google.com，搜索 weather NYC，把结果告诉我",
    }],
)
```

**response 里 Claude 决定调 computer tool**：

```json
{
    "type": "tool_use",
    "name": "computer",
    "input": {
        "action": "left_click",
        "coordinate": [500, 300]
    }
}
```

## 二、3 类动作

| 动作 | 含义 |
| --- | --- |
| **screenshot** | 截屏（看当前屏幕） |
| **left_click / right_click / double_click** | 鼠标点击（坐标） |
| **type** | 输入文字 |
| **key** | 按键（Enter / Tab / 箭头 / 组合键） |
| **scroll** | 滚动 |
| **wait** | 等待 |
| **zoom** | 缩放截图（聚焦某区域） |

## 三、5 个实战场景

### 1. GUI 自动化测试

```text
任务：测试 Gmail 登录
步骤：
1. 打开 chrome
2. 访问 gmail.com
3. 填邮箱 + 密码
4. 验证登录成功
5. 截图存档
```

### 2. 浏览器爬虫（无 API 替代）

```text
任务：从某网站抓取数据
步骤：
1. 打开 URL
2. 截图识别列表
3. 点击 "下一页"
4. 累加数据
5. 导出 CSV
```

### 3. 跨应用工作流

```text
任务：把 Figma 设计稿转 Jira 工单
步骤：
1. 截图 Figma
2. 识别组件
3. 打开 Jira
4. 填标题 + 描述 + 上传截图
5. 提交
```

### 4. 自动化数据录入

```text
任务：把 Excel 100 条记录录到 Web 表单
步骤：循环每行 → 浏览器填字段 → 提交
```

### 5. 旧系统迁移

```text
任务：把 SAP 老系统数据导出到新 SaaS
步骤：截图 SAP → OCR → 填新系统
```

## 四、最小完整循环

```python
import pyautogui    # 或 pynput / 自实现
from PIL import Image
import base64
import io

def execute_computer_action(action: dict):
    if action["action"] == "left_click":
        x, y = action["coordinate"]
        pyautogui.click(x, y)
    elif action["action"] == "type":
        pyautogui.typewrite(action["text"])
    elif action["action"] == "key":
        pyautogui.press(action["text"])
    # ... 其他动作

    # 返回新截图
    img = pyautogui.screenshot()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

# 循环
messages = [{"role": "user", "content": "..."}]
for turn in range(50):
    msg = client.messages.create(model=..., tools=[...], messages=messages)
    if msg.stop_reason == "end_turn":
        break
    messages.append({"role": "assistant", "content": msg.content})
    results = []
    for block in msg.content:
        if block.type == "tool_use" and block.name == "computer":
            new_screenshot = execute_computer_action(block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": [{
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": new_screenshot,
                    },
                }],
            })
    messages.append({"role": "user", "content": results})
```

## 五、4 个常见坑

**1. 没 sandbox**

```python
# ❌ Claude 能控制整个电脑——能删文件、发邮件、转账
# ✅ 限定范围：专用 VM / Docker / 物理隔离机器
```

详见 [Tool Runner 沙箱](/claude-capabilities/sdk/tool-runner)。

**2. 坐标错位（DPI / 缩放）**

```python
# 1920x1080 屏幕在 4K + 缩放 200% 时坐标错位
# ✅ 禁用 DPI 缩放 / 用真实分辨率截图
```

**3. 截图分辨率太大**

```python
# 4K 截图 1 张 ~ 5-10 MB → 1 个 tool call 几千 token
# ✅ 缩到 1024x768 或更低
```

**4. 速度失控**

```python
# Claude 一步 = 1 个 tool call + 1 个截图 = 2-3 秒
# 50 步 = 2-3 分钟
# ✅ max_turns 限 20-30 步
```

## 六、安全警告

> ⚠️ Computer Use 是**最高风险工具**——Claude 能：
> - 看到你屏幕上**所有内容**（含敏感信息）
> - 点击任何按钮（**包括误点**）
> - 输入文字（**含密码**）
> - 触发任何 GUI 操作（**含不可逆操作**）

**强制建议**：
- 用**专用 sandbox**（VM / Docker）
- **不接生产账号**
- **每次跑前备份**
- 监控日志

## 参考

- [Anthropic Docs · Computer Use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool)（访问于 2026-08-07）
- [Tool Runner 沙箱](/claude-capabilities/sdk/tool-runner)
- [Tool Use 协议](/claude-capabilities/core/tool-use)
- [安全](/claude-capabilities/agentic/safety)
- [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)

## 下一步

- 多 agent 协作 → [多 Agent 模式](/claude-capabilities/agentic/multi-agent-patterns)
- 安全实践 → [安全](/claude-capabilities/agentic/safety)
- 切到 Claude Code → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

## 如果你想

- MCP 协议 → [MCP 协议规范](/claude-capabilities/mcp-protocol/protocol-spec)
- 切到 Subagent → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- 沙箱安全 → [Tool Runner](/claude-capabilities/sdk/tool-runner)

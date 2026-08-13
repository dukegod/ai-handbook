import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// ============================================================================
// Claude Handbook — VitePress 配置
//
// 目录结构见 /Users/liuhui15/jd-projects/sz-fe/claude-wiki/README.md
// 写作规范见 contributing/style-guide.md
// 路线图见 contributing/roadmap.md
// ============================================================================

// 占位页面用 🚧 标注；已发布内容不加标注。
// 后续每篇上线后，把对应条目的 🚧 去掉即可。
const P = (text: string) => `${text} 🚧`

export default withMermaid(defineConfig({
  lang: 'zh-CN',
  title: 'AI Handbook',
  description: 'AI 知识体系、技术核心、产品动向与 Coding 落地（中文）',

  cleanUrls: true,
  lastUpdated: true,
  metaChunk: true,

  // 仓库根级元文档，不作为 wiki 页面
  srcExclude: ['README.md', 'CLAUDE.md'],

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#c96442' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:locale', content: 'zh_CN' }],
    ['meta', { name: 'og:site_name', content: 'Claude Handbook' }],
  ],

  markdown: {
    lineNumbers: true,
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'AI Handbook',

    nav: [
      { text: '入门', link: '/getting-started/', activeMatch: '/getting-started/' },
      { text: 'Claude', link: '/claude-code/', activeMatch: '/claude-code/' },
      { text: 'AI 技术', link: '/ai-core/', activeMatch: '/ai-core/' },
      { text: 'AI Coding', link: '/ai-coding/', activeMatch: '/ai-coding/' },
      { text: 'LLM 全景', link: '/llm-landscape/', activeMatch: '/llm-landscape/' },
      { text: 'Cookbook', link: '/cookbook/', activeMatch: '/cookbook/' },
      { text: '参考', link: '/reference/', activeMatch: '/reference/' },
      { text: '贡献', link: '/contributing/style-guide', activeMatch: '/contributing/' },
    ],

    sidebar: {
      // ----------------------------------------------------------------------
      // 入门
      // ----------------------------------------------------------------------
      '/getting-started/': [
        {
          text: '入门',
          items: [
            { text: '总览', link: '/getting-started/' },
            { text: '什么是 Claude Code', link: '/getting-started/what-is-claude-code' },
            { text: '安装与认证', link: '/getting-started/installation' },
            { text: '第一次对话', link: '/getting-started/first-conversation' },
            { text: '心智模型', link: '/getting-started/mental-model' },
            { text: '对比 Cursor / Copilot / Codex CLI', link: '/getting-started/comparisons' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // Claude Code
      // ----------------------------------------------------------------------
      '/claude-code/': [
        {
          text: 'Claude Code',
          items: [{ text: '总览', link: '/claude-code/' }],
        },
        {
          text: '基础',
          collapsed: false,
          items: [
            { text: '会话 Session', link: '/claude-code/basics/sessions' },
            { text: '上下文窗口', link: '/claude-code/basics/context-window' },
            { text: 'CLAUDE.md 项目记忆', link: '/claude-code/basics/claude-md' },
            { text: '权限系统', link: '/claude-code/basics/permissions' },
            { text: '成本与 Token 管理', link: '/claude-code/basics/cost-and-tokens' },
            { text: '模型选择', link: '/claude-code/basics/model-selection' },
            { text: 'Plan Mode', link: '/claude-code/basics/plan-mode' },
          ],
        },
        {
          text: '内置工具',
          collapsed: true,
          items: [
            { text: '工具总览', link: '/claude-code/tools/overview' },
            { text: P('Read 读文件'), link: '/claude-code/tools/read' },
            { text: P('Edit / Write 改文件'), link: '/claude-code/tools/edit-and-write' },
            { text: P('Bash 执行命令'), link: '/claude-code/tools/shell' },
            { text: P('Grep / Glob 搜索'), link: '/claude-code/tools/search' },
            { text: P('WebFetch / WebSearch'), link: '/claude-code/tools/web' },
            { text: P('TodoWrite 任务列表'), link: '/claude-code/tools/todo' },
            { text: P('Task 派生子代理'), link: '/claude-code/tools/dispatch-subagent' },
            { text: P('Notebook 编辑'), link: '/claude-code/tools/notebook' },
          ],
        },
        {
          text: '定制化',
          collapsed: true,
          items: [
            { text: 'Slash Commands', link: '/claude-code/customization/slash-commands' },
            { text: 'Hooks', link: '/claude-code/customization/hooks' },
            { text: 'Settings 配置文件', link: '/claude-code/customization/settings' },
            { text: '键位配置', link: '/claude-code/customization/keybindings' },
          ],
        },
        {
          text: 'Skills',
          collapsed: true,
          items: [
            { text: '什么是 Skill', link: '/claude-code/skills/what-is-a-skill' },
            { text: 'SKILL.md 规范', link: '/claude-code/skills/skill-md-spec' },
            { text: '写好触发描述', link: '/claude-code/skills/writing-triggers' },
            { text: 'Skill vs Command vs Agent', link: '/claude-code/skills/skills-vs-commands-vs-agents' },
            { text: '内置 Skills 一览', link: '/claude-code/skills/built-in-skills' },
            { text: '写你的第一个 Skill', link: '/claude-code/skills/custom-skill' },
            { text: 'Plugins 与 Marketplace', link: '/claude-code/skills/plugins-marketplace' },
          ],
        },
        {
          text: 'MCP（使用层）',
          collapsed: true,
          items: [
            { text: '什么是 MCP', link: '/claude-code/mcp/what-is-mcp' },
            { text: '传输：stdio / SSE / HTTP', link: '/claude-code/mcp/transports' },
            { text: '官方常用 Server', link: '/claude-code/mcp/official-servers' },
            { text: '写你自己的 MCP Server', link: '/claude-code/mcp/build-your-own' },
            { text: '鉴权与调试', link: '/claude-code/mcp/auth-and-debug' },
            { text: '.mcp.json 项目配置', link: '/claude-code/mcp/mcp-json-config' },
          ],
        },
        {
          text: '子代理与编排',
          collapsed: true,
          items: [
            { text: '什么是 Subagent', link: '/claude-code/subagents-and-workflows/what-is-a-subagent' },
            { text: 'Agent 类型清单', link: '/claude-code/subagents-and-workflows/agent-types' },
            { text: 'Workflow 编排', link: '/claude-code/subagents-and-workflows/workflow-orchestration' },
            { text: '多 Agent 常见模式', link: '/claude-code/subagents-and-workflows/multi-agent-patterns' },
          ],
        },
        {
          text: '进阶',
          collapsed: true,
          items: [
            { text: 'Worktree 隔离', link: '/claude-code/advanced/worktree' },
            { text: 'Headless / CI 模式', link: '/claude-code/advanced/headless' },
            { text: '后台与定时任务', link: '/claude-code/advanced/automation' },
            { text: 'Git 与 PR 工作流', link: '/claude-code/advanced/git-workflow' },
            { text: '全局记忆', link: '/claude-code/advanced/memory' },
          ],
        },
        {
          text: '生态',
          collapsed: true,
          items: [
            { text: P('VS Code 集成'), link: '/claude-code/ecosystem/vscode' },
            { text: P('JetBrains 集成'), link: '/claude-code/ecosystem/jetbrains' },
            { text: P('Neovim 集成'), link: '/claude-code/ecosystem/neovim' },
            { text: P('企业部署 SSO / Bedrock / Vertex'), link: '/claude-code/ecosystem/enterprise' },
            { text: '接入非 Claude 模型（国内主流方案）', link: '/claude-code/ecosystem/third-party-models' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // Claude 能力
      // ----------------------------------------------------------------------
      '/claude-capabilities/': [
        {
          text: 'Claude 能力',
          items: [{ text: '总览', link: '/claude-capabilities/' }],
        },
        {
          text: '模型家族',
          collapsed: false,
          items: [
            { text: '模型概览', link: '/claude-capabilities/models/overview' },
            { text: 'Opus 5', link: '/claude-capabilities/models/opus' },
            { text: 'Sonnet 5', link: '/claude-capabilities/models/sonnet' },
            { text: 'Haiku 4.5', link: '/claude-capabilities/models/haiku' },
            { text: 'Fable 5', link: '/claude-capabilities/models/fable' },
            { text: '模型选型', link: '/claude-capabilities/models/choosing-model' },
          ],
        },
        {
          text: '核心能力',
          collapsed: true,
          items: [
            { text: '推理', link: '/claude-capabilities/core/reasoning' },
            { text: 'Extended Thinking', link: '/claude-capabilities/core/extended-thinking' },
            { text: '代码', link: '/claude-capabilities/core/coding' },
            { text: '多模态 Vision', link: '/claude-capabilities/core/vision' },
            { text: '长上下文', link: '/claude-capabilities/core/long-context' },
            { text: '工具使用', link: '/claude-capabilities/core/tool-use' },
          ],
        },
        {
          text: '深度提示工程',
          collapsed: true,
          items: [
            { text: '最佳实践', link: '/claude-capabilities/prompting/best-practices' },
            { text: 'System Prompt', link: '/claude-capabilities/prompting/system-prompts' },
            { text: '思维链', link: '/claude-capabilities/prompting/chain-of-thought' },
            { text: 'Few-shot 示例', link: '/claude-capabilities/prompting/few-shot' },
            { text: 'Prefill 与 XML 标签', link: '/claude-capabilities/prompting/prefill-and-xml' },
            { text: '常用模板', link: '/claude-capabilities/prompting/templates' },
          ],
        },
        {
          text: 'API',
          collapsed: true,
          items: [
            { text: 'Messages API', link: '/claude-capabilities/api/messages' },
            { text: 'Tool Use', link: '/claude-capabilities/api/tool-use' },
            { text: '流式响应', link: '/claude-capabilities/api/streaming' },
            { text: '结构化输出', link: '/claude-capabilities/api/structured-outputs' },
            { text: 'Prompt Caching', link: '/claude-capabilities/api/prompt-caching' },
            { text: 'Message Batches', link: '/claude-capabilities/api/message-batches' },
            { text: 'Files API', link: '/claude-capabilities/api/files' },
            { text: 'Token Counting', link: '/claude-capabilities/api/token-counting' },
            { text: 'Admin & Usage', link: '/claude-capabilities/api/admin-usage' },
          ],
        },
        {
          text: 'SDK',
          collapsed: true,
          items: [
            { text: 'SDK 概览', link: '/claude-capabilities/sdk/overview' },
            { text: 'Python SDK', link: '/claude-capabilities/sdk/python-sdk' },
            { text: 'TypeScript SDK', link: '/claude-capabilities/sdk/typescript-sdk' },
            { text: 'Agent SDK', link: '/claude-capabilities/sdk/agent-sdk' },
            { text: 'Tool Runner', link: '/claude-capabilities/sdk/tool-runner' },
            { text: 'Managed Agents', link: '/claude-capabilities/sdk/managed-agents' },
            { text: 'Claude Code SDK', link: '/claude-capabilities/sdk/claude-code-sdk' },
          ],
        },
        {
          text: 'MCP 协议层',
          collapsed: true,
          items: [
            { text: '协议规范', link: '/claude-capabilities/mcp-protocol/protocol-spec' },
            { text: 'Server 作者指南', link: '/claude-capabilities/mcp-protocol/server-authoring' },
            { text: 'Client 实现要点', link: '/claude-capabilities/mcp-protocol/client-implementation' },
          ],
        },
        {
          text: 'Agentic 能力',
          collapsed: true,
          items: [
            { text: 'Computer Use', link: '/claude-capabilities/agentic/computer-use' },
            { text: '多 Agent 模式', link: '/claude-capabilities/agentic/multi-agent-patterns' },
            { text: '安全 Safety', link: '/claude-capabilities/agentic/safety' },
          ],
        },
        {
          text: '产品面 Surfaces',
          collapsed: true,
          items: [
            { text: 'Claude.ai', link: '/claude-capabilities/surfaces/claude-ai' },
            { text: 'Artifacts', link: '/claude-capabilities/surfaces/artifacts' },
            { text: '桌面应用', link: '/claude-capabilities/surfaces/desktop-app' },
            { text: '网页版', link: '/claude-capabilities/surfaces/web-app' },
            { text: '移动端', link: '/claude-capabilities/surfaces/mobile' },
            { text: 'Claude in Slack', link: '/claude-capabilities/surfaces/claude-in-slack' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // LLM landscape
      // ----------------------------------------------------------------------
      '/llm-landscape/': [
        {
          text: 'LLM landscape',
          items: [
            { text: P('总览'), link: '/llm-landscape/' },
            { text: '技术架构总览', link: '/llm-landscape/architecture' },
            { text: 'Anthropic · Claude 全系', link: '/llm-landscape/anthropic' },
            { text: P('OpenAI · GPT 全系'), link: '/llm-landscape/openai' },
            { text: P('Moonshot · Kimi 全系'), link: '/llm-landscape/moonshot' },
            { text: P('Zhipu · 智谱 GLM 全系'), link: '/llm-landscape/zhipu' },
            { text: P('Qwen · 阿里通义千问全系'), link: '/llm-landscape/qwen' },
            { text: P('5 厂商横向对比'), link: '/llm-landscape/comparison' },
            { text: P('选型决策树'), link: '/llm-landscape/selection-guide' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // AI 核心技术
      // ----------------------------------------------------------------------
      '/ai-core/': [
        {
          text: 'AI 核心技术',
          items: [{ text: '总览', link: '/ai-core/' }],
        },
        {
          text: '基础原理',
          collapsed: false,
          items: [
            { text: P('Transformer 架构'), link: '/ai-core/fundamentals/transformer' },
            { text: P('注意力机制'), link: '/ai-core/fundamentals/attention' },
            { text: P('预训练与微调'), link: '/ai-core/fundamentals/pretraining' },
            { text: P('RLHF 与对齐'), link: '/ai-core/fundamentals/alignment' },
          ],
        },
        {
          text: '模型架构',
          collapsed: true,
          items: [
            { text: P('Dense vs MoE'), link: '/ai-core/model-arch/dense-vs-moe' },
            { text: P('长上下文技术'), link: '/ai-core/model-arch/long-context' },
            { text: P('多模态架构'), link: '/ai-core/model-arch/multimodal' },
          ],
        },
        {
          text: '训练与优化',
          collapsed: true,
          items: [
            { text: P('数据工程'), link: '/ai-core/training/data-engineering' },
            { text: P('推理优化'), link: '/ai-core/training/inference-optimization' },
            { text: P('量化与蒸馏'), link: '/ai-core/training/quantization' },
          ],
        },
        {
          text: '评估方法',
          collapsed: true,
          items: [
            { text: P('基准测试'), link: '/ai-core/eval/benchmarks' },
            { text: P('评估方法论'), link: '/ai-core/eval/methodology' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // AI 产品动向
      // ----------------------------------------------------------------------
      '/ai-trends/': [
        {
          text: 'AI 产品动向',
          items: [{ text: '总览', link: '/ai-trends/' }],
        },
        {
          text: '产品动态',
          collapsed: false,
          items: [
            { text: P('月度产品速报'), link: '/ai-trends/product-updates/monthly' },
            { text: P('Claude 动态'), link: '/ai-trends/product-updates/claude' },
            { text: P('ChatGPT 动态'), link: '/ai-trends/product-updates/chatgpt' },
            { text: P('国内厂商动态'), link: '/ai-trends/product-updates/china' },
          ],
        },
        {
          text: '技术速递',
          collapsed: true,
          items: [
            { text: P('重要论文速递'), link: '/ai-trends/research-highlights/papers' },
            { text: P('开源项目推荐'), link: '/ai-trends/research-highlights/open-source' },
          ],
        },
        {
          text: '行业观察',
          collapsed: true,
          items: [
            { text: P('行业趋势'), link: '/ai-trends/industry/trends' },
            { text: P('投融资动态'), link: '/ai-trends/industry/funding' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // AI Coding 落地
      // ----------------------------------------------------------------------
      '/ai-coding/': [
        {
          text: 'AI Coding 落地',
          items: [{ text: '总览', link: '/ai-coding/' }],
        },
        {
          text: '工具横评',
          collapsed: false,
          items: [
            { text: P('AI Coding 工具全景'), link: '/ai-coding/tools/overview' },
            { text: P('Claude Code 深度评测'), link: '/ai-coding/tools/claude-code' },
            { text: P('Cursor 深度评测'), link: '/ai-coding/tools/cursor' },
            { text: P('GitHub Copilot 评测'), link: '/ai-coding/tools/copilot' },
            { text: P('Codex CLI / Trae 评测'), link: '/ai-coding/tools/others' },
          ],
        },
        {
          text: '团队工作流',
          collapsed: true,
          items: [
            { text: P('团队 AI 工作流'), link: '/ai-coding/workflows/team' },
            { text: P('CI/CD 集成'), link: '/ai-coding/workflows/ci-cd' },
            { text: P('Code Review 自动化'), link: '/ai-coding/workflows/code-review' },
          ],
        },
        {
          text: '常见模式',
          collapsed: true,
          items: [
            { text: P('代码重构模式'), link: '/ai-coding/patterns/refactor' },
            { text: P('测试生成模式'), link: '/ai-coding/patterns/testing' },
            { text: P('文档生成模式'), link: '/ai-coding/patterns/documentation' },
          ],
        },
        {
          text: '企业落地',
          collapsed: true,
          items: [
            { text: P('企业部署指南'), link: '/ai-coding/enterprise/deployment' },
            { text: P('安全与合规'), link: '/ai-coding/enterprise/security' },
            { text: P('成本控制'), link: '/ai-coding/enterprise/cost' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // Cookbook
      // ----------------------------------------------------------------------
      '/cookbook/': [
        {
          text: 'Cookbook',
          items: [
            { text: '总览', link: '/cookbook/' },
            { text: '第一个真实任务', link: '/cookbook/first-real-task' },
            { text: '写你的第一个 Skill', link: '/cookbook/build-first-skill' },
            { text: '写你的第一个 MCP Server', link: '/cookbook/build-first-mcp-server' },
            { text: P('用 Claude Code 重构老项目'), link: '/cookbook/refactor-legacy-project' },
            { text: P('数据分析工作流'), link: '/cookbook/data-analysis-workflow' },
            { text: P('多 Agent 研究流水线'), link: '/cookbook/multi-agent-research' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // 参考
      // ----------------------------------------------------------------------
      '/reference/': [
        {
          text: '速查手册',
          items: [
            { text: '总览', link: '/reference/' },
            { text: 'CLI Flags', link: '/reference/cli-flags' },
            { text: P('环境变量'), link: '/reference/env-vars' },
            { text: P('模型 ID 与定价'), link: '/reference/model-ids' },
            { text: '术语表（速查）', link: '/reference/glossary' },
          ],
        },
      ],

      // ----------------------------------------------------------------------
      // 贡献
      // ----------------------------------------------------------------------
      '/contributing/': [
        {
          text: '贡献指南',
          items: [
            { text: '写作规范', link: '/contributing/style-guide' },
            { text: '术语表（真相源）', link: '/contributing/glossary' },
            { text: '概念文模板', link: '/contributing/template-concept' },
            { text: '操作文模板', link: '/contributing/template-howto' },
            { text: 'Published 门槛自检', link: '/contributing/checklist-published' },
            { text: '架构 review', link: '/contributing/architecture-review-2026-08-10' },
            { text: '路线图', link: '/contributing/roadmap' },
          ],
        },
      ],
    },

    outline: {
      level: [2, 3],
      label: '本页目录',
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇',
    },

    lastUpdated: {
      text: '最后更新',
      formatOptions: { dateStyle: 'long', timeStyle: 'short' },
    },

    editLink: {
      // 内网 coding.jd.com 路径；后续镜像到 GitHub 时可改
      pattern: 'https://coding.jd.com/sz-fe/claude-wiki/edit/main/:path',
      text: '在 Coding 上编辑此页',
    },

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档',
              },
              modal: {
                noResultsText: '没有相关结果',
                resetButtonTitle: '清除搜索',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭',
                },
              },
            },
          },
        },
      },
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/anthropics/claude-code' },
    ],

    footer: {
      message: '内容采用 CC BY-SA 4.0 授权 · 代码采用 MIT 授权',
      copyright: '与 Anthropic 无官方关联 · 社区中文学习资料',
    },

    langMenuLabel: '切换语言',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
  },
}))

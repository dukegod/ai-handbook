// Claude Handbook 主题入口
//
// 挂载点：doc-top slot（在 .vp-doc 容器内、markdown 内容之前）依次渲染：
// - DifficultyBadge —— 读 frontmatter.difficulty 显示难度胶囊（🟢/🟡/🔴），无值时不渲染
// - VersionBanner  —— 读 frontmatter.lastUpdated，超 90/180 天显示黄/红警示
//
// 用 doc-top 而非 doc-before：badge 与正文同宽同 padding，视觉贴近正文头部；
// doc-before 会把 badge 甩到 <main> 之外、页面最顶端，不美观。
//
// 首页（layout: home，无常规 frontmatter）两个组件都跳过。
// 章导读通常带 difficulty 但不带 lastUpdated，所以只显示难度徽章、不显示时效横幅。
//
// 参见 contributing/style-guide.md 第一、第四节。

import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import DifficultyBadge from './components/DifficultyBadge.vue'
import VersionBanner from './components/VersionBanner.vue'

const theme: Theme = {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'doc-top': () => [h(DifficultyBadge), h(VersionBanner)],
    })
  },
}

export default theme

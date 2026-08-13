<script setup lang="ts">
// VersionBanner —— 根据 frontmatter.lastUpdated 显示时效警示
//
// - 90 天以内：不渲染（返回 null）
// - 90-180 天：黄色 "可能过时" 提示
// - 超 180 天：红色 "已过时" 提示
//
// 依赖 frontmatter 里的 `lastUpdated: YYYY-MM-DD`。首页 / 章导读（无 lastUpdated）自动跳过。
// 引自 contributing/style-guide.md 第四节「时效横幅」。

import { computed } from 'vue'
import { useData } from 'vitepress'

const { frontmatter } = useData()

interface BannerStatus {
  level: 'warn' | 'error'
  days: number
  dateStr: string
}

const status = computed<BannerStatus | null>(() => {
  const raw = frontmatter.value?.lastUpdated
  if (!raw) return null

  const then = new Date(raw as string)
  if (Number.isNaN(then.getTime())) return null

  const now = new Date()
  const days = Math.floor((now.getTime() - then.getTime()) / (1000 * 60 * 60 * 24))

  if (days >= 180) return { level: 'error', days, dateStr: raw as string }
  if (days >= 90) return { level: 'warn', days, dateStr: raw as string }
  return null
})
</script>

<template>
  <div
    v-if="status"
    class="vb-banner"
    :class="`vb-${status.level}`"
    role="note"
  >
    <div class="vb-icon" aria-hidden="true">
      {{ status.level === 'error' ? '🚨' : '⚠️' }}
    </div>
    <div class="vb-body">
      <template v-if="status.level === 'error'">
        <strong>本页已过时</strong>（更新于 {{ status.dateStr }}，距今 {{ status.days }} 天）。<br />
        请以 <a href="https://code.claude.com/docs/en/" target="_blank" rel="noopener">官方文档</a> 为准，本页仅作历史参考。
      </template>
      <template v-else>
        <strong>本页可能过时</strong>（更新于 {{ status.dateStr }}，距今 {{ status.days }} 天）。<br />
        Claude Code 约两周一版，如与实际有出入请查 <a href="/contributing/roadmap">路线图</a> 或 <a href="https://code.claude.com/docs/en/" target="_blank" rel="noopener">官方文档</a>。
      </template>
    </div>
  </div>
</template>

<style scoped>
.vb-banner {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 14px 16px;
  margin: 16px 0 24px;
  border-radius: 8px;
  border-left: 4px solid;
  font-size: 14px;
  line-height: 1.6;
}

.vb-icon {
  font-size: 20px;
  line-height: 1;
  flex-shrink: 0;
}

.vb-body {
  flex: 1;
}

.vb-body a {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* 90 天 · warn（琥珀）*/
.vb-warn {
  background: #fff8e6;
  border-left-color: #f5a623;
  color: #7a4b00;
}
.dark .vb-warn {
  background: rgba(245, 166, 35, 0.12);
  color: #f5c47a;
}

/* 180 天 · error（红）*/
.vb-error {
  background: #ffeeed;
  border-left-color: #d0342c;
  color: #8f1e18;
}
.dark .vb-error {
  background: rgba(208, 52, 44, 0.15);
  color: #ff8f88;
}
</style>

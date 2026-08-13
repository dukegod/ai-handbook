<script setup lang="ts">
// DifficultyBadge —— 根据 frontmatter.difficulty 显示难度胶囊
//
// - 🟢 → 入门（绿）
// - 🟡 → 进阶（琥珀）
// - 🔴 → 高阶（红）
// - 无 difficulty 字段（首页 / 章导读）→ 不渲染
//
// 引自 contributing/style-guide.md 第一节「Frontmatter 强制字段」。

import { computed } from 'vue'
import { useData } from 'vitepress'

interface Badge {
  emoji: string
  text: string
  level: 'beginner' | 'intermediate' | 'advanced'
}

const { frontmatter } = useData()

const badge = computed<Badge | null>(() => {
  const raw = frontmatter.value?.difficulty
  if (!raw || typeof raw !== 'string') return null

  // 顺序判定：多个 emoji 共存时以第一个命中的为准
  if (raw.includes('🟢')) return { emoji: '🟢', text: '入门', level: 'beginner' }
  if (raw.includes('🟡')) return { emoji: '🟡', text: '进阶', level: 'intermediate' }
  if (raw.includes('🔴')) return { emoji: '🔴', text: '高阶', level: 'advanced' }
  return null
})
</script>

<template>
  <div v-if="badge" class="db-badge" :class="`db-${badge.level}`">
    <span class="db-emoji">{{ badge.emoji }}</span>
    <span class="db-text">{{ badge.text }}</span>
  </div>
</template>

<style scoped>
.db-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  margin: 4px 0 20px;
  line-height: 1;
}

.db-emoji {
  font-size: 14px;
  line-height: 1;
}

/* 🟢 入门（绿） */
.db-beginner {
  background: #e6f7ea;
  color: #1e6b3a;
}
.dark .db-beginner {
  background: rgba(46, 160, 67, 0.16);
  color: #7ee787;
}

/* 🟡 进阶（琥珀） */
.db-intermediate {
  background: #fff5db;
  color: #8f5a00;
}
.dark .db-intermediate {
  background: rgba(245, 166, 35, 0.16);
  color: #f5c47a;
}

/* 🔴 高阶（红） */
.db-advanced {
  background: #ffece9;
  color: #a03028;
}
.dark .db-advanced {
  background: rgba(248, 81, 73, 0.16);
  color: #ff8f88;
}
</style>

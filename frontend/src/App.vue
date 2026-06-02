<template>
  <div class="app-container" :class="{ dark: true }">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>⚙️ AMS 配置管理</h1>
        <div class="subtitle">船舶数据采集配置系统</div>
      </div>
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: currentRoute === item.path }"
        >
          <span class="icon" v-html="item.icon"></span>
          <span>{{ item.name }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div style="font-size: 12px; color: #a0a0b8;">AMS Config Manager v1.0</div>
      </div>
    </aside>

    <!-- Main -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Status Bar -->
    <div class="status-bar" :class="dbStatus">
      <span v-if="dbStatus === 'connected'">🟢 数据库已连接</span>
      <span v-else>🔴 数据库未连接</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentRoute = computed(() => route.path)
const dbStatus = ref('disconnected')

const navItems = [
  { path: '/database', name: '数据库操作', icon: '🗄️' },
  { path: '/engine-room', name: '机舱设备', icon: '⚙️' },
  { path: '/cfg2db', name: '配置入库', icon: '📥' },
  { path: '/templates', name: '导入模板', icon: '📋' },
  { path: '/help', name: '参考说明', icon: '📖' },
]
</script>

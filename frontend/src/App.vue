<template>
  <div class="app-container" :class="{ dark: true }">
    <template v-if="!isLoginPage">
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
          <div style="margin-bottom: 8px;">👤 {{ username || '未登录' }}</div>
          <el-button size="small" text @click="handleLogout" style="color: var(--text-secondary); padding:0;">
            退出登录
          </el-button>
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
    </template>

    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const currentRoute = computed(() => route.path)
const username = computed(() => auth.username)
const dbStatus = ref('disconnected')

const navItems = [
  { path: '/database', name: '数据库操作', icon: '🗄️' },
  { path: '/engine-room', name: '机舱设备', icon: '⚙️' },
  { path: '/cfg2db', name: '配置入库', icon: '📥' },
  { path: '/templates', name: '导入模板', icon: '📋' },
  { path: '/help', name: '参考说明', icon: '📖' },
]

const isLoginPage = computed(() => route.path === '/login')

function handleLogout() {
  auth.logout()
  router.push('/login')
}

onMounted(() => {
  if (!auth.isLoggedIn && route.path !== '/login') {
    router.push('/login')
  }
})
</script>

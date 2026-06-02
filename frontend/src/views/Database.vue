<template>
  <div>
    <div class="page-header">
      <h2>🗄️ 数据库操作</h2>
      <p class="desc">配置 MySQL 数据库连接，验证连接状态</p>
    </div>

    <el-card>
      <el-form :model="form" label-width="120px" size="large">
        <el-form-item label="数据库IP地址">
          <el-input v-model="form.host" placeholder="192.168.8.48" />
        </el-form-item>
        <el-form-item label="端口号">
          <el-input v-model.number="form.port" placeholder="3306" />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="root" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="数据库密码" show-password />
        </el-form-item>
        <el-form-item label="数据库名">
          <el-input v-model="form.database" placeholder="hlx" />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="testing"
            @click="handleTest"
            size="large"
          >
            {{ testing ? '连接中...' : '连接数据库' }}
          </el-button>
          <el-button v-if="connected" type="success" disabled size="large">
            ✅ 已连接
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Result -->
    <el-card v-if="result" style="margin-top: 16px;">
      <div :style="{ color: result.success ? '#52c41a' : '#ff4d4f' }">
        <strong>{{ result.success ? '✅ 连接成功' : '❌ 连接失败' }}</strong>
        <p style="margin: 8px 0 0;">{{ result.message }}</p>
        <p v-if="result.server_version" style="margin: 4px 0 0; color: #a0a0b8; font-size: 13px;">
          服务器版本: {{ result.server_version }}
        </p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { dbApi } from '../api'

const testing = ref(false)
const connected = ref(false)
const result = ref<any>(null)

const form = ref({
  host: '192.168.8.48',
  port: 3306,
  username: 'root',
  password: '',
  database: 'hlx',
})

async function handleTest() {
  testing.value = true
  result.value = null
  try {
    const res = await dbApi.testConnection(form.value)
    result.value = res.data
    connected.value = res.data.success
  } catch (e: any) {
    result.value = {
      success: false,
      message: e.response?.data?.detail || '连接请求失败',
    }
    connected.value = false
  } finally {
    testing.value = false
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>📥 配置数据入库</h2>
      <p class="desc">将生成的配置数据写入目标数据库</p>
    </div>

    <el-row :gutter="16">
      <!-- Target Database Config -->
      <el-col :span="8">
        <el-card>
          <template #header><span>🎯 目标数据库</span></template>
          <el-form :model="dbConfig" label-width="100px" size="small">
            <el-form-item label="IP地址"><el-input v-model="dbConfig.host" /></el-form-item>
            <el-form-item label="端口"><el-input v-model.number="dbConfig.port" /></el-form-item>
            <el-form-item label="用户名"><el-input v-model="dbConfig.username" /></el-form-item>
            <el-form-item label="密码"><el-input v-model="dbConfig.password" type="password" show-password /></el-form-item>
            <el-form-item label="数据库名"><el-input v-model="dbConfig.database" /></el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Available Configs -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between;">
              <span>📋 待入库配置</span>
              <el-button type="primary" size="small" @click="loadConfigs">刷新列表</el-button>
            </div>
          </template>

          <el-table :data="configs" stripe size="small">
            <el-table-column prop="name" label="客户端名称" min-width="160" />
            <el-table-column prop="transport_mode" label="模式" width="70" />
            <el-table-column prop="baud_rate" label="波特率" width="90" />
            <el-table-column prop="slave_id" label="从站ID" width="80" />
            <el-table-column prop="points_count" label="工况点数" width="90" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="doCfg2DB(row.id)">
                  📥 配置入库
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- Result -->
        <el-card v-if="result" style="margin-top: 16px;">
          <el-alert
            :title="result.message"
            :type="result.success ? 'success' : 'error'"
            show-icon
            :closable="false"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { modbusApi, importApi } from '../api'

const dbConfig = ref({
  host: '192.168.8.48',
  port: 3306,
  username: 'root',
  password: '',
  database: 'hlx',
})
const configs = ref<any[]>([])
const result = ref<any>(null)

async function loadConfigs() {
  // For simplicity, load all configs from gateway id 1
  try {
    const res = await modbusApi.listConfigs(1)
    configs.value = res.data
  } catch {
    configs.value = []
  }
}

async function doCfg2DB(configId: number) {
  result.value = null
  try {
    const formData = new FormData()
    formData.append('target_host', dbConfig.value.host)
    formData.append('target_port', String(dbConfig.value.port))
    formData.append('target_user', dbConfig.value.username)
    formData.append('target_password', dbConfig.value.password)
    formData.append('target_db', dbConfig.value.database)

    const res = await importApi.cfg2db(configId, formData)
    result.value = res.data
    if (res.data.success) ElMessage.success('入库成功')
  } catch (e: any) {
    result.value = {
      success: false,
      message: e.response?.data?.detail || '入库请求失败',
    }
  }
}

onMounted(loadConfigs)
</script>

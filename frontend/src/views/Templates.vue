<template>
  <div>
    <div class="page-header">
      <h2>📋 导入模板管理</h2>
      <p class="desc">管理 AMS 厂商 Excel 的导入映射模板，同系列船可复用</p>
    </div>

    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between;">
          <span>模板列表</span>
          <el-button type="primary" size="small" @click="showDialog = true">+ 新建模板</el-button>
        </div>
      </template>

      <el-table :data="templates" stripe size="small" v-loading="loading">
        <el-table-column prop="name" label="模板名称" min-width="160" />
        <el-table-column prop="manufacturer" label="AMS厂商" width="140" />
        <el-table-column prop="ship_series" label="船型系列" width="140" />
        <el-table-column label="列映射" min-width="200">
          <template #default="{ row }">
            <div style="display: flex; flex-wrap: wrap; gap: 2px;">
              <el-tag v-for="(col, field) in row.column_mapping" :key="field" size="small" v-if="col">
                {{ field }}:{{ col }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="120" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button size="small" text @click="editTemplate(row)">编辑</el-button>
            <el-button size="small" text type="danger" @click="deleteTemplate(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Edit Dialog -->
    <el-dialog v-model="showDialog" :title="editing ? '编辑模板' : '新建模板'" width="600px">
      <el-form :model="form" label-width="120px" size="small">
        <el-form-item label="模板名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="AMS厂商"><el-input v-model="form.manufacturer" /></el-form-item>
        <el-form-item label="船型系列"><el-input v-model="form.ship_series" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" rows="2" /></el-form-item>
        <el-divider>列映射配置（Excel列的字母）</el-divider>
        <el-form-item label="名称列"><el-input v-model="form.column_mapping.name" style="width:100px;" /></el-form-item>
        <el-form-item label="Modbus地址列"><el-input v-model="form.column_mapping.modbus_address" style="width:100px;" /></el-form-item>
        <el-form-item label="信号类型列"><el-input v-model="form.column_mapping.signal_type" style="width:100px;" /></el-form-item>
        <el-form-item label="序号列"><el-input v-model="form.column_mapping.point_index" style="width:100px;" /></el-form-item>
        <el-form-item label="单位列"><el-input v-model="form.column_mapping.unit" style="width:100px;" /></el-form-item>
        <el-form-item label="数据类型列"><el-input v-model="form.column_mapping.data_type" style="width:100px;" /></el-form-item>
        <el-form-item label="AMS编号列"><el-input v-model="form.column_mapping.ams_module_id" style="width:100px;" /></el-form-item>
        <el-form-item label="表头行"><el-input v-model.number="form.header_row" style="width:100px;" /></el-form-item>
        <el-form-item label="数据起始行"><el-input v-model.number="form.data_start_row" style="width:100px;" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveTemplate">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { importApi } from '../api'

const loading = ref(false)
const templates = ref<any[]>([])
const showDialog = ref(false)
const editing = ref<any>(null)

const form = reactive({
  name: '', manufacturer: '', ship_series: '', description: '',
  column_mapping: {
    name: 'B', modbus_address: 'C', signal_type: 'D',
    point_index: 'A', unit: '', data_type: '', ams_module_id: '',
  },
  header_row: 7, data_start_row: 8, comm_params_row: 1,
})

onMounted(loadTemplates)

async function loadTemplates() {
  loading.value = true
  try {
    const res = await importApi.listTemplates()
    templates.value = res.data
  } catch { /* ignore */ }
  finally { loading.value = false }
}

function editTemplate(row: any) {
  editing.value = row
  form.name = row.name
  form.manufacturer = row.manufacturer || ''
  form.ship_series = row.ship_series || ''
  form.description = row.description || ''
  form.column_mapping = { ...row.column_mapping }
  form.header_row = row.header_row || 7
  form.data_start_row = row.data_start_row || 8
  form.comm_params_row = row.comm_params_row || 1
  showDialog.value = true
}

async function deleteTemplate(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除模板"${row.name}"?`)
    await importApi.deleteTemplate(row.id)
    ElMessage.success('已删除')
    await loadTemplates()
  } catch { /* cancelled */ }
}

async function saveTemplate() {
  try {
    if (editing.value) {
      await importApi.updateTemplate(editing.value.id, form)
      ElMessage.success('已更新')
    } else {
      await importApi.createTemplate(form)
      ElMessage.success('已创建')
    }
    showDialog.value = false
    editing.value = null
    await loadTemplates()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
}

// Reset form on dialog close
import { watch } from 'vue'
watch(showDialog, (v) => {
  if (!v) {
    editing.value = null
    Object.assign(form, {
      name: '', manufacturer: '', ship_series: '', description: '',
      column_mapping: { name: 'B', modbus_address: 'C', signal_type: 'D', point_index: 'A', unit: '', data_type: '', ams_module_id: '' },
      header_row: 7, data_start_row: 8, comm_params_row: 1,
    })
  }
})
</script>

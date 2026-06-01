<template>
  <el-dialog :model-value="visible" title="📥 AMS Excel 导入" width="800px" @update:model-value="$emit('update:visible', $event)" @close="handleClose">
    <!-- Step 1: Upload & Preview -->
    <template v-if="step === 'upload'">
      <el-upload
        drag
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleUpload"
        accept=".xlsx,.xls"
      >
        <div style="font-size: 48px; text-align: center; color: #4a9eff;">📤</div>
        <div style="margin: 8px 0;">拖拽或点击上传 AMS 厂商的 Excel 文件</div>
        <template #tip>
          <div style="color: #a0a0b8; font-size: 12px;">支持 .xlsx 格式，文件大小不超过 10MB</div>
        </template>
      </el-upload>

      <!-- Template Selector -->
      <div v-if="templates.length > 0" style="margin-top: 16px;">
        <label style="color: #a0a0b8; font-size: 13px; display: block; margin-bottom: 8px;">或选择已有导入模板</label>
        <el-select v-model="selectedTemplateId" placeholder="选择模板" style="width: 100%;" @change="onTemplateSelect">
          <el-option v-for="t in templates" :key="t.id" :label="`${t.name} (${t.manufacturer})`" :value="t.id" />
        </el-select>
      </div>
    </template>

    <!-- Step 2: Column Mapping -->
    <template v-if="step === 'mapping'">
      <el-alert title="请将 Excel 的列映射到系统字段" type="info" show-icon :closable="false" style="margin-bottom: 16px;" />

      <div style="margin-bottom: 12px;">
        <label style="color: #a0a0b8; font-size: 13px;">Excel 表头：</label>
        <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px;">
          <el-tag v-for="(h, i) in preview.headers" :key="i" size="small">
            {{ getColLetter(i + 1) }}: {{ h || `(列${i + 1})` }}
          </el-tag>
        </div>
      </div>

      <el-form :model="mapping" label-width="120px" size="small">
        <el-form-item label="名称列">
          <el-select v-model="mapping.name" filterable placeholder="选择列">
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
          </el-select>
        </el-form-item>
        <el-form-item label="Modbus地址列">
          <el-select v-model="mapping.modbus_address" filterable placeholder="选择列">
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
          </el-select>
        </el-form-item>
        <el-form-item label="信号类型列">
          <el-select v-model="mapping.signal_type" filterable placeholder="选择列" clearable>
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
            <el-option label="（不指定）" value="" />
          </el-select>
        </el-form-item>
        <el-form-item label="序号列">
          <el-select v-model="mapping.point_index" filterable placeholder="选择列" clearable>
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
            <el-option label="（自动编号）" value="" />
          </el-select>
        </el-form-item>
        <el-form-item label="单位列">
          <el-select v-model="mapping.unit" filterable placeholder="选择列" clearable>
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
            <el-option label="（无）" value="" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据类型列">
          <el-select v-model="mapping.data_type" filterable placeholder="选择列" clearable>
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
            <el-option label="（无）" value="" />
          </el-select>
        </el-form-item>
        <el-form-item label="AMS编号列">
          <el-select v-model="mapping.ams_module_id" filterable placeholder="选择列" clearable>
            <el-option v-for="(h, i) in preview.headers" :key="i" :label="`${getColLetter(i + 1)} - ${h || '列' + (i+1)}`" :value="getColLetter(i + 1)" />
            <el-option label="（无）" value="" />
          </el-select>
        </el-form-item>
      </el-form>

      <div style="margin-top: 12px;">
        <label style="color: #a0a0b8; font-size: 13px;">数据预览：</label>
        <el-table :data="preview.rows.slice(0, 5)" size="small" border style="margin-top: 4px;" max-height="200">
          <el-table-column v-for="(h, i) in preview.headers" :key="i" :label="h || `列${i+1}`" min-width="100" show-overflow-tooltip>
            <template #default="{ row }">{{ row[i] }}</template>
          </el-table-column>
        </el-table>
      </div>

      <div style="margin-top: 12px;">
        <el-checkbox v-model="saveAsTemplate">保存为导入模板</el-checkbox>
        <el-input v-if="saveAsTemplate" v-model="templateName" placeholder="模板名称（如：远东德华 AMS）" style="margin-top: 8px;" />
      </div>
    </template>

    <!-- Step 3: Version Diff Result -->
    <template v-if="step === 'diff'">
      <el-alert
        :title="`比对完成: ${diffResult?.old_version} → ${diffResult?.new_version}`"
        type="success"
        show-icon
        :closable="false"
        style="margin-bottom: 16px;"
      />

      <el-tabs>
        <el-tab-pane>
          <template #label>
            <span class="tag-added">🟢 新增 ({{ diffResult?.added?.length || 0 }})</span>
          </template>
          <el-table :data="diffResult?.added || []" size="small" max-height="300">
            <el-table-column prop="name" label="名称" min-width="180" />
            <el-table-column prop="modbus_address" label="地址" width="100" />
            <el-table-column prop="signal_type" label="类型" width="80" />
            <el-table-column prop="ams_module_id" label="AMS编号" width="140" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane>
          <template #label>
            <span class="tag-deleted">🔴 删除 ({{ diffResult?.deleted?.length || 0 }})</span>
          </template>
          <el-table :data="diffResult?.deleted || []" size="small" max-height="300">
            <el-table-column prop="name" label="名称" min-width="180" />
            <el-table-column prop="modbus_address" label="地址" width="100" />
            <el-table-column prop="signal_type" label="类型" width="80" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane>
          <template #label>
            <span class="tag-modified">🟡 修改 ({{ diffResult?.modified?.length || 0 }})</span>
          </template>
          <el-table :data="diffResult?.modified || []" size="small" max-height="300">
            <el-table-column prop="name" label="名称" min-width="160" />
            <el-table-column prop="modbus_address" label="地址" width="80" />
            <el-table-column label="变更详情" min-width="200">
              <template #default="{ row }">
                <div v-for="f in row.diff_fields" :key="f.field" style="font-size: 12px; color: #a0a0b8;">
                  {{ f.field }}: {{ f.old_value }} → <span style="color: #ff4d4f;">{{ f.new_value }}</span>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <div style="margin-top: 16px; display: flex; gap: 12px;">
        <el-button type="primary" @click="batchApprove('accept_all')">✅ 全部接受</el-button>
        <el-button type="danger" @click="batchApprove('reject_all')">❌ 全部拒绝</el-button>
      </div>
    </template>

    <!-- Navigation -->
    <template #footer>
      <el-button v-if="step === 'mapping'" @click="step = 'upload'">上一步</el-button>
      <el-button v-if="step === 'mapping'" type="primary" @click="doImport">导入并比对</el-button>
      <el-button v-if="step === 'diff'" @click="finish">完成</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { importApi } from '../api'

const props = defineProps<{ visible: boolean; configId: number }>()
const emit = defineEmits(['update:visible', 'imported'])

const step = ref('upload')
const templates = ref<any[]>([])
const selectedTemplateId = ref<number | null>(null)
const preview = reactive({ headers: [] as string[], rows: [] as any[][], total_rows: 0, total_cols: 0 })
const filePath = ref('')
const fileName = ref('')
const mapping = reactive<any>({
  name: 'B', modbus_address: 'C', signal_type: 'D',
  point_index: 'A', unit: '', data_type: '', ams_module_id: '',
})
const saveAsTemplate = ref(false)
const templateName = ref('')
const diffResult = ref<any>(null)
const diffVersionId = ref<number | null>(null)
const importedVersionTag = ref('')

function getColLetter(n: number): string {
  let s = ''
  while (n > 0) { n--; s = String.fromCharCode(65 + (n % 26)) + s; n = Math.floor(n / 26) }
  return s || 'A'
}

// Load templates
watch(() => props.visible, async (v) => {
  if (v) {
    try {
      const res = await importApi.listTemplates()
      templates.value = res.data
    } catch { templates.value = [] }
    step.value = 'upload'
    diffResult.value = null
  }
})

async function handleUpload(file: any) {
  const formData = new FormData()
  formData.append('file', file.raw || file)
  formData.append('header_row', '7')
  try {
    const res = await importApi.previewExcel(formData)
    preview.headers = res.data.headers
    preview.rows = res.data.rows
    preview.total_rows = res.data.total_rows
    preview.total_cols = res.data.total_cols
    filePath.value = res.data.file_path
    fileName.value = res.data.file_name
    step.value = 'mapping'
    ElMessage.success('文件解析成功')
  } catch (e: any) {
    ElMessage.error('文件解析失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function onTemplateSelect(templateId: number) {
  try {
    const res = await importApi.getTemplate(templateId)
    const t = res.data
    Object.assign(mapping, t.column_mapping)
    ElMessage.success(`已应用模板: ${t.name}`)
  } catch { /* ignore */ }
}

async function doImport() {
  // 1. Save template if needed
  if (saveAsTemplate.value && templateName.value) {
    try {
      await importApi.createTemplate({
        name: templateName.value,
        manufacturer: '',
        ship_series: '',
        description: '',
        column_mapping: { ...mapping },
        header_row: 7,
        data_start_row: 8,
        comm_params_row: 1,
      })
    } catch { /* template may already exist */ }
  }

  // 2. Parse Excel
  const formData = new FormData()
  formData.append('file_path', filePath.value)
  formData.append('template_id', '1') // placeholder
  formData.append('modbus_config_id', String(props.configId))

  // Actually need to find or create template dynamically
  // For now, parse using mapping directly via a custom endpoint
  try {
    // First create a temporary template
    const tmplRes = await importApi.createTemplate({
      name: `临时_${fileName.value}`,
      manufacturer: '',
      ship_series: '',
      description: '',
      column_mapping: { ...mapping },
      header_row: 7,
      data_start_row: 8,
      comm_params_row: 1,
    })
    const tmplId = tmplRes.data.id

    const parseData = new FormData()
    parseData.append('file_path', filePath.value)
    parseData.append('template_id', String(tmplId))
    parseData.append('modbus_config_id', String(props.configId))

    await importApi.parseExcel(parseData)

    // 3. Create version diff
    const now = new Date()
    const versionTag = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`
    importedVersionTag.value = versionTag

    const diffData = new FormData()
    diffData.append('modbus_config_id', String(props.configId))
    diffData.append('version_tag', versionTag)
    diffData.append('source_file', fileName.value)

    const diffRes = await importApi.createDiff(diffData)
    diffResult.value = diffRes.data

    // Store version id if available
    step.value = 'diff'
    ElMessage.success(`导入完成，发现 ${diffRes.data.added.length + diffRes.data.deleted.length + diffRes.data.modified.length} 项变更`)
  } catch (e: any) {
    ElMessage.error('导入失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function batchApprove(action: string) {
  try {
    await importApi.batchApprove({ action })
    ElMessage.success(`已${action === 'accept_all' ? '接受' : '拒绝'}全部变更`)
  } catch (e: any) {
    ElMessage.error('操作失败')
  }
}

function finish() {
  step.value = 'upload'
  emit('imported')
  emit('update:visible', false)
}

function handleClose() {
  step.value = 'upload'
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>⚙️ 机舱设备</h2>
      <p class="desc">选择船舶 → Modbus客户端 → 配置通讯参数与工况点</p>
    </div>

    <!-- Ship / Gateway / Client Selector -->
    <el-card style="margin-bottom: 16px;">
      <div style="display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 200px;">
          <label style="color: #a0a0b8; font-size: 13px; display: block; margin-bottom: 4px;">船舶</label>
          <el-select v-model="selectedShipId" placeholder="选择船舶" style="width: 100%;" @change="onShipChange">
            <el-option v-for="s in ships" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </div>
        <div style="flex: 1; min-width: 200px;">
          <label style="color: #a0a0b8; font-size: 13px; display: block; margin-bottom: 4px;">网关</label>
          <el-select v-model="selectedGatewayId" placeholder="选择网关" style="width: 100%;" @change="onGatewayChange">
            <el-option v-for="g in gateways" :key="g.id" :label="g.name" :value="g.id" />
          </el-select>
        </div>
        <div style="flex: 1; min-width: 200px;">
          <label style="color: #a0a0b8; font-size: 13px; display: block; margin-bottom: 4px;">Modbus客户端</label>
          <el-select v-model="selectedConfigId" placeholder="选择客户端" style="width: 100%;" @change="onConfigChange">
            <el-option v-for="c in configs" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </div>
        <div style="padding-top: 18px;">
          <el-button type="primary" size="small" @click="showAddConfig = true">+ 新增客户端</el-button>
        </div>
      </div>
    </el-card>

    <!-- Communication Parameters + Signal Points -->
    <template v-if="selectedConfig">
      <el-row :gutter="16">
        <!-- Left: Communication Parameters -->
        <el-col :span="8">
          <el-card>
            <template #header><span>📡 通讯参数</span></template>
            <el-form :model="selectedConfig" label-width="100px" size="small">
              <el-form-item label="通讯类型"><el-input v-model="selectedConfig.comm_type" /></el-form-item>
              <el-form-item label="传输模式"><el-select v-model="selectedConfig.transport_mode" style="width:100%;">
                <el-option label="TCP" value="TCP" /><el-option label="RTU" value="RTU" />
              </el-select></el-form-item>
              <el-form-item label="电气接口"><el-input v-model="selectedConfig.electrical_interface" /></el-form-item>
              <el-form-item label="波特率"><el-input v-model.number="selectedConfig.baud_rate" /></el-form-item>
              <el-form-item label="数据位"><el-input v-model.number="selectedConfig.data_bits" /></el-form-item>
              <el-form-item label="停止位"><el-input v-model.number="selectedConfig.stop_bits" /></el-form-item>
              <el-form-item label="校验位"><el-select v-model="selectedConfig.parity" style="width:100%;">
                <el-option label="无 None" value="None" />
                <el-option label="奇 Odd" value="Odd" />
                <el-option label="偶 Even" value="Even" />
              </el-select></el-form-item>
              <el-form-item label="从站ID"><el-input v-model.number="selectedConfig.slave_id" /></el-form-item>
              <el-form-item label="开关量功能码"><el-input v-model.number="selectedConfig.func_code_read_di" /></el-form-item>
              <el-form-item label="模拟量功能码"><el-input v-model.number="selectedConfig.func_code_read_ai" /></el-form-item>
              <el-form-item label="IP地址"><el-input v-model="selectedConfig.ip_address" /></el-form-item>
              <el-form-item label="端口"><el-input v-model.number="selectedConfig.port" /></el-form-item>
            </el-form>
            <div style="margin-top: 12px;">
              <el-button type="primary" size="small" @click="saveConfig">保存通讯参数</el-button>
            </div>
          </el-card>
        </el-col>

        <!-- Right: Signal Points -->
        <el-col :span="16">
          <el-card>
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>📋 工况点列表 ({{ points.length }}项)</span>
                <div>
                  <el-button type="primary" size="small" @click="showImportDialog = true">
                    📥 Excel导入
                  </el-button>
                  <el-button type="warning" size="small" @click="generateConfig">
                    📄 生成配置
                  </el-button>
                </div>
              </div>
            </template>

            <el-table :data="points" max-height="500" size="small" stripe>
              <el-table-column prop="point_index" label="序号" width="60" />
              <el-table-column prop="name" label="名称" min-width="180" show-overflow-tooltip />
              <el-table-column prop="modbus_address" label="Modbus地址" width="110" />
              <el-table-column prop="signal_type" label="信号类型" width="90">
                <template #default="{ row }">
                  <el-tag :type="row.signal_type === '开关量' ? 'info' : 'warning'" size="small">
                    {{ row.signal_type }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="unit" label="单位" width="60" />
              <el-table-column prop="ams_module_id" label="AMS编号" width="130" show-overflow-tooltip />
              <el-table-column prop="is_active" label="状态" width="70">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
                    {{ row.is_active ? '有效' : '备用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="100" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" text @click="editPoint(row)">编辑</el-button>
                  <el-button size="small" text type="danger" @click="deletePoint(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div style="margin-top: 12px;">
              <el-button size="small" @click="showAddPoint = true">+ 添加工况点</el-button>
              <el-button size="small" type="danger" @click="generateConfig">🔴 生成配置</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </template>

    <!-- Add Modbus Config Dialog -->
    <el-dialog v-model="showAddConfig" title="新增Modbus客户端" width="500px">
      <el-form :model="newConfig" label-width="100px">
        <el-form-item label="客户端名称"><el-input v-model="newConfig.name" /></el-form-item>
        <el-form-item label="传输模式">
          <el-select v-model="newConfig.transport_mode" style="width:100%;">
            <el-option label="TCP" value="TCP" /><el-option label="RTU" value="RTU" />
          </el-select>
        </el-form-item>
        <el-form-item label="从站ID"><el-input v-model.number="newConfig.slave_id" /></el-form-item>
        <el-form-item label="IP地址"><el-input v-model="newConfig.ip_address" /></el-form-item>
        <el-form-item label="端口"><el-input v-model.number="newConfig.port" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddConfig = false">取消</el-button>
        <el-button type="primary" @click="addConfig">确定</el-button>
      </template>
    </el-dialog>

    <!-- Add/Edit Point Dialog -->
    <el-dialog v-model="showAddPoint" :title="editingPoint ? '编辑工况点' : '添加工况点'" width="600px">
      <el-form :model="pointForm" label-width="120px" size="small">
        <el-form-item label="名称"><el-input v-model="pointForm.name" /></el-form-item>
        <el-form-item label="Modbus地址"><el-input v-model="pointForm.modbus_address" /></el-form-item>
        <el-form-item label="信号类型">
          <el-select v-model="pointForm.signal_type" style="width:100%;">
            <el-option label="开关量" value="开关量" />
            <el-option label="模拟量" value="模拟量" />
            <el-option label="浮点数" value="浮点数" />
          </el-select>
        </el-form-item>
        <el-form-item label="序号"><el-input v-model.number="pointForm.point_index" /></el-form-item>
        <el-form-item label="单位"><el-input v-model="pointForm.unit" /></el-form-item>
        <el-form-item label="数据类型"><el-input v-model="pointForm.data_type" /></el-form-item>
        <el-form-item label="字节顺序"><el-input v-model="pointForm.byte_order" /></el-form-item>
        <el-form-item label="AMS编号"><el-input v-model="pointForm.ams_module_id" /></el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="pointForm.is_active" :active-value="1" :inactive-value="0" active-text="有效" inactive-text="备用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddPoint = false">取消</el-button>
        <el-button type="primary" @click="savePoint">确定</el-button>
      </template>
    </el-dialog>

    <!-- Excel Import Dialog -->
    <ExcelImportDialog
      v-model:visible="showImportDialog"
      :config-id="selectedConfigId"
      @imported="onPointsImported"
    />

    <!-- Config Generation Result -->
    <el-dialog v-model="showGenResult" title="配置生成结果" width="600px">
      <div v-if="genResult">
        <el-alert :title="genResult.message" :type="genResult.success ? 'success' : 'error'" show-icon />
        <el-input
          v-if="genResult.json_content"
          type="textarea"
          :rows="10"
          :model-value="JSON.stringify(genResult.json_content, null, 2)"
          style="margin-top: 12px;"
          readonly
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { modbusApi } from '../api'
import ExcelImportDialog from '../components/ExcelImportDialog.vue'

// Ship / Gateway / Config
const ships = ref<any[]>([])
const gateways = ref<any[]>([])
const configs = ref<any[]>([])
const selectedShipId = ref<number | null>(null)
const selectedGatewayId = ref<number | null>(null)
const selectedConfigId = ref<number | null>(null)
const selectedConfig = ref<any>(null)
const points = ref<any[]>([])

// Dialogs
const showAddConfig = ref(false)
const showAddPoint = ref(false)
const showImportDialog = ref(false)
const showGenResult = ref(false)
const genResult = ref<any>(null)

const editingPoint = ref<any>(null)
const newConfig = reactive({
  channel_id: 0, name: '', transport_mode: 'TCP',
  slave_id: 1, ip_address: '', port: 502,
})
const pointForm = reactive({
  modbus_config_id: 0, point_index: null, name: '',
  modbus_address: '', signal_type: '开关量',
  unit: '', data_type: '', byte_order: '',
  ams_module_id: '', is_active: 1,
})

// Load ships
onMounted(async () => {
  try {
    const res = await modbusApi.listShips()
    ships.value = res.data
    if (ships.value.length > 0) {
      selectedShipId.value = ships.value[0].id
      await onShipChange()
    }
  } catch { /* ship list can be empty */ }
})

async function onShipChange() {
  selectedGatewayId.value = null
  selectedConfigId.value = null
  selectedConfig.value = null
  points.value = []
  if (!selectedShipId.value) return
  const res = await modbusApi.listGateways(selectedShipId.value)
  gateways.value = res.data
}

async function onGatewayChange() {
  selectedConfigId.value = null
  selectedConfig.value = null
  points.value = []
  if (!selectedGatewayId.value) return
  // Use gateway id as channel id
  const res = await modbusApi.listConfigs(selectedGatewayId.value)
  configs.value = res.data
}

async function onConfigChange() {
  selectedConfig.value = null
  points.value = []
  if (!selectedConfigId.value) return
  const found = configs.value.find((c: any) => c.id === selectedConfigId.value)
  if (found) {
    selectedConfig.value = { ...found }
  }
  await loadPoints()
}

async function loadPoints() {
  if (!selectedConfigId.value) return
  const res = await modbusApi.listPoints(selectedConfigId.value)
  points.value = res.data
}

// Add config
async function addConfig() {
  newConfig.channel_id = selectedGatewayId.value || 0
  try {
    const res = await modbusApi.createConfig(newConfig)
    ElMessage.success('客户端已创建')
    showAddConfig.value = false
    if (selectedGatewayId.value) {
      const r2 = await modbusApi.listConfigs(selectedGatewayId.value)
      configs.value = r2.data
    }
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  }
}

// Save config params
async function saveConfig() {
  if (!selectedConfig.value?.id) return
  try {
    await modbusApi.updateConfig(selectedConfig.value.id, selectedConfig.value)
    ElMessage.success('通讯参数已保存')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  }
}

// Edit / Delete point
function editPoint(row: any) {
  editingPoint.value = row
  Object.assign(pointForm, row)
  showAddPoint.value = true
}

async function deletePoint(row: any) {
  try {
    await ElMessageBox.confirm(`确定删除"${row.name}"?`)
    await modbusApi.deletePoint(row.id)
    ElMessage.success('已删除')
    await loadPoints()
  } catch { /* cancelled */ }
}

async function savePoint() {
  pointForm.modbus_config_id = selectedConfigId.value || 0
  try {
    if (editingPoint.value) {
      await modbusApi.updatePoint(editingPoint.value.id, pointForm)
      ElMessage.success('已更新')
    } else {
      await modbusApi.createPoint(pointForm)
      ElMessage.success('已添加')
    }
    showAddPoint.value = false
    editingPoint.value = null
    resetPointForm()
    await loadPoints()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  }
}

function resetPointForm() {
  Object.assign(pointForm, {
    modbus_config_id: 0, point_index: null, name: '',
    modbus_address: '', signal_type: '开关量',
    unit: '', data_type: '', byte_order: '',
    ams_module_id: '', is_active: 1,
  })
}

async function generateConfig() {
  if (!selectedConfigId.value) return
  try {
    const res = await modbusApi.generateConfig(selectedConfigId.value)
    genResult.value = res.data
    showGenResult.value = true
    if (res.data.success) ElMessage.success('配置已生成')
  } catch (e: any) {
    ElMessage.error('生成失败')
  }
}

function onPointsImported() {
  showImportDialog.value = false
  loadPoints()
}

// Watch dialog close
watch(showAddPoint, (v) => { if (!v) { editingPoint.value = null; resetPointForm() } })
</script>

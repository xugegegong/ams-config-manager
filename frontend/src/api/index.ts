import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Auto-attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auto-redirect on 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

// ─── Auth ───
export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  getMe: () => api.get('/auth/me'),
  initAdmin: () => api.post('/auth/init-admin'),
}

// ─── Database ───
export const dbApi = {
  testConnection: (data: any) =>
    api.post('/database/test-connection', data),
}

// ─── Ships & Modbus ───
export const modbusApi = {
  listShips: () => api.get('/modbus/ships'),
  createShip: (name: string, imo = '', mmsi = '') =>
    api.post(`/modbus/ships?name=${encodeURIComponent(name)}&imo=${imo}&mmsi=${mmsi}`),

  listGateways: (shipId: number) => api.get(`/modbus/gateways/${shipId}`),

  listConfigs: (channelId: number) => api.get(`/modbus/configs/${channelId}`),
  createConfig: (data: any) => api.post('/modbus/configs', data),
  updateConfig: (id: number, data: any) => api.put(`/modbus/configs/${id}`, data),
  deleteConfig: (id: number) => api.delete(`/modbus/configs/${id}`),

  listPoints: (configId: number) => api.get(`/modbus/points/${configId}`),
  createPoint: (data: any) => api.post('/modbus/points', data),
  updatePoint: (id: number, data: any) => api.put(`/modbus/points/${id}`, data),
  deletePoint: (id: number) => api.delete(`/modbus/points/${id}`),
  batchSavePoints: (configId: number, points: any[]) =>
    api.post(`/modbus/points/batch/${configId}`, points),

  generateConfig: (configId: number) =>
    api.post(`/modbus/generate/${configId}`),
}

// ─── Import ───
export const importApi = {
  previewExcel: (formData: FormData) =>
    api.post('/import/preview', formData),

  listTemplates: () => api.get('/import/templates'),
  getTemplate: (id: number) => api.get(`/import/templates/${id}`),
  createTemplate: (data: any) => api.post('/import/templates', data),
  updateTemplate: (id: number, data: any) => api.put(`/import/templates/${id}`, data),
  deleteTemplate: (id: number) => api.delete(`/import/templates/${id}`),

  parseExcel: (formData: FormData) =>
    api.post('/import/parse', formData),

  createDiff: (formData: FormData) =>
    api.post('/import/diff', formData),

  listChanges: (versionId: number) =>
    api.get(`/import/changes/${versionId}`),

  batchApprove: (data: any) =>
    api.post('/import/changes/batch-approve', data),

  cfg2db: (configId: number, data: any) =>
    api.post(`/import/cfg2db/${configId}`, data),
}

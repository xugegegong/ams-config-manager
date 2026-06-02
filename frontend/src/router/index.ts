import { createRouter, createWebHistory } from 'vue-router'
import Database from '../views/Database.vue'
import EngineRoom from '../views/EngineRoom.vue'
import Cfg2DB from '../views/Cfg2DB.vue'
import Templates from '../views/Templates.vue'
import Help from '../views/Help.vue'

const routes = [
  { path: '/', redirect: '/database' },
  { path: '/database', name: 'Database', component: Database },
  { path: '/engine-room', name: 'EngineRoom', component: EngineRoom },
  { path: '/cfg2db', name: 'Cfg2DB', component: Cfg2DB },
  { path: '/templates', name: 'Templates', component: Templates },
  { path: '/help', name: 'Help', component: Help },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

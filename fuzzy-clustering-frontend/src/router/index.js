import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import UploadEnhanced from '../views/UploadEnhanced.vue'
import AnalysisEnhanced from '../views/AnalysisEnhanced.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/upload',
    name: 'Upload',
    component: UploadEnhanced
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisEnhanced
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
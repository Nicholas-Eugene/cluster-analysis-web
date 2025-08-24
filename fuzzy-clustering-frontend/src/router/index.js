import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Upload from '../views/Upload.vue'
import UploadMockup from '../views/UploadMockup.vue'
import UploadSimple from '../views/UploadSimple.vue'
import Analysis from '../views/Analysis.vue'
import AnalysisMockup from '../views/AnalysisMockup.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/upload',
    name: 'Upload',
    component: UploadMockup
  },
  {
    path: '/upload-simple',
    name: 'UploadSimple',
    component: UploadSimple
  },
  {
    path: '/upload-full',
    name: 'UploadFull',
    component: Upload
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisMockup
  },
  {
    path: '/analysis-full',
    name: 'AnalysisFull',
    component: Analysis
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
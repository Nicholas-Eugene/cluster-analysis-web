import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Upload from '../views/Upload.vue'
import UploadMockup from '../views/UploadMockup.vue'
import UploadEnhanced from '../views/UploadEnhanced.vue'
import UploadSimple from '../views/UploadSimple.vue'
import Analysis from '../views/Analysis.vue'
import AnalysisMockup from '../views/AnalysisMockup.vue'
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
    path: '/upload-mockup',
    name: 'UploadMockup',
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
    component: AnalysisEnhanced
  },
  {
    path: '/analysis-mockup',
    name: 'AnalysisMockup',
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
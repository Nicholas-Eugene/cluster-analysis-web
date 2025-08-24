import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Upload from '../views/Upload.vue'
import UploadSimple from '../views/UploadSimple.vue'
import Analysis from '../views/Analysis.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/upload',
    name: 'Upload',
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
    component: Analysis
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
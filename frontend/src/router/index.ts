import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import { useSettingsStore } from '../stores/settings.store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('../views/Dashboard/index.vue')
        },
        {
          path: 'single-prediction',
          name: 'single-prediction',
          component: () => import('../views/SinglePrediction/index.vue')
        },
        {
          path: 'batch-prediction',
          name: 'batch-prediction',
          component: () => import('../views/BatchPrediction/index.vue')
        },
        {
          path: 'prediction-result/:id',
          name: 'prediction-result',
          component: () => import('../views/PredictionResult/index.vue'),
          props: true
        },
        {
          path: 'prediction-history',
          name: 'prediction-history',
          component: () => import('../views/PredictionHistory/index.vue')
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('../views/About/index.vue')
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/Settings/index.vue')
        }
      ]
    }
  ]
})

router.beforeResolve(() => {
  if (!document.startViewTransition) return;
  try {
    const settingsStore = useSettingsStore();
    if (!settingsStore.motionEffects) return;
  } catch (e) {
    // pinia not ready yet
  }
  return new Promise<void>((resolve) => {
    document.startViewTransition(resolve);
  });
})

export default router

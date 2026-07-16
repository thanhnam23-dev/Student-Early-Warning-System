<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import PageHeader from '../../components/common/PageHeader.vue';
import Card from 'primevue/card';

const { t } = useI18n();

const techStackFrontend = [
  { name: 'Vue 3', desc: 'Progressive JavaScript framework for UI components' },
  { name: 'Pinia', desc: 'Reactive state management pattern and store' },
  { name: 'Tailwind CSS v4', desc: 'Utility-first CSS framework for modern design aesthetics' },
  { name: 'PrimeVue v4', desc: 'Rich component library styled with Aura design presets' },
  { name: 'TypeScript', desc: 'Strong static typings for enterprise codebase consistency' }
];

const techStackBackend = [
  { name: 'Laravel 11', desc: 'PHP framework for administrative API & role control (Future)' },
  { name: 'PostgreSQL', desc: 'Relational database for secure history and profile logs (Future)' }
];

const techStackAI = [
  { name: 'FastAPI', desc: 'Python API framework for high-throughput AI predictions' },
  { name: 'XGBoost / LightGBM', desc: 'Gradient boosted tree algorithms achieving 87%+ PR-AUC' },
  { name: 'SHAP (Explainable AI)', desc: 'Game-theoretic approach explaining prediction features' }
];
</script>

<template>
  <div class="space-y-6 max-w-5xl mx-auto">
    <PageHeader 
      :title="t('about.title')" 
      :description="t('about.description')"
    />

    <!-- 1. Description & Objectives Card -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card class="md:col-span-2 border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
        <template #content>
          <div class="space-y-4">
            <h4 class="text-base font-bold text-gray-850 dark:text-gray-200">
              {{ t('about.overview.title') }}
            </h4>
            <p class="text-xs text-gray-555 dark:text-gray-400 leading-relaxed font-medium">
              {{ t('about.overview.p1') }}
            </p>
            <p class="text-xs text-gray-555 dark:text-gray-400 leading-relaxed font-medium">
              {{ t('about.overview.p2') }}
            </p>
          </div>
        </template>
      </Card>
      
      <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
        <template #content>
          <div class="space-y-3.5">
            <h4 class="text-base font-bold text-gray-850 dark:text-gray-200">
              {{ t('about.overview.titleObjectives') }}
            </h4>
            <ul class="space-y-2.5 list-none p-0 m-0 text-xs font-semibold text-gray-650 dark:text-gray-300">
              <li class="flex items-start">
                <i class="fa-solid fa-check text-primary-500 mr-2.5 pt-0.5"></i>
                <span>{{ t('about.overview.obj1') }}</span>
              </li>
              <li class="flex items-start">
                <i class="fa-solid fa-check text-primary-500 mr-2.5 pt-0.5"></i>
                <span>{{ t('about.overview.obj2') }}</span>
              </li>
              <li class="flex items-start">
                <i class="fa-solid fa-check text-primary-500 mr-2.5 pt-0.5"></i>
                <span>{{ t('about.overview.obj3') }}</span>
              </li>
              <li class="flex items-start">
                <i class="fa-solid fa-check text-primary-500 mr-2.5 pt-0.5"></i>
                <span>{{ t('about.overview.obj4') }}</span>
              </li>
            </ul>
          </div>
        </template>
      </Card>
    </div>

    <!-- 2. Dataset Information -->
    <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
      <template #content>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="md:col-span-3 space-y-4">
            <h4 class="text-base font-bold text-gray-850 dark:text-gray-200">
              {{ t('about.dataset.title') }}
            </h4>
            <p class="text-xs text-gray-555 dark:text-gray-400 leading-relaxed font-medium">
              {{ t('about.dataset.p1') }}
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-semibold text-gray-650 dark:text-gray-350">
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 bg-primary-500 rounded-full"></span>
                <span>{{ t('singlePrediction.steps.step1') }} & {{ t('singlePrediction.steps.step2') }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 bg-primary-500 rounded-full"></span>
                <span>{{ t('singlePrediction.steps.step3') }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 bg-primary-500 rounded-full"></span>
                <span>{{ t('singlePrediction.steps.step4') }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 bg-primary-500 rounded-full"></span>
                <span>Macroeconomic Indices</span>
              </div>
            </div>
          </div>
          <div class="bg-gray-50/50 dark:bg-gray-950/20 p-4 border border-gray-150 dark:border-gray-800 rounded-xl flex flex-col items-center justify-center text-center font-bold">
            <i class="fa-solid fa-database text-3xl text-primary-500 mb-2"></i>
            <span class="text-lg font-black text-gray-900 dark:text-white">4,424</span>
            <span class="text-[9px] text-gray-450 uppercase tracking-wide">{{ t('about.dataset.records') }}</span>
            <span class="text-lg font-black text-gray-900 dark:text-white mt-2">36</span>
            <span class="text-[9px] text-gray-450 uppercase tracking-wide">{{ t('about.dataset.features') }}</span>
          </div>
        </div>
      </template>
    </Card>

    <!-- 3. Machine Learning Algorithms -->
    <div class="space-y-3">
      <h4 class="text-sm font-bold text-gray-450 dark:text-gray-550 uppercase tracking-wider pl-1">
        {{ t('about.algorithms.title') }}
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <!-- RF -->
        <div class="bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 rounded-2xl p-5 shadow-sm space-y-2.5 transition-colors">
          <div class="flex items-center justify-between">
            <h5 class="text-xs font-bold text-gray-900 dark:text-white">
              {{ t('about.algorithms.rf') }}
            </h5>
            <span class="px-2 py-0.5 rounded bg-primary-50 text-primary-600 dark:bg-primary-950/20 dark:text-primary-400 text-[9px] font-extrabold">
              Bagging Ensemble
            </span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 leading-normal font-medium">
            {{ t('about.algorithms.rfDesc') }}
          </p>
        </div>

        <!-- XGB -->
        <div class="bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 rounded-2xl p-5 shadow-sm space-y-2.5 transition-colors">
          <div class="flex items-center justify-between">
            <h5 class="text-xs font-bold text-gray-900 dark:text-white">
              {{ t('about.algorithms.xgb') }}
            </h5>
            <span class="px-2 py-0.5 rounded bg-primary-50 text-primary-600 dark:bg-primary-950/20 dark:text-primary-400 text-[9px] font-extrabold">
              Gradient Boosting
            </span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 leading-normal font-medium">
            {{ t('about.algorithms.xgbDesc') }}
          </p>
        </div>

        <!-- LGBM -->
        <div class="bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 rounded-2xl p-5 shadow-sm space-y-2.5 transition-colors">
          <div class="flex items-center justify-between">
            <h5 class="text-xs font-bold text-gray-900 dark:text-white">
              {{ t('about.algorithms.lgbm') }}
            </h5>
            <span class="px-2 py-0.5 rounded bg-primary-50 text-primary-600 dark:bg-primary-950/20 dark:text-primary-400 text-[9px] font-extrabold">
              Gradient Boosting
            </span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 leading-normal font-medium">
            {{ t('about.algorithms.lgbmDesc') }}
          </p>
        </div>
      </div>
    </div>

    <!-- 4. Technology Stack Config -->
    <div class="space-y-3">
      <h4 class="text-sm font-bold text-gray-450 dark:text-gray-550 uppercase tracking-wider pl-1">
        {{ t('about.stack.title') }}
      </h4>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <!-- Frontend -->
        <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-850 dark:text-gray-250">
              <i class="fa-solid fa-desktop text-primary-500 text-xs"></i>
              <span>{{ t('about.stack.client') }}</span>
            </div>
          </template>
          <template #content>
            <ul class="space-y-3 list-none p-0 m-0 text-xs font-semibold text-gray-650 dark:text-gray-300">
              <li v-for="item in techStackFrontend" :key="item.name">
                <span class="block font-bold text-gray-900 dark:text-white">{{ item.name }}</span>
                <span class="text-[10px] text-gray-400 dark:text-gray-500 leading-none">{{ item.desc }}</span>
              </li>
            </ul>
          </template>
        </Card>

        <!-- Backend -->
        <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-850 dark:text-gray-250">
              <i class="fa-solid fa-server text-primary-500 text-xs"></i>
              <span>{{ t('about.stack.gateway') }}</span>
            </div>
          </template>
          <template #content>
            <ul class="space-y-3 list-none p-0 m-0 text-xs font-semibold text-gray-650 dark:text-gray-300">
              <li v-for="item in techStackBackend" :key="item.name">
                <span class="block font-bold text-gray-900 dark:text-white">{{ item.name }}</span>
                <span class="text-[10px] text-gray-400 dark:text-gray-500 leading-none">{{ item.desc }}</span>
              </li>
            </ul>
            <div class="mt-4 p-2.5 bg-gray-50 dark:bg-gray-850 rounded-lg text-[10px] text-gray-400 dark:text-gray-550 border border-gray-100 dark:border-gray-800/80 font-bold leading-normal">
              {{ t('about.stack.gatewayNote') }}
            </div>
          </template>
        </Card>

        <!-- AI Server -->
        <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-850 dark:text-gray-250">
              <i class="fa-solid fa-microchip text-primary-500 text-xs"></i>
              <span>{{ t('about.stack.classifier') }}</span>
            </div>
          </template>
          <template #content>
            <ul class="space-y-3 list-none p-0 m-0 text-xs font-semibold text-gray-650 dark:text-gray-300">
              <li v-for="item in techStackAI" :key="item.name">
                <span class="block font-bold text-gray-900 dark:text-white">{{ item.name }}</span>
                <span class="text-[10px] text-gray-400 dark:text-gray-500 leading-none">{{ item.desc }}</span>
              </li>
            </ul>
          </template>
        </Card>
      </div>
    </div>

    <!-- 5. Research Team Details -->
    <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
      <template #content>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 font-semibold">
          <div class="space-y-1">
            <h4 class="text-base font-bold text-gray-850 dark:text-gray-200">
              {{ t('about.team.title') }}
            </h4>
            <p class="text-xs text-gray-450 dark:text-gray-550">
              {{ t('about.team.initiative') }}
            </p>
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">
            <span class="block">{{ t('about.team.lead') }}: <strong class="text-gray-900 dark:text-white">{{ t('about.team.leadName') }}</strong></span>
            <span class="block mt-0.5">{{ t('about.team.sponsor') }}: <strong class="text-gray-900 dark:text-white">{{ t('about.team.sponsorName') }}</strong></span>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from '../../stores/settings.store';
import { ROUTES } from '../../constants/routes';
import { useI18n } from 'vue-i18n';

import { watch } from 'vue';
import { useRoute } from 'vue-router';

const { t } = useI18n();
const settingsStore = useSettingsStore();
const route = useRoute();

watch(() => route.path, () => {
  settingsStore.setMobileSidebar(false);
});

const menuGroups = [
  {
    titleEn: 'OVERVIEW',
    titleVi: 'TỔNG QUAN',
    items: [
      { labelKey: 'sidebar.dashboard', path: ROUTES.DASHBOARD, icon: 'fa-solid fa-chart-line' }
    ]
  },
  {
    titleEn: 'PREDICTIONS',
    titleVi: 'DỰ ĐOÁN',
    items: [
      { labelKey: 'sidebar.singlePrediction', path: ROUTES.SINGLE_PREDICTION, icon: 'fa-solid fa-user-graduate' },
      { labelKey: 'sidebar.batchPrediction', path: ROUTES.BATCH_PREDICTION, icon: 'fa-solid fa-file-import' },
      { labelKey: 'sidebar.history', path: ROUTES.PREDICTION_HISTORY, icon: 'fa-solid fa-clock-rotate-left' }
    ]
  },
  {
    titleEn: 'INFORMATION',
    titleVi: 'THÔNG TIN',
    items: [
      { labelKey: 'sidebar.about', path: ROUTES.ABOUT, icon: 'fa-solid fa-circle-info' }
    ]
  },
  {
    titleEn: 'SYSTEM',
    titleVi: 'HỆ THỐNG',
    items: [
      { labelKey: 'sidebar.settings', path: ROUTES.SETTINGS, icon: 'fa-solid fa-gear' }
    ]
  }
];
</script>

<template>
  <aside 
    class="w-64 border-r border-gray-150 dark:border-gray-800 bg-white dark:bg-gray-900 flex flex-col h-full 
           fixed md:relative top-0 md:top-auto bottom-0 left-0 md:left-auto z-40 md:z-30 font-sans transition-transform duration-300 flex-shrink-0"
    :class="[
      settingsStore.mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
    ]"
  >
    <!-- Mobile Sidebar Close Header -->
    <div class="flex md:hidden items-center justify-between px-5 h-16 border-b border-gray-150 dark:border-gray-800 flex-shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center text-white shadow-sm shadow-primary-500/25">
          <i class="fa-solid fa-graduation-cap text-xs"></i>
        </div>
        <span class="text-xs font-black text-gray-900 dark:text-white tracking-tight">SEWS Menu</span>
      </div>
      <button 
        @click="settingsStore.setMobileSidebar(false)"
        class="w-7 h-7 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 flex items-center justify-center border border-gray-150 dark:border-gray-700/60 text-gray-400 hover:text-gray-650 cursor-pointer"
      >
        <i class="fa-solid fa-xmark text-xs"></i>
      </button>
    </div>

    <!-- Menu Categories Links -->
    <nav class="flex-1 px-4 py-6 space-y-5 overflow-y-auto">
      <div v-for="group in menuGroups" :key="group.titleEn" class="space-y-1.5">
        <!-- Group Header Title -->
        <span class="block px-4 text-[9px] font-extrabold text-gray-400 dark:text-gray-550 uppercase tracking-widest leading-none mb-2">
          {{ settingsStore.language === 'vi' ? group.titleVi : group.titleEn }}
        </span>

        <!-- Group Items -->
        <router-link
          v-for="item in group.items"
          :key="item.path"
          :to="item.path"
          v-slot="{ isActive }"
          class="no-underline block"
        >
          <span
            class="relative flex items-center px-4 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 cursor-pointer group"
            :class="isActive 
              ? 'bg-primary-50/60 text-primary-600 dark:bg-primary-950/20 dark:text-primary-400' 
              : 'text-gray-650 hover:bg-gray-50/50 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-800/30 dark:hover:text-white'"
          >
            <!-- Sliding active indicator -->
            <transition name="sidebar-indicator">
              <span 
                v-if="isActive" 
                class="absolute left-0 top-3 bottom-3 w-1 rounded-r bg-primary-600 dark:bg-primary-400"
                style="view-transition-name: sidebar-indicator;"
              ></span>
            </transition>

            <i 
              :class="[
                item.icon, 
                'w-4 text-center text-[13px] mr-3 transition-all duration-200',
                isActive ? 'text-primary-600 dark:text-primary-400 scale-105' : 'text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300'
              ]"
            ></i>
            {{ t(item.labelKey) }}
          </span>
        </router-link>
      </div>
    </nav>

    <!-- Sidebar footer mock mode card -->
    <div class="p-4 border-t border-gray-150 dark:border-gray-800">
      <div class="bg-gray-50/50 dark:bg-gray-800/20 rounded-xl p-3.5 border border-gray-150 dark:border-gray-800 flex items-start space-x-2.5">
        <span class="flex-shrink-0 w-2 h-2 rounded-full bg-emerald-500 mt-1 shadow-sm shadow-emerald-400/55 animate-pulse"></span>
        <div class="flex-1 min-w-0">
          <h6 class="text-[11px] font-bold text-gray-700 dark:text-gray-300 leading-tight">
            {{ settingsStore.language === 'vi' ? 'Chế độ Giả Lập' : 'Mock Mode Active' }}
          </h6>
          <p class="text-[9px] text-gray-400 font-semibold leading-normal mt-0.5">
            {{ settingsStore.language === 'vi' ? 'Hệ thống đang hoạt động bình thường' : 'Warning models are simulating cleanly' }}
          </p>
        </div>
      </div>

      <!-- Small Copyright Label -->
      <div class="mt-4 text-[9px] text-gray-400 font-bold tracking-tight text-center">
        <span>SEWS v1.0.0-beta</span>
        <span class="mx-1.5">•</span>
        <span>© 2026 SEWS Team</span>
      </div>
    </div>
  </aside>
</template>

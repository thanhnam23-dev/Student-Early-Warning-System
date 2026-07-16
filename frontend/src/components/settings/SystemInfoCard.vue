<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import Card from 'primevue/card';

const { t } = useI18n();

const systemDetails = [
  { label: 'settings.system.version', value: 'v1.0.0-beta.frontend' },
  { label: 'settings.system.framework', value: 'Vue 3.5.13 (Vite 6)' },
  { label: 'settings.system.backend', value: 'settings.system.mockMode', isMock: true },
  { label: 'settings.system.ai', value: 'settings.system.mockMode', isMock: true }
];
</script>

<template>
  <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
    <template #title>
      <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-800 dark:text-gray-200">
        <i class="fa-solid fa-server text-primary-500 text-xs"></i>
        <span>{{ t('settings.system.title') }}</span>
      </div>
    </template>
    <template #content>
      <div class="space-y-4">
        <div 
          v-for="detail in systemDetails" 
          :key="detail.label"
          class="flex items-center justify-between py-1.5 border-b border-gray-50 dark:border-gray-800 last:border-0"
        >
          <span class="text-xs font-bold text-gray-500 dark:text-gray-400">
            {{ t(detail.label) }}
          </span>
          <div class="flex items-center space-x-2 text-xs font-bold">
            <span 
              v-if="detail.isMock"
              class="px-2 py-0.5 rounded text-[10px] bg-amber-50 text-amber-600 border border-amber-100 dark:bg-amber-950/20 dark:text-amber-400 dark:border-amber-900"
            >
              {{ t(detail.value) }}
            </span>
            <span v-else class="text-gray-900 dark:text-white">
              {{ detail.value }}
            </span>
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

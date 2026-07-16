<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useSettingsStore } from '../../stores/settings.store';
import { useI18n } from 'vue-i18n';

defineProps<{
  isScrolled?: boolean;
}>();

const { t } = useI18n();
const settingsStore = useSettingsStore();
const currentFormattedDate = ref('');

const isDarkMode = computed(() => settingsStore.appearance === 'dark');

const updateTime = () => {
  const options: Intl.DateTimeFormatOptions = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };
  const locale = settingsStore.language === 'vi' ? 'vi-VN' : 'en-US';
  currentFormattedDate.value = new Date().toLocaleDateString(locale, options);
};

const toggleDarkMode = () => {
  const nextMode = settingsStore.appearance === 'dark' ? 'light' : 'dark';
  settingsStore.setAppearance(nextMode);
};

watch(() => settingsStore.language, () => updateTime());
onMounted(() => updateTime());
</script>

<template>
  <header
    class="h-16 px-5 flex items-center justify-between sticky top-0 z-40 transition-all duration-300 w-full flex-shrink-0"
    :class="[
      isScrolled 
        ? 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200/80 dark:border-gray-800/80 shadow-md shadow-slate-100/30 dark:shadow-[#05070c]/30' 
        : 'bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm border-b border-gray-150 dark:border-gray-850 shadow-none'
    ]"
  >
    <!-- Left: Logo + Title -->
    <div class="flex items-center space-x-3">
      <!-- Mobile Sidebar Toggle -->
      <button 
        @click="settingsStore.toggleMobileSidebar"
        class="md:hidden w-8 h-8 rounded-lg bg-gray-50/50 dark:bg-gray-800/40 hover:bg-gray-100 dark:hover:bg-gray-700
               flex items-center justify-center border border-gray-150 dark:border-gray-700/60
               text-gray-500 dark:text-gray-400 cursor-pointer active:scale-95 transition-all duration-200"
      >
        <i class="fa-solid fa-bars text-xs"></i>
      </button>

      <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700
                  flex items-center justify-center text-white shadow-md shadow-primary-500/25
                  flex-shrink-0">
        <i class="fa-solid fa-graduation-cap text-base"></i>
      </div>
      <div class="leading-none">
        <h1 class="text-sm font-black text-gray-900 dark:text-white leading-tight tracking-tight">
          {{ t('header.earlyWarningSystem') }}
        </h1>
        <p class="text-[9px] font-extrabold text-primary-500 dark:text-primary-400 tracking-widest uppercase mt-0.5 leading-none">
          {{ t('header.mockPrediction') }}
        </p>
      </div>
    </div>

    <!-- Right: Date + Toggle Actions -->
    <div class="flex items-center space-x-2.5">
      <!-- Date display -->
      <div class="hidden md:flex items-center space-x-2 bg-gray-50/50 dark:bg-gray-800/40
                  border border-gray-150 dark:border-gray-700/60 rounded-xl px-3 h-9">
        <i class="fa-solid fa-calendar-days text-[11px] text-primary-500"></i>
        <span class="text-[11px] font-bold text-gray-500 dark:text-gray-400 whitespace-nowrap">
          {{ currentFormattedDate }}
        </span>
      </div>
    </div>
  </header>
</template>

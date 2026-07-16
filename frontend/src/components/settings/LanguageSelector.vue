<script setup lang="ts">
import { computed } from 'vue';
import { useSettingsStore } from '../../stores/settings.store';
import { useI18n } from 'vue-i18n';

const i18n = useI18n();
const settingsStore = useSettingsStore();

const activeLang = computed(() => settingsStore.language);

const languages = [
  { code: 'en', labelKey: 'settings.languages.en', flag: '🇺🇸' },
  { code: 'vi', labelKey: 'settings.languages.vi', flag: '🇻🇳' }
];

const handleLanguageChange = (code: 'en' | 'vi') => {
  settingsStore.setLanguage(code, i18n);
};
</script>

<template>
  <div class="space-y-4">
    <span class="block text-[10px] font-bold text-gray-400 uppercase tracking-wider">
      {{ i18n.t('settings.general.language') }}
    </span>
    
    <div class="flex flex-col sm:flex-row gap-3">
      <button
        v-for="lang in languages"
        :key="lang.code"
        @click="handleLanguageChange(lang.code as 'en' | 'vi')"
        class="flex-1 flex items-center justify-between p-3.5 rounded-xl border cursor-pointer transition-all duration-200"
        :class="[
          activeLang === lang.code
            ? 'border-primary-500 bg-primary-50/20 text-primary-950 dark:bg-primary-950/10 font-bold'
            : 'border-gray-150 bg-white hover:bg-gray-50/50 hover:border-gray-300 text-gray-700 dark:bg-transparent dark:border-gray-800'
        ]"
      >
        <div class="flex items-center space-x-3 text-xs font-bold">
          <span class="text-base leading-none">{{ lang.flag }}</span>
          <span>{{ i18n.t(lang.labelKey) }}</span>
        </div>
        <i v-if="activeLang === lang.code" class="fa-solid fa-circle-check text-sm text-primary-500"></i>
      </button>
    </div>
  </div>
</template>

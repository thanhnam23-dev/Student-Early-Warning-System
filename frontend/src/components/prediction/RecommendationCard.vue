<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps<{
  recommendations: string[];
  prediction: 'Graduate' | 'Enrolled' | 'Dropout';
}>();

const { tm, te, t } = useI18n();

const localizedRecs = computed<string[]>(() => {
  const key = `recommendations.${props.prediction}`;
  if (te(key)) {
    const list = tm(key);
    if (Array.isArray(list)) return list as string[];
  }
  return props.recommendations;
});

const headerTheme = computed(() => {
  if (props.prediction === 'Dropout') {
    return {
      border: 'border-red-100 dark:border-red-900/30',
      bg: 'bg-red-50/50 dark:bg-red-950/10',
      text: 'text-red-800 dark:text-red-400',
      icon: 'fa-solid fa-triangle-exclamation text-red-500'
    };
  } else if (props.prediction === 'Enrolled') {
    return {
      border: 'border-amber-100 dark:border-amber-900/30',
      bg: 'bg-amber-50/50 dark:bg-amber-950/10',
      text: 'text-amber-800 dark:text-amber-400',
      icon: 'fa-solid fa-circle-info text-amber-500'
    };
  } else {
    return {
      border: 'border-green-100 dark:border-green-900/30',
      bg: 'bg-green-50/50 dark:bg-green-950/10',
      text: 'text-green-800 dark:text-green-400',
      icon: 'fa-solid fa-circle-check text-green-500'
    };
  }
});
</script>

<template>
  <div 
    class="border rounded-2xl overflow-hidden transition-colors duration-200"
    :class="[headerTheme.border]"
  >
    <!-- Header banner -->
    <div 
      class="px-4 py-3.5 flex items-center space-x-2 border-b border-inherit"
      :class="[headerTheme.bg]"
    >
      <i :class="[headerTheme.icon, 'text-sm']"></i>
      <h5 
        class="text-xs font-bold uppercase tracking-wider"
        :class="[headerTheme.text]"
      >
        {{ t('result.advisoryCard') }}
      </h5>
    </div>
    
    <!-- Body list -->
    <div class="p-4 bg-white dark:bg-gray-900">
      <ul v-if="localizedRecs.length > 0" class="space-y-3.5 list-none p-0 m-0">
        <li 
          v-for="(rec, index) in localizedRecs" 
          :key="index"
          class="flex items-start text-xs font-semibold text-gray-650 dark:text-gray-300 leading-normal"
        >
          <span 
            class="w-5 h-5 rounded-full bg-gray-50 dark:bg-gray-800 flex items-center justify-center text-[10px] text-gray-400 dark:text-gray-550 mr-2.5 shrink-0 border border-gray-150 dark:border-gray-700 font-bold"
          >
            {{ index + 1 }}
          </span>
          <span class="pt-0.5">{{ rec }}</span>
        </li>
      </ul>
      <p v-else class="text-xs font-medium text-gray-400 dark:text-gray-500 text-center py-2">
        {{ t('general.loading').startsWith('L') ? 'No specific recommendations provided.' : 'Không có khuyến nghị cụ thể nào được cung cấp.' }}
      </p>
    </div>
  </div>
</template>

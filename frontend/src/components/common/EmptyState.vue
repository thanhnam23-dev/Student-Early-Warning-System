<script setup lang="ts">
import Button from 'primevue/button';

withDefaults(
  defineProps<{
    icon?: string;
    title: string;
    description: string;
    actionLabel?: string;
    actionIcon?: string;
  }>(),
  {
    icon: 'fa-solid fa-folder-open'
  }
);

defineEmits<{
  (e: 'action'): void;
}>();
</script>

<template>
  <div class="flex flex-col items-center justify-center text-center p-8 py-16 bg-white dark:bg-gray-900 rounded-2xl border border-gray-150 dark:border-gray-850 shadow-sm max-w-lg mx-auto animate-card-enter">
    <div class="w-14 h-14 rounded-full bg-primary-50 dark:bg-primary-950/20 flex items-center justify-center text-primary-500 dark:text-primary-400 mb-5 border border-primary-100/30 dark:border-primary-900/20">
      <i :class="[icon, 'text-xl']"></i>
    </div>
    <h3 class="text-sm font-bold text-gray-900 dark:text-white mb-1.5 tracking-tight">
      {{ title }}
    </h3>
    <p class="text-xs text-gray-450 dark:text-gray-400 max-w-xs leading-relaxed mb-6 font-medium">
      {{ description }}
    </p>
    
    <div v-if="$slots.default || actionLabel" class="flex justify-center w-full">
      <slot v-if="$slots.default"></slot>
      <Button 
        v-else-if="actionLabel"
        :label="actionLabel" 
        :icon="actionIcon || 'fa-solid fa-plus'" 
        class="text-xs font-bold px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl cursor-pointer shadow-md shadow-primary-500/20"
        @click="$emit('action')"
      />
    </div>
  </div>
</template>

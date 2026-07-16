<script setup lang="ts">
defineProps<{
  title: string;
  description?: string;
}>();
</script>

<template>
  <div class="flex flex-col md:flex-row md:items-start md:justify-between pb-5 mb-6 border-b border-gray-100 dark:border-gray-800/80">
    <div class="space-y-1">
      <h2 class="text-xl font-black text-gray-900 dark:text-white tracking-tight leading-snug">
        {{ title }}
      </h2>
      <p v-if="description" class="text-[13px] text-gray-500 dark:text-gray-400 font-medium leading-relaxed max-w-prose">
        {{ description }}
      </p>
    </div>

    <!-- Optional action buttons slot -->
    <div v-if="$slots.actions" class="mt-4 md:mt-0 flex items-center space-x-2.5 flex-shrink-0">
      <slot name="actions" />
    </div>
  </div>
</template>

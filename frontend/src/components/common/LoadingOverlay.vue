<script setup lang="ts">
import ProgressSpinner from 'primevue/progressspinner';

defineProps<{
  visible: boolean;
  message?: string;
}>();
</script>

<template>
  <Transition name="fade">
    <div 
      v-if="visible" 
      class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex flex-col items-center justify-center text-white"
    >
      <div class="bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 p-8 rounded-2xl shadow-2xl flex flex-col items-center max-w-sm w-full mx-4 transition-colors duration-200">
        <ProgressSpinner 
          style="width: 50px; height: 50px" 
          strokeWidth="4" 
          fill="transparent" 
          animationDuration=".8s" 
          aria-label="Loading"
        />
        <h4 class="mt-4 text-base font-bold text-gray-900 dark:text-white">
          Processing Request
        </h4>
        <p class="mt-2 text-xs text-gray-500 dark:text-gray-400 font-medium text-center leading-normal">
          {{ message || 'Analyzing data. Please wait a moment...' }}
        </p>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

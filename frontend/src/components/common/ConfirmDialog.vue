<script setup lang="ts">
import ConfirmDialog from 'primevue/confirmdialog';
</script>

<template>
  <ConfirmDialog>
    <template #container="{ message, acceptCallback, rejectCallback }">
      <div class="flex flex-col items-center p-6 bg-white dark:bg-gray-900 rounded-2xl border border-gray-150 dark:border-gray-800 shadow-xl max-w-sm w-full transition-colors duration-200">
        <div class="w-12 h-12 rounded-full bg-primary-50 dark:bg-primary-950/30 flex items-center justify-center text-primary-500 dark:text-primary-400 mb-4">
          <i class="fa-solid fa-circle-question text-2xl"></i>
        </div>
        <span class="font-bold text-lg text-gray-900 dark:text-white mb-2">{{ message.header || 'Confirmation' }}</span>
        <p class="text-sm text-gray-500 dark:text-gray-400 font-medium text-center mb-6 leading-normal">{{ message.message }}</p>
        <div class="flex items-center justify-center space-x-3 w-full">
          <button 
            @click="rejectCallback" 
            class="flex-1 py-2 px-4 border border-gray-200 dark:border-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-750 text-gray-700 dark:text-gray-300 rounded-xl text-sm font-semibold cursor-pointer transition-all duration-200"
          >
            {{ message.rejectLabel || 'Cancel' }}
          </button>
          <button 
            @click="acceptCallback" 
            class="flex-1 py-2 px-4 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-sm font-semibold cursor-pointer transition-all duration-200 shadow-md shadow-primary-500/20"
          >
            {{ message.acceptLabel || 'Confirm' }}
          </button>
        </div>
      </div>
    </template>
  </ConfirmDialog>
</template>

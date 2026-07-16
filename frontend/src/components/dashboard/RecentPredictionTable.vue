<script setup lang="ts">
import type { StudentPredictionResult } from '../../types/prediction';
import { formatPercent } from '../../utils/formatter';
import { formatDate } from '../../utils/date';
import { useI18n } from 'vue-i18n';
import RiskBadge from '../prediction/RiskBadge.vue';

const { t } = useI18n();

defineProps<{
  predictions: StudentPredictionResult[];
}>();

defineEmits<{
  (e: 'view-record', id: string): void;
}>();
</script>

<template>
  <div class="card flex flex-col overflow-hidden">
    <!-- Card Header -->
    <div class="flex items-center justify-between px-5 py-4 border-b dark:border-gray-800/60" style="border-bottom-color: #F1F5F9;">
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-table text-primary-500 text-xs"></i>
        <h4 class="text-sm font-bold text-gray-880 dark:text-gray-100 tracking-tight">
          {{ t('dashboard.recentPredictionsTable') || 'Recent Student Predictions' }}
        </h4>
      </div>
      <router-link
        to="/prediction-history"
        class="flex items-center space-x-1 text-[11px] font-bold text-primary-600 hover:text-primary-700
               dark:text-primary-400 dark:hover:text-primary-300 no-underline
               transition-colors duration-150"
      >
        <span>{{ t('general.viewAll') || 'View All' }}</span>
        <i class="fa-solid fa-arrow-right text-[10px]"></i>
      </router-link>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <!-- Head -->
        <thead>
          <tr class="bg-gray-50/60 dark:bg-gray-800/30 border-b dark:border-gray-800" style="border-bottom-color: #F1F5F9;">
            <th class="py-3 px-5 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest whitespace-nowrap">
              {{ t('singlePrediction.fields.studentCode') || 'Student Code' }}
            </th>
            <th class="py-3 px-5 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">
              {{ t('singlePrediction.fields.studentName') || 'Name' }}
            </th>
            <th class="py-3 px-5 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">
              {{ t('result.outcomeLabel') || 'Prediction' }}
            </th>
            <th class="py-3 px-5 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">
              {{ t('result.probabilityLabel') || 'Probability' }}
            </th>
            <th class="py-3 px-5 text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">
              {{ t('history.columns.dateTime') || 'Date' }}
            </th>
            <th class="py-3 px-5 text-right text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">
              {{ t('history.columns.actions') || 'Actions' }}
            </th>
          </tr>
        </thead>

        <!-- Body -->
        <tbody class="divide-y divide-slate-100 dark:divide-gray-800/60">
          <!-- Empty state row -->
          <tr v-if="predictions.length === 0">
            <td colspan="6" class="py-12 text-center">
              <div class="flex flex-col items-center space-y-2">
                <i class="fa-solid fa-inbox text-2xl text-gray-300 dark:text-gray-600"></i>
                <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">
                  {{ t('dashboard.noPredictions') || 'No recent predictions available.' }}
                </span>
              </div>
            </td>
          </tr>

          <!-- Data rows -->
          <tr
            v-for="student in predictions"
            :key="student.id"
            class="group text-xs font-semibold text-gray-700 dark:text-gray-300
                   hover:bg-primary-50/20 dark:hover:bg-primary-950/10
                   transition-colors duration-150"
          >
            <td class="py-3.5 px-5 font-bold text-gray-900 dark:text-white tracking-tight">
              {{ student.studentCode }}
            </td>
            <td class="py-3.5 px-5">
              {{ student.studentName }}
            </td>
            <td class="py-3.5 px-5">
              <RiskBadge :outcome="student.prediction" />
            </td>
            <td class="py-3.5 px-5 tabular-nums text-gray-600 dark:text-gray-400">
              {{ formatPercent(student.probability) }}
            </td>
            <td class="py-3.5 px-5 text-gray-400 dark:text-gray-500 font-medium whitespace-nowrap">
              {{ formatDate(student.date) }}
            </td>
            <td class="py-3.5 px-5 text-right">
              <button
                @click="$emit('view-record', student.id)"
                class="inline-flex items-center space-x-1.5 py-1.5 px-3 rounded-lg
                       bg-transparent border dark:border-gray-700
                       hover:bg-primary-50 hover:border-primary-300 hover:text-primary-600
                       dark:hover:bg-primary-950/20 dark:hover:border-primary-700 dark:hover:text-primary-400
                       text-gray-500 dark:text-gray-400 text-[11px] font-bold
                       cursor-pointer transition-all duration-150"
                style="border-color: #E7EDF4;"
              >
                <i class="fa-solid fa-eye text-[10px]"></i>
                <span>{{ t('general.viewDetails') || 'View' }}</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

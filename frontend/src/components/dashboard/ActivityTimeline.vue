<script setup lang="ts">
import type { ActivityTimelineEvent } from '../../types/dashboard';
import { formatRelativeTime } from '../../utils/date';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

defineProps<{
  events: ActivityTimelineEvent[];
}>();

const formatEventMessage = (event: any) => {
  if (!event || !event.message) return '';
  const msg = event.message;

  // Try matching single predictions: "Single prediction completed for [Name]: [Prediction] ([Prob]% probability, [Risk] Risk)"
  const singleMatch = msg.match(/Single prediction completed for\s+(.+?):\s+(\w+)\s+\((\d+)%\s+probability(?:,\s+(\w+)\s+Risk)?\)/i);
  if (singleMatch) {
    const [, name, prediction, prob, risk] = singleMatch;
    const tPrediction = t(`outcomes.${prediction}`) || prediction;
    const tRisk = risk ? (t(`risk.${risk}`) || risk) : '';
    return t('dashboard.activity.singleMsg', {
      name,
      outcome: tPrediction,
      prob,
      risk: tRisk
    });
  }

  return msg;
};
</script>

<template>
  <div class="card flex flex-col overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between px-5 py-4 border-b dark:border-gray-800/60" style="border-bottom-color: #F1F5F9;">
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-bell text-primary-500 text-xs"></i>
        <h4 class="text-sm font-bold text-gray-880 dark:text-gray-100 tracking-tight">
          {{ t('dashboard.activityFeed') }}
        </h4>
      </div>
      <span class="text-[9px] font-extrabold text-gray-300 dark:text-gray-600 uppercase tracking-widest leading-none">
        Live
      </span>
    </div>

    <!-- Content -->
    <div class="px-5 py-4">
      <div v-if="events.length === 0" class="py-8 text-center">
        <i class="fa-solid fa-clock-rotate-left text-2xl text-gray-300 dark:text-gray-600 mb-2 block animate-pulse"></i>
        <span class="text-xs font-semibold text-gray-400 dark:text-gray-500">
          {{ t('dashboard.noActivity') }}
        </span>
      </div>

      <div v-else class="relative pl-5 border-l-2 border-gray-150 dark:border-gray-800 space-y-5 ml-1.5">
        <div
          v-for="event in events"
          :key="event.id"
          class="relative text-xs group"
        >
          <!-- Dot on the timeline rail -->
          <span
            class="absolute -left-[22px] top-1 w-2.5 h-2.5 rounded-full border-2 bg-white dark:bg-gray-900
                   transition-colors duration-200 flex-shrink-0"
            :class="[
              event.riskLevel === 'High'   ? 'border-red-400 shadow-[0_0_0_3px_rgba(239,68,68,0.12)]' :
              event.riskLevel === 'Medium' ? 'border-amber-400 shadow-[0_0_0_3px_rgba(245,158,11,0.12)]' :
              event.riskLevel === 'Low'    ? 'border-emerald-400 shadow-[0_0_0_3px_rgba(16,185,129,0.12)]' :
              'border-primary-400 shadow-[0_0_0_3px_rgba(59,130,246,0.12)]'
            ]"
          ></span>

          <!-- Content -->
          <div class="flex flex-col space-y-1 pl-1">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold text-gray-700 dark:text-gray-200">
                {{ t('general.singleEval') }}
              </span>
              <time class="text-[10px] text-gray-400 dark:text-gray-500 font-semibold ml-3 whitespace-nowrap">
                {{ formatRelativeTime(event.timestamp) }}
              </time>
            </div>

            <p class="text-[11px] text-gray-500 dark:text-gray-400 font-medium leading-relaxed">
              {{ formatEventMessage(event) }}
            </p>

            <!-- Mini badges: studentCode + prediction -->
            <div
              v-if="event.studentCode && event.prediction"
              class="flex items-center flex-wrap gap-1.5 pt-0.5"
            >
              <span class="px-1.5 py-0.5 rounded-md text-[10px] font-bold bg-gray-100 dark:bg-gray-800
                           text-gray-500 dark:text-gray-400 border border-gray-150 dark:border-gray-700">
                {{ event.studentCode }}
              </span>
              <span
                class="px-1.5 py-0.5 rounded-md text-[10px] font-bold"
                :class="[
                  event.prediction === 'Graduate' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/20 dark:text-emerald-400' :
                  event.prediction === 'Dropout'  ? 'bg-red-50 text-red-700 dark:bg-red-950/20 dark:text-red-400' :
                  'bg-amber-50 text-amber-700 dark:bg-amber-950/20 dark:text-amber-400'
                ]"
              >
                {{ t('outcomes.' + event.prediction) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

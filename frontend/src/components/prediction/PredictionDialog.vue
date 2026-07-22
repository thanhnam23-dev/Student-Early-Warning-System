<script setup lang="ts">
import Dialog from 'primevue/dialog';
import type { StudentPredictionInput } from '../../types/student';
import type { StudentPredictionResult } from '../../types/prediction';
import { formatPercent } from '../../utils/formatter';
import RiskBadge from './RiskBadge.vue';
import RecommendationCard from './RecommendationCard.vue';
import InputSummaryCard from './InputSummaryCard.vue';
import ShapCard from './ShapCard.vue';
import { RISK_COLORS, OUTCOME_COLORS } from '../../constants/colors';
import { computed } from 'vue';

const props = defineProps<{
  visible: boolean;
  result: StudentPredictionResult | null;
  studentInput: StudentPredictionInput | null;
}>();

defineEmits<{
  (e: 'update:visible', value: boolean): void;
}>();

const headerTheme = computed(() => {
  if (!props.result) return null;
  const pred = props.result.prediction;
  if (pred === 'Dropout') {
    return {
      border: 'border-red-200 dark:border-red-900',
      text: 'text-red-650 dark:text-red-400',
      bgGradient: 'from-red-500/10 via-transparent to-transparent'
    };
  } else if (pred === 'Enrolled') {
    return {
      border: 'border-amber-200 dark:border-amber-900',
      text: 'text-amber-650 dark:text-amber-400',
      bgGradient: 'from-amber-500/10 via-transparent to-transparent'
    };
  } else {
    return {
      border: 'border-green-200 dark:border-green-900',
      text: 'text-green-650 dark:text-green-400',
      bgGradient: 'from-green-500/10 via-transparent to-transparent'
    };
  }
});
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="$emit('update:visible', $event)"
    modal
    dismissableMask
    :style="{ width: '90vw', maxWidth: '640px' }"
    class="prediction-result-dialog"
    aria-labelledby="prediction-header"
  >
    <!-- Custom Header Wrapper -->
    <template #header>
      <div v-if="result" class="flex items-center space-x-2.5">
        <div class="w-9 h-9 rounded-xl bg-primary-50 dark:bg-primary-950/40 flex items-center justify-center text-primary-600 dark:text-primary-400">
          <i class="fa-solid fa-brain text-base animate-pulse"></i>
        </div>
        <div>
          <h3 id="prediction-header" class="text-sm font-bold text-gray-900 dark:text-white leading-none">
            {{ $t('singlePrediction.predictionComplete') }}
          </h3>
          <span class="text-[10px] text-gray-400 font-semibold">ID: {{ result.id }}</span>
        </div>
      </div>
    </template>

    <div v-if="result" class="space-y-6 pt-1">
      <!-- Main Status Card -->
      <div 
        class="border rounded-2xl p-5 bg-gradient-to-tr transition-all duration-200 flex flex-col sm:flex-row items-center justify-between gap-6"
        :class="[headerTheme?.border, headerTheme?.bgGradient]"
      >
        <div class="space-y-2.5 text-center sm:text-left">
          <div class="space-y-1">
            <span class="text-[10px] font-bold text-gray-455 dark:text-gray-500 uppercase tracking-widest block">{{ $t('result.outcomeLabel') }}</span>
            <h4 class="text-2xl font-black tracking-tight" :class="[headerTheme?.text]">
              {{ $t('outcomes.' + result.prediction) }}
            </h4>
          </div>
          
          <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2.5">
            <span class="text-xs font-semibold text-gray-500 dark:text-gray-400">{{ $t('result.riskLabel') }}:</span>
            <RiskBadge :outcome="result.riskLevel" />
          </div>
        </div>

        <!-- Radial Gauge Probability Placeholder -->
        <div class="relative w-24 h-24 flex items-center justify-center shrink-0">
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <!-- Background circle -->
            <circle 
              cx="50" cy="50" r="40" 
              class="stroke-gray-100 dark:stroke-gray-800 fill-none" 
              stroke-width="8" 
            />
            <!-- Active circle -->
            <circle 
              cx="50" cy="50" r="40" 
              class="fill-none transition-all duration-500" 
              :class="[
                result.prediction === 'Graduate' ? 'stroke-green-500' :
                result.prediction === 'Dropout' ? 'stroke-red-500' : 'stroke-amber-500'
              ]"
              stroke-width="8" 
              :stroke-dasharray="251.2"
              :stroke-dashoffset="251.2 - (251.2 * result.probability)"
              stroke-linecap="round"
            />
          </svg>
          <div class="absolute flex flex-col items-center justify-center">
            <span class="text-lg font-black text-gray-900 dark:text-white leading-none">
              {{ formatPercent(result.probability) }}
            </span>
            <span class="text-[9px] text-gray-400 font-bold uppercase tracking-wider mt-0.5">{{ $t('result.probShort') }}</span>
          </div>
        </div>
      </div>

      <!-- Recommendation Card -->
      <RecommendationCard 
        :recommendations="result.recommendations" 
        :prediction="result.prediction" 
      />

      <!-- AI Explainability (SHAP) -->
      <ShapCard :shap-values="result.shapValues" />

      <!-- Input Summary Collapse Accordion -->
      <div v-if="studentInput" class="space-y-2">
        <h5 class="text-xs font-bold text-gray-400 uppercase tracking-wider">
          {{ $t('result.academicIdentity') }}
        </h5>
        <InputSummaryCard :student-data="studentInput" />
      </div>
    </div>
  </Dialog>
</template>

<style>
/* Remove standard padding headers to match custom styles */
.prediction-result-dialog .p-dialog-header {
  border-bottom: 1px solid var(--p-dialog-border-color, #e2e8f0);
  padding: 1rem 1.5rem !important;
}
.prediction-result-dialog .p-dialog-content {
  padding: 1.5rem !important;
}
</style>

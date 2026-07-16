<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useHistoryStore } from '../../stores/history.store';
import PageHeader from '../../components/common/PageHeader.vue';
import RiskBadge from '../../components/prediction/RiskBadge.vue';
import RecommendationCard from '../../components/prediction/RecommendationCard.vue';
import InputSummaryCard from '../../components/prediction/InputSummaryCard.vue';
import { formatPercent } from '../../utils/formatter';
import { formatDate } from '../../utils/date';
import type { StudentPredictionInput } from '../../types/student';
import Skeleton from 'primevue/skeleton';
import EmptyState from '../../components/common/EmptyState.vue';

const props = defineProps<{
  id: string;
}>();

const router = useRouter();
const historyStore = useHistoryStore();

onMounted(async () => {
  await historyStore.fetchRecordById(props.id);
});

const record = computed(() => historyStore.activeRecord);
const loading = computed(() => historyStore.loading);

// Reconstruct fake student input properties for the summary card since the history mock detail only stores outcomes and display info
const studentInputMockData = computed<StudentPredictionInput | null>(() => {
  if (!record.value) return null;
  // Reconstruct standard values to display in summary card
  return {
    studentCode: record.value.studentCode,
    studentName: record.value.studentName,
    className: record.value.className,
    faculty: record.value.faculty,
    maritalStatus: 1,
    ageAtEnrollment: 20,
    gender: 1,
    nationality: 1,
    international: 0,
    applicationMode: 1,
    applicationOrder: 1,
    course: 9119,
    daytimeEvening: 1,
    previousQualification: 1,
    previousQualificationGrade: 135.5,
    admissionGrade: 140.0,
    motherQualification: 1,
    fatherQualification: 1,
    motherOccupation: 8,
    fatherOccupation: 9,
    scholarshipHolder: 1,
    debtor: 0,
    tuitionFeesUpToDate: 1,
    displaced: 1,
    educationalSpecialNeeds: 0,
    sem1Credited: 0,
    sem1Enrolled: 6,
    sem1Evaluations: 6,
    sem1Approved: 6,
    sem1Grade: 14.5,
    sem1WithoutEvaluations: 0,
    sem2Credited: 0,
    sem2Enrolled: 6,
    sem2Evaluations: 6,
    sem2Approved: 6,
    sem2Grade: 14.2,
    sem2WithoutEvaluations: 0,
    unemploymentRate: 9.4,
    inflationRate: 1.4,
    gdp: 2.5
  };
});

const handlePrint = () => {
  window.print();
};
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <PageHeader 
      :title="$t('result.title')" 
      :description="record ? ($t('result.reportTitle') + ' - ' + formatDate(record.date)) : $t('general.loading')"
    >
      <template #actions>
        <button 
          @click="router.back()"
          class="py-2 px-4 border border-gray-200 dark:border-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-750 text-gray-700 dark:text-gray-300 rounded-xl text-xs font-semibold cursor-pointer transition-all duration-200"
        >
          <i class="fa-solid fa-chevron-left mr-1.5"></i> {{ $t('result.back') }}
        </button>
        <button 
          @click="handlePrint"
          class="py-2 px-4 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-xs font-semibold cursor-pointer transition-all duration-200 shadow-md shadow-primary-500/20"
        >
          <i class="fa-solid fa-print mr-1.5"></i> {{ $t('result.print') }}
        </button>
      </template>
    </PageHeader>

    <!-- Skeleton Loader -->
    <div v-if="loading" class="max-w-4xl mx-auto space-y-6">
      <div class="card p-6 space-y-4">
        <Skeleton width="30%" height="1rem" />
        <Skeleton width="60%" height="2rem" />
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <Skeleton height="3rem" v-for="i in 3" :key="i" />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="card p-5 space-y-4" v-for="i in 2" :key="i">
          <Skeleton width="40%" height="1.25rem" />
          <Skeleton height="2rem" v-for="j in 4" :key="j" />
        </div>
      </div>
    </div>

    <!-- Elegant Empty State -->
    <div v-else-if="!record" class="py-12">
      <EmptyState
        icon="fa-solid fa-triangle-exclamation"
        :title="$t('result.noResult')"
        :description="$t('result.noResultDesc')"
        :actionLabel="$t('sidebar.history')"
        actionIcon="fa-solid fa-clock-rotate-left"
        @action="router.push('/prediction-history')"
      />
    </div>

    <!-- Core Report Layout -->
    <div v-else class="max-w-4xl mx-auto space-y-6 print-container">
      <!-- 1. Headline box -->
      <div 
        class="bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 transition-colors duration-200"
        :class="[
          record.prediction === 'Graduate' ? 'border-l-4 border-l-green-500' :
          record.prediction === 'Dropout' ? 'border-l-4 border-l-red-500' :
          'border-l-4 border-l-amber-500'
        ]"
      >
        <div class="space-y-3">
          <div>
            <span class="text-[9px] font-bold text-gray-400 uppercase tracking-widest block mb-0.5">{{ $t('result.studentProfile') }}</span>
            <h3 class="text-xl font-black text-gray-900 dark:text-white leading-tight">
              {{ record.studentName }}
            </h3>
            <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs font-bold text-gray-500 dark:text-gray-400 mt-1">
              <span>{{ $t('singlePrediction.fields.studentCode') }}: {{ record.studentCode }}</span>
              <span>•</span>
              <span>{{ $t('singlePrediction.fields.className') }}: {{ record.className }}</span>
              <span>•</span>
              <span>{{ record.faculty }}</span>
            </div>
          </div>
          
          <div class="flex items-center space-x-2 pt-1.5">
            <span class="text-xs font-semibold text-gray-400">{{ $t('result.outcomeLabel') }}:</span>
            <RiskBadge :outcome="record.prediction" />
          </div>
        </div>

        <div class="flex items-center space-x-6 shrink-0 md:border-l md:border-gray-105 dark:md:border-gray-805 md:pl-6">
          <div class="text-center">
            <span class="block text-[9px] text-gray-400 font-bold uppercase tracking-wider mb-1">{{ $t('result.probabilityLabel') }}</span>
            <span class="text-2xl font-black text-gray-900 dark:text-white leading-none">
              {{ formatPercent(record.probability) }}
            </span>
          </div>
          
          <div class="text-center">
            <span class="block text-[9px] text-gray-400 font-bold uppercase tracking-wider mb-1">{{ $t('result.confidenceLabel') }}</span>
            <span class="text-2xl font-black text-gray-900 dark:text-white leading-none">
              {{ formatPercent(record.confidence) }}
            </span>
          </div>

          <div class="text-center">
            <span class="block text-[9px] text-gray-400 font-bold uppercase tracking-wider mb-1">{{ $t('result.riskLabel') }}</span>
            <span 
              class="text-xs font-bold block mt-1"
              :class="[
                record.riskLevel === 'High' ? 'text-red-500' :
                record.riskLevel === 'Medium' ? 'text-amber-500' : 'text-green-500'
              ]"
            >
              {{ $t('risk.' + record.riskLevel) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 2. Recommendations card -->
      <RecommendationCard 
        :recommendations="record.recommendations" 
        :prediction="record.prediction" 
      />

      <!-- 3. Collapsible summary card -->
      <div v-if="studentInputMockData" class="space-y-2">
        <h5 class="text-xs font-bold text-gray-400 uppercase tracking-wider">
          {{ $t('result.academicIdentity') }}
        </h5>
        <InputSummaryCard :student-data="studentInputMockData" />
      </div>
    </div>
  </div>
</template>

<style media="print">
@media print {
  body {
    background: white !important;
    color: black !important;
  }
  aside, header, footer, button, a {
    display: none !important;
  }
  main {
    padding: 0 !important;
    margin: 0 !important;
  }
  .print-container {
    max-width: 100% !important;
    box-shadow: none !important;
    border: none !important;
  }
}
</style>

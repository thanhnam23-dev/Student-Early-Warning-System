<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useHistoryStore } from '../../stores/history.store';
import PageHeader from '../../components/common/PageHeader.vue';
import EmptyState from '../../components/common/EmptyState.vue';
import { formatDateTime } from '../../utils/date';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import { useI18n } from 'vue-i18n';
import Skeleton from 'primevue/skeleton';

const { t } = useI18n();
const router = useRouter();
const historyStore = useHistoryStore();

onMounted(async () => {
  await historyStore.fetchHistory();
});

const historyList = computed(() => historyStore.filteredHistory);
const loading = computed(() => historyStore.loading);
const filters = computed(() => historyStore.filters);

const translateResultSummary = (summary: string) => {
  if (!summary) return '';
  
  // Try matching single predictions: "1 [Prediction] ([Risk] Risk)"
  const singleMatch = summary.match(/^1\s+(\w+)\s+\((\w+)\s+Risk\)$/i);
  if (singleMatch) {
    const [, prediction, risk] = singleMatch;
    const tPrediction = t(`outcomes.${prediction}`) || prediction;
    const tRisk = t(`risk.${risk}`) || risk;
    return `1 ${tPrediction} (${tRisk})`;
  }
  return summary;
};

const handleViewReport = (id: string) => {
  router.push({ name: 'prediction-result', params: { id } });
};

const handleActionClick = (session: any) => {
  if (session.details && session.details[0]) {
    handleViewReport(session.details[0].id);
  }
};

const outcomeOptions = computed(() => [
  { label: t('history.filters.allOutcomes'), value: 'all' },
  { label: t('outcomes.Graduate'), value: 'Graduate' },
  { label: t('outcomes.Dropout'), value: 'Dropout' },
  { label: t('outcomes.Enrolled'), value: 'Enrolled' }
]);

const riskOptions = computed(() => [
  { label: t('history.filters.allRisks'), value: 'all' },
  { label: t('risk.Low'), value: 'Low' },
  { label: t('risk.Medium'), value: 'Medium' },
  { label: t('risk.High'), value: 'High' }
]);

const resetFilters = () => {
  historyStore.resetFilters();
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader 
      :title="t('history.title')" 
      :description="t('history.description')"
    />

    <!-- Filters Panel Card -->
    <div class="bg-white dark:bg-gray-900 border border-gray-150/80 dark:border-gray-800/70 rounded-2xl p-5 md:p-6 shadow-[var(--shadow-card)] transition-colors duration-200">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <!-- Text Search -->
        <div class="flex flex-col space-y-1.5">
          <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{{ t('history.filters.searchLabel') }}</label>
          <div class="relative w-full">
            <i class="fa-solid fa-magnifying-glass absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-gray-400 pointer-events-none"></i>
            <InputText 
              v-model="filters.search" 
              :placeholder="t('history.filters.searchPlaceholder')" 
              class="w-full text-xs font-semibold py-2 pl-3 pr-9 rounded-lg border border-gray-250 dark:border-gray-700 bg-transparent dark:text-white"
            />
          </div>
        </div>

        <!-- Outcome -->
        <div class="flex flex-col space-y-1.5">
          <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{{ t('history.filters.outcomeLabel') }}</label>
          <Dropdown 
            v-model="filters.prediction" 
            :options="outcomeOptions" 
            optionLabel="label" 
            optionValue="value" 
            class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent"
          />
        </div>

        <!-- Risk Level -->
        <div class="flex flex-col space-y-1.5">
          <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{{ t('history.filters.riskLabel') }}</label>
          <Dropdown 
            v-model="filters.riskLevel" 
            :options="riskOptions" 
            optionLabel="label" 
            optionValue="value" 
            class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent"
          />
        </div>
      </div>

      <div class="flex items-center justify-end mt-4 pt-3 border-t border-gray-100 dark:border-gray-800">
        <button 
          @click="resetFilters"
          class="py-1.5 px-4 bg-gray-50 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-lg text-xs font-bold border border-gray-200 dark:border-gray-700 cursor-pointer transition-colors"
        >
          {{ t('general.resetFilters') }}
        </button>
      </div>
    </div>

    <!-- History Log Table -->
    <!-- Skeleton Table Loader -->
    <div v-if="loading && historyList.length === 0" class="card p-5 space-y-4">
      <div class="flex justify-between items-center pb-3 border-b border-gray-150 dark:border-gray-800">
        <Skeleton width="20%" height="1.25rem" />
        <Skeleton width="30%" height="2.25rem" borderRadius="8px" />
      </div>
      <div class="space-y-3 pt-2">
        <Skeleton height="2.5rem" />
        <Skeleton height="2rem" v-for="i in 6" :key="i" />
      </div>
    </div>

    <div v-else class="bg-white dark:bg-gray-900 border border-gray-150/80 dark:border-gray-800/70 rounded-2xl shadow-[var(--shadow-card)] overflow-hidden transition-colors duration-200">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs font-semibold">
          <thead>
            <tr class="border-b border-gray-100 dark:border-gray-800 text-[10px] font-bold text-gray-400 dark:text-gray-550 uppercase tracking-widest bg-gray-50/80 dark:bg-gray-800/30">
              <th class="py-3.5 px-5">{{ t('history.columns.sessionId') }}</th>
              <th class="py-3.5 px-5">{{ t('history.columns.dateTime') }}</th>
              <th class="py-3.5 px-5">{{ t('history.columns.type') }}</th>
              <th class="py-3.5 px-5">{{ t('history.columns.studentsCount') }}</th>
              <th class="py-3.5 px-5">{{ t('history.columns.summary') }}</th>
              <th class="py-3.5 px-5 text-right">{{ t('history.columns.actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50 dark:divide-gray-800">
            <tr v-if="historyList.length === 0">
              <td colspan="6" class="py-12">
                <EmptyState 
                  icon="pi-history"
                  :title="t('history.empty') || 'No History Logged'" 
                  :description="t('history.emptyDesc') || 'You have not run any AI models or predictions yet.'"
                  :actionLabel="t('sidebar.singlePrediction') || 'New Prediction'"
                  actionIcon="fa-solid fa-plus"
                  @action="router.push('/single-prediction')"
                />
              </td>
            </tr>

            <template v-for="(session, idx) in historyList" :key="session.id">
              <!-- Session Header Row -->
              <tr 
                class="hover:bg-primary-50/20 dark:hover:bg-primary-950/10 text-gray-700 dark:text-gray-300 transition-colors duration-150 animate-card-enter"
                :class="'stagger-' + ((idx % 6) + 1)"
              >
                <td class="py-3.5 px-5 text-gray-900 dark:text-white font-extrabold">{{ session.id }}</td>
                <td class="py-3.5 px-5 text-gray-500 dark:text-gray-400 font-medium">{{ formatDateTime(session.date) }}</td>
                <td class="py-3.5 px-5">
                  <span 
                    class="px-2 py-0.5 rounded text-[10px] font-bold border bg-primary-50 text-primary-600 border-primary-100 dark:bg-primary-950/20 dark:text-primary-400 dark:border-primary-900"
                  >
                    {{ t('history.filters.single') }}
                  </span>
                </td>
                <td class="py-3.5 px-5 font-bold">{{ session.studentCount }}</td>
                <td class="py-3.5 px-5 font-medium">{{ translateResultSummary(session.resultSummary) }}</td>
                <td class="py-3.5 px-5 text-right">
                  <button 
                    @click="handleActionClick(session)"
                    class="inline-flex items-center space-x-1 py-1.5 px-3 rounded-lg
                           bg-transparent border border-gray-200 dark:border-gray-700
                           hover:bg-primary-50 hover:border-primary-300 hover:text-primary-600
                           dark:hover:bg-primary-950/20 dark:hover:border-primary-700 dark:hover:text-primary-400
                           text-gray-500 dark:text-gray-400 text-[11px] font-bold
                           cursor-pointer transition-all duration-150"
                  >
                    <i class="fa-solid fa-eye text-[10px]"></i>
                    <span>{{ t('general.viewDetails') }}</span>
                  </button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

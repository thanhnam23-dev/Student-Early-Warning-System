<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useDashboardStore } from '../../stores/dashboard.store';
import PageHeader from '../../components/common/PageHeader.vue';
import StatCard from '../../components/dashboard/StatCard.vue';
import PredictionChart from '../../components/dashboard/PredictionChart.vue';
import ActivityTimeline from '../../components/dashboard/ActivityTimeline.vue';
import RecentPredictionTable from '../../components/dashboard/RecentPredictionTable.vue';
import RiskBadge from '../../components/prediction/RiskBadge.vue';
import Button from 'primevue/button';
import { formatPercent } from '../../utils/formatter';
import { formatDate } from '../../utils/date';
import { useI18n } from 'vue-i18n';
import Skeleton from 'primevue/skeleton';

const { t } = useI18n();
const router = useRouter();
const dashboardStore = useDashboardStore();

onMounted(async () => {
  await dashboardStore.fetchDashboardData();
});

const data = computed(() => dashboardStore.dashboardData);
const loading = computed(() => dashboardStore.loading);

const handleViewRecord = (id: string) => {
  router.push({ name: 'prediction-result', params: { id } });
};
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <PageHeader
      :title="$t('dashboard.title')"
      :description="$t('dashboard.description')"
    >
      <template #actions>
        <router-link to="/single-prediction">
          <Button
            :label="$t('sidebar.singlePrediction')"
            icon="fa-solid fa-plus"
            class="text-xs font-bold px-4 bg-primary-600 hover:bg-primary-700 text-white rounded-xl
                   cursor-pointer shadow-md shadow-primary-500/20"
          />
        </router-link>
      </template>
    </PageHeader>

    <!-- Skeleton Loading State -->
    <div v-if="loading && !data" class="space-y-6">
      <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-4">
        <div class="card p-5 space-y-4" v-for="i in 6" :key="i">
          <div class="flex justify-between items-center">
            <Skeleton width="45%" height="10px" />
            <Skeleton size="1.75rem" borderRadius="8px" />
          </div>
          <Skeleton width="60%" height="2rem" />
          <Skeleton width="80%" height="12px" />
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-5">
        <div class="lg:col-span-2 card p-5 space-y-4 min-h-[320px] flex flex-col justify-between">
          <div class="flex justify-between items-center pb-3 border-b border-gray-150 dark:border-gray-800">
            <Skeleton width="60%" height="1rem" />
            <Skeleton size="1.75rem" borderRadius="8px" />
          </div>
          <div class="flex-1 flex items-center justify-center min-h-[220px]">
            <Skeleton shape="circle" size="140px" />
          </div>
        </div>
        <div class="lg:col-span-3 card p-5 space-y-4 min-h-[320px] flex flex-col justify-between">
          <div class="flex justify-between items-center pb-3 border-b border-gray-150 dark:border-gray-800">
            <Skeleton width="40%" height="1rem" />
            <Skeleton size="1.75rem" borderRadius="8px" />
          </div>
          <div class="flex-1 flex flex-col justify-end space-y-2 min-h-[220px] pt-4">
            <div class="flex items-end justify-between space-x-4 h-full">
              <Skeleton width="12%" height="40%" />
              <Skeleton width="12%" height="70%" />
              <Skeleton width="12%" height="50%" />
              <Skeleton width="12%" height="90%" />
              <Skeleton width="12%" height="30%" />
              <Skeleton width="12%" height="80%" />
            </div>
            <div class="flex justify-between text-[10px] text-gray-400 pt-2 border-t border-gray-100 dark:border-gray-800">
              <Skeleton width="10%" height="8px" />
              <Skeleton width="10%" height="8px" />
              <Skeleton width="10%" height="8px" />
              <Skeleton width="10%" height="8px" />
              <Skeleton width="10%" height="8px" />
              <Skeleton width="10%" height="8px" />
            </div>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-1 xl:grid-cols-5 gap-5">
        <div class="xl:col-span-2 card p-5 space-y-4">
          <Skeleton width="30%" height="1rem" />
          <div class="space-y-4 pt-2">
            <div class="flex space-x-3" v-for="i in 3" :key="i">
              <Skeleton size="1.5rem" shape="circle" />
              <div class="flex-1 space-y-1.5">
                <Skeleton width="40%" height="10px" />
                <Skeleton width="80%" height="12px" />
              </div>
            </div>
          </div>
        </div>
        <div class="xl:col-span-3 card p-5 space-y-4">
          <Skeleton width="40%" height="1rem" />
          <div class="space-y-4 pt-2">
            <Skeleton height="1.5rem" v-for="i in 4" :key="i" />
          </div>
        </div>
      </div>
    </div>

    <template v-else-if="data">
      <!-- ── 1. KPI Cards ─────────────────────────────────────────────── -->
      <section>
        <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 px-0.5">
          {{ t('dashboard.statsSection') || 'Overview Statistics' }}
        </p>
        <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-4">
          <StatCard
            class="animate-card-enter stagger-1"
            :title="$t('dashboard.totalPredictions')"
            :value="data.stats.totalPredictions"
            icon="fa-solid fa-chart-line"
            colorClass="blue"
            shape="circle"
            :trend="{ value: 8, direction: 'up', label: t('dashboard.vsLastMonth') || 'vs last month' }"
          />
          <StatCard
            class="animate-card-enter stagger-2"
            :title="$t('dashboard.graduates')"
            :value="data.stats.graduateCount"
            icon="fa-solid fa-circle-check"
            colorClass="green"
            shape="squircle"
            :trend="{ value: 4, direction: 'up', label: t('dashboard.vsLastMonth') || 'vs last month' }"
          />
          <StatCard
            class="animate-card-enter stagger-3"
            :title="$t('dashboard.dropouts')"
            :value="data.stats.dropoutCount"
            icon="fa-solid fa-triangle-exclamation"
            colorClass="red"
            shape="square"
            :trend="{ value: 2, direction: 'down', label: t('dashboard.vsLastMonth') || 'vs last month' }"
          />
          <StatCard
            class="animate-card-enter stagger-4"
            :title="$t('dashboard.enrolled')"
            :value="data.stats.enrolledCount"
            icon="fa-solid fa-graduation-cap"
            colorClass="amber"
            shape="squircle"
          />
          <StatCard
            class="animate-card-enter stagger-5"
            :title="$t('sidebar.singlePrediction')"
            :value="data.stats.singlePredictions"
            icon="fa-solid fa-user-graduate"
            colorClass="blue"
            shape="circle"
          />
        </div>
      </section>

      <!-- ── 2. Charts ────────────────────────────────────────────────── -->
      <section>
        <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 px-0.5">
          {{ t('dashboard.analyticsSection') || 'Analytics' }}
        </p>
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-5">
          <div class="lg:col-span-2 min-h-[320px] animate-card-enter stagger-4">
            <PredictionChart
              type="pie"
              :data="data.distribution"
              :title="$t('dashboard.activeDistribution')"
            />
          </div>
          <div class="lg:col-span-3 min-h-[320px] animate-card-enter stagger-5">
            <PredictionChart
              type="bar"
              :data="data.history"
              :title="$t('dashboard.recentPredictions')"
              :subtitle="t('dashboard.last6Months') || 'Last 6 months'"
            />
          </div>
        </div>
      </section>

      <!-- ── 3. Latest Predictions Summary ──────────────────────────── -->
      <section>
        <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 px-0.5">
          {{ t('dashboard.latestSection') || 'Latest Predictions' }}
        </p>
        <div class="max-w-2xl">
          <!-- Latest Single -->
          <div class="card overflow-hidden animate-card-enter stagger-6">
            <div class="flex items-center space-x-2 px-5 py-4 border-b border-gray-100 dark:border-gray-800/60">
              <i class="fa-solid fa-user-graduate text-primary-500 text-xs"></i>
              <h4 class="text-sm font-bold text-gray-800 dark:text-gray-100 tracking-tight">
                {{ $t('dashboard.latestSingle') }}
              </h4>
            </div>
            <div class="p-5">
              <div v-if="data.latestSingle" class="space-y-4">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0">
                    <h5 class="text-sm font-black text-gray-900 dark:text-white leading-tight truncate">
                      {{ data.latestSingle.studentName }}
                    </h5>
                    <span class="text-[10px] text-gray-400 font-bold block mt-0.5">
                      {{ $t('singlePrediction.fields.studentCode') }}: {{ data.latestSingle.studentCode }}
                    </span>
                  </div>
                  <RiskBadge :outcome="data.latestSingle.prediction" />
                </div>

                <div class="grid grid-cols-3 gap-2 p-3 bg-gray-50 dark:bg-gray-800/40 rounded-xl
                            border border-gray-150 dark:border-gray-800 text-center">
                  <div>
                    <span class="block text-[9px] text-gray-400 uppercase font-bold tracking-wider mb-0.5">
                      {{ $t('singlePrediction.fields.className') }}
                    </span>
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">
                      {{ data.latestSingle.className }}
                    </span>
                  </div>
                  <div>
                    <span class="block text-[9px] text-gray-400 uppercase font-bold tracking-wider mb-0.5">
                      {{ $t('result.probabilityLabel') }}
                    </span>
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200 tabular-nums">
                      {{ formatPercent(data.latestSingle.probability) }}
                    </span>
                  </div>
                  <div>
                    <span class="block text-[9px] text-gray-400 uppercase font-bold tracking-wider mb-0.5">
                      {{ $t('result.riskLabel') }}
                    </span>
                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">
                      {{ $t(`risk.${data.latestSingle.riskLevel}`) }}
                    </span>
                  </div>
                </div>

                <button
                  @click="handleViewRecord(data.latestSingle.id)"
                  class="w-full py-2 rounded-xl text-xs font-bold cursor-pointer transition-all duration-200
                         bg-primary-50 hover:bg-primary-100 text-primary-600
                         dark:bg-primary-950/20 dark:hover:bg-primary-900/30 dark:text-primary-400
                         border border-primary-100 dark:border-primary-900"
                >
                  {{ $t('dashboard.reviewReport') }}
                </button>
              </div>
              <div v-else class="py-10 text-center">
                <i class="fa-solid fa-inbox text-2xl text-gray-300 dark:text-gray-600 mb-2 block animate-pulse"></i>
                <span class="text-xs font-semibold text-gray-400">{{ $t('dashboard.noSingle') }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── 4. Activity Feed + Table ─────────────────────────────────── -->
      <section>
        <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 px-0.5">
          {{ t('dashboard.activitySection') || 'Activity & Records' }}
        </p>
        <div class="grid grid-cols-1 xl:grid-cols-5 gap-5">
          <div class="xl:col-span-2 animate-card-enter stagger-7">
            <ActivityTimeline :events="data.recentActivity" />
          </div>
          <div class="xl:col-span-3 animate-card-enter stagger-7">
            <RecentPredictionTable
              :predictions="data.recentPredictions"
              @view-record="handleViewRecord"
            />
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

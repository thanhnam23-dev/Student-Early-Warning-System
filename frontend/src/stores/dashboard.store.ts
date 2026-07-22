import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { dashboardService } from '../api/dashboard.service';
import { useHistoryStore } from './history.store';
import type { DashboardData, DashboardStats, ChartDataPoint, ActivityTimelineEvent } from '../types/dashboard';
import type { StudentPredictionResult } from '../types/prediction';

export const useDashboardStore = defineStore('dashboard', () => {
  const baseDashboardData = ref<DashboardData | null>(null);
  const loading = ref(false);
  
  // Set of session IDs loaded initially to differentiate from newly simulated ones
  const initialSessionIds = ref<Set<string>>(new Set());

  const historyStore = useHistoryStore();

  const fetchDashboardData = async () => {
    loading.value = true;
    try {
      // 1. Fetch history first to populate history list
      if (historyStore.historyList.length === 0) {
        await historyStore.fetchHistory();
      }

      // Record initial session IDs
      if (initialSessionIds.value.size === 0) {
        historyStore.historyList.forEach((session) => {
          initialSessionIds.value.add(session.id);
        });
      }

      // 2. Fetch baseline dashboard aggregations
      const data = await dashboardService.getDashboardData();
      baseDashboardData.value = data;
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      loading.value = false;
    }
  };

  /**
   * Computed reactive dashboard values.
   * Merges baseline static data with newly added predictions in-memory.
   */
  const dashboardData = computed<DashboardData | null>(() => {
    if (!baseDashboardData.value) return null;

    // Deep clone the base data to avoid mutating refs directly
    const merged: DashboardData = JSON.parse(JSON.stringify(baseDashboardData.value));

    // Find any new sessions that were added since the app loaded
    const newSessions = historyStore.historyList.filter(
      (session) => !initialSessionIds.value.has(session.id)
    );

    if (newSessions.length === 0) {
      return merged; // No new predictions to merge
    }

    // Sort new sessions chronologically (oldest to newest) to apply cumulative calculations
    const orderedNewSessions = [...newSessions].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    // Dynamic stats trackers
    let newSingles = 0;
    let newGraduates = 0;
    let newDropouts = 0;
    let newEnrolled = 0;
    let newTotalPredictedCount = 0;

    const newPredictionsList: StudentPredictionResult[] = [];
    const newActivityEvents: ActivityTimelineEvent[] = [];

    orderedNewSessions.forEach((session) => {
      newTotalPredictedCount += session.studentCount;
      newPredictionsList.unshift(...session.details); // Newest first

      if (session.type === 'single') {
        newSingles += 1;
        const student = session.details[0] as StudentPredictionResult;
        
        if (student.prediction === 'Graduate') newGraduates += 1;
        else if (student.prediction === 'Dropout') newDropouts += 1;
        else if (student.prediction === 'Enrolled') newEnrolled += 1;

        // Add to activity timeline
        newActivityEvents.unshift({
          id: `ACT-${session.id}`,
          timestamp: session.date,
          type: 'single',
          message: `Single prediction run completed for student ${student.studentName}. Outcome: ${student.prediction} (${Math.round(student.probability * 100)}% probability, Risk: ${student.riskLevel}).`,
          studentName: student.studentName,
          studentCode: student.studentCode,
          prediction: student.prediction,
          riskLevel: student.riskLevel
        });

        // Set as latest single prediction
        merged.latestSingle = student || null;
      }
    });

    // 1. Merge core stats
    merged.stats.totalPredictions += newTotalPredictedCount;
    merged.stats.singlePredictions += newSingles;
    merged.stats.graduateCount += newGraduates;
    merged.stats.dropoutCount += newDropouts;
    merged.stats.enrolledCount += newEnrolled;

    // 2. Merge distribution list for Pie Chart
    merged.distribution = [
      { label: 'Graduate', value: merged.stats.graduateCount },
      { label: 'Dropout', value: merged.stats.dropoutCount },
      { label: 'Enrolled', value: merged.stats.enrolledCount }
    ];

    // 3. Merge history values for Bar Chart
    // Dynamically increment the value for the last bar chart item (representing the current month)
    if (merged.history && merged.history.length > 0) {
      const lastIndex = merged.history.length - 1;
      const lastItem = merged.history[lastIndex];
      if (lastItem) {
        lastItem.value += newTotalPredictedCount;
      }
    }

    // 4. Merge recent activity timeline (keep top 5)
    merged.recentActivity = [...newActivityEvents, ...merged.recentActivity].slice(0, 5);

    // 5. Merge recent predictions table (keep top 5)
    merged.recentPredictions = [...newPredictionsList, ...merged.recentPredictions].slice(0, 5);

    return merged;
  });

  return {
    baseDashboardData,
    loading,
    fetchDashboardData,
    dashboardData
  };
});

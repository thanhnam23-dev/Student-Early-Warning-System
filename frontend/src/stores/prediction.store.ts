import { defineStore } from 'pinia';
import { ref } from 'vue';
import { predictionService } from '../api/prediction.service';
import { useHistoryStore } from './history.store';
import { useDashboardStore } from './dashboard.store';
import type { StudentPredictionInput } from '../types/student';
import type { StudentPredictionResult } from '../types/prediction';
import type { PredictionHistoryItem } from '../types/history';

export const usePredictionStore = defineStore('prediction', () => {
  const loading = ref(false);
  const currentSingleResult = ref<StudentPredictionResult | null>(null);

  const historyStore = useHistoryStore();
  const dashboardStore = useDashboardStore();

  /**
   * Triggers a single warning prediction.
   */
  const executeSinglePrediction = async (studentData: StudentPredictionInput) => {
    loading.value = true;
    currentSingleResult.value = null;
    try {
      const result = await predictionService.predictSingle(studentData);
      currentSingleResult.value = result;

      // Log in prediction history
      const session: PredictionHistoryItem = {
        id: `PR-${Date.now()}`,
        date: result.date,
        type: 'single',
        studentCount: 1,
        resultSummary: `1 ${result.prediction} (${result.riskLevel} Risk)`,
        details: [result]
      };

      await historyStore.addSession(session);
      // Trigger dashboard update
      await dashboardStore.fetchDashboardData();
      
      return result;
    } catch (error) {
      console.error('Single prediction failed:', error);
      throw error;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    currentSingleResult,
    executeSinglePrediction
  };
});

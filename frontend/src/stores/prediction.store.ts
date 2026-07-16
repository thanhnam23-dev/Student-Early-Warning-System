import { defineStore } from 'pinia';
import { ref } from 'vue';
import { predictionService } from '../api/prediction.service';
import { uploadService } from '../api/upload.service';
import { useHistoryStore } from './history.store';
import { useDashboardStore } from './dashboard.store';
import type { StudentPredictionInput } from '../types/student';
import type { StudentPredictionResult } from '../types/prediction';
import type { PredictionHistoryItem } from '../types/history';

export const usePredictionStore = defineStore('prediction', () => {
  const loading = ref(false);
  const currentSingleResult = ref<StudentPredictionResult | null>(null);
  const currentBatchResults = ref<StudentPredictionResult[]>([]);
  
  // Excel parsing preview state
  const parsedPreviewList = ref<StudentPredictionInput[]>([]);

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

  /**
   * Triggers warning predictions for a batch of student rows parsed from excel.
   */
  const executeBatchPrediction = async (studentsData: StudentPredictionInput[]) => {
    loading.value = true;
    currentBatchResults.value = [];
    try {
      const results = await predictionService.predictBatch(studentsData);
      currentBatchResults.value = results;

      // Group counts for summary
      const grads = results.filter((r) => r.prediction === 'Graduate').length;
      const drops = results.filter((r) => r.prediction === 'Dropout').length;
      const enrolls = results.filter((r) => r.prediction === 'Enrolled').length;

      const summaryParts: string[] = [];
      if (grads > 0) summaryParts.push(`${grads} Graduate${grads > 1 ? 's' : ''}`);
      if (enrolls > 0) summaryParts.push(`${enrolls} Enrolled`);
      if (drops > 0) summaryParts.push(`${drops} Dropout${drops > 1 ? 's' : ''}`);
      const resultSummary = summaryParts.join(' / ');

      // Log in prediction history
      const session: PredictionHistoryItem = {
        id: `PR-${Date.now()}`,
        date: new Date().toISOString(),
        type: 'batch',
        studentCount: results.length,
        resultSummary,
        details: results
      };

      await historyStore.addSession(session);
      // Trigger dashboard update
      await dashboardStore.fetchDashboardData();

      return results;
    } catch (error) {
      console.error('Batch prediction failed:', error);
      throw error;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Parses uploaded spreadsheet file.
   */
  const parseExcelUpload = async (file: File) => {
    loading.value = true;
    parsedPreviewList.value = [];
    try {
      const parsedData = await uploadService.parseUpload(file);
      parsedPreviewList.value = parsedData;
      return parsedData;
    } catch (error) {
      console.error('Excel upload parsing failed:', error);
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const clearExcelPreview = () => {
    parsedPreviewList.value = [];
    currentBatchResults.value = [];
  };

  return {
    loading,
    currentSingleResult,
    currentBatchResults,
    parsedPreviewList,
    executeSinglePrediction,
    executeBatchPrediction,
    parseExcelUpload,
    clearExcelPreview
  };
});

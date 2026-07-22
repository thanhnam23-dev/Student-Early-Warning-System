import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { historyService } from '../api/history.service';
import type { PredictionHistoryItem, HistoryFilter } from '../types/history';
import type { StudentPredictionResult } from '../types/prediction';

export const useHistoryStore = defineStore('history', () => {
  const historyList = ref<PredictionHistoryItem[]>([]);
  const loading = ref(false);
  const activeRecord = ref<StudentPredictionResult | null>(null);
  
  const filters = ref<Omit<HistoryFilter, 'type'>>({
    search: '',
    prediction: 'all',
    riskLevel: 'all'
  });

  const fetchHistory = async () => {
    loading.value = true;
    try {
      const data = await historyService.getHistory();
      historyList.value = data;
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      loading.value = false;
    }
  };

  const addSession = async (session: PredictionHistoryItem) => {
    loading.value = true;
    try {
      const savedSession = await historyService.savePredictionSession(session);
      // Append to top of the history list (newest first)
      historyList.value.unshift(savedSession);
    } catch (error) {
      console.error('Failed to save session:', error);
    } finally {
      loading.value = false;
    }
  };

  const fetchRecordById = async (id: string): Promise<StudentPredictionResult | null> => {
    loading.value = true;
    activeRecord.value = null;
    try {
      // First check local loaded history
      for (const session of historyList.value) {
        const found = session.details.find((d) => d.id === id);
        if (found) {
          activeRecord.value = found;
          return found;
        }
      }
      
      // Fallback to service API simulation
      const data = await historyService.getPredictionResultById(id);
      if (data) {
        activeRecord.value = data;
      }
      return data;
    } catch (error) {
      console.error('Failed to fetch record details:', error);
      return null;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Computed list of history sessions matching filter criteria.
   */
  const filteredHistory = computed(() => {
    return historyList.value.filter((session) => {
      // 1. Check if any student details within this session match the search queries
      const matchesSearch = session.details.some((student) => {
        const query = filters.value.search.toLowerCase().trim();
        if (!query) return true;
        
        return (
          student.studentName.toLowerCase().includes(query) ||
          student.studentCode.toLowerCase().includes(query) ||
          student.className.toLowerCase().includes(query) ||
          student.faculty.toLowerCase().includes(query)
        );
      });

      if (!matchesSearch) return false;

      // 2. Filter by Prediction Outcome (Graduate / Dropout / Enrolled)
      if (filters.value.prediction !== 'all') {
        const matchesPrediction = session.details.some(
          (student) => student.prediction === filters.value.prediction
        );
        if (!matchesPrediction) return false;
      }

      // 3. Filter by Risk Level (Low / Medium / High)
      if (filters.value.riskLevel !== 'all') {
        const matchesRisk = session.details.some(
          (student) => student.riskLevel === filters.value.riskLevel
        );
        if (!matchesRisk) return false;
      }

      return true;
    });
  });

  const resetFilters = () => {
    filters.value = {
      search: '',
      prediction: 'all',
      riskLevel: 'all'
    };
  };

  return {
    historyList,
    loading,
    activeRecord,
    filters,
    fetchHistory,
    addSession,
    fetchRecordById,
    filteredHistory,
    resetFilters
  };
});

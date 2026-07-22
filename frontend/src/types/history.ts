import type { StudentPredictionResult } from './prediction';

export interface PredictionHistoryItem {
  id: string;
  date: string;
  type: 'single';
  studentCount: number;
  resultSummary: string;
  details: StudentPredictionResult[];
}

export interface HistoryFilter {
  search: string;
  prediction: 'all' | 'Graduate' | 'Dropout' | 'Enrolled';
  riskLevel: 'all' | 'Low' | 'Medium' | 'High';
}

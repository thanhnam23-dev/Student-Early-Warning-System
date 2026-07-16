import type { StudentPredictionResult } from './prediction';

export interface PredictionHistoryItem {
  id: string;
  date: string;
  type: 'single' | 'batch';
  studentCount: number;
  resultSummary: string;
  details: StudentPredictionResult[];
}

export interface HistoryFilter {
  search: string;
  type: 'all' | 'single' | 'batch';
  prediction: 'all' | 'Graduate' | 'Dropout' | 'Enrolled';
  riskLevel: 'all' | 'Low' | 'Medium' | 'High';
}

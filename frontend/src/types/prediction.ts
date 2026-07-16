import type { StudentDisplayInfo } from './student';

export interface PredictionResult {
  prediction: 'Graduate' | 'Dropout' | 'Enrolled';
  probability: number; // 0 to 1
  riskLevel: 'Low' | 'Medium' | 'High';
  recommendations: string[];
  confidence: number; // 0 to 1
}

export type StudentPredictionResult = StudentDisplayInfo & PredictionResult & {
  id: string;
  date: string;
};

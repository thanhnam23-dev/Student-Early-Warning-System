import type { StudentPredictionResult } from './prediction';

export interface DashboardStats {
  totalPredictions: number;
  singlePredictions: number;
  batchPredictions: number;
  graduateCount: number;
  dropoutCount: number;
  enrolledCount: number;
}

export interface ChartDataPoint {
  label: string;
  value: number;
}

export interface ActivityTimelineEvent {
  id: string;
  timestamp: string;
  type: 'single' | 'batch';
  message: string;
  studentName?: string;
  studentCode?: string;
  prediction?: 'Graduate' | 'Dropout' | 'Enrolled';
  riskLevel?: 'Low' | 'Medium' | 'High';
}

export interface DashboardData {
  stats: DashboardStats;
  distribution: ChartDataPoint[]; // Graduate, Dropout, Enrolled ratios
  history: ChartDataPoint[];      // Over time chart points
  latestSingle: StudentPredictionResult | null;
  latestBatch: {
    id: string;
    date: string;
    total: number;
    graduates: number;
    dropouts: number;
    enrolled: number;
    successRate: number;
  } | null;
  recentActivity: ActivityTimelineEvent[];
  recentPredictions: StudentPredictionResult[];
}

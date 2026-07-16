import type { PredictionHistoryItem } from '../types/history';
import type { StudentPredictionResult } from '../types/prediction';
import historyMock from '../mocks/prediction-history.json';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const historyService = {
  /**
   * Retrieves all historical prediction sessions.
   */
  async getHistory(): Promise<PredictionHistoryItem[]> {
    await delay(500); // Simulate API latency
    
    // Cast and return copy of the mock DB
    return JSON.parse(JSON.stringify(historyMock)) as PredictionHistoryItem[];
  },

  /**
   * Retrieves a specific single student prediction result across all historical sessions.
   * Used to review specific predictions.
   */
  async getPredictionResultById(id: string): Promise<StudentPredictionResult | null> {
    await delay(300);
    
    for (const session of historyMock) {
      const result = session.details.find((d) => d.id === id);
      if (result) {
        return JSON.parse(JSON.stringify(result)) as StudentPredictionResult;
      }
    }
    
    return null;
  },

  /**
   * Simulates saving a new prediction session to the database.
   */
  async savePredictionSession(session: PredictionHistoryItem): Promise<PredictionHistoryItem> {
    await delay(400);
    // In production, this would make a POST request to persist the record.
    console.log('API Request - Session saved to DB:', session);
    return session;
  }
};

export const RISK_THRESHOLDS = {
  LOW_MAX: 0.30,
  HIGH_MIN: 0.70
} as const;

export const getRiskLevel = (probability: number): 'Low' | 'Medium' | 'High' => {
  if (probability < RISK_THRESHOLDS.LOW_MAX) {
    return 'Low';
  } else if (probability > RISK_THRESHOLDS.HIGH_MIN) {
    return 'High';
  } else {
    return 'Medium';
  }
};

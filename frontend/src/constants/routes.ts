export const ROUTES = {
  DASHBOARD: '/dashboard',
  SINGLE_PREDICTION: '/single-prediction',
  PREDICTION_RESULT: '/prediction-result/:id',
  PREDICTION_HISTORY: '/prediction-history',
  ABOUT: '/about',
  SETTINGS: '/settings'
} as const;

export type RouteKey = keyof typeof ROUTES;

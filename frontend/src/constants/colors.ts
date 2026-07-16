export interface StyleMapping {
  colorClass: string;
  bgClass: string;
  borderClass: string;
  textClass: string;
  hex: string;
  icon: string;
}

export const RISK_COLORS: Record<'Low' | 'Medium' | 'High', StyleMapping> = {
  Low: {
    colorClass: 'green',
    bgClass: 'bg-green-50 dark:bg-green-950/20',
    borderClass: 'border-green-200 dark:border-green-900',
    textClass: 'text-green-700 dark:text-green-300',
    hex: '#10B981',
    icon: 'fa-solid fa-circle-check'
  },
  Medium: {
    colorClass: 'amber',
    bgClass: 'bg-amber-50 dark:bg-amber-950/20',
    borderClass: 'border-amber-200 dark:border-amber-900',
    textClass: 'text-amber-700 dark:text-amber-300',
    hex: '#F59E0B',
    icon: 'fa-solid fa-triangle-exclamation'
  },
  High: {
    colorClass: 'red',
    bgClass: 'bg-red-50 dark:bg-red-950/20',
    borderClass: 'border-red-200 dark:border-red-900',
    textClass: 'text-red-700 dark:text-red-300',
    hex: '#EF4444',
    icon: 'fa-solid fa-triangle-exclamation'
  }
};

export const OUTCOME_COLORS: Record<'Graduate' | 'Enrolled' | 'Dropout', StyleMapping> = {
  Graduate: {
    colorClass: 'green',
    bgClass: 'bg-green-50 dark:bg-green-950/20',
    borderClass: 'border-green-200 dark:border-green-900',
    textClass: 'text-green-700 dark:text-green-300',
    hex: '#10B981',
    icon: 'fa-solid fa-circle-check'
  },
  Enrolled: {
    colorClass: 'amber',
    bgClass: 'bg-amber-50 dark:bg-amber-950/20',
    borderClass: 'border-amber-200 dark:border-amber-900',
    textClass: 'text-amber-700 dark:text-amber-300',
    hex: '#F59E0B',
    icon: 'fa-solid fa-arrows-rotate'
  },
  Dropout: {
    colorClass: 'red',
    bgClass: 'bg-red-50 dark:bg-red-950/20',
    borderClass: 'border-red-200 dark:border-red-900',
    textClass: 'text-red-700 dark:text-red-300',
    hex: '#EF4444',
    icon: 'fa-solid fa-ban'
  }
};

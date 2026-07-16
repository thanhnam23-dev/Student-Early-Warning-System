export const MOTION_DURATIONS = {
  FAST: 120,    // ms
  NORMAL: 200,  // ms
  SLOW: 300,    // ms
};

export const MOTION_EASINGS = {
  DEFAULT: 'cubic-bezier(0.16, 1, 0.3, 1)', // easeOutExpo
  EASE_OUT: 'cubic-bezier(0.16, 1, 0.3, 1)',
  EASE_IN_OUT: 'cubic-bezier(0.87, 0, 0.13, 1)',
  BOUNCY: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
  iOS: 'cubic-bezier(0.25, 0.8, 0.25, 1)',
};

export const MOTION_PRESETS = {
  FADE: 'fade',
  FADE_UP: 'fade-up',
  FADE_DOWN: 'fade-down',
  SLIDE_LEFT: 'slide-left',
  SLIDE_RIGHT: 'slide-right',
  SCALE: 'scale',
  SCALE_FADE: 'scale-fade',
  CARD_ENTER: 'card-enter',
  DIALOG_ENTER: 'dialog-enter',
  PAGE_ENTER: 'page-enter',
  SIDEBAR_INDICATOR: 'sidebar-indicator',
  TABLE_ROW: 'table-row',
};

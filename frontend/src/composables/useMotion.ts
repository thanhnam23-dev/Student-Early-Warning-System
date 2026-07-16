import { computed } from 'vue';
import { useSettingsStore } from '../stores/settings.store';
import { MOTION_DURATIONS } from '../constants/motion';

export function useMotion() {
  const settingsStore = useSettingsStore();

  const isMotionEnabled = computed(() => settingsStore.motionEffects);

  const durationFast = computed(() => (isMotionEnabled.value ? MOTION_DURATIONS.FAST : 0));
  const durationNormal = computed(() => (isMotionEnabled.value ? MOTION_DURATIONS.NORMAL : 0));
  const durationSlow = computed(() => (isMotionEnabled.value ? MOTION_DURATIONS.SLOW : 0));

  const chartAnimation = computed(() => {
    return isMotionEnabled.value
      ? {
          duration: 400,
          easing: 'easeOutQuart' as const,
        }
      : false;
  });

  return {
    isMotionEnabled,
    durationFast,
    durationNormal,
    durationSlow,
    chartAnimation,
  };
}

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useSettingsStore } from '../../stores/settings.store';

const props = withDefaults(
  defineProps<{
    title: string;
    value: string | number;
    icon: string;
    colorClass?: string; // 'blue' | 'green' | 'amber' | 'red' | 'indigo'
    description?: string;
    trend?: { value: number; direction: 'up' | 'down' | 'neutral'; label?: string };
    shape?: 'circle' | 'square' | 'squircle';
  }>(),
  {
    shape: 'circle',
    colorClass: 'blue'
  }
);

const settingsStore = useSettingsStore();
const displayValue = ref<string | number>(props.value);

const startCountUp = () => {
  if (!settingsStore.motionEffects) {
    displayValue.value = props.value;
    return;
  }

  const rawStr = String(props.value);
  const numericPart = rawStr.replace(/,/g, '');
  const targetNum = Number(numericPart);

  if (isNaN(targetNum) || targetNum <= 0) {
    displayValue.value = props.value;
    return;
  }

  const start = 0;
  const end = targetNum;
  const duration = 1200; // 1.2 seconds count up
  const startTime = performance.now();

  const step = (currentTime: number) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Smooth quadratic ease-out curve
    const easeProgress = progress * (2 - progress);
    const currentVal = Math.floor(start + (end - start) * easeProgress);

    if (rawStr.includes(',')) {
      displayValue.value = currentVal.toLocaleString('en-US');
    } else {
      displayValue.value = currentVal;
    }

    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      displayValue.value = props.value; // set exact final target
    }
  };

  requestAnimationFrame(step);
};

onMounted(() => startCountUp());
watch(() => props.value, () => startCountUp());
</script>

<template>
  <div
    class="card group relative p-5 overflow-hidden kpi-card"
  >
    <!-- Subtle accent gradient strip on left edge (shown on hover) -->
    <div
      class="absolute inset-y-0 left-0 w-0.5 rounded-l-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"
      :class="[
        colorClass === 'green'  ? 'bg-emerald-400' :
        colorClass === 'red'    ? 'bg-red-400' :
        colorClass === 'amber'  ? 'bg-amber-400' :
        colorClass === 'indigo' ? 'bg-indigo-400' :
        'bg-[var(--p-primary-500)]'
      ]"
    ></div>

    <!-- Top row: title + icon -->
    <div class="flex items-start justify-between">
      <!-- Title -->
      <span class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest leading-none select-none">
        {{ title }}
      </span>

      <!-- Icon Box -->
      <div
        class="icon-circle w-9 h-9 flex items-center justify-center flex-shrink-0 transition-colors duration-200"
        :class="[
          shape === 'squircle' ? 'rounded-[35%]' : shape === 'square' ? 'rounded-xl' : 'rounded-full',
          colorClass === 'green'  ? 'bg-gradient-to-br from-emerald-500/10 to-emerald-500/25 text-emerald-500 dark:from-emerald-400/20 dark:to-emerald-500/5 dark:text-emerald-400' :
          colorClass === 'red'    ? 'bg-gradient-to-br from-red-500/10 to-red-500/25 text-red-500 dark:from-red-400/20 dark:to-red-500/5 dark:text-red-400' :
          colorClass === 'amber'  ? 'bg-gradient-to-br from-amber-500/10 to-amber-500/25 text-amber-500 dark:from-amber-400/20 dark:to-amber-500/5 dark:text-amber-400' :
          colorClass === 'indigo' ? 'bg-gradient-to-br from-indigo-500/10 to-indigo-500/25 text-indigo-500 dark:from-indigo-400/20 dark:to-indigo-500/5 dark:text-indigo-400' :
          'bg-gradient-to-br from-[var(--p-primary-500)]/10 to-[var(--p-primary-500)]/25 text-[var(--p-primary-500)] dark:from-[var(--p-primary-400)]/20 dark:to-[var(--p-primary-500)]/5 dark:text-[var(--p-primary-400)]'
        ]"
      >
        <i :class="[icon, 'text-xs']"></i>
      </div>
    </div>

    <!-- Main value -->
    <div class="mt-3">
      <p class="text-3xl font-black text-gray-900 dark:text-white leading-none tracking-tight tabular-nums">
        {{ displayValue }}
      </p>
    </div>

    <!-- Footer: description OR trend indicator -->
    <div class="mt-3 flex items-center justify-between min-h-[18px]">
      <!-- Trend badge -->
      <div v-if="trend" class="flex items-center space-x-1.5">
        <span
          class="inline-flex items-center space-x-0.5 px-1.5 py-0.5 rounded-md text-[10px] font-bold transition-all duration-200"
          :class="[
            trend.direction === 'up'   ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/20 dark:text-emerald-400' :
            trend.direction === 'down' ? 'bg-red-50 text-red-600 dark:bg-red-950/20 dark:text-red-400' :
            'bg-gray-50 text-gray-500 dark:bg-gray-800 dark:text-gray-400'
          ]"
        >
          <i
            :class="[
              trend.direction === 'up'   ? 'fa-solid fa-arrow-up transition-transform duration-200 group-hover:translate-y-[-1px] group-hover:translate-x-[1px]' :
              trend.direction === 'down' ? 'fa-solid fa-arrow-down transition-transform duration-200 group-hover:translate-y-[1px] group-hover:translate-x-[1px]' :
              'fa-solid fa-minus',
              'text-[8px]'
            ]"
          ></i>
          <span>{{ Math.abs(trend.value) }}%</span>
        </span>
        <span class="text-[10px] text-gray-400 dark:text-gray-500 font-semibold">
          {{ trend.label || 'vs last period' }}
        </span>
      </div>

      <!-- Plain description -->
      <p v-else-if="description" class="text-[10px] font-semibold text-gray-400 dark:text-gray-500 flex items-center space-x-1">
        <i class="fa-solid fa-circle-info text-[9px]"></i>
        <span>{{ description }}</span>
      </p>

      <!-- No content placeholder keeps height consistent -->
      <span v-else class="block h-4"></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { OUTCOME_COLORS, RISK_COLORS, type StyleMapping } from '../../constants/colors';

const props = defineProps<{
  outcome: 'Graduate' | 'Enrolled' | 'Dropout' | 'Low' | 'Medium' | 'High';
}>();

const styling = computed<StyleMapping>(() => {
  const target = props.outcome;
  if (target === 'Graduate' || target === 'Enrolled' || target === 'Dropout') {
    return OUTCOME_COLORS[target];
  } else {
    return RISK_COLORS[target];
  }
});
</script>

<template>
  <span 
    class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-extrabold border transition-colors duration-200"
    :class="[styling.bgClass, styling.borderClass, styling.textClass]"
  >
    <i :class="[styling.icon, 'mr-1 text-[9px]']"></i>
    <span>{{ $t(outcome === 'Graduate' || outcome === 'Dropout' || outcome === 'Enrolled' ? 'outcomes.' + outcome : 'risk.' + outcome) }}</span>
  </span>
</template>

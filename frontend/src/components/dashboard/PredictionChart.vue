<script setup lang="ts">
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useMotion } from '../../composables/useMotion';
import { useSettingsStore } from '../../stores/settings.store';

Chart.register(...registerables);

const props = defineProps<{
  type: 'pie' | 'bar';
  data: { label: string; value: number }[];
  title: string;
  subtitle?: string;
}>();

const canvasRef = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const { chartAnimation } = useMotion();
const settingsStore = useSettingsStore();

const totalCount = computed(() => props.data.reduce((acc, d) => acc + d.value, 0));

const isDark = () => document.documentElement.classList.contains('dark');

const PIE_COLORS = {
  Graduate: { bg: '#10b981', hover: '#059669' },
  Dropout:  { bg: '#f43f5e', hover: '#e11d48' },
  Enrolled: { bg: '#f59e0b', hover: '#d97706' },
  default:  { bg: '#3b82f6', hover: '#2563eb' },
};

const getThemeColors = (theme: string, dark: boolean) => {
  switch (theme) {
    case 'green':
      return {
        color1: dark ? 'rgba(16, 185, 129, 0.80)' : 'rgba(16, 185, 129, 0.75)',
        color2: dark ? 'rgba(132, 204, 22, 0.15)' : 'rgba(132, 204, 22, 0.12)',
        hoverColor: dark ? 'rgba(16, 185, 129, 0.95)' : 'rgba(16, 185, 129, 0.95)',
        border: '#10b981'
      };
    case 'purple':
      return {
        color1: dark ? 'rgba(168, 85, 247, 0.80)' : 'rgba(168, 85, 247, 0.75)',
        color2: dark ? 'rgba(139, 92, 246, 0.15)' : 'rgba(139, 92, 246, 0.12)',
        hoverColor: dark ? 'rgba(168, 85, 247, 0.95)' : 'rgba(168, 85, 247, 0.95)',
        border: '#a855f7'
      };
    case 'orange':
      return {
        color1: dark ? 'rgba(249, 115, 22, 0.80)' : 'rgba(249, 115, 22, 0.75)',
        color2: dark ? 'rgba(245, 158, 11, 0.15)' : 'rgba(245, 158, 11, 0.12)',
        hoverColor: dark ? 'rgba(249, 115, 22, 0.95)' : 'rgba(249, 115, 22, 0.95)',
        border: '#f97316'
      };
    case 'red':
      return {
        color1: dark ? 'rgba(239, 68, 68, 0.80)' : 'rgba(239, 68, 68, 0.75)',
        color2: dark ? 'rgba(244, 63, 94, 0.15)' : 'rgba(244, 63, 94, 0.12)',
        hoverColor: dark ? 'rgba(239, 68, 68, 0.95)' : 'rgba(239, 68, 68, 0.95)',
        border: '#ef4444'
      };
    case 'teal':
      return {
        color1: dark ? 'rgba(20, 184, 166, 0.80)' : 'rgba(20, 184, 166, 0.75)',
        color2: dark ? 'rgba(6, 182, 212, 0.15)' : 'rgba(6, 182, 212, 0.12)',
        hoverColor: dark ? 'rgba(20, 184, 166, 0.95)' : 'rgba(20, 184, 166, 0.95)',
        border: '#14b8a6'
      };
    case 'blue':
    default:
      return {
        color1: dark ? 'rgba(59, 130, 246, 0.80)' : 'rgba(59, 130, 246, 0.75)',
        color2: dark ? 'rgba(99, 102, 241, 0.15)' : 'rgba(99, 102, 241, 0.12)',
        hoverColor: dark ? 'rgba(59, 130, 246, 0.95)' : 'rgba(59, 130, 246, 0.95)',
        border: '#3b82f6'
      };
  }
};

const translateLabel = (label: string) => {
  if (settingsStore.language === 'vi') {
    switch (label) {
      case 'Graduate': return 'Tốt nghiệp';
      case 'Dropout': return 'Thôi học';
      case 'Enrolled': return 'Đang học';
      case 'Jan': return 'T1';
      case 'Feb': return 'T2';
      case 'Mar': return 'T3';
      case 'Apr': return 'T4';
      case 'May': return 'T5';
      case 'Jun': return 'T6';
      case 'Jul': return 'T7';
      case 'Aug': return 'T8';
      case 'Sep': return 'T9';
      case 'Oct': return 'T10';
      case 'Nov': return 'T11';
      case 'Dec': return 'T12';
      default: return label;
    }
  } else {
    switch (label) {
      case 'Graduate': return 'Graduate';
      case 'Dropout': return 'Dropout';
      case 'Enrolled': return 'Enrolled';
      default: return label;
    }
  }
};

const createChart = () => {
  if (!canvasRef.value) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const dark = isDark();
  const labelColor = dark ? '#94a3b8' : '#64748b';
  const gridColor  = dark ? 'rgba(51,65,85,0.3)' : 'rgba(241,245,249,1)';

  const labels = props.data.map((d) => translateLabel(d.label));
  const values = props.data.map((d) => d.value);

  const ctx = canvasRef.value.getContext('2d');
  if (!ctx) return;

  let backgroundColor: string | string[] | CanvasGradient;
  let hoverBackgroundColor: string | string[];
  let borderColor: string | string[];

  if (props.type === 'pie') {
    backgroundColor = props.data.map((d) => {
      const c = PIE_COLORS[d.label as keyof typeof PIE_COLORS] ?? PIE_COLORS.default;
      return c.bg;
    });
    hoverBackgroundColor = props.data.map((d) => {
      const c = PIE_COLORS[d.label as keyof typeof PIE_COLORS] ?? PIE_COLORS.default;
      return c.hover;
    });
    borderColor = dark ? '#080b11' : '#ffffff';
  } else {
    // Dynamic theme-aware gradient
    const chartHeight = canvasRef.value.clientHeight || 200;
    const gradient = ctx.createLinearGradient(0, 0, 0, chartHeight);
    const themeColors = getThemeColors(settingsStore.themeColor, dark);
    gradient.addColorStop(0, themeColors.color1);
    gradient.addColorStop(1, themeColors.color2);
    
    backgroundColor = gradient;
    hoverBackgroundColor = themeColors.hoverColor;
    borderColor = themeColors.border;
  }

  chartInstance = new Chart(ctx, {
    type: props.type === 'pie' ? 'doughnut' : 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Students',
        data: values,
        backgroundColor,
        hoverBackgroundColor,
        borderColor,
        borderWidth: props.type === 'pie' ? 3 : 1,
        borderRadius: props.type === 'bar' ? 6 : 0,
        borderSkipped: false,
        hoverBorderWidth: 2,
        hoverBorderColor: props.type === 'pie' ? (dark ? '#080b11' : '#ffffff') : getThemeColors(settingsStore.themeColor, dark).border,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: chartAnimation.value,
      plugins: {
        legend: {
          display: props.type === 'pie',
          position: 'bottom',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            boxWidth: 7,
            boxHeight: 7,
            padding: 18,
            font: { family: 'Inter, system-ui, sans-serif', size: 11, weight: 'bold' },
            color: labelColor,
          },
        },
        tooltip: {
          backgroundColor: dark ? '#1e293b' : '#ffffff',
          titleColor: dark ? '#f8fafc' : '#1e293b',
          bodyColor: dark ? '#cbd5e1' : '#475569',
          borderColor: dark ? '#334155' : '#e7edf4',
          borderWidth: 1,
          padding: 12,
          cornerRadius: 10,
          titleFont: { family: 'Inter, system-ui, sans-serif', size: 12, weight: 'bold' },
          bodyFont:  { family: 'Inter, system-ui, sans-serif', size: 11 },
          callbacks: {
            label: (context) => {
              const val = context.parsed as number;
              const pct = totalCount.value > 0 ? ((val / totalCount.value) * 100).toFixed(1) : '0';
              const studentLabel = settingsStore.language === 'vi' ? 'sinh viên' : 'students';
              return props.type === 'pie'
                ? `  ${val} ${studentLabel} (${pct}%)`
                : `  ${val} ${studentLabel}`;
            },
          },
        },
      },
      scales: props.type === 'bar' ? {
        y: {
          beginAtZero: true,
          grid: { color: gridColor },
          border: { display: false },
          ticks: {
            color: labelColor,
            font: { family: 'Inter, system-ui, sans-serif', size: 10, weight: 'bold' },
            padding: 8,
            maxTicksLimit: 6,
          },
        },
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: {
            color: labelColor,
            font: { family: 'Inter, system-ui, sans-serif', size: 10, weight: 'bold' },
            padding: 6,
          },
        },
      } : undefined,
      cutout: props.type === 'pie' ? '68%' : undefined,
    },
  });
};

const updateChartTheme = () => {
  if (!chartInstance) return;
  const dark = isDark();
  const labelColor = dark ? '#94a3b8' : '#64748b';
  const gridColor  = dark ? 'rgba(51,65,85,0.3)' : 'rgba(241,245,249,1)';

  // Update scale colors smoothly
  if (chartInstance.options.scales?.y?.ticks) {
    chartInstance.options.scales.y.ticks.color = labelColor;
  }
  if (chartInstance.options.scales?.y?.grid) {
    chartInstance.options.scales.y.grid.color = gridColor;
  }
  if (chartInstance.options.scales?.x?.ticks) {
    chartInstance.options.scales.x.ticks.color = labelColor;
  }
  if (chartInstance.options.plugins?.legend?.labels) {
    chartInstance.options.plugins.legend.labels.color = labelColor;
  }
  if (chartInstance.options.plugins?.tooltip) {
    chartInstance.options.plugins.tooltip.backgroundColor = dark ? '#1e293b' : '#ffffff';
    chartInstance.options.plugins.tooltip.titleColor = dark ? '#f8fafc' : '#1e293b';
    chartInstance.options.plugins.tooltip.bodyColor = dark ? '#cbd5e1' : '#475569';
    chartInstance.options.plugins.tooltip.borderColor = dark ? '#334155' : '#e7edf4';
  }

  // Re-generate gradient context for bar chart
  const ds = chartInstance.data.datasets[0];
  if (ds) {
    const themeColors = getThemeColors(settingsStore.themeColor, dark);
    ds.borderColor = props.type === 'pie' 
      ? (dark ? '#080b11' : '#ffffff')
      : themeColors.border;
    ds.hoverBorderColor = props.type === 'pie' 
      ? (dark ? '#080b11' : '#ffffff')
      : themeColors.border;

    if (props.type === 'bar' && canvasRef.value) {
      const ctx = canvasRef.value.getContext('2d');
      if (ctx) {
        const chartHeight = canvasRef.value.clientHeight || 200;
        const gradient = ctx.createLinearGradient(0, 0, 0, chartHeight);
        gradient.addColorStop(0, themeColors.color1);
        gradient.addColorStop(1, themeColors.color2);
        ds.backgroundColor = gradient;
        ds.hoverBackgroundColor = themeColors.hoverColor;
      }
    }
  }

  chartInstance.update('active'); // smooth animated update
};

watch(() => props.data, (newData) => {
  if (chartInstance) {
    chartInstance.data.labels = newData.map((d) => translateLabel(d.label));
    const ds = chartInstance.data.datasets[0];
    if (ds) {
      ds.data = newData.map((d) => d.value);
      if (props.type === 'pie') {
        ds.backgroundColor = newData.map((d) => {
          const c = PIE_COLORS[d.label as keyof typeof PIE_COLORS] ?? PIE_COLORS.default;
          return c.bg;
        });
      }
    }
    chartInstance.update('active');
  } else {
    createChart();
  }
}, { deep: true });

watch(chartAnimation, (newAnim) => {
  if (chartInstance) {
    chartInstance.options.animation = newAnim;
    chartInstance.update('active');
  }
});

watch(() => settingsStore.themeColor, () => {
  updateChartTheme();
});

watch(() => settingsStore.language, () => {
  if (chartInstance) {
    chartInstance.data.labels = props.data.map((d) => translateLabel(d.label));
    if (chartInstance.options.plugins?.tooltip?.callbacks) {
      chartInstance.options.plugins.tooltip.callbacks.label = (context) => {
        const val = context.parsed as number;
        const pct = totalCount.value > 0 ? ((val / totalCount.value) * 100).toFixed(1) : '0';
        const studentLabel = settingsStore.language === 'vi' ? 'sinh viên' : 'students';
        return props.type === 'pie'
          ? `  ${val} ${studentLabel} (${pct}%)`
          : `  ${val} ${studentLabel}`;
      };
    }
    chartInstance.update('active');
  }
});

onMounted(() => {
  createChart();
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((m) => {
      if (m.attributeName === 'class') {
        updateChartTheme();
      }
    });
  });
  observer.observe(document.documentElement, { attributes: true });
  onBeforeUnmount(() => {
    observer.disconnect();
    chartInstance?.destroy();
  });
});
</script>

<template>
  <div class="card flex flex-col h-full overflow-hidden">
    <!-- Card Header -->
    <div class="px-5 pt-5 pb-3 flex items-center justify-between border-b dark:border-gray-800/60" style="border-bottom-color: #F1F5F9;">
      <div class="space-y-0.5">
        <h4 class="text-sm font-bold text-gray-800 dark:text-gray-100 tracking-tight leading-tight">
          {{ title }}
        </h4>
        <p v-if="subtitle" class="text-[10px] font-semibold text-gray-400 dark:text-gray-500">
          {{ subtitle }}
        </p>
        <p v-else-if="type === 'pie'" class="text-[10px] font-semibold text-gray-400 dark:text-gray-500">
          {{ settingsStore.language === 'vi' ? `Tổng cộng ${totalCount} sinh viên` : `${totalCount} students total` }}
        </p>
      </div>
      <div class="w-7 h-7 rounded-lg bg-primary-50 dark:bg-primary-950/20 flex items-center justify-center">
        <i :class="type === 'pie' ? 'fa-solid fa-chart-pie' : 'fa-solid fa-chart-bar'"
           class="text-[10px] text-primary-500"></i>
      </div>
    </div>

    <!-- Chart Area — with donut center label -->
    <div class="flex-1 relative px-4 py-4 min-h-[260px]">
      <canvas ref="canvasRef"></canvas>
      <!-- Center label for donut chart -->
      <div
        v-if="type === 'pie'"
        class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none"
        style="padding-bottom: 2.5rem"
      >
        <span class="text-2xl font-black text-gray-800 dark:text-white leading-none">{{ totalCount }}</span>
        <span class="text-[10px] font-bold text-gray-400 dark:text-gray-500 mt-0.5 uppercase tracking-wide">
          {{ settingsStore.language === 'vi' ? 'Tổng số' : 'Total' }}
        </span>
      </div>
    </div>
  </div>
</template>

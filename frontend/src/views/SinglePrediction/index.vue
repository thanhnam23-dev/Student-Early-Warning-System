<script setup lang="ts">
import { ref, computed } from 'vue';
import { usePredictionStore } from '../../stores/prediction.store';
import { useSettingsStore } from '../../stores/settings.store';
import PageHeader from '../../components/common/PageHeader.vue';
import PredictionForm from '../../components/prediction/PredictionForm.vue';
import PredictionDialog from '../../components/prediction/PredictionDialog.vue';
import LoadingOverlay from '../../components/common/LoadingOverlay.vue';
import type { StudentPredictionInput } from '../../types/student';

const predictionStore = usePredictionStore();
const settingsStore = useSettingsStore();

const showResultDialog = ref(false);
const activeInput = ref<StudentPredictionInput | null>(null);

const isAnalyzing = ref(false);
const analysisStep = ref(0);

const loading = computed(() => predictionStore.loading);
const predictionResult = computed(() => predictionStore.currentSingleResult);

const analysisSteps = computed(() => {
  return settingsStore.language === 'vi' 
    ? [
        'Đang phân tích thông tin sinh viên...',
        'Đang đánh giá kết quả học tập...',
        'Đang kiểm tra chỉ số tài chính...',
        'Đang chạy mô hình dự đoán...',
        'Đang tính toán mức độ tin cậy...',
        'Hoàn tất dự đoán.'
      ]
    : [
        'Analyzing student profile...',
        'Evaluating academic performance...',
        'Checking financial indicators...',
        'Running prediction model...',
        'Calculating confidence...',
        'Prediction Complete.'
      ];
});

const handlePredict = async (studentData: StudentPredictionInput) => {
  activeInput.value = studentData;
  
  if (!settingsStore.motionEffects) {
    // Instant execution if Motion Effects is disabled
    try {
      await predictionStore.executeSinglePrediction(studentData);
      showResultDialog.value = true;
    } catch (error) {
      console.error('Failed to execute single prediction:', error);
    }
    return;
  }

  // Visual AI analysis sequence when Motion Effects is enabled
  isAnalyzing.value = true;
  analysisStep.value = 0;

  // Run calculation concurrently in the background
  const predictionPromise = predictionStore.executeSinglePrediction(studentData);

  // Progressive analysis ticker steps every 450ms
  const interval = setInterval(() => {
    if (analysisStep.value < 5) {
      analysisStep.value++;
    } else {
      clearInterval(interval);
      predictionPromise.then(() => {
        isAnalyzing.value = false;
        showResultDialog.value = true;
      }).catch((err) => {
        isAnalyzing.value = false;
        console.error('Prediction failed:', err);
      });
    }
  }, 450);
};
</script>

<template>
  <div class="space-y-6" :class="{ 'ai-accent-active': isAnalyzing }">
    <PageHeader 
      :title="$t('singlePrediction.title')" 
      :description="$t('singlePrediction.description')"
    />

    <!-- Multi-step Stepper Form with AI Accent visual state -->
    <div class="max-w-4xl mx-auto relative">
      <!-- Gentle pulse glow behind the card -->
      <div 
        v-if="isAnalyzing" 
        class="absolute -inset-1 rounded-[20px] bg-gradient-to-r from-primary-500 via-purple-500 to-cyan-500 opacity-20 blur-md animate-pulse z-0 pointer-events-none"
      ></div>

      <div 
        class="relative bg-white dark:bg-gray-900 rounded-2xl border border-gray-150 dark:border-gray-800 transition-all duration-500 overflow-hidden z-10"
        :class="{ 'shadow-xl shadow-primary-500/10 border-primary-500/50 dark:border-primary-400/40': isAnalyzing }"
      >
        <!-- Top animated progress line -->
        <div v-if="isAnalyzing" class="absolute top-0 left-0 right-0 h-1 z-30 overflow-hidden">
          <div class="h-full bg-gradient-to-r from-primary-500 via-purple-500 to-cyan-500 animate-progress-slide"></div>
        </div>

        <!-- Form Component -->
        <PredictionForm @predict="handlePredict" />

        <!-- AI analysis steps overlay -->
        <Transition name="fade">
          <div 
            v-if="isAnalyzing" 
            class="absolute inset-0 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md flex flex-col items-center justify-center z-20"
          >
            <!-- Pulsing brain squircle background -->
            <div class="w-16 h-16 rounded-[28%] bg-gradient-to-br from-primary-500 via-indigo-500 to-purple-600 flex items-center justify-center text-white text-2xl shadow-lg shadow-primary-500/25 mb-6 relative animate-pulse">
              <div class="absolute inset-0 rounded-[28%] bg-inherit filter blur-sm opacity-50 animate-ping"></div>
              <i class="fa-solid fa-brain relative z-10"></i>
            </div>
            
            <!-- Analysis status text -->
            <div class="text-[13px] font-bold text-gray-800 dark:text-gray-100 tracking-tight transition-all duration-200">
              {{ analysisSteps[analysisStep] }}
            </div>

            <!-- Steps Dots -->
            <div class="flex items-center space-x-2 mt-4 select-none">
              <span 
                v-for="(step, idx) in 6" 
                :key="idx"
                class="w-1.5 h-1.5 rounded-full transition-all duration-300"
                :class="[
                  idx === analysisStep ? 'bg-primary-500 scale-150' : 
                  idx < analysisStep ? 'bg-primary-400 dark:bg-primary-600' : 
                  'bg-gray-200 dark:bg-gray-800'
                ]"
              ></span>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Results Modal overlay -->
    <PredictionDialog 
      v-model:visible="showResultDialog"
      :result="predictionResult"
      :student-input="activeInput"
    />

    <!-- Processing Overlay fallback (for background/batch predictions) -->
    <LoadingOverlay 
      :visible="loading && !isAnalyzing" 
      :message="$t('batchPrediction.processing')"
    />
  </div>
</template>

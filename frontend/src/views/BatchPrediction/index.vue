<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue';
import FileUpload from 'primevue/fileupload';
import Card from 'primevue/card';
import Button from 'primevue/button';
import { usePredictionStore } from '../../stores/prediction.store';
import PageHeader from '../../components/common/PageHeader.vue';
import LoadingOverlay from '../../components/common/LoadingOverlay.vue';
import RiskBadge from '../../components/prediction/RiskBadge.vue';
import { uploadService } from '../../api/upload.service';
import { exportToExcel } from '../../utils/excel';
import { getCourseLabel, getGenderLabel } from '../../utils/mapper';
import { formatPercent } from '../../utils/formatter';

const predictionStore = usePredictionStore();

const fileUploadRef = ref<any>(null);
const fileSelected = ref<File | null>(null);

const loading = computed(() => predictionStore.loading);
const previewList = computed(() => predictionStore.parsedPreviewList);
const resultsList = computed(() => predictionStore.currentBatchResults);

const triggerTemplateDownload = async () => {
  try {
    await uploadService.downloadTemplate();
  } catch (error) {
    console.error('Failed to download template:', error);
  }
};

const handleFileSelect = async (event: any) => {
  const file = event.files[0];
  if (!file) return;
  fileSelected.value = file;
  try {
    await predictionStore.parseExcelUpload(file);
  } catch (error) {
    console.error('Failed to parse excel file:', error);
    fileSelected.value = null;
  }
};

const triggerPrediction = async () => {
  if (previewList.value.length === 0) return;
  try {
    await predictionStore.executeBatchPrediction(previewList.value);
  } catch (error) {
    console.error('Failed to run batch predictions:', error);
  }
};

const handleExport = () => {
  if (resultsList.value.length === 0) return;
  
  const reportData = resultsList.value.map((item) => ({
    'Student Code': item.studentCode,
    'Student Name': item.studentName,
    'Class': item.className,
    'Faculty': item.faculty,
    'Prediction': item.prediction,
    'Probability': formatPercent(item.probability),
    'Risk Level': item.riskLevel,
    'Recommendation': item.recommendations.join('; ')
  }));

  exportToExcel(reportData, `student_early_warning_report_${Date.now()}`);
};

const clearUpload = () => {
  predictionStore.clearExcelPreview();
  fileSelected.value = null;
  if (fileUploadRef.value) {
    fileUploadRef.value.clear();
  }
};

onBeforeUnmount(() => {
  predictionStore.clearExcelPreview();
});
</script>

<template>
  <div class="space-y-6">
    <PageHeader 
      :title="$t('batchPrediction.title')" 
      :description="$t('batchPrediction.description')"
    >
      <template #actions>
        <button 
          @click="triggerTemplateDownload"
          class="py-2 px-4 border border-gray-200 dark:border-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-750 text-gray-750 dark:text-gray-300 rounded-xl text-xs font-semibold cursor-pointer transition-all duration-200 shadow-sm"
        >
          <i class="fa-solid fa-file-arrow-down mr-1.5"></i> {{ $t('batchPrediction.uploadCard.downloadTemplate') }}
        </button>
      </template>
    </PageHeader>

    <div class="max-w-5xl mx-auto space-y-6">
      <!-- 1. Drag & Drop File Upload -->
      <Card class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden">
        <template #content>
          <div class="space-y-4">
            <FileUpload 
              ref="fileUploadRef"
              mode="basic" 
              name="studentsFile" 
              accept=".xlsx, .xls" 
              :maxFileSize="1000000" 
              @select="handleFileSelect" 
              auto
              customUpload
              :chooseLabel="$t('general.select') + ' Excel'"
              class="hidden"
            />
            
            <div 
              v-if="!fileSelected"
              @click="fileUploadRef?.$el.querySelector('input[type=file]')?.click()"
              class="border-2 border-dashed border-gray-200 dark:border-gray-800 hover:border-primary-500 dark:hover:border-primary-500 rounded-2xl py-12 px-4 flex flex-col items-center justify-center cursor-pointer transition-all duration-200 bg-gray-50/20 dark:bg-gray-950/10 group"
            >
              <div class="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-950/30 text-primary-600 dark:text-primary-400 flex items-center justify-center mb-4 transition-transform group-hover:scale-110">
                <i class="fa-solid fa-cloud-arrow-up text-xl animate-icon-pulse"></i>
              </div>
              <h5 class="text-xs font-bold text-gray-800 dark:text-gray-200 mb-1">
                {{ $t('batchPrediction.uploadCard.dragDrop') }}
              </h5>
              <p class="text-[10px] text-gray-400 dark:text-gray-500 font-medium">
                {{ $t('batchPrediction.uploadCard.fileFormats') }}
              </p>
            </div>
            
            <div 
              v-else 
              class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-850 rounded-xl border border-gray-150 dark:border-gray-800"
            >
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-green-50 text-green-600 dark:bg-green-950/20 dark:text-green-400 flex items-center justify-center">
                  <i class="fa-solid fa-file-excel text-lg"></i>
                </div>
                <div>
                  <h6 class="text-xs font-bold text-gray-850 dark:text-gray-200">
                    {{ fileSelected.name }}
                  </h6>
                  <span class="text-[10px] text-gray-400 font-medium block mt-0.5">
                    {{ $t('batchPrediction.preview', { count: previewList.length }).split('&').pop() }}
                  </span>
                </div>
              </div>
              
              <button 
                @click="clearUpload"
                class="w-8 h-8 rounded-lg bg-white hover:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 flex items-center justify-center border border-gray-200 dark:border-gray-750 text-gray-400 hover:text-red-500 cursor-pointer transition-all duration-200"
                title="Remove file"
              >
                <i class="fa-solid fa-trash-can"></i>
              </button>
            </div>
          </div>
        </template>
      </Card>

      <!-- 2. Preview data table (before predict) -->
      <Card 
        v-if="previewList.length > 0 && resultsList.length === 0"
        class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden"
      >
        <template #title>
          <div class="flex items-center justify-between px-5 pt-4">
            <h5 class="text-sm font-bold text-gray-850 dark:text-gray-200">
              {{ $t('batchPrediction.preview', { count: previewList.length }).split('&')[0] }}
            </h5>
            <Button 
              :label="$t('singlePrediction.triggerPredict')" 
              icon="fa-solid fa-play" 
              @click="triggerPrediction"
              class="text-xs font-bold px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl cursor-pointer shadow-md shadow-primary-500/20"
            />
          </div>
        </template>
        <template #content>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs font-semibold">
              <thead>
                <tr class="border-b border-gray-100 dark:border-gray-800 text-[10px] text-gray-455 uppercase tracking-wider">
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.studentCode') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.studentName') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.className') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.course') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.gender') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.ageAtEnrollment') }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50 dark:divide-gray-800 text-gray-650 dark:text-gray-300">
                <tr 
                  v-for="(student, idx) in previewList.slice(0, 10)" 
                  :key="idx"
                  class="hover:bg-gray-50/30 dark:hover:bg-gray-800/10"
                >
                  <td class="py-3 px-5 text-gray-900 dark:text-white font-bold">{{ student.studentCode }}</td>
                  <td class="py-3 px-5">{{ student.studentName }}</td>
                  <td class="py-3 px-5 text-gray-500 dark:text-gray-400 font-medium">{{ student.className }}</td>
                  <td class="py-3 px-5 text-gray-500 dark:text-gray-400 font-medium">{{ getCourseLabel(student.course) }}</td>
                  <td class="py-3 px-5 text-gray-500 dark:text-gray-400 font-medium">{{ getGenderLabel(student.gender) }}</td>
                  <td class="py-3 px-5 text-gray-500 dark:text-gray-400 font-medium">{{ student.ageAtEnrollment }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div 
            v-if="previewList.length > 10" 
            class="text-center py-3 border-t border-gray-50 dark:border-gray-800 text-[10px] font-bold text-gray-450 tracking-wide uppercase bg-gray-50/10 dark:bg-gray-900/5"
          >
            And {{ previewList.length - 10 }} more student records...
          </div>
        </template>
      </Card>

      <!-- 3. Result log table (after predict) -->
      <Card 
        v-if="resultsList.length > 0"
        class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden"
      >
        <template #title>
          <div class="flex items-center justify-between px-5 pt-4">
            <div>
              <h5 class="text-sm font-bold text-gray-855 dark:text-gray-200 leading-none">
                {{ ($t('batchPrediction.results', { count: resultsList.length }) || '').split('(')[0]?.trim() }}
              </h5>
              <span class="text-[10px] text-gray-400 font-semibold block mt-1">
                {{ $t('batchPrediction.results', { count: resultsList.length }) }}
              </span>
            </div>
            <div class="flex items-center space-x-3">
              <Button 
                :label="$t('general.cancel')" 
                icon="fa-solid fa-arrows-rotate" 
                severity="secondary"
                @click="clearUpload"
                class="text-xs font-semibold px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl cursor-pointer"
              />
              <Button 
                :label="$t('batchPrediction.exportBtn')" 
                icon="fa-solid fa-file-export" 
                @click="handleExport"
                class="text-xs font-bold px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl cursor-pointer shadow-md shadow-primary-500/20"
              />
            </div>
          </div>
        </template>
        <template #content>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs font-semibold">
              <thead>
                <tr class="border-b border-gray-100 dark:border-gray-800 text-[10px] text-gray-450 uppercase tracking-wider">
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.studentCode') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.studentName') }}</th>
                  <th class="py-3 px-5">{{ $t('singlePrediction.fields.className') }}</th>
                  <th class="py-3 px-5">{{ $t('result.outcomeLabel') }}</th>
                  <th class="py-3 px-5">{{ $t('result.probabilityLabel') }}</th>
                  <th class="py-3 px-5">{{ $t('result.riskLabel') }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50 dark:divide-gray-800 text-gray-650 dark:text-gray-300">
                <tr 
                  v-for="item in resultsList" 
                  :key="item.id"
                  class="hover:bg-gray-50/30 dark:hover:bg-gray-800/10"
                >
                  <td class="py-3 px-5 text-gray-900 dark:text-white font-bold">{{ item.studentCode }}</td>
                  <td class="py-3 px-5">{{ item.studentName }}</td>
                  <td class="py-3 px-5 text-gray-500 dark:text-gray-400 font-medium">{{ item.className }}</td>
                  <td class="py-3 px-5">
                    <span 
                      class="font-extrabold"
                      :class="[
                        item.prediction === 'Graduate' ? 'text-green-600' :
                        item.prediction === 'Dropout' ? 'text-red-600' : 'text-amber-600'
                      ]"
                    >
                      {{ $t('outcomes.' + item.prediction) }}
                    </span>
                  </td>
                  <td class="py-3 px-5 tabular-nums">{{ formatPercent(item.probability) }}</td>
                  <td class="py-3 px-5">
                    <RiskBadge :outcome="item.riskLevel" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </Card>
    </div>

    <!-- Processing Overlay spinner -->
    <LoadingOverlay 
      :visible="loading" 
      :message="$t('batchPrediction.processing')"
    />
  </div>
</template>

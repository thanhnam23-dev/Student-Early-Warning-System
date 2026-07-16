<script setup lang="ts">
import { ref } from 'vue';
import type { StudentPredictionInput } from '../../types/student';
import {
  getMaritalStatusLabel,
  getGenderLabel,
  getDaytimeEveningLabel,
  getYesNoLabel,
  getCourseLabel,
  getApplicationModeLabel,
  getQualificationLabel,
  getOccupationLabel
} from '../../utils/mapper';
import { formatNumber } from '../../utils/formatter';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

defineProps<{
  studentData: StudentPredictionInput;
}>();

// Track open sections
const openSections = ref({
  identification: true,
  personal: false,
  family: false,
  academic: false
});

const toggleSection = (section: keyof typeof openSections.value) => {
  openSections.value[section] = !openSections.value[section];
};
</script>

<template>
  <div class="space-y-4">
    <!-- Section 1: Identification -->
    <div class="border border-gray-150 dark:border-gray-800 rounded-2xl overflow-hidden transition-colors duration-200">
      <button 
        @click="toggleSection('identification')"
        class="w-full px-5 py-4 bg-gray-50/50 hover:bg-gray-100/40 dark:bg-gray-900/10 dark:hover:bg-gray-800/10 flex items-center justify-between text-left font-bold text-sm text-gray-800 dark:text-gray-200 border-none cursor-pointer"
      >
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-address-card text-primary-500 text-xs"></i>
          <span>{{ t('singlePrediction.sections.identification') }}</span>
        </div>
        <i :class="['fa-solid', openSections.identification ? 'fa-chevron-up' : 'fa-chevron-down', 'text-[10px] text-gray-400']"></i>
      </button>
      
      <div v-show="openSections.identification" class="p-5 bg-white dark:bg-gray-900 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-semibold text-gray-600 dark:text-gray-400">
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.studentCode') }}</span>
          <span class="text-gray-900 dark:text-white font-extrabold">{{ studentData.studentCode || 'N/A' }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.studentName') }}</span>
          <span class="text-gray-900 dark:text-white font-extrabold">{{ studentData.studentName || 'N/A' }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.className') }}</span>
          <span class="text-gray-900 dark:text-white font-bold">{{ studentData.className || 'N/A' }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.faculty') }}</span>
          <span class="text-gray-900 dark:text-white font-bold">{{ studentData.faculty || 'N/A' }}</span>
        </div>
      </div>
    </div>

    <!-- Section 2: Personal & Admission -->
    <div class="border border-gray-150 dark:border-gray-800 rounded-2xl overflow-hidden transition-colors duration-200">
      <button 
        @click="toggleSection('personal')"
        class="w-full px-5 py-4 bg-gray-50/50 hover:bg-gray-100/40 dark:bg-gray-900/10 dark:hover:bg-gray-800/10 flex items-center justify-between text-left font-bold text-sm text-gray-800 dark:text-gray-200 border-none cursor-pointer"
      >
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-user text-primary-500 text-xs"></i>
          <span>{{ t('singlePrediction.sections.personal') }}</span>
        </div>
        <i :class="['fa-solid', openSections.personal ? 'fa-chevron-up' : 'fa-chevron-down', 'text-[10px] text-gray-400']"></i>
      </button>
      
      <div v-show="openSections.personal" class="p-5 bg-white dark:bg-gray-900 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-xs font-semibold text-gray-650 dark:text-gray-400">
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.maritalStatus') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getMaritalStatusLabel(studentData.maritalStatus) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.ageAtEnrollment') }}</span>
          <span class="text-gray-900 dark:text-white">{{ studentData.ageAtEnrollment }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.gender') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getGenderLabel(studentData.gender) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.course') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getCourseLabel(studentData.course) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.applicationMode') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getApplicationModeLabel(studentData.applicationMode) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.applicationOrder') }}</span>
          <span class="text-gray-900 dark:text-white">{{ studentData.applicationOrder }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.daytimeEvening') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getDaytimeEveningLabel(studentData.daytimeEvening) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.previousQualification') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getQualificationLabel(studentData.previousQualification) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.previousQualificationGrade') }}</span>
          <span class="text-gray-900 dark:text-white">{{ formatNumber(studentData.previousQualificationGrade) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.admissionGrade') }}</span>
          <span class="text-gray-900 dark:text-white">{{ formatNumber(studentData.admissionGrade) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.international') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getYesNoLabel(studentData.international) }}</span>
        </div>
      </div>
    </div>

    <!-- Section 3: Family & Financial -->
    <div class="border border-gray-150 dark:border-gray-800 rounded-2xl overflow-hidden transition-colors duration-200">
      <button 
        @click="toggleSection('family')"
        class="w-full px-5 py-4 bg-gray-50/50 hover:bg-gray-100/40 dark:bg-gray-900/10 dark:hover:bg-gray-800/10 flex items-center justify-between text-left font-bold text-sm text-gray-800 dark:text-gray-200 border-none cursor-pointer"
      >
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-wallet text-primary-500 text-xs"></i>
          <span>{{ t('singlePrediction.sections.family') }}</span>
        </div>
        <i :class="['fa-solid', openSections.family ? 'fa-chevron-up' : 'fa-chevron-down', 'text-[10px] text-gray-400']"></i>
      </button>
      
      <div v-show="openSections.family" class="p-5 bg-white dark:bg-gray-900 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-semibold text-gray-650 dark:text-gray-400">
        <div class="sm:col-span-2">
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.motherQualification') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getQualificationLabel(studentData.motherQualification) }}</span>
        </div>
        <div class="sm:col-span-2">
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.fatherQualification') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getQualificationLabel(studentData.fatherQualification) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.motherOccupation') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getOccupationLabel(studentData.motherOccupation) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.fatherOccupation') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getOccupationLabel(studentData.fatherOccupation) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.scholarshipHolder') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getYesNoLabel(studentData.scholarshipHolder) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.debtor') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getYesNoLabel(studentData.debtor) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.tuitionFeesUpToDate') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getYesNoLabel(studentData.tuitionFeesUpToDate) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.displaced') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getYesNoLabel(studentData.displaced) }}</span>
        </div>
        <div>
          <span class="block text-[10px] text-gray-400 uppercase tracking-wider mb-0.5">{{ t('singlePrediction.fields.educationalSpecialNeeds') }}</span>
          <span class="text-gray-900 dark:text-white">{{ getYesNoLabel(studentData.educationalSpecialNeeds) }}</span>
        </div>
      </div>
    </div>

    <!-- Section 4: Academic & Macroeconomics -->
    <div class="border border-gray-150 dark:border-gray-800 rounded-2xl overflow-hidden transition-colors duration-200">
      <button 
        @click="toggleSection('academic')"
        class="w-full px-5 py-4 bg-gray-50/50 hover:bg-gray-100/40 dark:bg-gray-900/10 dark:hover:bg-gray-800/10 flex items-center justify-between text-left font-bold text-sm text-gray-800 dark:text-gray-200 border-none cursor-pointer"
      >
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-chart-line text-primary-500 text-xs"></i>
          <span>{{ t('singlePrediction.sections.academic') }}</span>
        </div>
        <i :class="['fa-solid', openSections.academic ? 'fa-chevron-up' : 'fa-chevron-down', 'text-[10px] text-gray-400']"></i>
      </button>
      
      <div v-show="openSections.academic" class="p-5 bg-white dark:bg-gray-900 space-y-5 text-xs font-semibold text-gray-650 dark:text-gray-400">
        <!-- Semester 1 Grid -->
        <div>
          <h6 class="text-xs font-bold text-gray-850 dark:text-gray-300 border-b border-gray-100 dark:border-gray-800 pb-1 mb-3 uppercase tracking-wider">
            Semester 1 Curricular Units
          </h6>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Credited</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem1Credited }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Enrolled</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem1Enrolled }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Evaluations</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem1Evaluations }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Approved</span>
              <span class="text-gray-950 dark:text-white font-extrabold text-primary-600 dark:text-primary-400">{{ studentData.sem1Approved }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Avg Grade</span>
              <span class="text-gray-900 dark:text-white font-extrabold">{{ formatNumber(studentData.sem1Grade) }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">No Eval</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem1WithoutEvaluations }}</span>
            </div>
          </div>
        </div>

        <!-- Semester 2 Grid -->
        <div>
          <h6 class="text-xs font-bold text-gray-850 dark:text-gray-300 border-b border-gray-100 dark:border-gray-800 pb-1 mb-3 uppercase tracking-wider">
            Semester 2 Curricular Units
          </h6>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Credited</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem2Credited }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Enrolled</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem2Enrolled }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Evaluations</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem2Evaluations }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Approved</span>
              <span class="text-gray-955 dark:text-white font-extrabold text-primary-600 dark:text-primary-400">{{ studentData.sem2Approved }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">Avg Grade</span>
              <span class="text-gray-900 dark:text-white font-extrabold">{{ formatNumber(studentData.sem2Grade) }}</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">No Eval</span>
              <span class="text-gray-900 dark:text-white">{{ studentData.sem2WithoutEvaluations }}</span>
            </div>
          </div>
        </div>

        <!-- Economic Indicators -->
        <div>
          <h6 class="text-xs font-bold text-gray-850 dark:text-gray-300 border-b border-gray-100 dark:border-gray-800 pb-1 mb-3 uppercase tracking-wider">
            Macroeconomic Indexes
          </h6>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">{{ (t('singlePrediction.fields.unemploymentRate') || '').split('(')[0]?.trim() }}</span>
              <span class="text-gray-900 dark:text-white">{{ formatNumber(studentData.unemploymentRate) }}%</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">{{ (t('singlePrediction.fields.inflationRate') || '').split('(')[0]?.trim() }}</span>
              <span class="text-gray-900 dark:text-white">{{ formatNumber(studentData.inflationRate) }}%</span>
            </div>
            <div>
              <span class="block text-[10px] text-gray-400 mb-0.5">{{ (t('singlePrediction.fields.gdp') || '').split('(')[0]?.trim() }}</span>
              <span class="text-gray-900 dark:text-white">{{ formatNumber(studentData.gdp) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

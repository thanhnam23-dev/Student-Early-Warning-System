<script setup lang="ts">
import { ref, computed } from 'vue';
import Card from 'primevue/card';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import ToggleSwitch from 'primevue/toggleswitch';
import type { StudentPredictionInput } from '../../types/student';
import {
  MARITAL_STATUS_OPTIONS,
  GENDER_OPTIONS,
  DAYTIME_EVENING_OPTIONS,
  YES_NO_OPTIONS,
  COURSE_OPTIONS,
  APPLICATION_MODE_OPTIONS,
  QUALIFICATION_OPTIONS,
  OCCUPATION_OPTIONS
} from '../../constants/datasetOptions';
import InputSummaryCard from './InputSummaryCard.vue';
import { useI18n } from 'vue-i18n';

const emit = defineEmits<{
  (e: 'predict', data: StudentPredictionInput): void;
}>();

const { t } = useI18n();
const currentStep = ref(1);
const formErrors = ref<Record<string, string>>({});

// Initialize default student values conforming to standard data types
const form = ref<StudentPredictionInput>({
  studentCode: '',
  studentName: '',
  className: '',
  faculty: '',
  maritalStatus: 1,
  ageAtEnrollment: 18,
  gender: 1,
  nationality: 1,
  international: 0,
  applicationMode: 1,
  applicationOrder: 1,
  course: 9119,
  daytimeEvening: 1,
  previousQualification: 1,
  previousQualificationGrade: 120.0,
  admissionGrade: 125.0,
  motherQualification: 1,
  fatherQualification: 1,
  motherOccupation: 9,
  fatherOccupation: 9,
  scholarshipHolder: 0,
  debtor: 0,
  tuitionFeesUpToDate: 1,
  displaced: 0,
  educationalSpecialNeeds: 0,
  sem1Credited: 0,
  sem1Enrolled: 6,
  sem1Evaluations: 6,
  sem1Approved: 6,
  sem1Grade: 14.2,
  sem1WithoutEvaluations: 0,
  sem2Credited: 0,
  sem2Enrolled: 6,
  sem2Evaluations: 6,
  sem2Approved: 5,
  sem2Grade: 13.8,
  sem2WithoutEvaluations: 0,
  unemploymentRate: 10.8,
  inflationRate: 1.4,
  gdp: 3.5
});

// Setup lookup array for steps header
const steps = computed(() => [
  { value: 1, label: t('singlePrediction.steps.step1') },
  { value: 2, label: t('singlePrediction.steps.step2') },
  { value: 3, label: t('singlePrediction.steps.step3') },
  { value: 4, label: t('singlePrediction.steps.step4') },
  { value: 5, label: t('singlePrediction.steps.step5') }
]);

const maritalStatusOptions = computed(() => 
  MARITAL_STATUS_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.marital.${opt.value}`)
  }))
);

const genderOptions = computed(() => 
  GENDER_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.gender.${opt.value}`)
  }))
);

const daytimeEveningOptions = computed(() => 
  DAYTIME_EVENING_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.shift.${opt.value}`)
  }))
);

const yesNoOptions = computed(() => 
  YES_NO_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.yesNo.${opt.value}`)
  }))
);

const courseOptions = computed(() => 
  COURSE_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.course.${opt.value}`)
  }))
);

const applicationModeOptions = computed(() => 
  APPLICATION_MODE_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.applicationMode.${opt.value}`)
  }))
);

const qualificationOptions = computed(() => 
  QUALIFICATION_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.qualification.${opt.value}`)
  }))
);

const occupationOptions = computed(() => 
  OCCUPATION_OPTIONS.map(opt => ({
    value: opt.value,
    label: t(`options.occupation.${opt.value}`)
  }))
);

const validateStep = (step: number): boolean => {
  formErrors.value = {};
  
  if (step === 1) {
    if (!form.value.studentCode.trim()) formErrors.value.studentCode = t('singlePrediction.errors.studentCode');
    if (!form.value.studentName.trim()) formErrors.value.studentName = t('singlePrediction.errors.studentName');
    if (!form.value.className.trim()) formErrors.value.className = t('singlePrediction.errors.className');
    if (!form.value.faculty.trim()) formErrors.value.faculty = t('singlePrediction.errors.faculty');
  }
  
  if (step === 2) {
    if (!form.value.ageAtEnrollment || form.value.ageAtEnrollment < 10 || form.value.ageAtEnrollment > 100) {
      formErrors.value.ageAtEnrollment = t('singlePrediction.errors.ageAtEnrollment');
    }
    if (form.value.previousQualificationGrade === null || form.value.previousQualificationGrade < 0) {
      formErrors.value.previousQualificationGrade = t('singlePrediction.errors.previousQualificationGrade');
    }
    if (form.value.admissionGrade === null || form.value.admissionGrade < 0) {
      formErrors.value.admissionGrade = t('singlePrediction.errors.admissionGrade');
    }
  }

  return Object.keys(formErrors.value).length === 0;
};

const nextStep = () => {
  if (validateStep(currentStep.value)) {
    if (currentStep.value < 5) {
      currentStep.value += 1;
    }
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value -= 1;
  }
};

const resetForm = () => {
  form.value = {
    studentCode: '',
    studentName: '',
    className: '',
    faculty: '',
    maritalStatus: 1,
    ageAtEnrollment: 18,
    gender: 1,
    nationality: 1,
    international: 0,
    applicationMode: 1,
    applicationOrder: 1,
    course: 9119,
    daytimeEvening: 1,
    previousQualification: 1,
    previousQualificationGrade: 120.0,
    admissionGrade: 125.0,
    motherQualification: 1,
    fatherQualification: 1,
    motherOccupation: 9,
    fatherOccupation: 9,
    scholarshipHolder: 0,
    debtor: 0,
    tuitionFeesUpToDate: 1,
    displaced: 0,
    educationalSpecialNeeds: 0,
    sem1Credited: 0,
    sem1Enrolled: 6,
    sem1Evaluations: 6,
    sem1Approved: 6,
    sem1Grade: 14.2,
    sem1WithoutEvaluations: 0,
    sem2Credited: 0,
    sem2Enrolled: 6,
    sem2Evaluations: 6,
    sem2Approved: 5,
    sem2Grade: 13.8,
    sem2WithoutEvaluations: 0,
    unemploymentRate: 10.8,
    inflationRate: 1.4,
    gdp: 3.5
  };
  currentStep.value = 1;
  formErrors.value = {};
};

const submitForm = () => {
  if (validateStep(5)) {
    emit('predict', form.value);
  }
};

const isScholarshipHolder = computed({
  get: () => form.value.scholarshipHolder === 1,
  set: (val: boolean) => { form.value.scholarshipHolder = val ? 1 : 0; }
});

const isDebtor = computed({
  get: () => form.value.debtor === 1,
  set: (val: boolean) => { form.value.debtor = val ? 1 : 0; }
});

const isTuitionFeesUpToDate = computed({
  get: () => form.value.tuitionFeesUpToDate === 1,
  set: (val: boolean) => { form.value.tuitionFeesUpToDate = val ? 1 : 0; }
});

const isDisplaced = computed({
  get: () => form.value.displaced === 1,
  set: (val: boolean) => { form.value.displaced = val ? 1 : 0; }
});

const isEducationalSpecialNeeds = computed({
  get: () => form.value.educationalSpecialNeeds === 1,
  set: (val: boolean) => { form.value.educationalSpecialNeeds = val ? 1 : 0; }
});

const progressPercent = computed(() => {
  return ((currentStep.value - 1) / 4) * 100;
});
</script>

<template>
  <div class="space-y-6">
    <!-- Stepper Navigation Header (Horizontal for Desktop, Hidden/Stacked on Mobile) -->
    <div class="bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 rounded-2xl p-5 shadow-sm transition-colors duration-200">
      <!-- Desktop layout -->
      <div class="hidden lg:flex items-center justify-between relative z-10">
        <div 
          v-for="step in steps" 
          :key="step.value"
          class="flex flex-col items-center flex-1 relative"
        >
          <!-- Step indicator bullet -->
          <button 
            @click="currentStep >= step.value ? currentStep = step.value : null"
            class="w-9 h-9 rounded-full font-bold text-xs flex items-center justify-center transition-all duration-200 cursor-pointer border-none z-10"
            :class="[
              currentStep === step.value ? 'bg-primary-600 text-white shadow-md shadow-primary-500/20 scale-110' :
              currentStep > step.value ? 'bg-primary-50 text-primary-600 dark:bg-primary-950/30 dark:text-primary-400' :
              'bg-gray-100 text-gray-400 dark:bg-gray-800 dark:text-gray-500'
            ]"
            :disabled="currentStep < step.value"
          >
            <i v-if="currentStep > step.value" class="fa-solid fa-check text-[10px]"></i>
            <span v-else>{{ step.value }}</span>
          </button>
          
          <span 
            class="mt-2 text-[10px] font-extrabold uppercase tracking-wider transition-colors duration-200"
            :class="currentStep === step.value ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400 dark:text-gray-500'"
          >
            {{ step.label }}
          </span>
        </div>
        
        <!-- Progress bar background -->
        <div class="absolute top-[18px] left-[10%] right-[10%] h-0.5 bg-gray-100 dark:bg-gray-800 -z-10 rounded">
          <div 
            class="h-full bg-primary-600 transition-all duration-300 rounded"
            :style="{ width: `${progressPercent}%` }"
          ></div>
        </div>
      </div>

      <!-- Mobile layout -->
      <div class="lg:hidden flex items-center justify-between">
        <div class="space-y-1">
          <span class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest block">
            {{ $t('general.loading').startsWith('L') ? 'Step' : 'Bước' }} {{ currentStep }} / 5
          </span>
          <h4 class="text-sm font-bold text-gray-900 dark:text-white leading-none">
            {{ steps[currentStep - 1]?.label || '' }}
          </h4>
        </div>
        <div class="w-20 bg-gray-100 dark:bg-gray-800 h-2 rounded-full overflow-hidden">
          <div 
            class="h-full bg-primary-600 transition-all duration-300"
            :style="{ width: `${progressPercent}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Active Step Content Area wrapper in Card -->
    <Card class="border border-gray-150 dark:border-gray-800 shadow-sm overflow-visible bg-white dark:bg-gray-900">
      <template #content>
        <!-- STEP 1: Student Information -->
        <transition name="step" mode="out-in">
        <div v-if="currentStep === 1" class="space-y-5">
          <h5 class="text-sm font-bold text-gray-800 dark:text-gray-200 border-b border-gray-100 dark:border-gray-800 pb-2 mb-4">
            {{ $t('singlePrediction.sections.identification') }}
          </h5>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div class="flex flex-col space-y-1.5">
              <label for="studentCode" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.studentCode') }} <span class="text-red-500">*</span></label>
              <InputText id="studentCode" v-model="form.studentCode" :placeholder="$t('singlePrediction.fields.studentCodePlaceholder')" :invalid="!!formErrors.studentCode" class="w-full text-xs font-semibold py-2 px-3 rounded-lg border border-gray-250 dark:border-gray-700 bg-transparent dark:text-white focus:border-primary-500" />
              <small v-if="formErrors.studentCode" class="text-[10px] font-bold text-red-500">{{ formErrors.studentCode }}</small>
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="studentName" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.studentName') }} <span class="text-red-500">*</span></label>
              <InputText id="studentName" v-model="form.studentName" :placeholder="$t('singlePrediction.fields.studentNamePlaceholder')" :invalid="!!formErrors.studentName" class="w-full text-xs font-semibold py-2 px-3 rounded-lg border border-gray-250 dark:border-gray-700 bg-transparent dark:text-white focus:border-primary-500" />
              <small v-if="formErrors.studentName" class="text-[10px] font-bold text-red-500">{{ formErrors.studentName }}</small>
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="className" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.className') }} <span class="text-red-500">*</span></label>
              <InputText id="className" v-model="form.className" :placeholder="$t('singlePrediction.fields.classNamePlaceholder')" :invalid="!!formErrors.className" class="w-full text-xs font-semibold py-2 px-3 rounded-lg border border-gray-250 dark:border-gray-700 bg-transparent dark:text-white focus:border-primary-500" />
              <small v-if="formErrors.className" class="text-[10px] font-bold text-red-500">{{ formErrors.className }}</small>
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="faculty" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.faculty') }} <span class="text-red-500">*</span></label>
              <InputText id="faculty" v-model="form.faculty" :placeholder="$t('singlePrediction.fields.facultyPlaceholder')" :invalid="!!formErrors.faculty" class="w-full text-xs font-semibold py-2 px-3 rounded-lg border border-gray-250 dark:border-gray-700 bg-transparent dark:text-white focus:border-primary-500" />
              <small v-if="formErrors.faculty" class="text-[10px] font-bold text-red-500">{{ formErrors.faculty }}</small>
            </div>
          </div>
          <div class="p-3 bg-primary-50/50 dark:bg-primary-950/15 border border-primary-100 dark:border-primary-900/30 rounded-xl text-[11px] text-primary-600 dark:text-primary-400 font-semibold leading-normal">
            <i class="fa-solid fa-circle-info mr-1 text-xs"></i>
            {{ $t('singlePrediction.identificationNote') }}
          </div>
        </div>

        <!-- STEP 2: Personal & Entry Info -->
        <div v-else-if="currentStep === 2" class="space-y-5">
          <h5 class="text-sm font-bold text-gray-800 dark:text-gray-200 border-b border-gray-100 dark:border-gray-800 pb-2 mb-4">
            {{ $t('singlePrediction.sections.personal') }}
          </h5>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.maritalStatus') }}</label>
              <Dropdown v-model="form.maritalStatus" :options="maritalStatusOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="age" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.ageAtEnrollment') }} <span class="text-red-500">*</span></label>
              <InputNumber id="age" v-model="form.ageAtEnrollment" :min="10" :max="100" :invalid="!!formErrors.ageAtEnrollment" class="w-full text-xs" />
              <small v-if="formErrors.ageAtEnrollment" class="text-[10px] font-bold text-red-500">{{ formErrors.ageAtEnrollment }}</small>
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.gender') }}</label>
              <Dropdown v-model="form.gender" :options="genderOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.course') }}</label>
              <Dropdown v-model="form.course" :options="courseOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.applicationMode') }}</label>
              <Dropdown v-model="form.applicationMode" :options="applicationModeOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="appOrder" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.applicationOrder') }}</label>
              <InputNumber id="appOrder" v-model="form.applicationOrder" :min="1" class="w-full text-xs" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.daytimeEvening') }}</label>
              <Dropdown v-model="form.daytimeEvening" :options="daytimeEveningOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.previousQualification') }}</label>
              <Dropdown v-model="form.previousQualification" :options="qualificationOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="prevGrade" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.previousQualificationGrade') }} <span class="text-red-500">*</span></label>
              <InputNumber id="prevGrade" v-model="form.previousQualificationGrade" :min="0" :max="200" :minFractionDigits="1" :maxFractionDigits="2" :invalid="!!formErrors.previousQualificationGrade" class="w-full text-xs" />
              <small v-if="formErrors.previousQualificationGrade" class="text-[10px] font-bold text-red-500">{{ formErrors.previousQualificationGrade }}</small>
            </div>
            <div class="flex flex-col space-y-1.5">
              <label for="admGrade" class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.admissionGrade') }} <span class="text-red-500">*</span></label>
              <InputNumber id="admGrade" v-model="form.admissionGrade" :min="0" :max="200" :minFractionDigits="1" :maxFractionDigits="2" :invalid="!!formErrors.admissionGrade" class="w-full text-xs" />
              <small v-if="formErrors.admissionGrade" class="text-[10px] font-bold text-red-500">{{ formErrors.admissionGrade }}</small>
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.international') }}</label>
              <Dropdown v-model="form.international" :options="yesNoOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
          </div>
        </div>

        <!-- STEP 3: Family & Financial Info -->
        <div v-else-if="currentStep === 3" class="space-y-5">
          <h5 class="text-sm font-bold text-gray-800 dark:text-gray-200 border-b border-gray-100 dark:border-gray-800 pb-2 mb-4">
            {{ $t('singlePrediction.sections.family') }}
          </h5>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.motherQualification') }}</label>
              <Dropdown v-model="form.motherQualification" :options="qualificationOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.fatherQualification') }}</label>
              <Dropdown v-model="form.fatherQualification" :options="qualificationOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.motherOccupation') }}</label>
              <Dropdown v-model="form.motherOccupation" :options="occupationOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
            <div class="flex flex-col space-y-1.5">
              <label class="text-xs font-bold text-gray-550 dark:text-gray-400">{{ $t('singlePrediction.fields.fatherOccupation') }}</label>
              <Dropdown v-model="form.fatherOccupation" :options="occupationOptions" optionLabel="label" optionValue="value" class="w-full text-xs font-semibold border border-gray-250 dark:border-gray-700 bg-transparent rounded-lg" />
            </div>
          </div>
          
          <div class="border-t border-gray-100 dark:border-gray-800 pt-5 mt-5">
            <h6 class="text-xs font-extrabold text-gray-400 uppercase tracking-wider mb-4">{{ $t('singlePrediction.sections.financial') }}</h6>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
              <!-- Scholarship -->
              <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                <div class="flex flex-col space-y-0.5">
                  <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ $t('singlePrediction.fields.scholarshipHolder') }}</span>
                  <span class="text-[10px] text-gray-400 font-semibold">{{ $t('general.loading').startsWith('L') ? 'Active school scholarship' : 'Học bổng đang hoạt động' }}</span>
                </div>
                <ToggleSwitch v-model="isScholarshipHolder" />
              </div>
              
              <!-- Debtor -->
              <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                <div class="flex flex-col space-y-0.5">
                  <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ $t('singlePrediction.fields.debtor') }}</span>
                  <span class="text-[10px] text-gray-400 font-semibold">{{ $t('general.loading').startsWith('L') ? 'Has tuition/fees arrears' : 'Đang nợ học phí' }}</span>
                </div>
                <ToggleSwitch v-model="isDebtor" />
              </div>

              <!-- Tuition up to date -->
              <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                <div class="flex flex-col space-y-0.5">
                  <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ $t('singlePrediction.fields.tuitionFeesUpToDate') }}</span>
                  <span class="text-[10px] text-gray-400 font-semibold">{{ $t('general.loading').startsWith('L') ? 'Fees are fully up to date' : 'Đã đóng đủ học phí' }}</span>
                </div>
                <ToggleSwitch v-model="isTuitionFeesUpToDate" />
              </div>

              <!-- Displaced -->
              <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                <div class="flex flex-col space-y-0.5">
                  <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ $t('singlePrediction.fields.displaced') }}</span>
                  <span class="text-[10px] text-gray-400 font-semibold">{{ $t('general.loading').startsWith('L') ? 'Living away from home' : 'Đang trọ học xa nhà' }}</span>
                </div>
                <ToggleSwitch v-model="isDisplaced" />
              </div>

              <!-- Special educational needs -->
              <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                <div class="flex flex-col space-y-0.5">
                  <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ $t('singlePrediction.fields.educationalSpecialNeeds') }}</span>
                  <span class="text-[10px] text-gray-400 font-semibold">{{ $t('general.loading').startsWith('L') ? 'Requires educational aid' : 'Cần hỗ trợ đặc biệt' }}</span>
                </div>
                <ToggleSwitch v-model="isEducationalSpecialNeeds" />
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 4: Academic Performance & Macroeconomics -->
        <div v-else-if="currentStep === 4" class="space-y-6">
          <!-- Semester 1 -->
          <div class="bg-gray-50 dark:bg-gray-800/30 border border-gray-100 dark:border-gray-800 rounded-xl p-4">
            <h5 class="text-xs font-extrabold text-gray-500 dark:text-gray-400 pb-2 mb-4 uppercase tracking-wider border-b border-gray-200 dark:border-gray-700">
              {{ $t('general.loading').startsWith('L') ? 'Semester 1 Academic Performance' : 'Kết Quả Học Tập Học Kỳ 1' }}
            </h5>
            <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3">
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem1Cred" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Units Credited' : 'Tín Chỉ Miễn Giảm' }}</label>
                <InputNumber id="sem1Cred" v-model="form.sem1Credited" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem1Enrolled" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Units Enrolled' : 'Tín Chỉ Đăng Ký' }}</label>
                <InputNumber id="sem1Enrolled" v-model="form.sem1Enrolled" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem1Eval" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Evaluations' : 'Lượt Đánh Giá' }}</label>
                <InputNumber id="sem1Eval" v-model="form.sem1Evaluations" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem1Appr" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Approved Units' : 'Tín Chỉ Đạt' }}</label>
                <InputNumber id="sem1Appr" v-model="form.sem1Approved" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem1Grade" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight">{{ $t('general.loading').startsWith('L') ? 'Avg. Grade (0-20)' : 'Điểm TB (0-20)' }}</label>
                <InputNumber id="sem1Grade" v-model="form.sem1Grade" :min="0" :max="20" :minFractionDigits="1" :maxFractionDigits="2" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem1NoEval" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'No Evaluation' : 'Không Đánh Giá' }}</label>
                <InputNumber id="sem1NoEval" v-model="form.sem1WithoutEvaluations" :min="0" fluid />
              </div>
            </div>
          </div>

          <!-- Semester 2 -->
          <div class="bg-gray-50 dark:bg-gray-800/30 border border-gray-100 dark:border-gray-800 rounded-xl p-4">
            <h5 class="text-xs font-extrabold text-gray-500 dark:text-gray-400 pb-2 mb-4 uppercase tracking-wider border-b border-gray-200 dark:border-gray-700">
              {{ $t('general.loading').startsWith('L') ? 'Semester 2 Academic Performance' : 'Kết Quả Học Tập Học Kỳ 2' }}
            </h5>
            <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3">
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem2Cred" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Units Credited' : 'Tín Chỉ Miễn Giảm' }}</label>
                <InputNumber id="sem2Cred" v-model="form.sem2Credited" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem2Enrolled" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Units Enrolled' : 'Tín Chỉ Đăng Ký' }}</label>
                <InputNumber id="sem2Enrolled" v-model="form.sem2Enrolled" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem2Eval" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Evaluations' : 'Lượt Đánh Giá' }}</label>
                <InputNumber id="sem2Eval" v-model="form.sem2Evaluations" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem2Appr" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'Approved Units' : 'Tín Chỉ Đạt' }}</label>
                <InputNumber id="sem2Appr" v-model="form.sem2Approved" :min="0" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem2Grade" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight">{{ $t('general.loading').startsWith('L') ? 'Avg. Grade (0-20)' : 'Điểm TB (0-20)' }}</label>
                <InputNumber id="sem2Grade" v-model="form.sem2Grade" :min="0" :max="20" :minFractionDigits="1" :maxFractionDigits="2" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="sem2NoEval" class="text-[10px] font-bold text-gray-500 dark:text-gray-400 leading-tight truncate">{{ $t('general.loading').startsWith('L') ? 'No Evaluation' : 'Không Đánh Giá' }}</label>
                <InputNumber id="sem2NoEval" v-model="form.sem2WithoutEvaluations" :min="0" fluid />
              </div>
            </div>
          </div>

          <!-- Economic indicators -->
          <div class="bg-gray-50 dark:bg-gray-800/30 border border-gray-100 dark:border-gray-800 rounded-xl p-4">
            <h5 class="text-xs font-extrabold text-gray-500 dark:text-gray-400 pb-2 mb-4 uppercase tracking-wider border-b border-gray-200 dark:border-gray-700">
              {{ $t('general.loading').startsWith('L') ? 'National Economic Indicators' : 'Chỉ Số Kinh Tế Vĩ Mô' }}
            </h5>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="unemp" class="text-xs font-bold text-gray-500 dark:text-gray-400">{{ $t('singlePrediction.fields.unemploymentRate') }}</label>
                <InputNumber id="unemp" v-model="form.unemploymentRate" :minFractionDigits="1" :maxFractionDigits="2" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="infl" class="text-xs font-bold text-gray-500 dark:text-gray-400">{{ $t('singlePrediction.fields.inflationRate') }}</label>
                <InputNumber id="infl" v-model="form.inflationRate" :minFractionDigits="1" :maxFractionDigits="2" fluid />
              </div>
              <div class="flex flex-col space-y-1.5 min-w-0">
                <label for="gdp" class="text-xs font-bold text-gray-500 dark:text-gray-400">{{ $t('singlePrediction.fields.gdp') }}</label>
                <InputNumber id="gdp" v-model="form.gdp" :minFractionDigits="1" :maxFractionDigits="2" fluid />
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 5: Review -->
        <div v-else-if="currentStep === 5" class="space-y-5">
          <div class="space-y-1 pb-1">
            <h5 class="text-sm font-bold text-gray-800 dark:text-gray-200">
              {{ $t('singlePrediction.sections.review') }}
            </h5>
            <p class="text-xs font-medium text-gray-400 dark:text-gray-550">
              {{ $t('general.loading').startsWith('L') ? 'Review entered demographic, admission, family, financial, and academic indicators before running the AI simulation.' : 'Kiểm tra lại các chỉ số nhân khẩu học, tuyển sinh, gia cảnh, tài chính và học tập trước khi chạy mô hình AI.' }}
            </p>
          </div>
          
          <InputSummaryCard :studentData="form" />
        </div>
        </transition>
      </template>
    </Card>

    <!-- Navigation Control Buttons -->
    <div class="flex items-center justify-between">
      <Button 
        :label="$t('general.loading').startsWith('L') ? 'Reset Form' : 'Đặt Lại'"
        icon="fa-solid fa-arrows-rotate"
        severity="secondary"
        @click="resetForm"
        class="text-xs font-semibold px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl cursor-pointer"
      />
      
      <div class="flex items-center space-x-3">
        <Button 
          v-if="currentStep > 1"
          :label="$t('general.back')"
          icon="fa-solid fa-chevron-left"
          severity="secondary"
          @click="prevStep"
          class="text-xs font-semibold px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl cursor-pointer"
        />
        
        <Button 
          v-if="currentStep < 5"
          :label="$t('general.next')"
          icon="fa-solid fa-chevron-right"
          iconPos="right"
          @click="nextStep"
          class="text-xs font-semibold px-5 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl cursor-pointer shadow-md shadow-primary-500/20"
        />
        
        <Button 
          v-else
          :label="$t('singlePrediction.triggerPredict')"
          icon="fa-solid fa-brain"
          @click="submitForm"
          class="text-xs font-semibold px-5 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl cursor-pointer shadow-md shadow-primary-500/20"
        />
      </div>
    </div>
  </div>
</template>

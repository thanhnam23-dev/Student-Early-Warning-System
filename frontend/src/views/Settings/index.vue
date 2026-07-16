<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useSettingsStore } from '../../stores/settings.store';
import PageHeader from '../../components/common/PageHeader.vue';
import Card from 'primevue/card';
import ToggleSwitch from 'primevue/toggleswitch';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import LanguageSelector from '../../components/settings/LanguageSelector.vue';
import AppearanceCard from '../../components/settings/AppearanceCard.vue';
import SystemInfoCard from '../../components/settings/SystemInfoCard.vue';

const { t } = useI18n();
const settingsStore = useSettingsStore();

// Track active settings tab
const activeTab = ref('appearance');

const tabs = [
  { id: 'overview', titleVi: 'Tổng Quan', titleEn: 'Overview', descVi: 'Thông tin hệ thống', descEn: 'System specifications', icon: 'fa-solid fa-sliders' },
  { id: 'appearance', titleVi: 'Giao Diện', titleEn: 'Appearance', descVi: 'Giao diện và hiển thị', descEn: 'Theme and display options', icon: 'fa-solid fa-palette' },
  { id: 'language', titleVi: 'Ngôn Ngữ', titleEn: 'Language', descVi: 'Ngôn ngữ hiển thị', descEn: 'System active language', icon: 'fa-solid fa-language' },
  { id: 'notifications', titleVi: 'Thông Báo', titleEn: 'Notifications', descVi: 'Cài đặt thông báo', descEn: 'Advisory email alerts', icon: 'fa-solid fa-bell' },
  { id: 'system', titleVi: 'Hệ Thống', titleEn: 'System Specs', descVi: 'Cài đặt phần cứng/API', descEn: 'Server API bindings', icon: 'fa-solid fa-microchip' },
  { id: 'about', titleVi: 'Giới Thiệu', titleEn: 'About Us', descVi: 'Về hệ thống & nhóm', descEn: 'Project credits & team', icon: 'fa-solid fa-circle-info' }
];

// Mock notification options
const emailAlerts = ref(true);
const studentArrearsAlerts = ref(false);
const weeklyDigests = ref(true);

// Mock system endpoint inputs
const fastapiEndpoint = ref('http://localhost:8000/api/v1/predict');
const laravelEndpoint = ref('http://localhost:8000/api');
const modelName = ref('XGBoost_UCI_v1.0.bin');
</script>

<template>
  <div class="space-y-6 max-w-5xl mx-auto font-sans p-2">
    <!-- Settings Header Layout -->
    <div class="flex items-center justify-between">
      <div class="space-y-1">
        <h2 class="text-xl font-bold text-gray-850 dark:text-white tracking-tight leading-tight">
          {{ settingsStore.language === 'vi' ? 'Cài Đặt' : 'System Settings' }}
        </h2>
        <p class="text-xs text-gray-400 font-semibold leading-normal">
          {{ settingsStore.language === 'vi' ? 'Tùy chỉnh giao diện và thiết lập hệ thống theo nhu cầu của bạn' : 'Configure interface preferences, languages, and endpoint parameters.' }}
        </p>
      </div>

      <!-- Gear Graphic illustration in Header -->
      <div class="hidden sm:flex w-16 h-16 items-center justify-center bg-primary-50 dark:bg-primary-950/20 text-primary-600 dark:text-primary-400 rounded-2xl border border-primary-100 dark:border-primary-900 shadow-sm animate-spin-slow">
        <i class="fa-solid fa-gear text-3xl"></i>
      </div>
    </div>

    <!-- Main Grid Content -->
    <div class="grid grid-cols-12 gap-6 items-start">
      <!-- Left Side: Tabs Selection -->
      <div class="col-span-12 md:col-span-4 space-y-2.5">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          @click="activeTab = tab.id"
          class="w-full flex items-center p-3 rounded-xl border text-left cursor-pointer transition-all duration-200 group font-bold"
          :class="[
            activeTab === tab.id
              ? 'border-primary-500 bg-primary-50/20 text-primary-600 dark:bg-primary-950/20 dark:text-primary-400 shadow-sm'
              : 'border-gray-150 bg-white hover:bg-gray-50/50 hover:border-gray-300 text-gray-700 dark:bg-gray-900 dark:border-gray-800 dark:text-gray-400'
          ]"
        >
          <div class="flex items-center space-x-3 w-full">
            <div 
              class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors shrink-0"
              :class="activeTab === tab.id ? 'bg-primary-500/20 text-primary-600 dark:text-primary-400' : 'bg-gray-50 dark:bg-gray-800 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300'"
            >
              <i :class="[tab.icon, 'text-sm']"></i>
            </div>
            <div class="flex-1 min-w-0">
              <span class="block text-xs font-bold leading-tight select-none">
                {{ settingsStore.language === 'vi' ? tab.titleVi : tab.titleEn }}
              </span>
              <span class="block text-[9px] text-gray-400 dark:text-gray-500 font-semibold leading-normal mt-0.5 select-none truncate">
                {{ settingsStore.language === 'vi' ? tab.descVi : tab.descEn }}
              </span>
            </div>
          </div>
        </button>
      </div>

      <!-- Right Side: Selected Content Panel View -->
      <div class="col-span-12 md:col-span-8">
        
        <!-- 1. APPEARANCE TAB -->
        <AppearanceCard v-if="activeTab === 'appearance'" />

        <!-- 2. LANGUAGE TAB -->
        <Card v-else-if="activeTab === 'language'" class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden transition-colors duration-200">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-800 dark:text-gray-200">
              <i class="fa-solid fa-language text-primary-500 text-xs"></i>
              <span>{{ settingsStore.language === 'vi' ? 'Cấu Hứng Ngôn Ngữ' : 'Language Configuration' }}</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-4">
              <p class="text-xs text-gray-400 font-semibold leading-normal pb-2">
                {{ settingsStore.language === 'vi' ? 'Chọn ngôn ngữ hiển thị chính thức của toàn bộ hệ thống.' : 'Select the primary layout display language across administrative elements.' }}
              </p>
              <LanguageSelector />
            </div>
          </template>
        </Card>

        <!-- 3. SYSTEM OVERVIEW TAB -->
        <SystemInfoCard v-else-if="activeTab === 'overview'" />

        <!-- 4. NOTIFICATIONS TAB (Mock panel) -->
        <Card v-else-if="activeTab === 'notifications'" class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden transition-colors duration-200">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-800 dark:text-gray-200">
              <i class="fa-solid fa-bell text-primary-500 text-xs"></i>
              <span>{{ settingsStore.language === 'vi' ? 'Cài Đặt Thông Báo' : 'Notifications Settings' }}</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-4">
              <p class="text-xs text-gray-400 font-semibold leading-normal mb-2">
                {{ settingsStore.language === 'vi' ? 'Định cấu hình các cảnh báo tự động gửi về Email hoặc Telegram của cố vấn học tập.' : 'Configure custom notifications thresholds and advisor digest schedules.' }}
              </p>
              
              <div class="space-y-4 pt-2">
                <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                  <div class="flex flex-col space-y-0.5">
                    <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ settingsStore.language === 'vi' ? 'Cảnh báo Email tự động' : 'Automatic Email Warnings' }}</span>
                    <span class="text-[10px] text-gray-400 font-semibold">{{ settingsStore.language === 'vi' ? 'Gửi mail khi phát hiện sinh viên rủi ro bỏ học rất cao.' : 'Alert advisor instantly when critical risks exceed 90%.' }}</span>
                  </div>
                  <ToggleSwitch v-model="emailAlerts" />
                </div>

                <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                  <div class="flex flex-col space-y-0.5">
                    <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ settingsStore.language === 'vi' ? 'Cảnh báo nợ học phí' : 'Tuition Fees Arrears Alert' }}</span>
                    <span class="text-[10px] text-gray-400 font-semibold">{{ settingsStore.language === 'vi' ? 'Cảnh báo định kỳ khi nợ học phí của sinh viên kéo dài.' : 'Alert warnings for students with unresolved financial arrears.' }}</span>
                  </div>
                  <ToggleSwitch v-model="studentArrearsAlerts" />
                </div>

                <div class="flex items-center justify-between p-3.5 bg-gray-50/50 dark:bg-gray-800/40 rounded-xl border border-gray-150 dark:border-gray-800">
                  <div class="flex flex-col space-y-0.5">
                    <span class="text-xs font-bold text-gray-850 dark:text-gray-200">{{ settingsStore.language === 'vi' ? 'Nhận báo cáo hàng tuần' : 'Weekly Status Digest' }}</span>
                    <span class="text-[10px] text-gray-400 font-semibold">{{ settingsStore.language === 'vi' ? 'Tóm tắt tổng số lượt cảnh báo học vụ mỗi cuối tuần.' : 'Send weekly metrics report to registered email.' }}</span>
                  </div>
                  <ToggleSwitch v-model="weeklyDigests" />
                </div>
              </div>
            </div>
          </template>
        </Card>

        <!-- 5. ADVANCED SYSTEM BINDINGS (Mock panel) -->
        <Card v-else-if="activeTab === 'system'" class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden transition-colors duration-200">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-800 dark:text-gray-200">
              <i class="fa-solid fa-microchip text-primary-500 text-xs"></i>
              <span>{{ settingsStore.language === 'vi' ? 'Cấu Hình Tích Hợp API / AI' : 'API & System Configurations' }}</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-5">
              <p class="text-xs text-gray-400 font-semibold leading-normal pb-2">
                {{ settingsStore.language === 'vi' ? 'Định cấu hình các đường dẫn API Gateway phục vụ tích hợp sau này.' : 'Set up model endpoint URLs and authentication credentials for backend integration.' }}
              </p>
              
              <div class="space-y-4">
                <div class="flex flex-col space-y-1.5">
                  <label class="text-[10px] font-bold text-gray-450 uppercase tracking-wider">{{ settingsStore.language === 'vi' ? 'API Dự đoán (FastAPI AI Server)' : 'AI Prediction Endpoint (FastAPI)' }}</label>
                  <InputText v-model="fastapiEndpoint" class="text-xs w-full bg-gray-50 border-gray-200 font-semibold rounded-lg" />
                </div>

                <div class="flex flex-col space-y-1.5">
                  <label class="text-[10px] font-bold text-gray-450 uppercase tracking-wider">{{ settingsStore.language === 'vi' ? 'API Quản trị (Laravel Dashboard Service)' : 'Admin Dashboard Gateway API' }}</label>
                  <InputText v-model="laravelEndpoint" class="text-xs w-full bg-gray-50 border-gray-200 font-semibold rounded-lg" />
                </div>

                <div class="flex flex-col space-y-1.5">
                  <label class="text-[10px] font-bold text-gray-450 uppercase tracking-wider">{{ settingsStore.language === 'vi' ? 'Tên Tệp Mô Hình AI Đang Chạy' : 'Active Model Filename' }}</label>
                  <InputText v-model="modelName" class="text-xs w-full bg-gray-50 border-gray-200 font-semibold rounded-lg" />
                </div>
              </div>

              <div class="flex justify-end pt-3">
                <Button :label="settingsStore.language === 'vi' ? 'Lưu Kết Nối' : 'Save Connection'" class="bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-xs font-semibold px-5 py-2 cursor-pointer shadow-md shadow-primary-500/20" />
              </div>
            </div>
          </template>
        </Card>

        <!-- 6. ABOUT THE TEAM TAB -->
        <Card v-else-if="activeTab === 'about'" class="border border-gray-150 dark:border-gray-800 shadow-sm bg-white dark:bg-gray-900 overflow-hidden transition-colors duration-200">
          <template #title>
            <div class="px-5 pt-4 flex items-center space-x-2 text-xs font-bold text-gray-800 dark:text-gray-200">
              <i class="fa-solid fa-circle-info text-primary-500 text-xs"></i>
              <span>{{ t('about.overview.title') }}</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-4 text-xs font-semibold text-gray-655 dark:text-gray-400 leading-relaxed">
              <p>{{ t('about.overview.p1') }}</p>
              <div class="border-t border-gray-100 dark:border-gray-800 my-3"></div>
              <div class="flex flex-col space-y-2.5 text-[11px]">
                <div>
                  <span class="text-gray-400 uppercase text-[9px] tracking-wider block font-bold">{{ t('about.team.lead') }}</span>
                  <span class="text-gray-800 dark:text-white font-extrabold">{{ t('about.team.leadName') }}</span>
                </div>
                <div>
                  <span class="text-gray-400 uppercase text-[9px] tracking-wider block font-bold">{{ t('about.team.sponsor') }}</span>
                  <span class="text-gray-800 dark:text-white font-extrabold">{{ t('about.team.sponsorName') }}</span>
                </div>
                <div>
                  <span class="text-gray-400 uppercase text-[9px] tracking-wider block font-bold">{{ settingsStore.language === 'vi' ? 'Cơ Quan Chủ Quản' : 'Institution' }}</span>
                  <span class="text-gray-800 dark:text-white font-extrabold">{{ t('about.team.initiative') }}</span>
                </div>
              </div>
            </div>
          </template>
        </Card>

      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-spin-slow {
  animation: spin 8s linear infinite;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>

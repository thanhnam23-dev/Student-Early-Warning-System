<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { useSettingsStore } from '../stores/settings.store';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import AppHeader from '../components/layout/AppHeader.vue';
import AppSidebar from '../components/layout/AppSidebar.vue';
import AppFooter from '../components/layout/AppFooter.vue';
import ConfirmDialog from '../components/common/ConfirmDialog.vue';

const settingsStore = useSettingsStore();
const route = useRoute();
const i18n = useI18n();

const mainContentRef = ref<HTMLElement | null>(null);
const isScrolled = ref(false);
const showBackToTop = ref(false);

const scrollCache = new Map<string, number>();

const supportsViewTransition = computed(() => {
  return typeof document !== 'undefined' && 'startViewTransition' in document && settingsStore.motionEffects;
});

const hasAurora = computed(() => {
  return ['/', '/dashboard', '/settings', '/about'].includes(route.path);
});

const handleScroll = (e: Event) => {
  const target = e.target as HTMLElement;
  isScrolled.value = target.scrollTop > 10;
  showBackToTop.value = target.scrollTop > 300;
};

const scrollToTop = () => {
  if (mainContentRef.value) {
    mainContentRef.value.scrollTo({
      top: 0,
      behavior: settingsStore.motionEffects ? 'smooth' : 'auto'
    });
  }
};

watch(
  () => route.fullPath,
  (newPath, oldPath) => {
    if (oldPath && mainContentRef.value) {
      scrollCache.set(oldPath, mainContentRef.value.scrollTop);
    }
    
    nextTick(() => {
      if (mainContentRef.value) {
        const saved = scrollCache.get(newPath);
        if (saved !== undefined) {
          mainContentRef.value.scrollTop = saved;
        } else {
          mainContentRef.value.scrollTop = 0;
        }
      }
    });
  }
);

onMounted(() => {
  i18n.locale.value = settingsStore.language;
});
</script>

<template>
  <div class="h-screen w-screen bg-slate-50 dark:bg-[#080b11] flex flex-col font-sans transition-colors duration-300 relative overflow-hidden">
    <!-- Layer 4: Subtle Noise Texture (Global) -->
    <div class="noise-overlay pointer-events-none fixed inset-0 z-0"></div>

    <!-- Layer 3: Slow-Moving Aurora Blobs (Scoped to Hero Pages + Motion Effects = ON) -->
    <div 
      v-if="settingsStore.motionEffects && hasAurora"
      class="aurora-container pointer-events-none fixed inset-0 z-0 overflow-hidden"
    >
      <div class="absolute -top-[15%] -left-[10%] w-[55vw] h-[55vw] rounded-full bg-gradient-to-br from-primary-500/8 to-indigo-500/0 dark:from-primary-500/12 dark:to-transparent blur-[120px] blob-float-1"></div>
      <div class="absolute top-[30%] -right-[15%] w-[60vw] h-[60vw] rounded-full bg-gradient-to-br from-purple-500/8 to-pink-500/0 dark:from-purple-500/12 dark:to-transparent blur-[140px] blob-float-2"></div>
      <div class="absolute -bottom-[15%] left-[10%] w-[50vw] h-[50vw] rounded-full bg-gradient-to-br from-cyan-500/4 to-blue-500/0 dark:from-cyan-500/8 dark:to-transparent blur-[110px] blob-float-3"></div>
    </div>

    <!-- Fixed Header -->
    <AppHeader :is-scrolled="isScrolled" class="z-40" />

    <!-- Body: Sidebar + Main Content Area -->
    <div class="flex-1 flex overflow-hidden w-full relative z-10">
      <!-- Translucent Backdrop Overlay (Mobile only, triggers drawer collapse) -->
      <div 
        v-if="settingsStore.mobileSidebarOpen" 
        @click="settingsStore.setMobileSidebar(false)"
        class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-30 md:hidden transition-opacity duration-300"
      ></div>

      <!-- Sidebar (Docked on desktop, drawer on mobile) -->
      <AppSidebar />

      <!-- Main scrollable content window -->
      <main 
        ref="mainContentRef"
        @scroll="handleScroll"
        class="flex-1 p-6 md:p-8 overflow-y-auto w-full max-w-full relative h-full scroll-smooth"
      >
        <router-view v-slot="{ Component }">
          <transition :name="supportsViewTransition ? '' : 'page'" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- Floating Back to Top Button -->
    <Transition name="fade">
      <button 
        v-if="showBackToTop" 
        @click="scrollToTop"
        class="fixed bottom-6 right-6 w-9 h-9 rounded-xl bg-white hover:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700
               flex items-center justify-center border border-gray-200 dark:border-gray-700/60
               text-gray-500 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400
               cursor-pointer shadow-lg shadow-gray-200/50 dark:shadow-[#05070c]/50 z-30 transition-all duration-200 hover:scale-105 active:scale-95"
        :title="settingsStore.language === 'vi' ? 'Lên đầu trang' : 'Back to top'"
      >
        <i class="fa-solid fa-arrow-up text-xs"></i>
      </button>
    </Transition>

    <!-- Popups -->
    <ConfirmDialog class="z-50" />
    <AppFooter class="z-10 flex-shrink-0" />
  </div>
</template>

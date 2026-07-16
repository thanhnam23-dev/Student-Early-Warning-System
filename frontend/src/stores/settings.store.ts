import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSettingsStore = defineStore('settings', () => {
  const defaultLang = (localStorage.getItem('language') || 'en') as 'en' | 'vi';
  const defaultTheme = (localStorage.getItem('themeColor') || 'blue') as
    | 'blue'
    | 'green'
    | 'purple'
    | 'orange'
    | 'red'
    | 'teal';
  const defaultAppearance = (localStorage.getItem('appearance') || 'light') as 'light' | 'dark';
  const defaultMotion = localStorage.getItem('motionEffects') !== 'false';

  const language = ref<'en' | 'vi'>(defaultLang);
  const themeColor = ref<
    'blue' | 'green' | 'purple' | 'orange' | 'red' | 'teal'
  >(defaultTheme);
  const appearance = ref<'light' | 'dark'>(defaultAppearance);
  const compactMode = ref<boolean>(
    localStorage.getItem('compactMode') === 'true'
  );
  const motionEffects = ref<boolean>(defaultMotion);
  const mobileSidebarOpen = ref<boolean>(false);

  const applyTheme = (color: typeof themeColor.value) => {
    const root = document.documentElement;
    const themeClasses = [
      'theme-blue',
      'theme-green',
      'theme-purple',
      'theme-orange',
      'theme-red',
      'theme-teal',
    ];
    themeClasses.forEach((cls) => root.classList.remove(cls));
    root.classList.add(`theme-${color}`);
  };

  const applyAppearance = (mode: typeof appearance.value) => {
    const root = document.documentElement;
    if (mode === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  };

  const applyMotionEffects = (enabled: boolean) => {
    const root = document.documentElement;
    if (enabled) {
      root.classList.remove('no-transitions');
      root.classList.add('premium-effects');
    } else {
      root.classList.add('no-transitions');
      root.classList.remove('premium-effects');
    }
  };

  // Initialize values on boot
  applyTheme(defaultTheme);
  applyAppearance(defaultAppearance);
  applyMotionEffects(defaultMotion);

  const setLanguage = (lang: 'en' | 'vi', i18nInstance?: any) => {
    language.value = lang;
    localStorage.setItem('language', lang);
    if (i18nInstance) {
      i18nInstance.locale.value = lang;
    }
  };

  const setThemeColor = (color: typeof themeColor.value) => {
    themeColor.value = color;
    localStorage.setItem('themeColor', color);
    applyTheme(color);
  };

  const setAppearance = (mode: typeof appearance.value) => {
    appearance.value = mode;
    localStorage.setItem('appearance', mode);
    
    const root = document.documentElement;
    if (motionEffects.value) {
      root.classList.add('theme-transition');
      applyAppearance(mode);
      setTimeout(() => {
        root.classList.remove('theme-transition');
      }, 300);
    } else {
      applyAppearance(mode);
    }
  };

  const setCompactMode = (mode: boolean) => {
    compactMode.value = mode;
    localStorage.setItem('compactMode', String(mode));
  };

  const setMotionEffects = (enabled: boolean) => {
    motionEffects.value = enabled;
    localStorage.setItem('motionEffects', String(enabled));
    applyMotionEffects(enabled);
  };

  const setMobileSidebar = (val: boolean) => {
    mobileSidebarOpen.value = val;
  };

  const toggleMobileSidebar = () => {
    mobileSidebarOpen.value = !mobileSidebarOpen.value;
  };

  return {
    language,
    themeColor,
    appearance,
    compactMode,
    motionEffects,
    mobileSidebarOpen,
    setLanguage,
    setThemeColor,
    setAppearance,
    setCompactMode,
    setMotionEffects,
    setMobileSidebar,
    toggleMobileSidebar,
  };
});

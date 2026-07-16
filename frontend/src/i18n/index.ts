import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import vi from './locales/vi.json';

const savedLang = localStorage.getItem('language') || 'en';

const i18n = createI18n({
  legacy: false, // Compulsory for Vue 3 Composition API
  locale: savedLang,
  fallbackLocale: 'en',
  messages: {
    en,
    vi,
  },
});

export default i18n;

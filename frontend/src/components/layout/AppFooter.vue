<template>
  <footer class="py-4 px-6 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-center text-[11px] text-gray-400 font-semibold transition-colors duration-200">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
      <p>© 2026 {{ $t('header.earlyWarningSystem') }}. {{ $t('footer.rights') }}</p>
      <div class="flex items-center space-x-4">
        <span>{{ $t('settings.system.version') }} v1.0.0-beta</span>
        <span class="text-gray-300 dark:text-gray-700">|</span>
        <span class="hover:text-primary-500 cursor-pointer">Demo Mode</span>
      </div>
    </div>
  </footer>
</template>

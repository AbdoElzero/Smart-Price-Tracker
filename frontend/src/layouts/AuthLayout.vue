<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4 py-10"
  >
    <button
      type="button"
      @click="themeStore.toggle"
      class="fixed top-4 left-4 p-2 rounded-full bg-white dark:bg-gray-800 shadow text-gray-600 dark:text-gray-300"
      aria-label="تبديل الوضع الليلي"
    >
      <span v-if="themeStore.isDark">☀️</span>
      <span v-else>🌙</span>
    </button>

    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div
          class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary-600 text-white text-2xl font-bold mb-3"
        >
          ٪
        </div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Smart Price Tracker
        </h1>
        <p class="text-gray-500 dark:text-gray-400 mt-1">{{ subtitle }}</p>
      </div>

      <div
        class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 sm:p-8"
      >
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useThemeStore } from "@/store/theme";

defineProps({
  subtitle: { type: String, default: "" },
});

const themeStore = useThemeStore();
</script>

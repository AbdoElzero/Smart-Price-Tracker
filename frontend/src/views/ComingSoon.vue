<template>
  <div class="max-w-3xl mx-auto px-4 py-20 text-center">
    <div class="text-5xl mb-4">🚧</div>
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ title }}</h1>
    <p class="text-gray-500 dark:text-gray-400">
      هذه الصفحة قيد الإنشاء وستكون متاحة قريبًا في أحد الأجزاء القادمة من المشروع.
    </p>
    <router-link
      to="/"
      class="inline-block mt-6 px-5 py-2.5 rounded-lg bg-primary-600 text-white font-medium hover:bg-primary-700 transition-colors"
    >
      رجوع للرئيسية
    </router-link>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const title = computed(() => route.meta.title || "قريبًا");
</script>

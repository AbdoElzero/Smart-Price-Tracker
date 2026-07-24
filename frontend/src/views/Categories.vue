<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-6">الفئات</h1>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else class="space-y-8">
      <div v-for="cat in categories" :key="cat.slug">
        <!-- الفئة الرئيسية -->
        <div class="flex items-center gap-3 mb-4">
          <span class="text-2xl">{{ cat.icon || "📦" }}</span>
          <h2 class="text-lg font-bold text-gray-900 dark:text-white">{{ cat.name_ar }}</h2>
          <router-link
            :to="{ path: '/products', query: { category: cat.slug } }"
            class="text-sm text-primary-600 dark:text-primary-400 hover:underline mr-auto"
          >
            عرض الكل
          </router-link>
        </div>

        <!-- الفئات الفرعية -->
        <div v-if="cat.children && cat.children.length" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <router-link
            v-for="child in cat.children"
            :key="child.slug"
            :to="{ path: '/products', query: { category: child.slug } }"
            class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all text-center"
          >
            <span class="text-2xl">{{ child.icon || "📁" }}</span>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ child.name_ar }}</span>
          </router-link>
        </div>

        <!-- لو الفئة بدون فروع، تعرض كبطاقة واحدة -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <router-link
            :to="{ path: '/products', query: { category: cat.slug } }"
            class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all text-center"
          >
            <span class="text-2xl">{{ cat.icon || "📦" }}</span>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ cat.name_ar }}</span>
          </router-link>
        </div>

        <div class="border-b border-gray-100 dark:border-gray-800 mt-6"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import catalogService from "@/services/catalog.service";

const categories = ref([]);
const isLoading = ref(false);

async function loadCategories() {
  isLoading.value = true;
  try {
    const { data } = await catalogService.listCategories();
    categories.value = data.data;
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadCategories);
</script>

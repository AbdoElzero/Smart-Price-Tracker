<template>
  <Teleport to="body">
    <Transition name="slide-up">
      <div
        v-if="compareStore.count > 0"
        class="fixed bottom-0 inset-x-0 z-40 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 shadow-lg py-3 px-4"
      >
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">
              المقارنة
              <span class="text-primary-600 dark:text-primary-400 font-bold">
                ({{ compareStore.count }}/4)
              </span>
            </span>

            <div class="flex items-center gap-2">
              <div
                v-for="id in compareStore.ids"
                :key="id"
                class="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 rounded-lg px-2 py-1"
              >
                <span class="text-xs text-gray-700 dark:text-gray-200">
                  {{ productNames[id] || `#${id}` }}
                </span>
                <button
                  type="button"
                  @click="compareStore.remove(id)"
                  class="text-gray-400 hover:text-danger transition-colors text-sm leading-none"
                  aria-label="إزالة"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0">
            <button
              type="button"
              @click="compareStore.clear()"
              class="text-xs text-gray-400 hover:text-danger transition-colors"
            >
              مسح الكل
            </button>
            <router-link
              v-if="compareStore.count >= 2"
              :to="{ name: 'compare', query: { ids: compareStore.ids.join(',') } }"
              class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors"
            >
              قارن الآن
            </router-link>
            <span v-else class="text-xs text-gray-400">اختر منتجًا آخر على الأقل</span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from "vue";
import { useCompareStore } from "@/store/compare";

const compareStore = useCompareStore();

// نخزّن أسماء المنتجات عند إضافتها (تُمرَّر من الخارج عبر provide/inject أو من الصفحة)
// في هذا التصميم البسيط، سنعرض رقم المعرّف فقط في الشريط العائم
// وسيُكمَل عرض الاسم الكامل في صفحة المقارنة نفسها
const productNames = computed(() => {
  return compareStore.ids.reduce((acc, id) => {
    acc[id] = `منتج #${id}`;
    return acc;
  }, {});
});
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.25s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>

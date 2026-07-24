<template>
  <button
    type="button"
    @click.stop.prevent="handleClick"
    class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-colors"
    :class="
      isInCompare
        ? 'bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300'
        : compareStore.isFull
        ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed'
        : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-primary-50 dark:hover:bg-primary-900/30 hover:text-primary-700 dark:hover:text-primary-300'
    "
    :disabled="!isInCompare && compareStore.isFull"
    :title="
      isInCompare
        ? 'إزالة من المقارنة'
        : compareStore.isFull
        ? 'المقارنة ممتلئة (حتى 4 منتجات)'
        : 'إضافة للمقارنة'
    "
  >
    <span>⚖️</span>
    <span>{{ isInCompare ? "تمت الإضافة" : "مقارنة" }}</span>
  </button>
</template>

<script setup>
import { computed } from "vue";
import { useCompareStore } from "@/store/compare";

const props = defineProps({
  productId: { type: Number, required: true },
});

const compareStore = useCompareStore();
const isInCompare = computed(() => compareStore.isInCompare(props.productId));

function handleClick() {
  compareStore.toggle(props.productId);
}
</script>

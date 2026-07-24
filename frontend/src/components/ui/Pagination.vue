<template>
  <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
    <button
      type="button"
      :disabled="page <= 1"
      @click="$emit('change', page - 1)"
      class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-800"
    >
      السابق
    </button>

    <span class="text-sm text-gray-500 dark:text-gray-400">صفحة {{ page }} من {{ totalPages }}</span>

    <button
      type="button"
      :disabled="page >= totalPages"
      @click="$emit('change', page + 1)"
      class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 text-sm text-gray-600 dark:text-gray-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-800"
    >
      التالي
    </button>
  </div>
</template>

<script setup>
defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true },
});
defineEmits(["change"]);
</script>

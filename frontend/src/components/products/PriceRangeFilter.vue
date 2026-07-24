<template>
  <div>
    <h3 class="font-semibold text-gray-900 dark:text-white mb-3 text-sm">نطاق السعر</h3>
    <div class="flex items-center gap-2">
      <input
        v-model.number="localMin"
        type="number"
        min="0"
        placeholder="من"
        class="w-full px-2 py-1.5 text-xs rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/30"
        @change="emitValues"
      />
      <span class="text-gray-400 text-xs shrink-0">—</span>
      <input
        v-model.number="localMax"
        type="number"
        min="0"
        placeholder="إلى"
        class="w-full px-2 py-1.5 text-xs rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/30"
        @change="emitValues"
      />
    </div>
    <button
      v-if="localMin || localMax"
      type="button"
      @click="clearPrice"
      class="text-xs text-gray-400 hover:text-danger mt-1.5 block"
    >
      مسح الفلتر
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  minPrice: { type: Number, default: null },
  maxPrice: { type: Number, default: null },
});

const emit = defineEmits(["update:minPrice", "update:maxPrice"]);

const localMin = ref(props.minPrice || "");
const localMax = ref(props.maxPrice || "");

// ← تم تغيير الاسم من emit() إلى emitValues() لتجنّب التعارض مع defineEmits
function emitValues() {
  emit("update:minPrice", localMin.value || null);
  emit("update:maxPrice", localMax.value || null);
}

function clearPrice() {
  localMin.value = "";
  localMax.value = "";
  emit("update:minPrice", null);
  emit("update:maxPrice", null);
}

watch(() => props.minPrice, (v) => { localMin.value = v || ""; });
watch(() => props.maxPrice, (v) => { localMax.value = v || ""; });
</script>

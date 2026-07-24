<template>
  <div v-if="isLoading" class="animate-pulse h-24 bg-gray-100 dark:bg-gray-800 rounded-2xl"></div>

  <div v-else-if="prediction" class="rounded-2xl border p-5" :class="cardClasses">
    <div class="flex items-start justify-between gap-3">
      <div class="flex-1">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">{{ prediction.icon }}</span>
          <span class="font-bold text-lg" :class="labelClasses">
            {{ prediction.label_ar }}
          </span>
          <span
            class="text-xs px-2 py-0.5 rounded-full font-medium"
            :class="badgeClasses"
          >
            ثقة {{ prediction.confidence_score }}%
          </span>
        </div>
        <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
          {{ prediction.reason_ar }}
        </p>
      </div>
    </div>

    <p class="text-xs text-gray-400 mt-3">
      آخر تحديث: {{ formatDate(prediction.analyzed_at) }}
    </p>
  </div>

  <div
    v-else
    class="rounded-2xl border border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-5"
  >
    <div class="flex items-center gap-2 mb-1">
      <span class="text-xl">📊</span>
      <span class="font-semibold text-gray-700 dark:text-gray-300">توصية السعر</span>
    </div>
    <p class="text-sm text-gray-500 dark:text-gray-400">
      لا تتوفر بيانات تاريخية كافية حاليًا لتقديم توصية موثوقة.
      ستظهر التوصية تلقائيًا بعد جمع بيانات أسعار حقيقية.
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import predictionService from "@/services/prediction.service";

const props = defineProps({
  productId: { type: Number, required: true },
});

const prediction = ref(null);
const isLoading = ref(false);

const colorMap = {
  success: {
    card: "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800",
    label: "text-green-700 dark:text-green-400",
    badge: "bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-400",
  },
  warning: {
    card: "bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800",
    label: "text-amber-700 dark:text-amber-400",
    badge: "bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-400",
  },
  danger: {
    card: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800",
    label: "text-red-700 dark:text-red-400",
    badge: "bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-400",
  },
};

const cardClasses = computed(() => colorMap[prediction.value?.color]?.card || "");
const labelClasses = computed(() => colorMap[prediction.value?.color]?.label || "");
const badgeClasses = computed(() => colorMap[prediction.value?.color]?.badge || "");

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleString("ar-EG", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

async function loadPrediction() {
  if (!props.productId) return;
  isLoading.value = true;
  try {
    const { data } = await predictionService.get(props.productId);
    prediction.value = data.data;
  } catch (err) {
    prediction.value = null;
  } finally {
    isLoading.value = false;
  }
}

watch(() => props.productId, loadPrediction);
onMounted(loadPrediction);
</script>

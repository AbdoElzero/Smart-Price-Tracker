<template>
  <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
      <h2 class="font-semibold text-gray-900 dark:text-white">تاريخ الأسعار</h2>

      <div class="flex items-center gap-2">
        <!-- فلتر المدة -->
        <div class="flex rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 text-xs">
          <button
            v-for="d in dayOptions"
            :key="d.value"
            type="button"
            @click="selectedDays = d.value"
            class="px-3 py-1.5 transition-colors"
            :class="
              selectedDays === d.value
                ? 'bg-primary-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700'
            "
          >
            {{ d.label }}
          </button>
        </div>

        <!-- فلتر المتجر -->
        <select
          v-if="stores.length > 1"
          v-model="selectedStoreId"
          class="text-xs px-2 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
        >
          <option value="">كل المتاجر</option>
          <option v-for="store in stores" :key="store.id" :value="store.id">
            {{ store.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div v-if="stats.min !== undefined" class="grid grid-cols-3 gap-3 mb-5">
      <div class="text-center p-3 rounded-xl bg-green-50 dark:bg-green-900/20">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">أدنى سعر</p>
        <p class="font-bold text-green-700 dark:text-green-400 text-sm">
          {{ stats.min }} {{ stats.currency_symbol }}
        </p>
      </div>
      <div class="text-center p-3 rounded-xl bg-blue-50 dark:bg-blue-900/20">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">المتوسط</p>
        <p class="font-bold text-blue-700 dark:text-blue-400 text-sm">
          {{ stats.avg }} {{ stats.currency_symbol }}
        </p>
      </div>
      <div class="text-center p-3 rounded-xl bg-red-50 dark:bg-red-900/20">
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">أعلى سعر</p>
        <p class="font-bold text-red-700 dark:text-red-400 text-sm">
          {{ stats.max }} {{ stats.currency_symbol }}
        </p>
      </div>
    </div>

    <!-- الرسم البياني -->
    <div v-if="isLoading" class="h-56 flex items-center justify-center text-gray-400 text-sm">
      جارٍ التحميل...
    </div>

    <div v-else-if="!hasData" class="h-56 flex flex-col items-center justify-center text-gray-400">
      <span class="text-3xl mb-2">📊</span>
      <p class="text-sm">لا تتوفر بيانات تاريخية للفترة المحددة.</p>
      <p class="text-xs mt-1">ستظهر البيانات تلقائيًا بعد جمع بيانات حقيقية.</p>
    </div>

    <div v-else class="relative h-56">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useThemeStore } from "@/store/theme";
import api from "@/services/api";
import {
  Chart,
  LineElement,
  PointElement,
  LineController,
  CategoryScale,
  LinearScale,
  Tooltip,
  Filler,
} from "chart.js";

Chart.register(LineElement, PointElement, LineController, CategoryScale, LinearScale, Tooltip, Filler);

const props = defineProps({
  productId: { type: Number, required: true },
});

const themeStore = useThemeStore();
const chartCanvas = ref(null);
const isLoading = ref(false);
const chartData = ref(null);
const stores = ref([]);
const stats = ref({});
const selectedDays = ref(90);
const selectedStoreId = ref("");
let chartInstance = null;

const dayOptions = [
  { label: "7 أيام", value: 7 },
  { label: "30 يوم", value: 30 },
  { label: "90 يوم", value: 90 },
  { label: "180 يوم", value: 180 },
];

const hasData = computed(() => {
  if (!chartData.value) return false;
  if (Array.isArray(chartData.value)) return chartData.value.length > 0;
  return Object.keys(chartData.value).some((k) => chartData.value[k].length > 0);
});

const isDark = computed(() => themeStore.isDark);
const gridColor = computed(() => isDark.value ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.06)");
const textColor = computed(() => isDark.value ? "#9ca3af" : "#6b7280");

async function loadData() {
  if (!props.productId) return;
  isLoading.value = true;

  try {
    const params = { days: selectedDays.value };
    if (selectedStoreId.value) params.store_id = selectedStoreId.value;

    const { data } = await api.get(`/products/${props.productId}/price-history`, { params });
    chartData.value = data.data;
    stores.value = data.stores || [];
    stats.value = data.stats || {};

    await nextTick();
    if (hasData.value) buildChart();
  } catch (err) {
    chartData.value = null;
  } finally {
    isLoading.value = false;
  }
}

function buildChart() {
  if (!chartCanvas.value) return;
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }

  const COLORS = [
    { line: "#3b82f6", fill: "rgba(59,130,246,0.1)" },
    { line: "#10b981", fill: "rgba(16,185,129,0.1)" },
    { line: "#f59e0b", fill: "rgba(245,158,11,0.1)" },
    { line: "#ef4444", fill: "rgba(239,68,68,0.1)" },
  ];

  let datasets = [];
  let labels = [];

  if (Array.isArray(chartData.value)) {
    // متجر واحد → خط واحد
    labels = chartData.value.map((d) => d.date);
    datasets = [{
      label: stores.value[0]?.name || "السعر",
      data: chartData.value.map((d) => d.price),
      borderColor: COLORS[0].line,
      backgroundColor: COLORS[0].fill,
      fill: true,
      tension: 0.4,
      pointRadius: chartData.value.length > 30 ? 0 : 3,
      pointHoverRadius: 5,
      borderWidth: 2,
    }];
  } else {
    // متاجر متعددة → خط لكل متجر
    const allDates = new Set();
    Object.values(chartData.value).forEach((records) =>
      records.forEach((r) => allDates.add(r.date))
    );
    labels = [...allDates].sort();

    Object.entries(chartData.value).forEach(([storeName, records], i) => {
      const priceMap = Object.fromEntries(records.map((r) => [r.date, r.price]));
      const color = COLORS[i % COLORS.length];
      datasets.push({
        label: storeName,
        data: labels.map((d) => priceMap[d] ?? null),
        borderColor: color.line,
        backgroundColor: color.fill,
        fill: i === 0,
        tension: 0.4,
        pointRadius: labels.length > 30 ? 0 : 3,
        pointHoverRadius: 5,
        borderWidth: 2,
        spanGaps: true,
      });
    });
  }

  chartInstance = new Chart(chartCanvas.value, {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: "index" },
      plugins: {
        legend: {
          display: datasets.length > 1,
          labels: { color: textColor.value, boxWidth: 12, font: { size: 11 } },
        },
        tooltip: {
          callbacks: {
            label(ctx) {
              const sym = stores.value[0]?.currency_symbol || "";
              return ` ${ctx.dataset.label}: ${ctx.parsed.y} ${sym}`;
            },
          },
        },
      },
      scales: {
        x: {
          grid: { color: gridColor.value },
          ticks: {
            color: textColor.value,
            maxTicksLimit: 8,
            font: { size: 10 },
          },
        },
        y: {
          grid: { color: gridColor.value },
          ticks: {
            color: textColor.value,
            font: { size: 10 },
            callback(value) {
              return `${value} ${stores.value[0]?.currency_symbol || ""}`;
            },
          },
        },
      },
    },
  });
}

watch([selectedDays, selectedStoreId], loadData);
watch(isDark, () => { if (hasData.value) buildChart(); });

onMounted(loadData);
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy();
});
</script>

<template>
  <div>
    <h2 class="text-lg font-bold text-gray-900 dark:text-white mb-6">نظرة عامة</h2>

    <div v-if="isLoading" class="text-center py-10 text-gray-400">جارٍ التحميل...</div>

    <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="stat in statCards" :key="stat.label"
        class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5">
        <div class="text-2xl mb-2">{{ stat.icon }}</div>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stat.value }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ stat.label }}</p>
      </div>
    </div>

    <div v-if="stats" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- المنتجات -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3">📦 المنتجات</h3>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-500">الكل</span>
            <span class="font-medium">{{ stats.products.total }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">الفعّالة</span>
            <span class="font-medium text-green-600">{{ stats.products.active }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">المُعطَّلة</span>
            <span class="font-medium text-danger">{{ stats.products.inactive }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">أسعار مُسجَّلة</span>
            <span class="font-medium">{{ stats.prices.total }}</span>
          </div>
        </div>
      </div>

      <!-- المستخدمون -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3">👥 المستخدمون</h3>
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-500">الكل</span>
            <span class="font-medium">{{ stats.users.total }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">الفعّالون</span>
            <span class="font-medium text-green-600">{{ stats.users.active }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">المشرفون</span>
            <span class="font-medium text-purple-600">{{ stats.users.admins }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">المفضلة</span>
            <span class="font-medium">{{ stats.activity.favorites }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">المتابعة</span>
            <span class="font-medium">{{ stats.activity.watchlist }}</span>
          </div>
        </div>
      </div>

      <!-- المهام الدورية -->
      <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 p-5">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3">⚙️ تشغيل المهام يدوياً</h3>
        <div class="space-y-2">
          <button type="button" @click="runTask('predictions')" :disabled="taskLoading === 'predictions'"
            class="w-full px-3 py-2 text-xs rounded-lg bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 hover:bg-primary-100 disabled:opacity-60 text-right">
            {{ taskLoading === "predictions" ? "جارٍ التشغيل..." : "🧠 تحديث التوقعات (AI)" }}
          </button>
          <button type="button" @click="runTask('notifications')" :disabled="taskLoading === 'notifications'"
            class="w-full px-3 py-2 text-xs rounded-lg bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 hover:bg-amber-100 disabled:opacity-60 text-right">
            {{ taskLoading === "notifications" ? "جارٍ التشغيل..." : "🔔 فحص الإشعارات" }}
          </button>
          <p v-if="taskMessage" class="text-xs text-green-600 dark:text-green-400 mt-1">{{ taskMessage }}</p>
          <p class="text-xs text-gray-400 mt-2">
            تُشغَّل المهام تلقائيًا بواسطة Celery Beat. هذه الأزرار للتشغيل الفوري فقط.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import adminService from "@/services/admin.service";

const stats = ref(null);
const isLoading = ref(false);
const taskLoading = ref("");
const taskMessage = ref("");

const statCards = computed(() => {
  if (!stats.value) return [];
  return [
    { icon: "📦", value: stats.value.products.total, label: "إجمالي المنتجات" },
    { icon: "👥", value: stats.value.users.total, label: "إجمالي المستخدمين" },
    { icon: "💰", value: stats.value.prices.total, label: "سجلات الأسعار" },
    { icon: "🏷️", value: stats.value.brands, label: "العلامات التجارية" },
  ];
});

async function loadStats() {
  isLoading.value = true;
  try {
    const { data } = await adminService.getStats();
    stats.value = data.data;
  } finally {
    isLoading.value = false;
  }
}

async function runTask(type) {
  taskLoading.value = type;
  taskMessage.value = "";
  try {
    if (type === "predictions") {
      await adminService.runPredictionsTask();
      taskMessage.value = "✅ تم إرسال مهمة التوقعات لـ Celery";
    } else {
      await adminService.runNotificationsTask();
      taskMessage.value = "✅ تم إرسال مهمة الإشعارات لـ Celery";
    }
    setTimeout(() => { taskMessage.value = ""; }, 4000);
  } catch (err) {
    taskMessage.value = "❌ " + (err.response?.data?.error || "تعذّر التشغيل");
  } finally {
    taskLoading.value = "";
  }
}

onMounted(loadStats);
</script>

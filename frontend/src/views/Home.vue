<template>
  <div>
    <!-- Hero -->
    <section class="bg-gradient-to-b from-primary-50 to-transparent dark:from-gray-800/40 px-4 py-16 sm:py-24 text-center">
      <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
        تابع أسعار أجهزتك المفضلة <br class="hidden sm:block" /> واعرف متى تشتري بذكاء
      </h1>
      <p class="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8">
        نتابع أسعار الكمبيوترات والهواتف والشاشات وقطع الكمبيوتر في كل المتاجر العربية الكبرى،
        ونحلّل تاريخ الأسعار لنخبرك: اشتري الآن، انتظر قليلاً، أو السعر مرتفع.
      </p>

      <form @submit.prevent="handleSearch" class="max-w-xl mx-auto flex gap-2">
        <input
          v-model="searchQuery"
          type="search"
          placeholder="ابحث عن iPhone 16، RTX 4070، Galaxy S24..."
          class="flex-1 px-5 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/30"
        />
        <button
          type="submit"
          class="px-6 py-3 rounded-xl bg-primary-600 text-white font-semibold hover:bg-primary-700 transition-colors"
        >
          بحث
        </button>
      </form>
    </section>

    <!-- الفئات الرئيسية -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">تصفّح حسب الفئة</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <router-link
          v-for="cat in categories"
          :key="cat.slug"
          to="/products"
          class="flex flex-col items-center gap-2 p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all"
        >
          <span class="text-3xl">{{ cat.icon }}</span>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ cat.name }}</span>
        </router-link>
      </div>
    </section>

    <!-- كيف نقرر -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">كيف نساعدك تقرر؟</h2>
      <div class="grid sm:grid-cols-3 gap-6">
        <div class="p-6 rounded-2xl bg-success/10 border border-success/20">
          <div class="text-2xl mb-2">✅</div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-1">اشتري الآن</h3>
          <p class="text-sm text-gray-600 dark:text-gray-300">
            السعر الحالي من أفضل الأسعار المسجَّلة تاريخيًا للمنتج.
          </p>
        </div>
        <div class="p-6 rounded-2xl bg-warning/10 border border-warning/20">
          <div class="text-2xl mb-2">⏳</div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-1">انتظر قليلاً</h3>
          <p class="text-sm text-gray-600 dark:text-gray-300">
            هناك مؤشرات على احتمال نزول السعر في الفترة القادمة.
          </p>
        </div>
        <div class="p-6 rounded-2xl bg-danger/10 border border-danger/20">
          <div class="text-2xl mb-2">🔴</div>
          <h3 class="font-semibold text-gray-900 dark:text-white mb-1">السعر مرتفع</h3>
          <p class="text-sm text-gray-600 dark:text-gray-300">
            السعر الحالي أعلى من المتوسط التاريخي بشكل واضح.
          </p>
        </div>
      </div>
    </section>

    <!-- دعوة لإنشاء حساب -->
    <section v-if="!authStore.isAuthenticated" class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="rounded-2xl bg-primary-600 text-white p-8 sm:p-10 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 class="text-lg font-bold mb-1">جاهز تبدأ بتتبع أسعارك؟</h3>
          <p class="text-primary-100 text-sm">أنشئ حسابًا مجانيًا وفعّل التنبيهات عند نزول السعر.</p>
        </div>
        <router-link
          to="/register"
          class="px-6 py-2.5 rounded-lg bg-white text-primary-700 font-semibold hover:bg-primary-50 transition-colors shrink-0"
        >
          إنشاء حساب مجاني
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const router = useRouter();
const authStore = useAuthStore();
const searchQuery = ref("");

const categories = [
  { slug: "computers", name: "أجهزة الكمبيوتر", icon: "💻" },
  { slug: "phones", name: "الهواتف", icon: "📱" },
  { slug: "monitors", name: "الشاشات", icon: "🖥️" },
  { slug: "pc-parts", name: "قطع الكمبيوتر", icon: "🔧" },
];

function handleSearch() {
  if (!searchQuery.value.trim()) return;
  router.push({ path: "/products", query: { q: searchQuery.value.trim() } });
}
</script>

<template>
  <footer class="border-t border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div>
        <div class="flex items-center gap-2 mb-3">
          <span
            class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-primary-600 text-white font-bold text-sm"
          >٪</span>
          <span class="font-bold text-gray-900 dark:text-white">Smart Price Tracker</span>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
          نتابع أسعار الكمبيوترات والهواتف والشاشات في الدول العربية، ونساعدك تقرر الوقت الأفضل للشراء.
        </p>
      </div>

      <div>
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3 text-sm">روابط سريعة</h3>
        <ul class="space-y-2 text-sm">
          <li>
            <router-link to="/products" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
              المنتجات
            </router-link>
          </li>
          <li>
            <router-link to="/categories" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
              الفئات
            </router-link>
          </li>
          <li>
            <router-link to="/brands" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
              العلامات التجارية
            </router-link>
          </li>
        </ul>
      </div>

      <div>
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3 text-sm">حسابي</h3>
        <ul class="space-y-2 text-sm">
          <li>
            <router-link to="/favorites" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
              المفضلة
            </router-link>
          </li>
          <li>
            <router-link to="/watchlist" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
              قائمة المتابعة
            </router-link>
          </li>
          <li>
            <router-link to="/profile" class="text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400">
              الملف الشخصي
            </router-link>
          </li>
        </ul>
      </div>

      <div>
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3 text-sm">الدول المدعومة</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
          🇸🇦 السعودية · 🇪🇬 مصر · 🇦🇪 الإمارات · 🇰🇼 الكويت · 🇶🇦 قطر · والمزيد
        </p>
      </div>
    </div>

    <div class="border-t border-gray-100 dark:border-gray-800 py-4 text-center text-xs text-gray-400 dark:text-gray-500">
      © {{ currentYear }} Smart Price Tracker. جميع الحقوق محفوظة.
    </div>
  </footer>
</template>

<script setup>
import { computed } from "vue";

const currentYear = computed(() => new Date().getFullYear());
</script>

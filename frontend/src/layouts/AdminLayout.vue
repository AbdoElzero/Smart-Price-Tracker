<template>
  <div class="min-h-screen flex bg-gray-100 dark:bg-gray-950" dir="rtl">
    <!-- Sidebar -->
    <aside class="w-56 shrink-0 bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800 flex flex-col">
      <div class="px-4 py-5 border-b border-gray-100 dark:border-gray-800">
        <router-link to="/" class="flex items-center gap-2">
          <span class="w-8 h-8 rounded-lg bg-primary-600 text-white flex items-center justify-center font-bold text-sm">٪</span>
          <div>
            <p class="text-xs font-bold text-gray-900 dark:text-white">Smart Price</p>
            <p class="text-[10px] text-danger font-medium">لوحة المشرف</p>
          </div>
        </router-link>
      </div>

      <nav class="flex-1 p-3 space-y-1">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors"
          :class="
            $route.path.startsWith(link.to)
              ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-medium'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
          "
        >
          <span>{{ link.icon }}</span>
          {{ link.label }}
        </router-link>
      </nav>

      <div class="p-3 border-t border-gray-100 dark:border-gray-800">
        <router-link
          to="/"
          class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800"
        >
          <span>🏠</span> العودة للموقع
        </router-link>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-3 flex items-center justify-between">
        <h1 class="font-semibold text-gray-900 dark:text-white text-sm">{{ pageTitle }}</h1>
        <div class="flex items-center gap-3">
          <span class="text-xs text-gray-400">{{ authStore.user?.name }}</span>
          <span class="text-xs bg-danger/10 text-danger px-2 py-0.5 rounded-full font-medium">مشرف</span>
        </div>
      </header>
      <main class="flex-1 overflow-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/store/auth";

const route = useRoute();
const authStore = useAuthStore();

const navLinks = [
  { to: "/admin", icon: "📊", label: "الإحصائيات" },
  { to: "/admin/products", icon: "📦", label: "المنتجات" },
  { to: "/admin/users", icon: "👥", label: "المستخدمون" },
];

const pageTitles = {
  "admin-dashboard": "لوحة التحكم",
  "admin-products": "إدارة المنتجات",
  "admin-users": "إدارة المستخدمين",
};

const pageTitle = computed(() => pageTitles[route.name] || "لوحة التحكم");
</script>

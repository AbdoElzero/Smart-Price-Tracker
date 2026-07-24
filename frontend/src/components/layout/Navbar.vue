<template>
  <header
    class="sticky top-0 z-40 bg-white/95 dark:bg-gray-900/95 backdrop-blur border-b border-gray-100 dark:border-gray-800"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-16 gap-4">
        <!-- الشعار -->
        <router-link to="/" class="flex items-center gap-2 shrink-0">
          <span
            class="inline-flex items-center justify-center w-9 h-9 rounded-xl bg-primary-600 text-white font-bold"
          >٪</span>
          <span class="font-bold text-gray-900 dark:text-white hidden sm:inline">
            Smart Price Tracker
          </span>
        </router-link>

        <!-- روابط التنقل (Desktop) -->
        <nav class="hidden md:flex items-center gap-6">
          <router-link
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
            active-class="text-primary-600 dark:text-primary-400"
          >
            {{ link.label }}
          </router-link>
        </nav>

        <!-- شريط البحث (Desktop) -->
        <form @submit.prevent="handleSearch" class="hidden lg:flex flex-1 max-w-md">
          <div class="relative w-full">
            <input
              v-model="searchQuery"
              type="search"
              placeholder="ابحث عن منتج، ماركة، أو موديل..."
              class="w-full px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
            />
            <span class="absolute inset-y-0 left-3 flex items-center text-gray-400 text-sm">🔍</span>
          </div>
        </form>

        <!-- أزرار اليمين -->
        <div class="flex items-center gap-2">
          <button
            type="button"
            @click="themeStore.toggle"
            class="p-2 rounded-full text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="تبديل الوضع الليلي"
          >
            <span v-if="themeStore.isDark">☀️</span>
            <span v-else>🌙</span>
          </button>

          <template v-if="authStore.isAuthenticated">
            <router-link
              to="/notifications"
              class="relative p-2 rounded-full text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors hidden sm:inline-flex"
              aria-label="الإشعارات"
            >
              🔔
              <span
                v-if="notificationsStore.unreadCount > 0"
                class="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 rounded-full bg-danger text-white text-[10px] font-bold flex items-center justify-center"
              >
                {{ notificationsStore.unreadCount > 9 ? "9+" : notificationsStore.unreadCount }}
              </span>
            </router-link>

            <router-link
              to="/favorites"
              class="p-2 rounded-full text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors hidden sm:inline-flex"
              aria-label="المفضلة"
            >
              ❤️
            </router-link>

            <div ref="userMenuRef" class="relative">
              <button
                type="button"
                @click="userMenuOpen = !userMenuOpen"
                class="flex items-center gap-2 p-1.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                <span
                  class="w-8 h-8 rounded-full overflow-hidden bg-primary-100 dark:bg-primary-900 flex items-center justify-center"
                >
                  <img
                    v-if="avatarSrc"
                    :src="avatarSrc"
                    alt="الصورة الشخصية"
                    class="w-full h-full object-cover"
                  />
                  <span v-else class="text-primary-700 dark:text-primary-300 font-semibold text-sm">
                    {{ userInitial }}
                  </span>
                </span>
              </button>

              <div
                v-if="userMenuOpen"
                class="absolute left-0 mt-2 w-52 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 py-2 text-sm z-50"
              >
                <p
                  class="px-4 py-2 text-gray-500 dark:text-gray-400 truncate border-b border-gray-100 dark:border-gray-700 mb-1"
                >
                  {{ authStore.user?.name }}
                </p>
                <router-link
                  v-if="authStore.user?.role === 'admin'"
                  to="/admin"
                  class="block px-4 py-2 text-danger dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 font-medium"
                  @click="userMenuOpen = false"
                >
                  🛡️ لوحة التحكم
                </router-link>
                <router-link
                  to="/profile"
                  class="block px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700"
                  @click="userMenuOpen = false"
                >
                  الملف الشخصي
                </router-link>
                <router-link
                  to="/watchlist"
                  class="block px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700"
                  @click="userMenuOpen = false"
                >
                  قائمة المتابعة
                </router-link>
                <router-link
                  to="/notifications"
                  class="block px-4 py-2 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700"
                  @click="userMenuOpen = false"
                >
                  الإشعارات
                </router-link>
                <button
                  type="button"
                  @click="handleLogout"
                  class="w-full text-right px-4 py-2 text-danger hover:bg-red-50 dark:hover:bg-red-900/20"
                >
                  تسجيل الخروج
                </button>
              </div>
            </div>
          </template>

          <template v-else>
            <router-link
              to="/login"
              class="hidden sm:inline-block px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-primary-600 dark:hover:text-primary-400"
            >
              تسجيل الدخول
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-sm font-medium rounded-lg bg-primary-600 text-white hover:bg-primary-700 transition-colors"
            >
              إنشاء حساب
            </router-link>
          </template>

          <!-- زر القائمة (Mobile) -->
          <button
            type="button"
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
            aria-label="فتح القائمة"
          >
            <span v-if="!mobileMenuOpen">☰</span>
            <span v-else>✕</span>
          </button>
        </div>
      </div>

      <!-- القائمة المنسدلة (Mobile) -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden border-t border-gray-100 dark:border-gray-800 py-3 space-y-1"
      >
        <form @submit.prevent="handleSearch" class="px-1 pb-2">
          <input
            v-model="searchQuery"
            type="search"
            placeholder="ابحث عن منتج..."
            class="w-full px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/30"
          />
        </form>
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="block px-3 py-2 rounded-lg text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800"
          @click="mobileMenuOpen = false"
        >
          {{ link.label }}
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { onClickOutside } from "@vueuse/core";
import { useAuthStore } from "@/store/auth";
import { useThemeStore } from "@/store/theme";
import { useNotificationsStore } from "@/store/notifications";
import { resolveAvatarUrl } from "@/utils/avatar";

const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const notificationsStore = useNotificationsStore();

const searchQuery = ref("");
const mobileMenuOpen = ref(false);
const userMenuOpen = ref(false);
const userMenuRef = ref(null);

onClickOutside(userMenuRef, () => {
  userMenuOpen.value = false;
});

const navLinks = [
  { to: "/", label: "الرئيسية" },
  { to: "/products", label: "المنتجات" },
  { to: "/categories", label: "الفئات" },
  { to: "/brands", label: "العلامات التجارية" },
];

const avatarSrc = computed(() => resolveAvatarUrl(authStore.user?.avatar_url));

const userInitial = computed(() => {
  const name = authStore.user?.name || "";
  return name.trim().charAt(0).toUpperCase() || "؟";
});

function handleSearch() {
  if (!searchQuery.value.trim()) return;
  router.push({ path: "/products", query: { q: searchQuery.value.trim() } });
  mobileMenuOpen.value = false;
}

async function handleLogout() {
  userMenuOpen.value = false;
  await authStore.logout();
  router.push("/login");
}
</script>

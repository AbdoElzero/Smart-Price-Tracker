import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { useFavoritesStore } from "@/store/favorites";
import { useWatchlistStore } from "@/store/watchlist";
import { useNotificationsStore } from "@/store/notifications";
import MainLayout from "@/layouts/MainLayout.vue";

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "home",
        component: () => import("@/views/Home.vue"),
      },
      {
        path: "products",
        name: "products",
        component: () => import("@/views/Products.vue"),
        meta: { title: "المنتجات" },
      },
      {
        path: "products/:slug",
        name: "product-detail",
        component: () => import("@/views/ProductDetail.vue"),
        meta: { title: "تفاصيل المنتج" },
      },
      {
        path: "compare",
        name: "compare",
        component: () => import("@/views/Compare.vue"),
        meta: { title: "مقارنة المنتجات" },
      },
      {
        path: "categories",
        name: "categories",
        component: () => import("@/views/Categories.vue"),
        meta: { title: "الفئات" },
      },
      {
        path: "brands",
        name: "brands",
        component: () => import("@/views/Brands.vue"),
        meta: { title: "العلامات التجارية" },
      },
      {
        path: "favorites",
        name: "favorites",
        component: () => import("@/views/Favorites.vue"),
        meta: { title: "المفضلة", requiresAuth: true },
      },
      {
        path: "watchlist",
        name: "watchlist",
        component: () => import("@/views/Watchlist.vue"),
        meta: { title: "قائمة المتابعة", requiresAuth: true },
      },
      {
        path: "notifications",
        name: "notifications",
        component: () => import("@/views/Notifications.vue"),
        meta: { title: "الإشعارات", requiresAuth: true },
      },
      {
        path: "profile",
        name: "profile",
        component: () => import("@/views/Profile.vue"),
        meta: { title: "الملف الشخصي", requiresAuth: true },
      },
    ],
  },
  {
    path: "/admin",
    component: () => import("@/layouts/AdminLayout.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: "",
        name: "admin-dashboard",
        component: () => import("@/views/admin/AdminDashboard.vue"),
      },
      {
        path: "products",
        name: "admin-products",
        component: () => import("@/views/admin/AdminProducts.vue"),
      },
      {
        path: "users",
        name: "admin-users",
        component: () => import("@/views/admin/AdminUsers.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/Register.vue"),
    meta: { guestOnly: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  const favoritesStore = useFavoritesStore();
  const watchlistStore = useWatchlistStore();
  const notificationsStore = useNotificationsStore();

  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchCurrentUser();
  }

  if (authStore.isAuthenticated) {
    favoritesStore.init();
    watchlistStore.init();
    notificationsStore.fetchUnreadCount();
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  }

  if (to.meta.requiresAdmin && authStore.user?.role !== "admin") {
    return { name: "home" };
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: "home" };
  }

  return true;
});

export default router;

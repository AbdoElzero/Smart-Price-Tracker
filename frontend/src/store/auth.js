import { defineStore } from "pinia";
import authService from "@/services/auth.service";
import {
  getAccessToken,
  setTokens,
  clearTokens,
} from "@/utils/token-storage";
import { useFavoritesStore } from "@/store/favorites";
import { useWatchlistStore } from "@/store/watchlist";
import { useNotificationsStore } from "@/store/notifications";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user || !!getAccessToken(),
  },

  actions: {
    async register(payload) {
      this.isLoading = true;
      this.error = null;
      try {
        const { data } = await authService.register(payload);
        setTokens(data);
        this.user = data.user;
        return data.user;
      } catch (err) {
        this.error =
          err.response?.data?.error || "حدث خطأ غير متوقع، حاول مرة أخرى";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    async login(payload) {
      this.isLoading = true;
      this.error = null;
      try {
        const { data } = await authService.login(payload);
        setTokens(data);
        this.user = data.user;
        return data.user;
      } catch (err) {
        this.error =
          err.response?.data?.error || "البريد الإلكتروني أو كلمة السر غير صحيحة";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    async loginWithGoogle(idToken) {
      this.isLoading = true;
      this.error = null;
      try {
        const { data } = await authService.loginWithGoogle(idToken);
        setTokens(data);
        this.user = data.user;
        return data.user;
      } catch (err) {
        this.error =
          err.response?.data?.error || "تعذّر تسجيل الدخول عبر Google";
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    async fetchCurrentUser() {
      if (!getAccessToken()) return null;
      try {
        const { data } = await authService.me();
        this.user = data.user;
        return data.user;
      } catch (err) {
        this.user = null;
        return null;
      }
    },

    async logout() {
      try {
        await authService.logout();
      } catch (err) {
        // تجاهل الخطأ - المهم تنظيف الجلسة محليًا حتى لو فشل الطلب
      }
      this.user = null;
      clearTokens();
      useFavoritesStore().reset();
      useWatchlistStore().reset();
      useNotificationsStore().reset();
    },
  },
});

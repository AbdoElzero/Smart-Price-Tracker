import { defineStore } from "pinia";

const THEME_KEY = "spt_theme";

export const useThemeStore = defineStore("theme", {
  state: () => ({
    isDark: localStorage.getItem(THEME_KEY) === "dark",
  }),

  actions: {
    toggle() {
      this.isDark = !this.isDark;
      this.apply();
    },

    apply() {
      document.documentElement.classList.toggle("dark", this.isDark);
      localStorage.setItem(THEME_KEY, this.isDark ? "dark" : "light");
    },

    init() {
      this.apply();
    },
  },
});

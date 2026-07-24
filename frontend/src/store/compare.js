import { defineStore } from "pinia";

const STORAGE_KEY = "spt_compare_ids";
const MAX_PRODUCTS = 4;

export const useCompareStore = defineStore("compare", {
  state: () => ({
    ids: JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"),
  }),

  getters: {
    isInCompare: (state) => (productId) => state.ids.includes(productId),
    count: (state) => state.ids.length,
    isFull: (state) => state.ids.length >= MAX_PRODUCTS,
  },

  actions: {
    toggle(productId) {
      const idx = this.ids.indexOf(productId);
      if (idx !== -1) {
        this.ids.splice(idx, 1);
      } else {
        if (this.ids.length >= MAX_PRODUCTS) return;
        this.ids.push(productId);
      }
      this._persist();
    },

    remove(productId) {
      this.ids = this.ids.filter((id) => id !== productId);
      this._persist();
    },

    clear() {
      this.ids = [];
      this._persist();
    },

    _persist() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.ids));
    },
  },
});

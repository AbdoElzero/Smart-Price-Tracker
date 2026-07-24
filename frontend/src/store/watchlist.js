import { defineStore } from "pinia";
import watchlistService from "@/services/watchlist.service";

export const useWatchlistStore = defineStore("watchlist", {
  state: () => ({
    entries: new Map(),
    loaded: false,
  }),

  getters: {
    isWatched: (state) => (productId) => state.entries.has(productId),
    getEntry: (state) => (productId) => state.entries.get(productId) || null,
  },

  actions: {
    async init() {
      if (this.loaded) return;
      try {
        const { data } = await watchlistService.list();
        const map = new Map();
        data.data.forEach((item) => {
          map.set(item.product.id, {
            target_price: item.target_price,
            notify_on_any_drop: item.notify_on_any_drop,
          });
        });
        this.entries = map;
        this.loaded = true;
      } catch (err) {
        this.entries = new Map();
      }
    },

    async upsert(productId, payload) {
      const { data } = await watchlistService.upsert(productId, payload);
      this.entries.set(productId, {
        target_price: data.data.target_price,
        notify_on_any_drop: data.data.notify_on_any_drop,
      });
    },

    async remove(productId) {
      await watchlistService.remove(productId);
      this.entries.delete(productId);
    },

    reset() {
      this.entries = new Map();
      this.loaded = false;
    },
  },
});

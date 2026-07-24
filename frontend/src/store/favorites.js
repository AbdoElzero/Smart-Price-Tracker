import { defineStore } from "pinia";
import favoriteService from "@/services/favorite.service";

export const useFavoritesStore = defineStore("favorites", {
  state: () => ({
    ids: new Set(),
    loaded: false,
  }),

  getters: {
    isFavorited: (state) => (productId) => state.ids.has(productId),
  },

  actions: {
    async init() {
      if (this.loaded) return;
      try {
        const { data } = await favoriteService.listIds();
        this.ids = new Set(data.data);
        this.loaded = true;
      } catch (err) {
        this.ids = new Set();
      }
    },

    async toggle(productId) {
      const { data } = await favoriteService.toggle(productId);
      if (data.favorited) {
        this.ids.add(productId);
      } else {
        this.ids.delete(productId);
      }
      return data.favorited;
    },

    reset() {
      this.ids = new Set();
      this.loaded = false;
    },
  },
});

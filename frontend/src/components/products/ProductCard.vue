<template>
  <router-link
    :to="`/products/${product.slug}`"
    class="group block bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 overflow-hidden hover:shadow-md hover:border-primary-300 dark:hover:border-primary-600 transition-all"
  >
    <div class="relative aspect-square bg-gray-50 dark:bg-gray-900 flex items-center justify-center overflow-hidden">
      <img
        v-if="product.primary_image"
        :src="product.primary_image"
        :alt="product.name_ar"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
      />
      <span v-else class="text-4xl">📦</span>

      <FavoriteButton :product-id="product.id" class="absolute top-2 left-2" />
      <div class="absolute top-2 right-2">
        <WatchlistButton :product-id="product.id" />
      </div>
    </div>

    <div class="p-4">
      <p class="text-xs text-gray-400 dark:text-gray-500 mb-1">{{ product.brand?.name_ar }}</p>
      <h3 class="font-medium text-gray-900 dark:text-white text-sm line-clamp-2 mb-2 min-h-[2.5rem]">
        {{ product.name_ar }}
      </h3>

      <div v-if="product.lowest_price" class="flex items-baseline gap-1 mb-2">
        <span class="text-lg font-bold text-gray-900 dark:text-white">
          {{ product.lowest_price.amount }}
        </span>
        <span class="text-sm text-gray-500 dark:text-gray-400">
          {{ product.lowest_price.currency_symbol }}
        </span>
      </div>
      <p v-else class="text-sm text-gray-400 dark:text-gray-500 mb-2">السعر غير متوفر حاليًا</p>

      <CompareButton :product-id="product.id" />
    </div>
  </router-link>
</template>

<script setup>
import FavoriteButton from "./FavoriteButton.vue";
import WatchlistButton from "./WatchlistButton.vue";
import CompareButton from "./CompareButton.vue";

defineProps({
  product: { type: Object, required: true },
});
</script>

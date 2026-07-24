<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-6">المفضلة</h1>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else-if="products.length === 0" class="text-center py-20">
      <div class="text-4xl mb-3">🤍</div>
      <p class="text-gray-500 dark:text-gray-400 mb-4">لم تُضِف أي منتج للمفضلة بعد.</p>
      <router-link to="/products" class="text-primary-600 dark:text-primary-400 hover:underline">
        تصفّح المنتجات
      </router-link>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import favoriteService from "@/services/favorite.service";
import ProductCard from "@/components/products/ProductCard.vue";

const products = ref([]);
const isLoading = ref(false);

async function loadFavorites() {
  isLoading.value = true;
  try {
    const { data } = await favoriteService.list();
    products.value = data.data;
  } catch (err) {
    products.value = [];
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadFavorites);
</script>

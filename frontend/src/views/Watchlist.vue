<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
    <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-6">قائمة المتابعة</h1>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else-if="items.length === 0" class="text-center py-20">
      <div class="text-4xl mb-3">🔔</div>
      <p class="text-gray-500 dark:text-gray-400 mb-4">لا توجد منتجات في قائمة المتابعة حاليًا.</p>
      <router-link to="/products" class="text-primary-600 dark:text-primary-400 hover:underline">
        تصفّح المنتجات
      </router-link>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="item in items"
        :key="item.id"
        class="flex items-center gap-4 p-4 rounded-2xl bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700"
      >
        <div
          class="w-16 h-16 rounded-xl bg-gray-50 dark:bg-gray-900 flex items-center justify-center overflow-hidden shrink-0"
        >
          <img
            v-if="item.product.primary_image"
            :src="item.product.primary_image"
            :alt="item.product.name_ar"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-2xl">📦</span>
        </div>

        <div class="flex-1 min-w-0">
          <router-link
            :to="`/products/${item.product.slug}`"
            class="font-medium text-gray-900 dark:text-white text-sm hover:text-primary-600 dark:hover:text-primary-400 line-clamp-1"
          >
            {{ item.product.name_ar }}
          </router-link>
          <p class="text-xs text-gray-400 mt-1">
            <span v-if="item.target_price">السعر المستهدف: {{ item.target_price }}</span>
            <span v-else>بدون سعر مستهدف - تنبيه عند أي نزول</span>
          </p>
        </div>

        <button
          type="button"
          @click="handleRemove(item.product.id)"
          class="text-xs text-danger hover:underline shrink-0"
        >
          إزالة
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import watchlistService from "@/services/watchlist.service";
import { useWatchlistStore } from "@/store/watchlist";

const watchlistStore = useWatchlistStore();
const items = ref([]);
const isLoading = ref(false);

async function loadWatchlist() {
  isLoading.value = true;
  try {
    const { data } = await watchlistService.list();
    items.value = data.data;
  } catch (err) {
    items.value = [];
  } finally {
    isLoading.value = false;
  }
}

async function handleRemove(productId) {
  try {
    await watchlistStore.remove(productId);
    items.value = items.value.filter((i) => i.product.id !== productId);
  } catch (err) {
    // تجاهل بسيط - يمكن إضافة Toast لاحقًا
  }
}

onMounted(loadWatchlist);
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">مقارنة المنتجات</h1>
      <button
        type="button"
        @click="handleClear"
        class="text-sm text-danger hover:underline"
      >
        مسح الكل
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else-if="products.length < 2" class="text-center py-20">
      <div class="text-4xl mb-3">⚖️</div>
      <p class="text-gray-500 dark:text-gray-400 mb-4">
        اختر منتجَين على الأقل للمقارنة (حتى 4 منتجات).
      </p>
      <router-link to="/products" class="text-primary-600 dark:text-primary-400 hover:underline">
        تصفّح المنتجات
      </router-link>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full min-w-[640px] border-collapse text-sm">
        <!-- رؤوس المنتجات -->
        <thead>
          <tr>
            <th class="w-44 bg-gray-50 dark:bg-gray-800 p-4 text-right text-gray-500 dark:text-gray-400 font-medium border border-gray-100 dark:border-gray-700">
              المنتج
            </th>
            <th
              v-for="product in products"
              :key="product.id"
              class="bg-white dark:bg-gray-900 p-4 border border-gray-100 dark:border-gray-700 align-top"
            >
              <div class="flex flex-col items-center gap-2">
                <div class="w-20 h-20 bg-gray-50 dark:bg-gray-800 rounded-xl flex items-center justify-center overflow-hidden">
                  <img
                    v-if="product.primary_image"
                    :src="product.primary_image"
                    :alt="product.name_ar"
                    class="w-full h-full object-cover"
                  />
                  <span v-else class="text-2xl">📦</span>
                </div>
                <router-link
                  :to="`/products/${product.slug}`"
                  class="text-center font-semibold text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400 text-sm leading-tight line-clamp-2"
                >
                  {{ product.name_ar }}
                </router-link>
                <span class="text-xs text-gray-400">{{ product.brand?.name_ar }}</span>
                <button
                  type="button"
                  @click="removeProduct(product.id)"
                  class="text-xs text-danger hover:underline"
                >
                  إزالة
                </button>
              </div>
            </th>
          </tr>
        </thead>

        <tbody>
          <!-- قسم الأسعار -->
          <tr>
            <td class="bg-primary-50 dark:bg-primary-900/20 p-3 font-semibold text-primary-700 dark:text-primary-300 border border-gray-100 dark:border-gray-700">
              أفضل سعر
            </td>
            <td
              v-for="product in products"
              :key="`price-${product.id}`"
              class="p-4 text-center border border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900"
            >
              <template v-if="lowestPrice(product)">
                <p class="text-lg font-bold text-gray-900 dark:text-white">
                  {{ lowestPrice(product).amount }}
                  {{ lowestPrice(product).currency_symbol }}
                </p>
                <p class="text-xs text-gray-400 mt-1">{{ lowestPrice(product).store_name }}</p>
              </template>
              <span v-else class="text-gray-400 text-xs">غير متوفر</span>
            </td>
          </tr>

          <!-- المواصفات مجمَّعة من كل المنتجات -->
          <template v-for="group in allSpecGroups" :key="group">
            <tr>
              <td
                colspan="99"
                class="bg-gray-50 dark:bg-gray-800 px-4 py-2 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase border border-gray-100 dark:border-gray-700"
              >
                {{ group }}
              </td>
            </tr>
            <tr
              v-for="key in allSpecKeys[group]"
              :key="`${group}-${key}`"
              class="hover:bg-gray-50 dark:hover:bg-gray-800/50"
            >
              <td class="p-3 text-gray-500 dark:text-gray-400 border border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/40">
                {{ key }}
              </td>
              <td
                v-for="product in products"
                :key="`${product.id}-${group}-${key}`"
                class="p-3 text-center text-gray-900 dark:text-white border border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900"
              >
                {{ getSpec(product, group, key) || "—" }}
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import compareService from "@/services/compare.service";
import { useCompareStore } from "@/store/compare";

const route = useRoute();
const router = useRouter();
const compareStore = useCompareStore();

const products = ref([]);
const isLoading = ref(false);

function lowestPrice(product) {
  if (!product.prices?.length) return null;
  const inStock = product.prices.filter((p) => p.in_stock);
  const list = inStock.length ? inStock : product.prices;
  return list.reduce((min, p) =>
    Number(p.current_price) < Number(min.current_price) ? p : min
  );
}

// تجميع كل مجموعات المواصفات الموجودة عبر كل المنتجات (union)
const allSpecGroups = computed(() => {
  const groups = new Set();
  products.value.forEach((p) => {
    Object.keys(p.specifications || {}).forEach((g) => groups.add(g));
  });
  return [...groups];
});

// تجميع كل مفاتيح المواصفات داخل كل مجموعة
const allSpecKeys = computed(() => {
  const result = {};
  products.value.forEach((p) => {
    Object.entries(p.specifications || {}).forEach(([group, specs]) => {
      if (!result[group]) result[group] = new Set();
      specs.forEach((s) => result[group].add(s.key));
    });
  });
  return Object.fromEntries(Object.entries(result).map(([g, s]) => [g, [...s]]));
});

function getSpec(product, group, key) {
  const specs = product.specifications?.[group] || [];
  return specs.find((s) => s.key === key)?.value || null;
}

async function loadProducts() {
  const raw = route.query.ids || "";
  const ids = raw.split(",").map((i) => i.trim()).filter(Boolean);
  if (!ids.length) {
    products.value = [];
    return;
  }
  isLoading.value = true;
  try {
    const { data } = await compareService.compare(ids);
    products.value = data.data;
  } catch (err) {
    products.value = [];
  } finally {
    isLoading.value = false;
  }
}

function removeProduct(productId) {
  compareStore.remove(productId);
  const newIds = compareStore.ids.join(",");
  router.replace({ name: "compare", query: { ids: newIds } });
}

function handleClear() {
  compareStore.clear();
  router.replace({ name: "compare" });
}

watch(() => route.query.ids, loadProducts);
onMounted(loadProducts);
</script>

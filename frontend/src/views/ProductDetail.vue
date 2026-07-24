<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else-if="!product" class="text-center py-20">
      <div class="text-4xl mb-3">❓</div>
      <p class="text-gray-500 dark:text-gray-400">المنتج غير موجود.</p>
      <router-link to="/products" class="text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">
        رجوع للمنتجات
      </router-link>
    </div>

    <div v-else class="space-y-6">
      <!-- القسم العلوي: صور + معلومات أساسية -->
      <div class="grid lg:grid-cols-2 gap-8">
        <!-- الصور -->
        <div>
          <div class="aspect-square bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden flex items-center justify-center">
            <img v-if="mainImage" :src="mainImage" :alt="product.name_ar" class="w-full h-full object-cover" />
            <span v-else class="text-5xl">📦</span>
          </div>
          <div v-if="product.images?.length > 1" class="flex gap-2 mt-3">
            <button
              v-for="img in product.images"
              :key="img.id"
              type="button"
              @click="mainImage = img.image_url"
              class="w-16 h-16 rounded-lg overflow-hidden border-2 transition-colors"
              :class="mainImage === img.image_url ? 'border-primary-500' : 'border-transparent'"
            >
              <img :src="img.image_url" class="w-full h-full object-cover" />
            </button>
          </div>
        </div>

        <!-- التفاصيل -->
        <div>
          <p class="text-sm text-gray-400 mb-1">{{ product.brand?.name_ar }}</p>
          <div class="flex items-start justify-between gap-3 mb-3">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ product.name_ar }}</h1>
            <div class="flex items-center gap-2 shrink-0">
              <FavoriteButton :product-id="product.id" />
              <WatchlistButton :product-id="product.id" />
            </div>
          </div>

          <p v-if="product.description_ar" class="text-gray-600 dark:text-gray-300 mb-5 leading-relaxed text-sm">
            {{ product.description_ar }}
          </p>

          <!-- توصية الذكاء الاصطناعي -->
          <div class="mb-5">
            <PredictionCard :product-id="product.id" />
          </div>

          <!-- مقارنة الأسعار -->
          <div class="mb-5">
            <h2 class="font-semibold text-gray-900 dark:text-white mb-3">مقارنة الأسعار</h2>
            <div v-if="sortedPrices.length" class="space-y-2">
              <div
                v-for="(price, idx) in sortedPrices"
                :key="idx"
                class="flex items-center justify-between p-3 rounded-xl border border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800"
                :class="idx === 0 ? 'border-primary-200 dark:border-primary-800 bg-primary-50/50 dark:bg-primary-900/10' : ''"
              >
                <div>
                  <div class="flex items-center gap-1.5">
                    <p class="font-medium text-gray-900 dark:text-white text-sm">{{ price.store_name }}</p>
                    <span v-if="idx === 0" class="text-[10px] bg-primary-600 text-white px-1.5 py-0.5 rounded-full">الأفضل</span>
                  </div>
                  <p class="text-xs text-gray-400 mt-0.5">{{ price.country_code }}</p>
                </div>
                <div class="text-left">
                  <p class="font-bold text-gray-900 dark:text-white">
                    {{ price.current_price }} {{ price.currency_symbol }}
                  </p>
                  <a
                    :href="price.product_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-xs text-primary-600 dark:text-primary-400 hover:underline"
                  >
                    زيارة المتجر
                  </a>
                </div>
              </div>
            </div>
            <p v-else class="text-gray-400 dark:text-gray-500 text-sm">
              لا تتوفر بيانات سعر حقيقية لهذا المنتج حاليًا.
            </p>
          </div>
        </div>
      </div>

      <!-- الرسم البياني للأسعار -->
      <PriceChart :product-id="product.id" />

      <!-- المواصفات التقنية -->
      <div v-if="hasSpecs" class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5">
        <h2 class="font-semibold text-gray-900 dark:text-white mb-4">المواصفات التقنية</h2>
        <div v-for="(specs, group) in product.specifications" :key="group" class="mb-4 last:mb-0">
          <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2 pb-1 border-b border-gray-100 dark:border-gray-700">
            {{ group }}
          </h3>
          <dl class="divide-y divide-gray-100 dark:divide-gray-700 text-sm">
            <div v-for="(spec, idx) in specs" :key="idx" class="flex justify-between py-2">
              <dt class="text-gray-500 dark:text-gray-400">{{ spec.key }}</dt>
              <dd class="text-gray-900 dark:text-white font-medium text-left">{{ spec.value }}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import productService from "@/services/product.service";
import FavoriteButton from "@/components/products/FavoriteButton.vue";
import WatchlistButton from "@/components/products/WatchlistButton.vue";
import PredictionCard from "@/components/products/PredictionCard.vue";
import PriceChart from "@/components/products/PriceChart.vue";

const route = useRoute();
const product = ref(null);
const isLoading = ref(false);
const mainImage = ref(null);

const hasSpecs = computed(
  () => product.value?.specifications && Object.keys(product.value.specifications).length > 0
);

const sortedPrices = computed(() => {
  if (!product.value?.prices) return [];
  return [...product.value.prices].sort(
    (a, b) => Number(a.current_price) - Number(b.current_price)
  );
});

async function loadProduct() {
  isLoading.value = true;
  product.value = null;
  try {
    const { data } = await productService.getBySlug(route.params.slug);
    product.value = data.data;
    const primary = product.value.images?.find((img) => img.is_primary) || product.value.images?.[0];
    mainImage.value = primary?.image_url || null;
  } catch (err) {
    product.value = null;
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadProduct);
watch(() => route.params.slug, loadProduct);
</script>

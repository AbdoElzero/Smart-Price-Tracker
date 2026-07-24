<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">العلامات التجارية</h1>
      <div class="relative">
        <input
          v-model="search"
          type="search"
          placeholder="بحث..."
          class="pl-8 pr-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/30"
        />
        <span class="absolute inset-y-0 left-2 flex items-center text-gray-400 text-xs">🔍</span>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else>
      <!-- رسالة لو مفيش نتائج -->
      <div v-if="filteredBrands.length === 0" class="text-center py-16">
        <div class="text-4xl mb-3">🔍</div>
        <p class="text-gray-500 dark:text-gray-400">لا توجد علامات تجارية تطابق بحثك.</p>
      </div>

      <!-- شبكة العلامات التجارية مجمّعة أبجدياً -->
      <div v-else>
        <div v-for="group in groupedBrands" :key="group.letter" class="mb-8">
          <h2 class="text-sm font-bold text-gray-400 dark:text-gray-500 mb-3 px-1">
            {{ group.letter }}
          </h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            <router-link
              v-for="brand in group.brands"
              :key="brand.slug"
              :to="{ path: '/products', query: { brand: brand.slug } }"
              class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 hover:shadow-md transition-all text-center"
            >
              <div
                v-if="brand.logo_url"
                class="w-12 h-12 rounded-xl overflow-hidden bg-gray-50 dark:bg-gray-900 flex items-center justify-center"
              >
                <img :src="brand.logo_url" :alt="brand.name_ar" class="w-full h-full object-contain" />
              </div>
              <div
                v-else
                class="w-12 h-12 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center font-bold text-primary-700 dark:text-primary-300 text-lg"
              >
                {{ brand.name_en.charAt(0).toUpperCase() }}
              </div>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-200">
                {{ brand.name_ar }}
              </span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import catalogService from "@/services/catalog.service";

const brands = ref([]);
const isLoading = ref(false);
const search = ref("");

const filteredBrands = computed(() => {
  if (!search.value.trim()) return brands.value;
  const q = search.value.trim().toLowerCase();
  return brands.value.filter(
    (b) =>
      b.name_ar.toLowerCase().includes(q) ||
      b.name_en.toLowerCase().includes(q)
  );
});

const groupedBrands = computed(() => {
  const groups = {};
  filteredBrands.value.forEach((brand) => {
    const letter = brand.name_en.charAt(0).toUpperCase();
    if (!groups[letter]) groups[letter] = [];
    groups[letter].push(brand);
  });
  return Object.entries(groups)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([letter, brands]) => ({ letter, brands }));
});

async function loadBrands() {
  isLoading.value = true;
  try {
    const { data } = await catalogService.listBrands();
    brands.value = data.data;
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadBrands);
</script>

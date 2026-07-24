<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">
        المنتجات
        <span class="text-sm font-normal text-gray-400">({{ meta.total }})</span>
      </h1>
      <select v-model="sort" @change="onSortChange"
        class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm text-gray-700 dark:text-gray-200">
        <option value="newest">الأحدث</option>
        <option value="price_asc">السعر: من الأقل للأعلى</option>
        <option value="price_desc">السعر: من الأعلى للأقل</option>
        <option value="name_asc">الاسم (أ - ي)</option>
        <option value="name_desc">الاسم (ي - أ)</option>
      </select>
    </div>

    <!-- Chips الفلاتر النشطة -->
    <div v-if="activeFiltersCount > 0" class="flex flex-wrap gap-2 mb-4">
      <span class="text-xs text-gray-500 dark:text-gray-400 self-center">فلاتر نشطة:</span>
      <button v-if="category" type="button" @click="removeFilter('category')"
        class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs">
        {{ getCategoryName(category) }} ✕
      </button>
      <button v-if="brandIds.length" type="button" @click="removeFilter('brandIds')"
        class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs">
        {{ brandIds.length }} علامة تجارية ✕
      </button>
      <button v-if="minPrice" type="button" @click="removeFilter('minPrice')"
        class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs">
        من {{ minPrice }} ✕
      </button>
      <button v-if="maxPrice" type="button" @click="removeFilter('maxPrice')"
        class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs">
        إلى {{ maxPrice }} ✕
      </button>
      <button type="button" @click="clearAllFilters"
        class="text-xs text-danger hover:underline self-center">مسح الكل</button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <aside class="lg:col-span-1">
        <ProductFilters
          :categories="categories"
          :brands="brands"
          :selected-category="category"
          :selected-brand="brand"
          :selected-brand-ids="brandIds"
          :selected-min-price="minPrice"
          :selected-max-price="maxPrice"
          @update:category="onFilterChange('category', $event)"
          @update:brand="onFilterChange('brand', $event)"
          @update:brandIds="onFilterChange('brandIds', $event)"
          @update:minPrice="onFilterChange('minPrice', $event)"
          @update:maxPrice="onFilterChange('maxPrice', $event)"
        />
      </aside>

      <div class="lg:col-span-3">
        <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

        <div v-else-if="products.length === 0" class="text-center py-20">
          <div class="text-4xl mb-3">📭</div>
          <p class="text-gray-500 dark:text-gray-400 mb-2">لا توجد منتجات مطابقة.</p>
          <button type="button" @click="clearAllFilters"
            class="text-sm text-primary-600 dark:text-primary-400 hover:underline">
            مسح الفلاتر
          </button>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <ProductCard v-for="product in products" :key="product.id" :product="product" />
        </div>

        <Pagination :page="page" :total-pages="meta.total_pages" @change="onPageChange" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import productService from "@/services/product.service";
import catalogService from "@/services/catalog.service";
import ProductCard from "@/components/products/ProductCard.vue";
import ProductFilters from "@/components/products/ProductFilters.vue";
import Pagination from "@/components/ui/Pagination.vue";

const route = useRoute();
const router = useRouter();

// ─── State ────────────────────────────────────────────────────────────────────
const products = ref([]);
const categories = ref([]);
const brands = ref([]);
const meta = ref({ total: 0, total_pages: 0 });
const isLoading = ref(false);

const searchQuery = ref(route.query.q || "");
const category = ref(route.query.category || "");
const brand = ref(route.query.brand || "");
const brandIds = ref(route.query.brands ? route.query.brands.split(",").map(Number) : []);
const minPrice = ref(route.query.min_price ? Number(route.query.min_price) : null);
const maxPrice = ref(route.query.max_price ? Number(route.query.max_price) : null);
const sort = ref(route.query.sort || "newest");
const page = ref(Number(route.query.page) || 1);

// ─── Debounce (بدون watch - مستدعى يدوياً فقط) ────────────────────────────────
let debounceTimer = null;

function scheduleLoad() {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    loadProducts();
  }, 350);
}

onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer);
});
// ─────────────────────────────────────────────────────────────────────────────

const activeFiltersCount = computed(() => {
  let c = 0;
  if (category.value) c++;
  if (brandIds.value.length) c++;
  if (minPrice.value) c++;
  if (maxPrice.value) c++;
  return c;
});

function getCategoryName(slug) {
  return categories.value.find((c) => c.slug === slug)?.name_ar || slug;
}

// تغيير فلتر → reset الصفحة ثم جدولة طلب واحد
function onFilterChange(key, value) {
  if (key === "category") category.value = value;
  else if (key === "brand") brand.value = value;
  else if (key === "brandIds") brandIds.value = value;
  else if (key === "minPrice") minPrice.value = value;
  else if (key === "maxPrice") maxPrice.value = value;

  page.value = 1; // reset مباشرة بدون watch
  scheduleLoad();
}

function removeFilter(key) {
  if (key === "category") category.value = "";
  else if (key === "brand") brand.value = "";
  else if (key === "brandIds") brandIds.value = [];
  else if (key === "minPrice") minPrice.value = null;
  else if (key === "maxPrice") maxPrice.value = null;

  page.value = 1;
  scheduleLoad();
}

function clearAllFilters() {
  category.value = "";
  brand.value = "";
  brandIds.value = [];
  minPrice.value = null;
  maxPrice.value = null;
  page.value = 1;
  scheduleLoad();
}

// تغيير الترتيب
function onSortChange() {
  page.value = 1;
  scheduleLoad();
}

// تغيير الصفحة (من Pagination) - مباشر بدون debounce
function onPageChange(newPage) {
  page.value = newPage;
  loadProducts(); // مباشر، بدون debounce
}

// ─── API Calls ────────────────────────────────────────────────────────────────
async function loadCatalog() {
  try {
    const [catRes, brandRes] = await Promise.all([
      catalogService.listCategories(),
      catalogService.listBrands(),
    ]);
    const flat = [];
    catRes.data.data.forEach((cat) => {
      flat.push(cat);
      cat.children?.forEach((child) => flat.push(child));
    });
    categories.value = flat;
    brands.value = brandRes.data.data;
  } catch {
    categories.value = [];
    brands.value = [];
  }
}

async function loadProducts() {
  isLoading.value = true;

  const params = { sort: sort.value, page: page.value, per_page: 12 };
  if (searchQuery.value) params.q = searchQuery.value;
  if (category.value) params.category = category.value;
  if (brand.value) params.brand = brand.value;
  if (brandIds.value.length) params.brands = brandIds.value.join(",");
  if (minPrice.value) params.min_price = minPrice.value;
  if (maxPrice.value) params.max_price = maxPrice.value;

  // تحديث URL
  const q = {};
  if (searchQuery.value) q.q = searchQuery.value;
  if (category.value) q.category = category.value;
  if (brand.value) q.brand = brand.value;
  if (brandIds.value.length) q.brands = brandIds.value.join(",");
  if (minPrice.value) q.min_price = minPrice.value;
  if (maxPrice.value) q.max_price = maxPrice.value;
  if (sort.value !== "newest") q.sort = sort.value;
  if (page.value > 1) q.page = page.value;
  router.replace({ query: q });

  try {
    const { data } = await productService.list(params);
    products.value = data.data;
    meta.value = data.meta;
  } catch {
    products.value = [];
    meta.value = { total: 0, total_pages: 0 };
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadCatalog();
  loadProducts();
});
</script>

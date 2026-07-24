<template>
  <div class="space-y-6">
    <!-- الفئات -->
    <div>
      <h3 class="font-semibold text-gray-900 dark:text-white mb-3 text-sm">التصنيف</h3>
      <div class="space-y-1.5">
        <button type="button" @click="$emit('update:category', '')"
          class="block w-full text-right px-3 py-1.5 rounded-lg text-sm transition-colors"
          :class="!selectedCategory
            ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-medium'
            : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'">
          الكل
        </button>
        <button v-for="cat in categories" :key="cat.slug" type="button"
          @click="$emit('update:category', cat.slug)"
          class="block w-full text-right px-3 py-1.5 rounded-lg text-sm transition-colors"
          :class="selectedCategory === cat.slug
            ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-medium'
            : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'">
          {{ cat.icon }} {{ cat.name_ar }}
        </button>
      </div>
    </div>

    <!-- العلامات التجارية (Checkboxes) -->
    <div>
      <h3 class="font-semibold text-gray-900 dark:text-white mb-3 text-sm">العلامة التجارية</h3>
      <div class="space-y-1.5 max-h-44 overflow-y-auto">
        <label v-for="brand in brands" :key="brand.id"
          class="flex items-center gap-2 px-2 py-1 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800">
          <input
            type="checkbox"
            :value="brand.id"
            :checked="localBrandIds.includes(brand.id)"
            @change="onBrandToggle(brand.id, $event.target.checked)"
            class="w-3.5 h-3.5 rounded accent-primary-600"
          />
          <span class="text-sm text-gray-700 dark:text-gray-300">{{ brand.name_ar }}</span>
        </label>
      </div>
      <button v-if="localBrandIds.length" type="button"
        @click="clearBrands"
        class="text-xs text-gray-400 hover:text-danger mt-1.5">
        مسح الاختيار
      </button>
    </div>

    <!-- نطاق السعر -->
    <PriceRangeFilter
      :min-price="selectedMinPrice"
      :max-price="selectedMaxPrice"
      @update:minPrice="$emit('update:minPrice', $event)"
      @update:maxPrice="$emit('update:maxPrice', $event)"
    />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue";
import PriceRangeFilter from "./PriceRangeFilter.vue";

const props = defineProps({
  categories: { type: Array, default: () => [] },
  brands: { type: Array, default: () => [] },
  selectedCategory: { type: String, default: "" },
  selectedBrand: { type: String, default: "" },
  selectedBrandIds: { type: Array, default: () => [] },
  selectedMinPrice: { type: Number, default: null },
  selectedMaxPrice: { type: Number, default: null },
});

const emit = defineEmits([
  "update:category",
  "update:brand",
  "update:brandIds",
  "update:minPrice",
  "update:maxPrice",
]);

// نسخة محلية من البراندات المختارة
const localBrandIds = ref([...props.selectedBrandIds]);

// Flag لمنع الحلقة المفرغة: لما التحديث جاي من الـ parent لا نعيد الـ emit
let syncingFromParent = false;

// الـ parent غيّر selectedBrandIds (مثل "مسح الكل") → نحدّث المحلي بدون emit
watch(
  () => props.selectedBrandIds,
  (newVal) => {
    syncingFromParent = true;
    localBrandIds.value = [...newVal];
    nextTick(() => { syncingFromParent = false; });
  },
  { deep: true }
);

// المستخدم اختار/أشيل براند بيده → نُطلق emit للـ parent
function onBrandToggle(brandId, checked) {
  if (checked) {
    localBrandIds.value = [...localBrandIds.value, brandId];
  } else {
    localBrandIds.value = localBrandIds.value.filter((id) => id !== brandId);
  }
  if (!syncingFromParent) {
    emit("update:brandIds", [...localBrandIds.value]);
  }
}

function clearBrands() {
  localBrandIds.value = [];
  emit("update:brandIds", []);
}
</script>

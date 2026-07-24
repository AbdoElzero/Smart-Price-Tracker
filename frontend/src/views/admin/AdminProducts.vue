<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-bold text-gray-900 dark:text-white">
        إدارة المنتجات
        <span class="text-sm font-normal text-gray-400">({{ meta.total }})</span>
      </h2>
      <button type="button" @click="openCreateModal"
        class="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 transition-colors">
        + إضافة منتج
      </button>
    </div>

    <!-- جدول المنتجات -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 dark:bg-gray-800 text-right">
          <tr>
            <th class="px-4 py-3 font-medium text-gray-500">#</th>
            <th class="px-4 py-3 font-medium text-gray-500">المنتج</th>
            <th class="px-4 py-3 font-medium text-gray-500 hidden sm:table-cell">العلامة</th>
            <th class="px-4 py-3 font-medium text-gray-500 hidden md:table-cell">الفئة</th>
            <th class="px-4 py-3 font-medium text-gray-500">الحالة</th>
            <th class="px-4 py-3 font-medium text-gray-500">إجراءات</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr v-if="isLoading">
            <td colspan="6" class="px-4 py-8 text-center text-gray-400">جارٍ التحميل...</td>
          </tr>
          <tr v-else-if="!products.length">
            <td colspan="6" class="px-4 py-8 text-center text-gray-400">لا توجد منتجات</td>
          </tr>
          <tr v-for="product in products" :key="product.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td class="px-4 py-3 text-gray-400">{{ product.id }}</td>
            <td class="px-4 py-3">
              <p class="font-medium text-gray-900 dark:text-white line-clamp-1">{{ product.name_ar }}</p>
              <p class="text-xs text-gray-400">{{ product.slug }}</p>
            </td>
            <td class="px-4 py-3 text-gray-500 hidden sm:table-cell">{{ product.brand?.name_ar }}</td>
            <td class="px-4 py-3 text-gray-500 hidden md:table-cell">{{ product.category?.name_ar }}</td>
            <td class="px-4 py-3">
              <span class="text-xs px-2 py-1 rounded-full font-medium"
                :class="product.is_active
                  ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                  : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400'">
                {{ product.is_active ? "فعّال" : "مُعطَّل" }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-2">
                <button type="button" @click="openEditModal(product)"
                  class="text-xs text-primary-600 dark:text-primary-400 hover:underline">
                  تعديل
                </button>
                <button type="button" @click="handleDelete(product)"
                  class="text-xs text-danger hover:underline">
                  حذف
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="flex items-center justify-between px-4 py-3 border-t border-gray-100 dark:border-gray-800">
        <span class="text-xs text-gray-400">إجمالي: {{ meta.total }}</span>
        <div class="flex gap-2">
          <button type="button" :disabled="page <= 1" @click="page--"
            class="text-xs px-3 py-1 rounded border border-gray-200 dark:border-gray-700 disabled:opacity-40">
            السابق
          </button>
          <button type="button" :disabled="page * perPage >= meta.total" @click="page++"
            class="text-xs px-3 py-1 rounded border border-gray-200 dark:border-gray-700 disabled:opacity-40">
            التالي
          </button>
        </div>
      </div>
    </div>

    <!-- Modal إضافة/تعديل -->
    <div v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4"
      @click.self="showModal = false">
      <div class="bg-white dark:bg-gray-900 rounded-2xl w-full max-w-2xl p-6 max-h-[90vh] overflow-y-auto">
        <h3 class="font-bold text-gray-900 dark:text-white mb-5">
          {{ editingProduct ? "تعديل منتج" : "إضافة منتج جديد" }}
        </h3>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- الأسماء -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="field-label">الاسم بالعربية *</label>
              <input v-model="form.name_ar" required class="field-input" />
            </div>
            <div>
              <label class="field-label">الاسم بالإنجليزية *</label>
              <input v-model="form.name_en" required class="field-input" />
            </div>
          </div>

          <!-- العلامة والفئة -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="field-label">العلامة التجارية *</label>
              <select v-model="form.brand_id" required class="field-input">
                <option value="">اختر...</option>
                <option v-for="b in brands" :key="b.id" :value="b.id">{{ b.name_ar }}</option>
              </select>
            </div>
            <div>
              <label class="field-label">الفئة *</label>
              <select v-model="form.category_id" required class="field-input">
                <option value="">اختر...</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name_ar }}</option>
              </select>
            </div>
          </div>

          <!-- رقم الموديل -->
          <div>
            <label class="field-label">رقم الموديل</label>
            <input v-model="form.model_number" class="field-input" placeholder="مثال: RTX4070, SM-S921B" />
          </div>

          <!-- الصورة -->
          <div>
            <label class="field-label">رابط الصورة الرئيسية</label>
            <input v-model="form.image_url" class="field-input" placeholder="https://..." />
          </div>

          <!-- الوصف -->
          <div>
            <label class="field-label">الوصف بالعربية</label>
            <textarea v-model="form.description_ar" rows="2" class="field-input resize-none"></textarea>
          </div>

          <!-- الحالة -->
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="form.is_active" id="is_active" class="w-4 h-4" />
            <label for="is_active" class="text-sm text-gray-700 dark:text-gray-300">منتج فعّال</label>
          </div>

          <!-- ─── المواصفات ─── -->
          <div class="border-t border-gray-100 dark:border-gray-700 pt-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="font-semibold text-gray-900 dark:text-white text-sm">المواصفات التقنية</h4>
              <button type="button" @click="addSpec"
                class="text-xs text-primary-600 dark:text-primary-400 hover:underline">
                + إضافة مواصفة
              </button>
            </div>

            <div v-if="form.specifications.length === 0"
              class="text-xs text-gray-400 text-center py-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              لا توجد مواصفات بعد — اضغط "إضافة مواصفة" للبدء
            </div>

            <div v-for="(spec, idx) in form.specifications" :key="idx"
              class="grid grid-cols-7 gap-2 items-center mb-2">
              <div class="col-span-2">
                <input v-model="spec.group_name" placeholder="المجموعة (مثال: المعالج)"
                  class="field-input text-xs" />
              </div>
              <div class="col-span-2">
                <input v-model="spec.key_ar" placeholder="الخاصية (مثال: نوع المعالج)"
                  class="field-input text-xs" required />
              </div>
              <div class="col-span-2">
                <input v-model="spec.value_ar" placeholder="القيمة (مثال: Intel Core i9)"
                  class="field-input text-xs" required />
              </div>
              <div class="col-span-1 flex justify-center">
                <button type="button" @click="removeSpec(idx)"
                  class="text-danger hover:text-red-700 text-sm font-bold">✕</button>
              </div>
            </div>

            <p v-if="form.specifications.length > 0"
              class="text-xs text-gray-400 mt-1">
              المجموعة → الخاصية → القيمة (مثال: الشاشة → الحجم → 6.1 بوصة)
            </p>
          </div>

          <p v-if="formError" class="text-xs text-danger">{{ formError }}</p>

          <div class="flex gap-2 pt-2">
            <button type="submit" :disabled="isSaving"
              class="flex-1 py-2.5 rounded-lg bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 disabled:opacity-60">
              {{ isSaving ? "جارٍ الحفظ..." : editingProduct ? "حفظ التعديلات" : "إضافة المنتج" }}
            </button>
            <button type="button" @click="showModal = false"
              class="px-4 py-2.5 rounded-lg border border-gray-200 dark:border-gray-700 text-sm">
              إلغاء
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from "vue";
import adminService from "@/services/admin.service";
import catalogService from "@/services/catalog.service";

const products = ref([]);
const brands = ref([]);
const categories = ref([]);
const meta = ref({ total: 0 });
const isLoading = ref(false);
const page = ref(1);
const perPage = 20;

const showModal = ref(false);
const editingProduct = ref(null);
const isSaving = ref(false);
const formError = ref("");

const defaultForm = () => ({
  name_ar: "",
  name_en: "",
  description_ar: "",
  description_en: "",
  model_number: "",
  image_url: "",
  brand_id: "",
  category_id: "",
  is_active: true,
  specifications: [],
});

const form = reactive(defaultForm());

function addSpec() {
  form.specifications.push({ group_name: "", key_ar: "", value_ar: "" });
}

function removeSpec(idx) {
  form.specifications.splice(idx, 1);
}

async function loadProducts() {
  isLoading.value = true;
  try {
    const { data } = await adminService.listProducts({ page: page.value, per_page: perPage });
    products.value = data.data;
    meta.value = data.meta;
  } finally {
    isLoading.value = false;
  }
}

async function loadCatalog() {
  const [b, c] = await Promise.all([catalogService.listBrands(), catalogService.listCategories()]);
  brands.value = b.data.data;
  const flat = [];
  c.data.data.forEach((cat) => {
    flat.push(cat);
    cat.children?.forEach((child) => flat.push(child));
  });
  categories.value = flat;
}

function openCreateModal() {
  editingProduct.value = null;
  Object.assign(form, defaultForm());
  form.specifications = [];
  formError.value = "";
  showModal.value = true;
}

async function openEditModal(product) {
  editingProduct.value = product;
  formError.value = "";

  // جلب التفاصيل الكاملة (مع المواصفات)
  try {
    const { data } = await adminService.getProduct(product.id);
    const p = data.data;

    Object.assign(form, {
      name_ar: p.name_ar || "",
      name_en: p.name_en || p.name_ar || "",
      description_ar: p.description_ar || "",
      description_en: p.description_en || "",
      model_number: p.model_number || "",
      image_url: p.primary_image || "",
      brand_id: p.brand?.id || "",
      category_id: p.category?.id || "",
      is_active: p.is_active !== false,
    });

    // تحويل المواصفات من الصيغة المُجمَّعة للصيغة المفردة
    form.specifications = [];
    if (p.specifications) {
      Object.entries(p.specifications).forEach(([group, specs]) => {
        specs.forEach((s) => {
          form.specifications.push({
            group_name: group,
            key_ar: s.key,
            value_ar: s.value,
          });
        });
      });
    }
  } catch (err) {
    formError.value = "تعذّر جلب بيانات المنتج";
  }

  showModal.value = true;
}

async function handleSubmit() {
  isSaving.value = true;
  formError.value = "";
  const payload = {
    name_ar: form.name_ar,
    name_en: form.name_en,
    description_ar: form.description_ar || null,
    description_en: form.description_en || null,
    model_number: form.model_number || null,
    image_url: form.image_url || null,
    brand_id: Number(form.brand_id),
    category_id: Number(form.category_id),
    is_active: form.is_active,
    specifications: form.specifications.filter((s) => s.key_ar && s.value_ar),
  };
  try {
    if (editingProduct.value) {
      await adminService.updateProduct(editingProduct.value.id, payload);
    } else {
      await adminService.createProduct(payload);
    }
    showModal.value = false;
    await loadProducts();
  } catch (err) {
    formError.value = err.response?.data?.error || "حدث خطأ، حاول مرة أخرى";
  } finally {
    isSaving.value = false;
  }
}

async function handleDelete(product) {
  if (!confirm(`هل أنت متأكد من حذف "${product.name_ar}"؟\nسيتم حذف كل البيانات المرتبطة به.`)) return;
  try {
    await adminService.deleteProduct(product.id);
    await loadProducts();
  } catch (err) {
    alert(err.response?.data?.error || "تعذّر الحذف");
  }
}

watch(page, loadProducts);
onMounted(() => { loadProducts(); loadCatalog(); });
</script>

<style scoped>
.field-label {
  @apply block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1;
}
.field-input {
  @apply w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500;
}
</style>

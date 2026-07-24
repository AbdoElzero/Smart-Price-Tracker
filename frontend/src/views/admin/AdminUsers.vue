<template>
  <div>
    <h2 class="text-lg font-bold text-gray-900 dark:text-white mb-6">
      إدارة المستخدمين
      <span class="text-sm font-normal text-gray-400">({{ meta.total }})</span>
    </h2>

    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 dark:bg-gray-800 text-right">
          <tr>
            <th class="px-4 py-3 font-medium text-gray-500">المستخدم</th>
            <th class="px-4 py-3 font-medium text-gray-500 hidden sm:table-cell">البريد</th>
            <th class="px-4 py-3 font-medium text-gray-500">الدور</th>
            <th class="px-4 py-3 font-medium text-gray-500">الحالة</th>
            <th class="px-4 py-3 font-medium text-gray-500">إجراءات</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr v-if="isLoading">
            <td colspan="5" class="px-4 py-8 text-center text-gray-400">جارٍ التحميل...</td>
          </tr>
          <tr v-else-if="!users.length">
            <td colspan="5" class="px-4 py-8 text-center text-gray-400">لا يوجد مستخدمون</td>
          </tr>
          <tr v-for="(user, idx) in users" :key="user.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td class="px-4 py-3">
              <p class="font-medium text-gray-900 dark:text-white">{{ user.name }}</p>
              <p class="text-xs text-gray-400">{{ formatDate(user.created_at) }}</p>
            </td>
            <td class="px-4 py-3 text-gray-500 hidden sm:table-cell">{{ user.email }}</td>
            <td class="px-4 py-3">
              <span class="text-xs px-2 py-1 rounded-full font-medium"
                :class="user.role === 'admin'
                  ? 'bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400'
                  : 'bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400'">
                {{ user.role === "admin" ? "مشرف" : "مستخدم" }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span class="text-xs px-2 py-1 rounded-full font-medium"
                :class="user.is_active
                  ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                  : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400'">
                {{ user.is_active ? "فعّال" : "مُعطَّل" }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-2">
                <button type="button" @click="toggleActive(idx, user)"
                  class="text-xs hover:underline"
                  :class="user.is_active ? 'text-danger' : 'text-success'">
                  {{ user.is_active ? "تعطيل" : "تفعيل" }}
                </button>
                <button type="button" @click="toggleRole(idx, user)"
                  class="text-xs text-primary-600 dark:text-primary-400 hover:underline">
                  {{ user.role === "admin" ? "إلغاء الإدارة" : "ترقية لمشرف" }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

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
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import adminService from "@/services/admin.service";

const users = ref([]);
const meta = ref({ total: 0 });
const isLoading = ref(false);
const page = ref(1);
const perPage = 20;

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("ar-EG");
}

async function loadUsers() {
  isLoading.value = true;
  try {
    const { data } = await adminService.listUsers({ page: page.value, per_page: perPage });
    users.value = data.data;
    meta.value = data.meta;
  } finally {
    isLoading.value = false;
  }
}

async function toggleActive(idx, user) {
  try {
    const { data } = await adminService.updateUser(user.id, { is_active: !user.is_active });
    // استبدال العنصر كاملاً في الـ Array بدل Object.assign (يضمن Vue Reactivity)
    users.value.splice(idx, 1, data.data);
  } catch (err) {
    alert(err.response?.data?.error || "تعذّر التعديل");
  }
}

async function toggleRole(idx, user) {
  const newRole = user.role === "admin" ? "user" : "admin";
  const label = newRole === "admin" ? "ترقية لمشرف" : "إلغاء الإدارة";
  if (!confirm(`هل أنت متأكد من ${label} للمستخدم "${user.name}"؟`)) return;
  try {
    const { data } = await adminService.updateUser(user.id, { role: newRole });
    // splice يضمن تحديث Vue للـ DOM فوراً
    users.value.splice(idx, 1, data.data);
  } catch (err) {
    alert(err.response?.data?.error || "تعذّر التعديل");
  }
}

watch(page, loadUsers);
onMounted(loadUsers);
</script>

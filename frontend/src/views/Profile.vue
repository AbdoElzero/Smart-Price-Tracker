<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
    <!-- هيدر الملف الشخصي -->
    <div class="rounded-2xl overflow-hidden bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 mb-6">
      <div class="h-24 bg-gradient-to-l from-primary-600 to-primary-400"></div>
      <div class="px-6 pb-6 -mt-14 flex flex-col sm:flex-row sm:items-end gap-4">
        <AvatarUpload />
        <div class="flex-1 sm:pb-1 text-center sm:text-right">
          <h1 class="text-lg font-bold text-gray-900 dark:text-white">
            {{ authStore.user?.name || "..." }}
          </h1>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ authStore.user?.email }}</p>
        </div>
      </div>
    </div>

    <!-- البيانات الأساسية -->
    <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 mb-6">
      <h2 class="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <span>👤</span> البيانات الأساسية
      </h2>

      <form @submit.prevent="handleProfileSubmit" class="space-y-4">
        <BaseInput id="name" v-model="profileForm.name" label="الاسم الكامل" />

        <div>
          <label class="block mb-1.5 text-sm font-medium text-gray-700 dark:text-gray-300">
            البريد الإلكتروني
          </label>
          <input
            :value="authStore.user?.email"
            disabled
            class="w-full px-4 py-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-400 dark:text-gray-500"
          />
        </div>

        <div>
          <label class="block mb-1.5 text-sm font-medium text-gray-700 dark:text-gray-300">
            الدولة المفضّلة
          </label>
          <select
            v-model="profileForm.preferred_country_id"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500"
          >
            <option :value="null">بدون تحديد</option>
            <option v-for="country in countries" :key="country.id" :value="country.id">
              {{ country.flag_emoji }} {{ country.name_ar }}
            </option>
          </select>
        </div>

        <div class="flex items-center gap-3 pt-2">
          <BaseButton type="submit" :loading="isSavingProfile" class="!w-auto px-6">
            حفظ التعديلات
          </BaseButton>
          <p v-if="profileSuccess" class="text-sm text-success">{{ profileSuccess }}</p>
          <p v-if="profileError" class="text-sm text-danger">{{ profileError }}</p>
        </div>
      </form>
    </section>

    <!-- الأمان وكلمة السر -->
    <section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6">
      <h2 class="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <span>🔒</span> الأمان وكلمة السر
      </h2>

      <div
        v-if="authStore.user && !authStore.user.has_password"
        class="text-sm text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-900 rounded-lg p-4"
      >
        هذا الحساب مسجَّل عبر Google، ولا يحتاج كلمة سر منفصلة.
      </div>

      <form v-else @submit.prevent="handlePasswordSubmit" class="space-y-4">
        <BaseInput
          id="current_password"
          v-model="passwordForm.current_password"
          type="password"
          label="كلمة السر الحالية"
          autocomplete="current-password"
        />
        <BaseInput
          id="new_password"
          v-model="passwordForm.new_password"
          type="password"
          label="كلمة السر الجديدة"
          autocomplete="new-password"
        />

        <div class="flex items-center gap-3 pt-2">
          <BaseButton type="submit" :loading="isSavingPassword" class="!w-auto px-6">
            تغيير كلمة السر
          </BaseButton>
          <p v-if="passwordSuccess" class="text-sm text-success">{{ passwordSuccess }}</p>
          <p v-if="passwordError" class="text-sm text-danger">{{ passwordError }}</p>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import { useAuthStore } from "@/store/auth";
import profileService from "@/services/profile.service";
import catalogService from "@/services/catalog.service";
import BaseInput from "@/components/ui/BaseInput.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import AvatarUpload from "@/components/profile/AvatarUpload.vue";

const authStore = useAuthStore();

const countries = ref([]);

const profileForm = reactive({
  name: authStore.user?.name || "",
  preferred_country_id: authStore.user?.preferred_country_id ?? null,
});

const isSavingProfile = ref(false);
const profileSuccess = ref("");
const profileError = ref("");

const passwordForm = reactive({
  current_password: "",
  new_password: "",
});
const isSavingPassword = ref(false);
const passwordSuccess = ref("");
const passwordError = ref("");

async function loadCountries() {
  try {
    const { data } = await catalogService.listCountries();
    countries.value = data.data;
  } catch (err) {
    countries.value = [];
  }
}

async function handleProfileSubmit() {
  isSavingProfile.value = true;
  profileSuccess.value = "";
  profileError.value = "";
  try {
    await profileService.updateProfile({
      name: profileForm.name,
      preferred_country_id: profileForm.preferred_country_id,
    });
    await authStore.fetchCurrentUser();
    profileSuccess.value = "تم حفظ التعديلات بنجاح";
  } catch (err) {
    profileError.value = err.response?.data?.error || "حدث خطأ، حاول مرة أخرى";
  } finally {
    isSavingProfile.value = false;
  }
}

async function handlePasswordSubmit() {
  isSavingPassword.value = true;
  passwordSuccess.value = "";
  passwordError.value = "";
  try {
    await profileService.changePassword(passwordForm);
    passwordSuccess.value = "تم تغيير كلمة السر بنجاح";
    passwordForm.current_password = "";
    passwordForm.new_password = "";
  } catch (err) {
    passwordError.value = err.response?.data?.error || "حدث خطأ، حاول مرة أخرى";
  } finally {
    isSavingPassword.value = false;
  }
}

watch(
  () => authStore.user,
  (user) => {
    if (user) {
      profileForm.name = user.name || "";
      profileForm.preferred_country_id = user.preferred_country_id ?? null;
    }
  }
);

onMounted(() => {
  loadCountries();
  if (!authStore.user) {
    authStore.fetchCurrentUser();
  }
});
</script>

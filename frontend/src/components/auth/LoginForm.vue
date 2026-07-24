<template>
  <form @submit.prevent="handleSubmit" class="space-y-5">
    <BaseInput
      id="email"
      v-model="form.email"
      type="email"
      label="البريد الإلكتروني"
      placeholder="example@email.com"
      autocomplete="email"
      :error="fieldErrors.email"
    />
    <BaseInput
      id="password"
      v-model="form.password"
      type="password"
      label="كلمة السر"
      placeholder="••••••••"
      autocomplete="current-password"
      :error="fieldErrors.password"
    />

    <div
      v-if="authStore.error"
      class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-danger text-sm"
    >
      {{ authStore.error }}
    </div>

    <BaseButton type="submit" :loading="authStore.isLoading">
      تسجيل الدخول
    </BaseButton>

    <div class="relative my-2">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-200 dark:border-gray-700"></div>
      </div>
      <div class="relative flex justify-center text-xs">
        <span class="bg-white dark:bg-gray-800 px-2 text-gray-400">أو</span>
      </div>
    </div>

    <GoogleSignInButton />

    <p class="text-center text-sm text-gray-600 dark:text-gray-400">
      ليس لديك حساب؟
      <router-link
        to="/register"
        class="text-primary-600 dark:text-primary-400 font-medium hover:underline"
      >
        أنشئ حسابًا جديدًا
      </router-link>
    </p>
  </form>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/store/auth";
import BaseInput from "@/components/ui/BaseInput.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import GoogleSignInButton from "@/components/auth/GoogleSignInButton.vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = reactive({
  email: "",
  password: "",
});

const fieldErrors = ref({});

function validate() {
  fieldErrors.value = {};
  if (!form.email) fieldErrors.value.email = "البريد الإلكتروني مطلوب";
  if (!form.password) fieldErrors.value.password = "كلمة السر مطلوبة";
  return Object.keys(fieldErrors.value).length === 0;
}

async function handleSubmit() {
  if (!validate()) return;
  try {
    await authStore.login(form);
    const redirect = route.query.redirect || "/";
    router.push(redirect);
  } catch (err) {
    // الخطأ معروض بالفعل من authStore.error أعلاه
  }
}
</script>

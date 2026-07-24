<template>
  <form @submit.prevent="handleSubmit" class="space-y-5">
    <BaseInput
      id="name"
      v-model="form.name"
      type="text"
      label="الاسم الكامل"
      placeholder="أحمد محمد"
      autocomplete="name"
      :error="fieldErrors.name"
    />
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
      placeholder="8 أحرف على الأقل"
      autocomplete="new-password"
      :error="fieldErrors.password"
    />
    <BaseInput
      id="password_confirmation"
      v-model="form.passwordConfirmation"
      type="password"
      label="تأكيد كلمة السر"
      placeholder="أعد كتابة كلمة السر"
      autocomplete="new-password"
      :error="fieldErrors.passwordConfirmation"
    />

    <div
      v-if="authStore.error"
      class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-danger text-sm"
    >
      {{ authStore.error }}
    </div>

    <BaseButton type="submit" :loading="authStore.isLoading">
      إنشاء حساب
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
      لديك حساب بالفعل؟
      <router-link
        to="/login"
        class="text-primary-600 dark:text-primary-400 font-medium hover:underline"
      >
        سجّل الدخول
      </router-link>
    </p>
  </form>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import BaseInput from "@/components/ui/BaseInput.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import GoogleSignInButton from "@/components/auth/GoogleSignInButton.vue";

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  name: "",
  email: "",
  password: "",
  passwordConfirmation: "",
});

const fieldErrors = ref({});

function validate() {
  fieldErrors.value = {};

  if (!form.name || form.name.trim().length < 2) {
    fieldErrors.value.name = "الاسم يجب أن يكون حرفين على الأقل";
  }
  if (!form.email) {
    fieldErrors.value.email = "البريد الإلكتروني مطلوب";
  }
  if (!form.password || form.password.length < 8) {
    fieldErrors.value.password = "كلمة السر يجب أن تكون 8 أحرف على الأقل";
  }
  if (form.password !== form.passwordConfirmation) {
    fieldErrors.value.passwordConfirmation = "كلمتا السر غير متطابقتين";
  }

  return Object.keys(fieldErrors.value).length === 0;
}

async function handleSubmit() {
  if (!validate()) return;
  try {
    await authStore.register({
      name: form.name,
      email: form.email,
      password: form.password,
    });
    router.push("/");
  } catch (err) {
    // الخطأ معروض بالفعل من authStore.error أعلاه
  }
}
</script>

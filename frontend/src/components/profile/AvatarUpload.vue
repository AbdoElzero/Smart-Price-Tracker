<template>
  <div class="relative w-28 h-28 mx-auto sm:mx-0">
    <div
      class="w-28 h-28 rounded-full overflow-hidden bg-primary-100 dark:bg-primary-900 flex items-center justify-center border-4 border-white dark:border-gray-800 shadow-md"
    >
      <img v-if="avatarSrc" :src="avatarSrc" alt="الصورة الشخصية" class="w-full h-full object-cover" />
      <span v-else class="text-3xl font-bold text-primary-700 dark:text-primary-300">{{ initial }}</span>
    </div>

    <button
      type="button"
      @click="fileInput?.click()"
      :disabled="isUploading"
      class="absolute bottom-0 left-0 w-9 h-9 rounded-full bg-primary-600 text-white flex items-center justify-center shadow hover:bg-primary-700 transition-colors disabled:opacity-60"
      aria-label="تغيير الصورة"
    >
      <span v-if="isUploading">⏳</span>
      <span v-else>📷</span>
    </button>

    <input
      ref="fileInput"
      type="file"
      accept="image/png, image/jpeg, image/webp"
      class="hidden"
      @change="handleFileChange"
    />

    <p v-if="error" class="absolute top-full mt-2 right-0 left-0 text-xs text-danger text-center">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "@/store/auth";
import profileService from "@/services/profile.service";
import { resolveAvatarUrl } from "@/utils/avatar";

const authStore = useAuthStore();
const fileInput = ref(null);
const isUploading = ref(false);
const error = ref("");

const avatarSrc = computed(() => resolveAvatarUrl(authStore.user?.avatar_url));

const initial = computed(() => {
  const name = authStore.user?.name || "";
  return name.trim().charAt(0).toUpperCase() || "؟";
});

async function handleFileChange(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  error.value = "";

  if (file.size > 5 * 1024 * 1024) {
    error.value = "حجم الصورة يجب أن يكون أقل من 5 ميجابايت";
    event.target.value = "";
    return;
  }

  const formData = new FormData();
  formData.append("avatar", file);

  isUploading.value = true;
  try {
    await profileService.uploadAvatar(formData);
    await authStore.fetchCurrentUser();
  } catch (err) {
    error.value = err.response?.data?.error || "تعذّر رفع الصورة، حاول مرة أخرى";
  } finally {
    isUploading.value = false;
    event.target.value = "";
  }
}
</script>

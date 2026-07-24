<template>
  <div>
    <div id="google-signin-button" class="flex justify-center"></div>
    <p v-if="!clientId" class="text-xs text-center text-gray-400 mt-2">
      (تسجيل الدخول عبر Google غير مُفعَّل حاليًا - يحتاج إضافة GOOGLE_CLIENT_ID)
    </p>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

const router = useRouter();
const authStore = useAuthStore();
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

function loadGoogleScript() {
  return new Promise((resolve, reject) => {
    if (window.google?.accounts?.id) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

async function handleCredentialResponse(response) {
  try {
    await authStore.loginWithGoogle(response.credential);
    router.push("/");
  } catch (err) {
    // الخطأ معروض بالفعل من authStore.error في الفورم الأب
  }
}

onMounted(async () => {
  if (!clientId) return;
  try {
    await loadGoogleScript();
    window.google.accounts.id.initialize({
      client_id: clientId,
      callback: handleCredentialResponse,
    });
    window.google.accounts.id.renderButton(
      document.getElementById("google-signin-button"),
      { theme: "outline", size: "large", width: 320, locale: "ar" }
    );
  } catch (err) {
    console.error("فشل تحميل مكتبة Google Sign-In", err);
  }
});
</script>

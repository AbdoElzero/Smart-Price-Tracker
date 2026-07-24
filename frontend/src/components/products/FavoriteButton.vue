<template>
  <button
    type="button"
    @click.stop.prevent="handleClick"
    class="w-9 h-9 flex items-center justify-center rounded-full bg-white/90 dark:bg-gray-900/80 shadow hover:scale-105 transition-transform"
    :aria-label="isFav ? 'إزالة من المفضلة' : 'إضافة للمفضلة'"
  >
    <span>{{ isFav ? "❤️" : "🤍" }}</span>
  </button>
</template>

<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { useFavoritesStore } from "@/store/favorites";

const props = defineProps({
  productId: { type: Number, required: true },
});

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const favoritesStore = useFavoritesStore();

const isFav = computed(() => favoritesStore.isFavorited(props.productId));

async function handleClick() {
  if (!authStore.isAuthenticated) {
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }
  try {
    await favoritesStore.toggle(props.productId);
  } catch (err) {
    // يمكن إضافة Toast لعرض رسالة خطأ لاحقًا
  }
}
</script>

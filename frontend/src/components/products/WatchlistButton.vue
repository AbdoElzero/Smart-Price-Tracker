<template>
  <div ref="containerRef" class="relative inline-block">
    <button
      ref="buttonRef"
      type="button"
      @click.stop.prevent="handleToggleOpen"
      class="w-9 h-9 flex items-center justify-center rounded-full bg-white/90 dark:bg-gray-900/80 shadow hover:scale-105 transition-transform"
      :aria-label="isWatched ? 'تعديل قائمة المتابعة' : 'إضافة لقائمة المتابعة'"
    >
      <span>{{ isWatched ? "🔔" : "🔕" }}</span>
    </button>

    <!-- ننقل النافذة المنبثقة لمستوى الصفحة (body) حتى لا تُقص بسبب overflow-hidden في بطاقة المنتج -->
    <Teleport to="body">
      <div
        v-if="isOpen"
        ref="popoverRef"
        :style="popoverStyle"
        class="fixed z-50 w-64 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 text-sm"
      >
        <p class="font-medium text-gray-900 dark:text-white mb-2">تنبيه عند نزول السعر</p>
        <label class="block mb-1.5 text-xs text-gray-500 dark:text-gray-400">
          السعر المستهدف (اختياري)
        </label>
        <input
          v-model="targetPrice"
          type="number"
          min="0"
          step="0.01"
          placeholder="مثال: 1500"
          class="w-full px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 mb-3 focus:outline-none focus:ring-2 focus:ring-primary-500/30"
        />

        <div class="flex gap-2">
          <button
            type="button"
            @click="handleSave"
            :disabled="isSaving"
            class="flex-1 px-3 py-2 rounded-lg bg-primary-600 text-white text-xs font-medium hover:bg-primary-700 disabled:opacity-60"
          >
            {{ isWatched ? "تحديث" : "إضافة للمتابعة" }}
          </button>
          <button
            v-if="isWatched"
            type="button"
            @click="handleRemove"
            :disabled="isSaving"
            class="px-3 py-2 rounded-lg border border-danger text-danger text-xs font-medium hover:bg-red-50 dark:hover:bg-red-900/20"
          >
            إزالة
          </button>
        </div>

        <p v-if="error" class="text-xs text-danger mt-2">{{ error }}</p>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import { onClickOutside } from "@vueuse/core";
import { useAuthStore } from "@/store/auth";
import { useWatchlistStore } from "@/store/watchlist";

const props = defineProps({
  productId: { type: Number, required: true },
});

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const watchlistStore = useWatchlistStore();

const containerRef = ref(null);
const buttonRef = ref(null);
const popoverRef = ref(null);
const isOpen = ref(false);
const isSaving = ref(false);
const error = ref("");
const targetPrice = ref("");
const popoverStyle = ref({});

// نتجاهل الضغط داخل النافذة المنبثقة نفسها (لأنها مُنقولة لـ body وليست ابنًا مباشرًا للحاوية)
onClickOutside(
  containerRef,
  () => {
    isOpen.value = false;
  },
  { ignore: [popoverRef] }
);

const isWatched = computed(() => watchlistStore.isWatched(props.productId));

function updatePopoverPosition() {
  if (!buttonRef.value) return;
  const rect = buttonRef.value.getBoundingClientRect();
  const popoverWidth = 256; // يطابق w-64
  let left = rect.right - popoverWidth;
  left = Math.max(8, Math.min(left, window.innerWidth - popoverWidth - 8));

  popoverStyle.value = {
    top: `${rect.bottom + 8}px`,
    left: `${left}px`,
  };
}

function handleReposition() {
  if (isOpen.value) updatePopoverPosition();
}

window.addEventListener("scroll", handleReposition, true);
window.addEventListener("resize", handleReposition);

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleReposition, true);
  window.removeEventListener("resize", handleReposition);
});

async function handleToggleOpen() {
  if (!authStore.isAuthenticated) {
    router.push({ name: "login", query: { redirect: route.fullPath } });
    return;
  }
  if (!isOpen.value) {
    const existing = watchlistStore.getEntry(props.productId);
    targetPrice.value = existing?.target_price ?? "";
  }
  isOpen.value = !isOpen.value;
  error.value = "";

  if (isOpen.value) {
    await nextTick();
    updatePopoverPosition();
  }
}

async function handleSave() {
  isSaving.value = true;
  error.value = "";
  try {
    await watchlistStore.upsert(props.productId, {
      target_price: targetPrice.value ? Number(targetPrice.value) : null,
    });
    isOpen.value = false;
  } catch (err) {
    error.value = err.response?.data?.error || "تعذّر الحفظ، حاول مرة أخرى";
  } finally {
    isSaving.value = false;
  }
}

async function handleRemove() {
  isSaving.value = true;
  error.value = "";
  try {
    await watchlistStore.remove(props.productId);
    isOpen.value = false;
  } catch (err) {
    error.value = err.response?.data?.error || "تعذّر الإزالة، حاول مرة أخرى";
  } finally {
    isSaving.value = false;
  }
}
</script>

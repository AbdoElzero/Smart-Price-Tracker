<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">الإشعارات</h1>
      <button
        v-if="notifications.length"
        type="button"
        @click="handleMarkAllRead"
        class="text-sm text-primary-600 dark:text-primary-400 hover:underline"
      >
        تعليم الكل كمقروء
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">جارٍ التحميل...</div>

    <div v-else-if="notifications.length === 0" class="text-center py-20">
      <div class="text-4xl mb-3">🔔</div>
      <p class="text-gray-500 dark:text-gray-400">لا توجد إشعارات حاليًا.</p>
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="notif in notifications"
        :key="notif.id"
        class="flex items-start gap-3 p-4 rounded-xl border transition-colors"
        :class="
          notif.is_read
            ? 'bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700'
            : 'bg-primary-50/60 dark:bg-primary-900/20 border-primary-100 dark:border-primary-800'
        "
      >
        <span class="text-xl shrink-0">{{ iconFor(notif.type) }}</span>

        <div class="flex-1 min-w-0">
          <p class="font-medium text-gray-900 dark:text-white text-sm">{{ notif.title }}</p>
          <p class="text-sm text-gray-600 dark:text-gray-300 mt-0.5">{{ notif.message }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ formatDate(notif.created_at) }}</p>
        </div>

        <div class="flex flex-col items-end gap-2 shrink-0">
          <button
            v-if="!notif.is_read"
            type="button"
            @click="handleMarkRead(notif)"
            class="text-xs text-primary-600 dark:text-primary-400 hover:underline whitespace-nowrap"
          >
            تعليم كمقروء
          </button>
          <button
            type="button"
            @click="handleDelete(notif.id)"
            class="text-xs text-danger hover:underline"
          >
            حذف
          </button>
        </div>
      </div>
    </div>

    <Pagination :page="page" :total-pages="meta.total_pages" @change="(p) => (page = p)" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import notificationService from "@/services/notification.service";
import { useNotificationsStore } from "@/store/notifications";
import Pagination from "@/components/ui/Pagination.vue";

const notificationsStore = useNotificationsStore();

const notifications = ref([]);
const meta = ref({ total_pages: 0 });
const isLoading = ref(false);
const page = ref(1);

const typeIcons = {
  price_drop: "📉",
  target_reached: "🎯",
  back_in_stock: "✅",
  system: "👋",
};

function iconFor(type) {
  return typeIcons[type] || "🔔";
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleString("ar-EG", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

async function loadNotifications() {
  isLoading.value = true;
  try {
    const { data } = await notificationService.list({ page: page.value, per_page: 20 });
    notifications.value = data.data;
    meta.value = data.meta;
    notificationsStore.unreadCount = data.meta.unread_count;
  } catch (err) {
    notifications.value = [];
  } finally {
    isLoading.value = false;
  }
}

async function handleMarkRead(notif) {
  try {
    await notificationService.markAsRead(notif.id);
    notif.is_read = true;
    notificationsStore.decrementUnread(1);
  } catch (err) {
    // تجاهل بسيط
  }
}

async function handleMarkAllRead() {
  try {
    await notificationService.markAllAsRead();
    notifications.value.forEach((n) => (n.is_read = true));
    notificationsStore.resetUnread();
  } catch (err) {
    // تجاهل بسيط
  }
}

async function handleDelete(id) {
  try {
    const notif = notifications.value.find((n) => n.id === id);
    await notificationService.remove(id);
    notifications.value = notifications.value.filter((n) => n.id !== id);
    if (notif && !notif.is_read) {
      notificationsStore.decrementUnread(1);
    }
  } catch (err) {
    // تجاهل بسيط
  }
}

watch(page, loadNotifications);
onMounted(loadNotifications);
</script>

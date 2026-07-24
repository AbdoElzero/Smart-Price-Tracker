import { defineStore } from "pinia";
import notificationService from "@/services/notification.service";

export const useNotificationsStore = defineStore("notifications", {
  state: () => ({
    unreadCount: 0,
  }),

  actions: {
    async fetchUnreadCount() {
      try {
        const { data } = await notificationService.unreadCount();
        this.unreadCount = data.unread_count;
      } catch (err) {
        this.unreadCount = 0;
      }
    },

    decrementUnread(amount = 1) {
      this.unreadCount = Math.max(0, this.unreadCount - amount);
    },

    resetUnread() {
      this.unreadCount = 0;
    },

    reset() {
      this.unreadCount = 0;
    },
  },
});

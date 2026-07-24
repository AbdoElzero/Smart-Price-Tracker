import api from "./api";

export default {
  list(params) {
    return api.get("/notifications", { params });
  },
  unreadCount() {
    return api.get("/notifications/unread-count");
  },
  markAsRead(id) {
    return api.put(`/notifications/${id}/read`);
  },
  markAllAsRead() {
    return api.put("/notifications/read-all");
  },
  remove(id) {
    return api.delete(`/notifications/${id}`);
  },
};

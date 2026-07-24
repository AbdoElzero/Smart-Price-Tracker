import api from "./api";

export default {
  // إحصائيات
  getStats() {
    return api.get("/admin/stats");
  },

  // منتجات
  listProducts(params) {
    return api.get("/admin/products", { params });
  },
  getProduct(id) {
    return api.get(`/admin/products/${id}`);
  },
  createProduct(payload) {
    return api.post("/admin/products", payload);
  },
  updateProduct(id, payload) {
    return api.put(`/admin/products/${id}`, payload);
  },
  deleteProduct(id) {
    return api.delete(`/admin/products/${id}`);
  },

  // مستخدمين
  listUsers(params) {
    return api.get("/admin/users", { params });
  },
  updateUser(id, payload) {
    return api.put(`/admin/users/${id}`, payload);
  },

  // مهام Celery
  runPredictionsTask() {
    return api.post("/admin/tasks/run-predictions");
  },
  runNotificationsTask() {
    return api.post("/admin/tasks/run-notifications");
  },
};

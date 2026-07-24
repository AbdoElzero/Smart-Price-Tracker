import api from "./api";

export default {
  list(params) {
    return api.get("/products", { params });
  },
  getBySlug(slug) {
    return api.get(`/products/${slug}`);
  },
};

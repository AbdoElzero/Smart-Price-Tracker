import api from "./api";

export default {
  get(productId) {
    return api.get(`/products/${productId}/prediction`);
  },
};

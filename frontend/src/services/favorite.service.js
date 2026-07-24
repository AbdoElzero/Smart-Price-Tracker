import api from "./api";

export default {
  list() {
    return api.get("/favorites");
  },
  listIds() {
    return api.get("/favorites/ids");
  },
  toggle(productId) {
    return api.post(`/favorites/${productId}/toggle`);
  },
};

import api from "./api";

export default {
  list() {
    return api.get("/watchlist");
  },
  upsert(productId, payload) {
    return api.post(`/watchlist/${productId}`, payload);
  },
  remove(productId) {
    return api.delete(`/watchlist/${productId}`);
  },
};

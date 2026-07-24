import api from "./api";

export default {
  compare(ids) {
    return api.get("/products/compare", { params: { ids: ids.join(",") } });
  },
};

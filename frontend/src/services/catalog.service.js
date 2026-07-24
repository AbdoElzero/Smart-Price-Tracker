import api from "./api";

export default {
  listCategories() {
    return api.get("/categories");
  },
  listBrands() {
    return api.get("/brands");
  },
  listCountries() {
    return api.get("/countries");
  },
};

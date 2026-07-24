import api from "./api";

export default {
  updateProfile(payload) {
    return api.put("/profile", payload);
  },
  changePassword(payload) {
    return api.put("/profile/password", payload);
  },
  uploadAvatar(formData) {
    return api.post("/profile/avatar", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

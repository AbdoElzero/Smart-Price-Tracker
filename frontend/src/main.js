import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./assets/styles/main.css";
import { useThemeStore } from "@/store/theme";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// تفعيل الوضع الليلي المحفوظ مسبقًا (إن وجد) قبل عرض الواجهة
const themeStore = useThemeStore();
themeStore.init();

app.mount("#app");

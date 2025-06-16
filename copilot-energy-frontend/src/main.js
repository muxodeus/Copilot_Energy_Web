import VueApexCharts from "vue3-apexcharts";
import { createApp } from "vue";
import App from "./App.vue";

const app = createApp(App);
app.component("VueApexChart", VueApexCharts);
app.mount("#app");

createApp(App).mount('#app')

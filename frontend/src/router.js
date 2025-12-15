import { createRouter, createWebHistory } from "vue-router";
import Home from "./pages/Home.vue";
import Stock from "./pages/Stock.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/stock/:ticker", component: Stock }, // dynamic route
  ],
});
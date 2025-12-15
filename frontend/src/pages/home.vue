<template>
  <div>
    <h1>Stock Lite</h1>
    <input v-model="ticker" placeholder="Enter ticker"/><br><br>
    <button @click="go">View Stock</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const ticker = ref("");

function go() {
  if (ticker.value) router.push(`/stock/${ticker.value}`);
}
</script>
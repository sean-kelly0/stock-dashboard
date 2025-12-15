<template>
  <div class="stock-layout" v-if="data">

    <!-- LEFT = Stock Name + Sparkline -->
    <div class="main-chart-area">
      <h1 class="stock-title">{{ data.name }} ({{ symbol }})</h1>

      <!-- 🟢 Sparkline container - correct, single layer -->
      <div class="chart-container">
        <div id="chart" ref="chart" class="chart-container"></div>      
      </div>
    </div>

    <!-- RIGHT = Live Stats -->
    <div class="side-info-panel">
      <h3>Market Data</h3>
      <ul class="stat-list">
        <li><strong>Price:</strong> <p :style="{color: data.price >= data.previous_close ? 'green' : 'red'}">${{ data.price.toFixed(2) }}</p></li>
        <li><strong>Open:</strong> ${{ data.open?.toFixed(2) }}</li>
        <li><strong>Prev Close:</strong> ${{ data.previous_close?.toFixed(2) }}</li>
        <li><strong>Day Range:</strong> ${{ data.day_low }} → ${{ data.day_high }}</li>
        <li><strong>52W Range:</strong> ${{ data.year_low }} → ${{ data.year_high }}</li>
        <li><strong>Volume:</strong> {{ data.volume?.toLocaleString() }}</li>
        <li><strong>50-Day Avg:</strong> ${{ data.fifty_day_avg?.toFixed(2) }}</li>
        <li><strong>200-Day Avg:</strong> ${{ data.two_hundred_day_avg?.toFixed(2) }}</li>
        <li><strong>Market Cap:</strong> {{ formattedMarketCap }}</li>
      </ul>
    </div>

  </div>

  <div v-else style="padding:30px;">Loading Stock Data...</div>
</template>


<script setup>
/* === Imports === */
import { ref, onMounted, onUnmounted, computed, watch } from "vue"
import { useRoute } from "vue-router"
import Plotly from "plotly.js-dist-min"

/* === Routing + symbol === */
const route = useRoute()
const symbol = route.params.ticker.toUpperCase()

/* === API Data === */
const data = ref(null)
const error = ref(null)

/* === Live Fetch Every 5 Seconds === */
let interval = null

const fetchData = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/stocks/${symbol}`)
    data.value = await res.json()
  } catch (e) {
    error.value = e.toString()
  }
}

onMounted(() => {
  fetchData()                           // first pull
  interval = setInterval(fetchData, 5000) // refresh 5s
})

onUnmounted(() => clearInterval(interval))

/* ===========================================================
   🔥 LIVE 2-MIN CANDLE ENGINE (NO HISTORY REQUIRED)
   Every fetch updates ONLY the active candle.
   Every 120s → new candle started.
=========================================================== */
const candles = ref([])
const candleStart = ref(Date.now())

watch(data, (newData) => {
  if (!newData?.price) return

  const price = newData.price
  const now = Date.now()

  // If first candle doesn't exist → initialize
  if (candles.value.length === 0) {
    candles.value.push({ open: price, high: price, low: price, close: price })
    return drawCandles()
  }

  const current = candles.value[candles.value.length - 1]

  // 2 minutes passed → freeze candle and open new one
  if (now - candleStart.value >= 30000) {
    candles.value.push({ open: price, high: price, low: price, close: price })
    candleStart.value = now
  } 
  // Update current candle live
  else {
    current.close = price
    current.high = Math.max(current.high, price)
    current.low = Math.min(current.low, price)
  }

  drawCandles()
})

/* ===========================================================
   📊 Plotly Candlestick Chart Renderer
=========================================================== */
const chart = ref(null)

const drawCandles = () => {
  if (!chart.value || candles.value.length === 0) return

  const opens = candles.value.map(c => c.open)
  const highs = candles.value.map(c => c.high)
  const lows  = candles.value.map(c => c.low)
  const closes = candles.value.map(c => c.close)
  const x = candles.value.map((_, i) => i) // candle index

  Plotly.newPlot(chart.value, [{
    x, open: opens, high: highs, low: lows, close: closes,
    type: "candlestick",
    increasing: { line: { color: "green" }},
    decreasing: { line: { color: "red" }},
  }], {
    margin: { t: 20, l: 30, r: 10, b: 20 },
    xaxis: { rangeslider: { visible: false }},
  })
}

/* === Market Cap Formatting (UI) === */
const formattedMarketCap = computed(() => {
  if (!data.value?.market_cap) return "N/A"
  const m = data.value.market_cap
  return m >= 1e12 ? (m/1e12).toFixed(2)+"T"
       : m >= 1e9  ? (m/1e9).toFixed(2)+"B"
       : m >= 1e6  ? (m/1e6).toFixed(2)+"M"
                   : m.toLocaleString()
})
</script>


<style scoped>
/* FULL WIDTH WHITE UI */

.stock-layout {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 30px 60px;
  background: white;
}

/* Left chart section */
.main-chart-area {
  flex: 3;
}

/* Title */
.stock-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: black;
}

/* Sparkline Container */
.chart-container {
  width: 100%;
  height: 550px;
  background: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sparkline {
  width: 100%;
  height: 100%;
  display: block;
}

/* Right stats */
.side-info-panel {
  flex: 1.1;
  padding: 25px;
  border-left: 1px solid #e0e0e0;
}

.stat-list { list-style:none; padding:0; margin-top:10px; }
.stat-list li { font-size:1.05rem; margin-bottom:12px; color:#333; }
#chart {
  width: 100%;
  height: 550px;
}
</style>
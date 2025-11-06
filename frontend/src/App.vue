<template>
  <main class="container">
    <h1>Stock Analysis Dashboard</h1>
    <div id="forms">
      <form action="GET">
        <label for="ticker">Enter Stock Ticker Symbol:</label>
        <input type="text" id="ticker" name="ticker" required />
        <button type="submit">Get Stock Data</button>
      </form>
    </div>
  </main>
</template>
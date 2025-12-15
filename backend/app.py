from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route("/stocks/<ticker>")
def api_stocks(ticker):
    stock = yf.Ticker(ticker)
    fast = stock.fast_info

    try:
        info = stock.info             # ← name, sector, industry, full details
    except:
        info = {}                     # fallback if API rate limited

    fast = stock.fast_info            # ← live pricing metrics

    return jsonify({
        "ticker": ticker.upper(),
        "name": info.get("longName") or info.get("shortName") or "Name Not Available",
        "price": round(fast.get("lastPrice"), 2),
        "open": round(fast.get("open"), 2),
        "previous_close": round(fast.get("previousClose"), 2),
        "day_high": round(fast.get("dayHigh"), 2),
        "day_low": round(fast.get("dayLow"), 2),
        "fifty_day_avg": round(fast.get("fiftyDayAverage"), 2),
        "two_hundred_day_avg": round(fast.get("twoHundredDayAverage"), 2),
        "year_high": round(fast.get("yearHigh"), 2),
        "year_low": round(fast.get("yearLow"), 2),
        "volume": fast.get("lastVolume"),
        "market_cap": fast.get("marketCap")
    })

if __name__ == "__main__":
    app.run(debug=True)
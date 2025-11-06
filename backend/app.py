from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow Vue dev server to talk to Flask
CORS(app)

@app.route("/api/records")
def api_records():
    # Dumb hard-coded JSON just to prove the link works
    return jsonify([
        {"id": 1, "field1": "Hello from Flask", "field2": "It works"},
        {"id": 2, "field1": "Second record", "field2": "Also works"},
    ])

@app.route("/api/stocks/<ticker>")
def api_stocks(ticker):
    # Dummy stock data for demonstration purposes
    stock_data = {
        "AAPL": {"price": 150.00, "change": "+1.5%"},
        "GOOGL": {"price": 2800.00, "change": "-0.5%"},
        "MSFT": {"price": 300.00, "change": "+0.8%"},
    }
    data = stock_data.get(ticker.upper(), {"error": "Ticker not found"})
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
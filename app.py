from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Get secrets from Render environment
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DEFAULT_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # Optional for now

# Send Telegram message
def send_message(text, chat_id=None):
    if not chat_id:
        chat_id = DEFAULT_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=payload)
    return response.json()

# Home route (Render health check)
@app.route('/')
def home():
    return "✅ Big Tony Sniper Bot is running."

# Alert webhook (from TradingView or custom system)
@app.route('/alert', methods=['POST'])
def alert():
    data = request.json

    pair = data.get("pair", "Unknown Pair")
    signal = data.get("signal", "No Signal")
    tf = data.get("timeframe", "Unknown TF")
    extra = data.get("note", "")

    message = f"""📡 SMC Alert Detected:
Pair: {pair}
Signal: {signal}
Timeframe: {tf}
{extra}"""

    send_message(message)
    return "✅ Alert received and sent."

if __name__ == '__main__':
    app.run(debug=True)

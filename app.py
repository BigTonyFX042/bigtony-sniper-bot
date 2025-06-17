
from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")  # Optional static chat ID for testing

def send_telegram_message(message, chat_id=None):
    chat_id = chat_id or CHAT_ID
    if not chat_id:
        return "Chat ID missing"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    return requests.post(url, json=payload).text

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    pair = data.get("pair", "Unknown")
    signal = data.get("signal", "No signal info")
    tf = data.get("timeframe", "Unknown")
    msg = f"📡 Signal Detected:
Pair: {pair}
Signal: {signal}
Timeframe: {tf}"
    return send_telegram_message(msg)

@app.route("/daily_summary", methods=["GET"])
def daily_summary():
    message = (
        "🧠 *Daily Sniper Summary*
"
        "📊 Bias: [Auto-generated bias]
"
        "💥 Watchlist: BTCUSD, GBPJPY, XAUUSD
"
        "📵 News Risk: Medium
"
        "🎯 Discipline: Max 3 trades today. +5% Target.
"
        "🙏 Stay focused. Let God guide every setup."
    )
    return send_telegram_message(message)

@app.route("/")
def index():
    return "Big Tony FX Sniper Bot is live."

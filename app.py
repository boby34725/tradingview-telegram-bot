from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })


def format_message(data):
    signal = data.get("signal", "")
    symbol = data.get("symbol", "")
    entry = data.get("entry", "")
    sl = data.get("sl", "")
    tp1 = data.get("tp1", "")
    tp2 = data.get("tp2", "")
    tp3 = data.get("tp3", "")
    time = data.get("time", "")

    if signal in ["BUY", "BUY EARLY"]:
        icon = "🟢"
        direction = "ACHAT"
    elif signal in ["SELL", "SELL EARLY"]:
        icon = "🔴"
        direction = "VENTE"
    else:
        icon = "🧪"
        direction = "TEST"

    message = (
        f"{icon} {direction}\n\n"
        f"📈 Symbole : {symbol}\n"
        f"📍 Entry : {entry}\n"
        f"🛑 SL : {sl}\n\n"
        f"🎯 TP1 : {tp1}\n"
        f"🎯 TP2 : {tp2}\n"
        f"🎯 TP3 : {tp3}\n\n"
        f"🕒 Heure : {time}\n"
        f"⚠️ Signal : {signal}"
    )

    return message


@app.route("/", methods=["GET"])
def home():
    return "Bot OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return {"status": "error", "message": "No JSON received"}, 400

    message = format_message(data)
    send_telegram_message(message)

    return {"status": "sent"}


@app.route("/test", methods=["GET"])
def test():
    data = {
        "signal": "BUY",
        "symbol": "XAUUSD",
        "entry": "3350.50",
        "sl": "3348.20",
        "tp1": "3352.80",
        "tp2": "3355.10",
        "tp3": "3357.40",
        "time": "TEST"
    }

    message = format_message(data)
    send_telegram_message(message)

    return {"status": "test sent"}


@app.route("/test-buy", methods=["GET"])
def test_buy():
    data = {
        "signal": "BUY",
        "symbol": "BTCUSD",
        "entry": "60000",
        "sl": "59920",
        "tp1": "60080",
        "tp2": "60160",
        "tp3": "60240",
        "time": "TEST BUY"
    }

    message = format_message(data)
    send_telegram_message(message)

    return {"status": "test buy sent"}


@app.route("/test-sell", methods=["GET"])
def test_sell():
    data = {
        "signal": "SELL",
        "symbol": "BTCUSD",
        "entry": "60000",
        "sl": "60100",
        "tp1": "59900",
        "tp2": "59800",
        "tp3": "59700",
        "time": "TEST SELL"
    }

    message = format_message(data)
    send_telegram_message(message)

    return {"status": "test sell sent"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

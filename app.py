from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

@app.route("/", methods=["GET"])
def home():
    return "Bot OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    signal = data.get("signal", "")
    symbol = data.get("symbol", "")
    price = data.get("price", "")

    if signal == "BUY":
        message = (
            f"🟢 ACHAT \n\n"
            f"📈 Symbole : {symbol}\n"
            f"💰 Prix : {price}\n"
            f"🚀 Signal BUY détecté"
        )
    else:
        message = (
            f"🔴 VENTE \n\n"
            f"📈 Symbole : {symbol}\n"
            f"💰 Prix : {price}\n"
            f"⚠️ Signal SELL détecté"
        )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return {"status": "sent"}

@app.route("/test-sell", methods=["GET"])
def test_sell():
    data = {
        "signal": "SELL",
        "symbol": "XAUUSD",
        "price": "4485.17",
        "time": "TEST"
    }

    signal = data.get("signal", "")
    symbol = data.get("symbol", "")
    price = data.get("price", "")
    time = data.get("time", "")

    message = (
        f"🔴 VENTE OR\n\n"
        f"📈 Symbole : {symbol}\n"
        f"💰 Prix : {price}\n"
        f"🕒 Heure : {time}\n\n"
        f"⚠️ Signal SELL détecté"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return {"status": "test sell sent"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

@app.route("/test")
def test():

    message = """
🧪 TEST SIGNAL

🟢 BUY XAUUSD

📍 Entry : 3350.50
🛑 SL : 3348.20

🎯 TP1 : 3352.80
🎯 TP2 : 3355.10
🎯 TP3 : 3357.40
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    return "Signal envoyé !"

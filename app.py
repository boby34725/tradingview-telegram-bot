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
    time = data.get("time", "")

    if signal == "BUY":
        message = (
            f"🟢 ACHAT OR\n\n"
            f"📈 Symbole : {symbol}\n"
            f"💰 Prix : {price}\n"
            f"🕒 Heure : {time}\n\n"
            f"🚀 Signal BUY détecté"
        )
    else:
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

    return {"status": "sent"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

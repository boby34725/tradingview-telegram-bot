from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def price(v):
    if v == "" or v is None:
        return "-"
    try:
        return f"{float(v):,.2f}".replace(",", " ")
    except:
        return str(v)


@app.route("/")
def home():
    return "Bot OK"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    signal = data.get("signal", "")
    event = data.get("event", "")

    symbol = data.get("symbol", "")
    timeframe = data.get("timeframe", "")
    time = data.get("time", "")

    entry = price(data.get("entry"))
    sl = price(data.get("sl"))
    tp1 = price(data.get("tp1"))
    tp2 = price(data.get("tp2"))
    tp3 = price(data.get("tp3"))
    level = price(data.get("level"))

    # ========================================
    # SIGNAL INITIAL
    # ========================================

    if signal == "BUY":

        message = f"""🟢 MT5 SIGNALS

🟢 ACHAT

📊 {symbol} {timeframe}

📍 Entrée : {entry}
🛑 SL : {sl}

🎯 TP1 : {tp1}
🎯 TP2 : {tp2}
🎯 TP3 : {tp3}

🕒 {time}
"""

    elif signal == "SELL":

        message = f"""🔴 MT5 SIGNALS

🔴 VENTE

📊 {symbol} {timeframe}

📍 Entrée : {entry}
🛑 SL : {sl}

🎯 TP1 : {tp1}
🎯 TP2 : {tp2}
🎯 TP3 : {tp3}

🕒 {time}
"""

    elif signal == "BUY EARLY":

        message = f"""🟢 BUY EARLY

📊 {symbol}

🕒 {time}
"""

    elif signal == "SELL EARLY":

        message = f"""🔴 SELL EARLY

📊 {symbol}

🕒 {time}
"""

    # ========================================
    # TP / SL / BE
    # ========================================

    elif event == "TP1":

        message = f"""🎯 TP1 ATTEINT

📊 {symbol}

Prix : {level}

➡️ Déplacer le Stop au Break Even.
"""

    elif event == "TP2":

        message = f"""🎯 TP2 ATTEINT

📊 {symbol}

Prix : {level}

Trade sécurisé.
"""

    elif event == "TP3":

        message = f"""🏆 TP3 ATTEINT

📊 {symbol}

Prix : {level}

Trade terminé.
"""

    elif event == "SL":

        message = f"""🛑 STOP LOSS

📊 {symbol}

Prix : {level}
"""

    elif event == "BE":

        message = f"""⚪ BREAK EVEN

📊 {symbol}

Trade clôturé à 0.
"""

    else:

        message = str(data)

    send(message)

    return {"status": "ok"}


# ========================================
# TEST
# ========================================

@app.route("/test")
def test():

    data = {
        "signal":"BUY",
        "symbol":"BTCUSD",
        "timeframe":"M5",
        "entry":"60000",
        "sl":"59920",
        "tp1":"60080",
        "tp2":"60160",
        "tp3":"60240",
        "time":"26/06/2026 18:15"
    }

    requests.post(
        "http://127.0.0.1:10000/webhook",
        json=data
    )

    return "Test envoyé"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

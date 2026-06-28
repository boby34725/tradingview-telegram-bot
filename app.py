from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})


def price(v):
    if v == "" or v is None:
        return "-"
    try:
        return f"{float(v):.2f}"
    except:
        return str(v).replace(" ", "")


@app.route("/")
def home():
    return "Bot OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

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
    # TP / SL / BE EN PREMIER
    # ========================================

    if event == "TP1":
        message = f"""🎯 TP1 ATTEINT

📊 {symbol} {timeframe}

Prix : {level}

➡️ Déplacer le Stop au Break Even.

🕒 {time}
"""

    elif event == "TP2":
        message = f"""🎯 TP2 ATTEINT

📊 {symbol} {timeframe}

Prix : {level}

Trade sécurisé.

🕒 {time}
"""

    elif event == "TP3":
        message = f"""🏆 TP3 ATTEINT

📊 {symbol} {timeframe}

Prix : {level}

Trade terminé.

🕒 {time}
"""

    elif event == "SL":
        message = f"""🛑 STOP LOSS

📊 {symbol} {timeframe}

Prix : {level}

🕒 {time}
"""

    elif event == "BE":
        message = f"""⚪ BREAK EVEN

📊 {symbol} {timeframe}

Prix : {level}

Trade clôturé à 0.

🕒 {time}
"""

    # ========================================
    # SIGNAL INITIAL
    # ========================================

    elif signal == "BUY":

        if sl == "-" or tp1 == "-":
            return {"status": "ignored", "reason": "BUY incomplete"}

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

        if sl == "-" or tp1 == "-":
            return {"status": "ignored", "reason": "SELL incomplete"}

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

📊 {symbol} {timeframe}

📍 Entrée : {entry}

🕒 {time}
"""

    elif signal == "SELL EARLY":
        message = f"""🔴 SELL EARLY

📊 {symbol} {timeframe}

📍 Entrée : {entry}

🕒 {time}
"""

    else:
        message = str(data)

    send(message)
    return {"status": "ok"}


@app.route("/test")
def test():
    data = {
        "signal": "BUY",
        "symbol": "BTCUSD",
        "timeframe": "M5",
        "entry": "60000",
        "sl": "59920",
        "tp1": "60080",
        "tp2": "60160",
        "tp3": "60240",
        "time": "TEST"
    }

    message = f"""🟢 MT5 SIGNALS

🟢 ACHAT

📊 {data["symbol"]} {data["timeframe"]}

📍 Entrée : {price(data["entry"])}
🛑 SL : {price(data["sl"])}

🎯 TP1 : {price(data["tp1"])}
🎯 TP2 : {price(data["tp2"])}
🎯 TP3 : {price(data["tp3"])}

🕒 {data["time"]}
"""
    send(message)
    return "Test BUY envoyé"


@app.route("/test-tp1")
def test_tp1():
    message = """🎯 TP1 ATTEINT

📊 BTCUSD M5

Prix : 60080.00

➡️ Déplacer le Stop au Break Even.

🕒 TEST
"""
    send(message)
    return "Test TP1 envoyé"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

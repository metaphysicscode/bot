from flask import Flask, request
import os
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data and "data" in data and "cast" in data["data"]:
        cast = data["data"]["cast"]
        author = cast.get("author", {}).get("username", "unknown")
        text = cast.get("text", "")
        url = cast.get("url", "")
        message = f"*New Cast from {author}*\n{text}\n{url}"
        send_telegram_message(message)
    return {"status": "ok"}

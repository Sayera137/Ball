import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7226274181:AAEbzTRtg_GciVh_wd1042QFMiu9YR-FaJ0"
OPENROUTER_API_KEY = "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"
WEBHOOK_URL = "https://your-app-name.onrender.com"  # Render এ তোমার URL অনুযায়ী এটি বদলাও

CHARACTER_NAME = "সায়েরা"

def generate_reply(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": f"তুমি একজন রোমান্টিক বাংলা মেয়ে, নাম {CHARACTER_NAME}, তুমি প্রেমিককে ভালোবাসা দাও।"},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "দুঃখিত, আমি এখন একটু ব্যস্ত আছি। পরে কথা বলো।"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_input = data["message"]["text"]
        reply = generate_reply(user_input)
        send_message(chat_id, reply)
    return "OK"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
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

# নতুন webhook সেট করার রুট
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    delete = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook").text
    set_hook = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}/{BOT_TOKEN}").text
    return f"Delete webhook: {delete}\nSet webhook: {set_hook}"

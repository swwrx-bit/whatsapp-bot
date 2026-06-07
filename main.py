from flask import Flask, request
import requests, os

app = Flask(__name__)

INSTANCE = os.environ["INSTANCE_ID"]
TOKEN = os.environ["TOKEN"]
AI_KEY = os.environ["AI_KEY"]

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={AI_KEY}"
    body = {
        "system_instruction": {
            "parts": [{"text": "Ты вежливый продавец-консультант. Помогаешь клиентам выбрать товар. Пиши кратко на русском языке."}]
        },
        "contents": [{"parts": [{"text": text}]}]
    }
    res = requests.post(url, json=body)
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        chat_id = data["senderData"]["chatId"]
        text = data["messageData"]["textMessageData"]["textMessage"]
    except:
        return "OK"

    reply = ask_gemini(text)

    requests.post(
        f"https://api.green-api.com/waInstance{INSTANCE}/sendMessage/{TOKEN}",
        json={"chatId": chat_id, "message": reply}
    )
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

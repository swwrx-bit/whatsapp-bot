from flask import Flask, request
from google import genai
import requests, os

app = Flask(__name__)

INSTANCE = os.environ["INSTANCE_ID"]
TOKEN = os.environ["TOKEN"]
AI_KEY = os.environ["AI_KEY"]

client = genai.Client(api_key=AI_KEY)

def ask_gemini(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=text
    )
    return response.text

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

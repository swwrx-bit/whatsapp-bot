from flask import Flask, request
import anthropic, requests, os

app = Flask(__name__)

INSTANCE = os.environ["INSTANCE_ID"]
TOKEN = os.environ["TOKEN"]
AI_KEY = os.environ["AI_KEY"]

client = anthropic.Anthropic(api_key=AI_KEY)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        chat_id = data["senderData"]["chatId"]
        text = data["messageData"]["textMessageData"]["textMessage"]
    except:
        return "OK"

    ai = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system="Ты вежливый продавец-консультант. Помогаешь клиентам выбрать товар и отвечаешь на вопросы. Пиши кратко и по делу на русском языке.",
        messages=[{"role": "user", "content": text}]
    )

    requests.post(
        f"https://api.green-api.com/waInstance{INSTANCE}/sendMessage/{TOKEN}",
        json={"chatId": chat_id, "message": ai.content[0].text}
    )
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, abort
from os import environ

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('TRia+XH1QWe/1KVzw7U7q623CMimWoZrx5SCxsowevIzCJwsCymFCX5IK6Tm49DQTXZBcU/ktVhUf5J6LL+Oh2I35lzuYZJEp+K7Cv+ZqXbhgahHPb/9vOQHMlN/VZD2VLCyyLZc7MuA6CHUGqGsswdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4c2b5a17e5a78d8d8cda06d0dfcdbf7c')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)

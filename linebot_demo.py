'''
Line Developer
'''
import json
from pathlib import Path
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, 
    ApiClient, 
    MessagingApi, 
    ReplyMessageRequest, 
    TextMessage)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
    )

app = Flask(__name__)
work_dir = Path(__file__).parent

with open(f"{work_dir}/login_info/line_dev.json", "r") as file:
    login_info = json.load(file)
    CHANNEL_SECRET = login_info["channel_secret"]
    CHANNEL_ACCESS_TOKEN = login_info["channel_access_token"]

config = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

'''
router setting
'''

# check the webhook is survival or not
@app.route("/callback", methods=["POST"])
def callback():
    print(request.headers)
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret!!")
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(config) as api_client:
        messaging_api = MessagingApi(api_client)
        
        reply_token = event.reply_token
        replyText = event.message.text
        print(replyText)

        list_reply = [
            TextMessage(text=replyText)
        ]

        messaging_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=list_reply
            )
        )
        
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8081
    )
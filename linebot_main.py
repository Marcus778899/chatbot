'''
Line Developer
'''
import json
import logging
from pathlib import Path
from flask import Flask, request, abort, send_from_directory
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
    TextMessageContent)

app = Flask(__name__)
work_dir = Path(__file__).parent

# Line Developer
line_login_info = json.load(open(f"{work_dir}/login_info/line_dev.json"))
configuration = Configuration(access_token=line_login_info['channel_access_token'])
handler = WebhookHandler(line_login_info['channel_secret'])

# ngrok url
def get_ngrok_url(url: str):
    return url

# test flask
@app.route("/test")
def hello_world():
    return "# Hello, World!"

# check webhook is actiavate or not
@app.route("/callback", methods=['POST'])
def callback():
    # get X line signature headler value
    signature = request.headers.get('X-Line-Signature')
    if signature is None:
        app.logger.info("Missing X_Line_Signature header")
        abort(400)

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# upload file
@app.route('/files/<path>')
def get_temp_path(path):
    return send_from_directory(f"{work_dir}/files", path)

# handle message
@handler.add(MessageEvent, message=TextMessageContent)
async def handle_text_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        # get api class
        api_instance = MessagingApi(api_client)
        # get replyToken
        reply_token = event.reply_token
        # get message
        replyText = event.message.text

        list_reply = [
            TextMessage(text=replyText)
        ]

        # response for user by lineBot
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=list_reply
            )
        )

if __name__ == "__main__":
    prefix_url = get_ngrok_url("https://0668-220-128-132-194.ngrok-free.app")
    logging.basicConfig(level=logging.INFO)
    app.run(
        host='0.0.0.0', 
        port=8080, 
        debug=True
    )
    print(prefix_url)
'''
LineBot initial
'''
from pathlib import Path
import json
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, 
    ApiClient, 
    MessagingApi
    )

app = Flask(__name__)

WORK_DIR = Path(__file__).parent.parent.absolute()
with open(WORK_DIR / "login_info/line_dev.json", "r") as f:
    login_info = json.load(f)
    CHANNEL_SECRET = login_info["channel_secret"]
    CHANNEL_ACCESS_TOKEN = login_info["channel_access_token"]

config = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
api_client = ApiClient(configuration=config)
message_api = MessagingApi(api_client)

'''
LineBot callback
'''
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
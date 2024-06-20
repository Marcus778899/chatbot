'''
question about rule
'''
import logging
from linebot.v3.messaging import (
    ReplyMessageRequest, 
    TextMessage
)
from linebot.v3.webhooks import (
    TextMessageContent,
    MessageEvent
)
from . import ChatOpenAPI
from .linebot_config import *

user_state = {}

def get_command(user_id, user_message):
    if user_message == "openai":
        reply_text = "What's your question?"
        user_state[user_id] = {"state": "waiting_for_question"}
        return reply_text
    else:
        return "It's not a keyword!!"

def update_user_state(user_id, state, data=None):
    user_state[user_id]['state'] = state
    if data:
        user_state[user_id].update(data)

def clear_user_state(user_id):
    if user_id in user_state:
        del user_state[user_id]

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with api_client:
        reply_token = event.reply_token
        request_message = event.message.text
        logging.info(f"event source is {event.source}")
        user_id = event.source.user_id
        logging.info(f"request_message is {request_message}")

        list_reply = [
            TextMessage(
                text = reply_message(request_message,user_id)
            )
        ]
        logging.info(f"list_reply is {list_reply}")
        message_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=list_reply
            )
        )
        
def reply_message(message,user_id) -> str:
    if user_id not in user_state:
        logging.info(f"user {user_id} is not in user_state")
        return get_command(user_id, message)

    if user_state[user_id]['state'] == "waiting_for_question":
        update_user_state(user_id, "waiting_for_answer", {"question": message})
        reply_text = ChatOpenAPI(message).main()
        clear_user_state(user_id)
        return reply_text

from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# client = WebClient(token=os.environ["SLACK_TOKEN"])

# # response = client.chat_postMessage(channel="#random", text="Hello World!")
# # response = client.conversations_history(channel="C07BM4NP291", limit = 100)
# # messages = response["messages"]
# # print(messages)

# # response = client.conversations_list()
# # print(response["channels"])

def get_channels(client): 
    response = client.conversations_list()
    allChannels = response["channels"]
    channels = []

    for channel in allChannels:
        if channel["is_member"]:
            channels.append({"id": channel["id"], "name": channel["name"]})

    return channels

def fetch_channel_messages(client, channel_id, limit=10):
    try: 
        response = client.conversations_history(channel=channel_id, limit=limit)
        allMessages = response["messages"]
        # print(allMessages)
        messages = []
        for message in allMessages:
            user_name = user_info(client, message["user"])
            messages.append({"userID": message["user"], "userName": user_name, "text": message["text"]})
        return messages
    except Exception as e:
        print(f"Error: {e}")

def user_info(client,user_id):
    try: 
        response = client.users_info(user=user_id)
        user = response["user"]
        # print(user['name'])
        return user['name']
    except Exception as e:
        print(f"Error: {e}")

# bot_channels=get_channels()
# channel_messages = []
# for bots in bot_channels:
#     messages = fetch_channel_messages(bots["id"], 10) 
#     channel_messages.append({"Channel": bots["name"],"messages": messages})

# print(channel_messages)

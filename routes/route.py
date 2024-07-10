from fastapi import APIRouter, WebSocket, Request, HTTPException
import httpx
from models.models import PostHistory, Todo
from config.database import collection_history, collection_user, collection_todos, collection_slack_access
from schema.schemas import list_serial_history, list_serial_user, list_serial_todo
from bson import ObjectId
from api.openaiEmbedding import get_embedding
from api.database import get_search_result
from dotenv import load_dotenv
import os
from openai import OpenAI
from slack_sdk import WebClient
from slackIntegration.slackTest import get_channels, fetch_channel_messages
load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

tokens = []
SLACK_CLIENT_ID = os.environ.get("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.environ.get("SLACK_CLIENT_SECRET")
SLACK_REDIRECT_URI = os.environ.get("SLACK_REDIRECT_URI")

# GET histories
@router.get("/history")
async def get_history(): 
    histories = list_serial_history(collection_history.find())
    return histories


# GET history by id
@router.get("/history/{id}")
async def get_history_by_id(id: str):
    history = collection_history.find({"user_id": id})
    return list_serial_history(history)

# POST histories
@router.post("/history")
async def post_history(postHistory: PostHistory):
    description_embedding = get_embedding(postHistory.description)
    collection_history.insert_one({
        "user_id": postHistory.user_id,
        "description": postHistory.description,
        "description_embedding": description_embedding
    })
    return {"message": "History has been added successfully.", "status": "success"}

# GET vector search
@router.websocket("/vector_search")
async def get_vector_search(websocket: WebSocket):
    print("api hit")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            query = data
            print(data)
            search_result = get_search_result(query, collection_history)
            print(search_result)
            combined_information = f"""
                Context: {search_result}
                Question: {query}
                Answer: Your answer goes here
            """
            # print(search_result)
            # gpt
            # prompt = ChatPromptTemplate.from_messages(
            #     [
            #     (
            #         "Answer using context. If no context, answer based on your knowledge."
            #     ),
            #     (
            #         """
            #         Context: {search_result}
            #         Question: {question}
            #         Answer: Your answer goes here.
            #         """
            #     )
            #     ]
            # )
            # llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
            # chain = prompt | llm
            # get the streaming response

            # chat=list()
            # response = chain.invoke({"search_result": search_result, "question": query})
            # print("Response",response)
            chat_completion = client.chat.completions.create(
            messages=[
            {
                "role": "system",
                "content": "Answer using context. If no context, answer based on your knowledge."
            },
            {
                "role": "user",
                "content": combined_information
            }
            ],
            model= "gpt-3.5-turbo-0125", # "gpt-3.5-turbo-0125
            temperature=0,
            stream=True
            )

            for chunk in chat_completion:
                content = chunk.choices[0].delta.content or ""
                if content:
                    await websocket.send_text(content)
            await websocket.send_text("End of response")
            # await websocket.close()
    except Exception as e:
        print(e)
        await websocket.close()
        return {"message": "Error in vector search", "status": "error"}
    # async def stream_response():
    #     for chunk in chat:
    #         print chunk
    # return StreamingResponse(stream_response(), media_type="text/event-stream")
    # return StreamingResponse(response.content, media_type="text/event-stream")

# GET users 
@router.get("/user")
async def get_user():
    users = list_serial_user(collection_user.find())
    return users

# POST users
@router.post("/user")
async def post_user(first_name: str, last_name: str, description: str):
    description_embedding = get_embedding(description)
    collection_user.insert_one({
        "first_name": first_name,
        "last_name": last_name, 
        "description": description,
        "description_embedding": description_embedding
    })

# POST todos
@router.post("/todo")
async def post_todo(todo: Todo):
    collection_todos.insert_one({
        "user_id": todo.user_id,
        "taskTitle": todo.taskTitle,
        "taskColor": todo.taskColor,
        "startDate": todo.startDate,
        "endDate": todo.endDate,
        "startTime": todo.startTime,
        "endTime": todo.endTime,
        "reminderTime": todo.reminderTime,
        "taskType": todo.taskType,
        "tag": todo.tag,
        "label": todo.label,
        "redirectURL": todo.redirectURL,
        "progress": todo.progress,
        "priority": todo.priority
    })
    return {"message": "Todo has been added successfully.", "status": "success"}

# GET todos by id
@router.get("/todo/{id}")
async def get_todo_by_id(id: str):
    todos = collection_todos.find({"user_id": id})
    return list_serial_todo(todos)


# PUT todos by id
@router.put("/todo-update/{id}")
async def update_todo_by_id(id: str, todo: Todo):
    collection_todos.update_one({"_id": ObjectId(id)}, {"$set": {
        "user_id": todo.user_id,
        "taskTitle": todo.taskTitle,
        "taskColor": todo.taskColor,
        "startDate": todo.startDate,
        "endDate": todo.endDate,
        "startTime": todo.startTime,
        "endTime": todo.endTime,
        "reminderTime": todo.reminderTime,
        "taskType": todo.taskType,
        "tag": todo.tag,
        "label": todo.label,
        "redirectURL": todo.redirectURL,
        "progress": todo.progress,
        "priority": todo.priority
    }})
    return {"message": "Todo has been updated successfully.", "status": "success"}

# DELETE todos by id
@router.delete("/todo-delete/{id}")
async def delete_todo_by_id(id: str):
    collection_todos.delete_one({"_id": ObjectId(id)})
    return {"message": "Todo has been deleted successfully.", "status": "success"}

# GET indexes
@router.get("/indexes")
async def get_indexes():
    indexes = collection_history.index_information()
    return indexes

@router.get('/oauth/callback')
async def oauth_callback(request: Request):
    # print("code: ", request.query_params.get("code"))
    code = request.query_params.get("code")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/oauth.v2.access",
            data={
                "client_id": os.environ["SLACK_CLIENT_ID"],
                "client_secret": os.environ["SLACK_CLIENT_SECRET"],
                "code": code,
                "redirect_uri": os.environ["SLACK_REDIRECT_URI"],
            }
        )
        data = response.json()
        
    if not data.get("ok"):
        raise HTTPException(status_code=400, detail="Error during OAuth")
    team_id = data["team"]["id"]
    access_token = data["access_token"]
    team_name = data["team"]["name"]    
    collection_slack_access.update_one(
        {"team_id": team_id},
        {"$set": {"team_name": team_name, "access_token": access_token}},
        upsert=True
    )
    return {"Message": "Successful", "team_id": data["team"]["id"], "access": data["access_token"], "team_name": data["team"]["name"]}

@router.get("/get_tokens")
async def get_tokens():
    print("tokens: ", tokens)
    return tokens

@router.get("/slack_channel_messages")
async def get_slack_channel_messages():
    # print("tokens: ", tokens)
    client = WebClient(token=os.environ["SLACK_TOKEN"])
    bot_channels = get_channels(client)
    channel_messages = []
    for bots in bot_channels:
        messages = fetch_channel_messages(client, bots["id"], 10) 
        channel_messages.append({"Channel": bots["name"],"messages": messages})
    
    print(channel_messages)

@router.post("/send_slack_messages")
async def send_slack_messages(text: str, channel_name: str):
    try:
        client = WebClient(token = os.environ["SLACK_TOKEN"])
        response = client.chat_postMessage(channel=channel_name, text=text)
        return {"message": "Message sent successfully", "status": "success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Error in sending message", "status": "error"}    
from fastapi import APIRouter
from models.models import History, PostHistory, Todo
from config.database import collection_history, collection_user, collection_todos
from schema.schemas import list_serial_history, list_serial_user, list_serial_todo
from bson import ObjectId
# from api.testing import get_embedding
from api.openaiEmbedding import get_embedding
from api.database import get_search_result
from api.gemma import client
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

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
@router.get("/vector_search")
async def get_vector_search(query: str):
    print("api hit")
    search_result = get_search_result(query, collection_history)
    print(search_result)

    # gpt
    prompt = ChatPromptTemplate.from_messages(
        [
        (
            "Answer using context."
        ),
        (
            """
            Context: {search_result}
            Question: {question}
            Answer: Your answer goes here.
            """
        )
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    chain = prompt | llm
    response = chain.invoke({"search_result": search_result, "question": query})
    print(response.content)


    # print(combined_information)
    # response = ""
    # for message in client.chat_completion(
    #     messages=[{"role": "user", "content": combined_information}],
    #     max_tokens=500,
    #     stream=True,
    # ):
    #     response += message.choices[0].delta.content

    # print(response, end="")
    
    return response.content
    # return search_result

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

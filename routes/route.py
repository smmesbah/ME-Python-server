from fastapi import APIRouter
from models.models import History
from config.database import collection_history, collection_user
from schema.schemas import list_serial_history, list_serial_user
from bson import ObjectId
from api.testing import get_embedding
from api.database import get_search_result
from api.gemma import client
from fastapi.responses import StreamingResponse

router = APIRouter()

# GET histories
@router.get("/history")
async def get_history(): 
    histories = list_serial_history(collection_history.find())
    return histories


# POST histories
@router.post("/history")
async def post_history(user_id: str, description: str):
    description_embedding = get_embedding(description)
    collection_history.insert_one({
        "user_id": user_id,
        "description": description,
        "description_embedding": description_embedding
    })

# GET vector search
@router.get("/vector_search")
async def get_vector_search(query: str):
    print("api hit")
    search_result = get_search_result(query, collection_history)
    combined_information = (
        f"Query: {query}\n\n Continue to answer the query by using the Search Results:\n{search_result}."
    )
    print(combined_information)
    response = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": combined_information}],
        max_tokens=500,
        stream=True,
    ):
        response += message.choices[0].delta.content

    print(response, end="")
    
    return response
    # return combined_information

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

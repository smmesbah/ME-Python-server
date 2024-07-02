from fastapi import FastAPI, HTTPException
from typing import List
from langchain_community.document_loaders import GitHubIssuesLoader
from pymongo.mongo_client import MongoClient
import os

app = FastAPI() 

mongo_uri = "mongodb+srv://Samina:samina@cluster0.grz1bag.mongodb.net/"

client = MongoClient(mongo_uri)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB.")
except Exception as e:
    print(f"An error occurred: {e}")

@app.get("/")
def index():
    return {"message": "Hello, World!"}


# @app.get("/github_issues", response_model=List[dict])
# async def get_github_issues(repo: str, include_prs: bool = False, state: str = "all"):
#     try:
#         loader = GitHubIssuesLoader(repo=repo, access_token="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", include_prs=include_prs, state=state)
#         docs = loader.load()
#         return docs[:10]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
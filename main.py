from fastapi import FastAPI
from routes.route import router

app = FastAPI() 

app.include_router(router)

# @app.get("/")
# def index():
#     return {"message": "Hello, World!"}


# @app.get("/github_issues", response_model=List[dict])
# async def get_github_issues(repo: str, include_prs: bool = False, state: str = "all"):
#     try:
#         loader = GitHubIssuesLoader(repo=repo, access_token="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", include_prs=include_prs, state=state)
#         docs = loader.load()
#         return docs[:10]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
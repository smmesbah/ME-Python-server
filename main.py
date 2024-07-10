from fastapi import FastAPI
from routes.route import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI() 
tokens=[]

app.include_router(router)

# @app.get('/oauth/callback')
# async def oauth_callback(request: Request):
#     # print("code: ", request.query_params.get("code"))
#     code = request.query_params.get("code")
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://slack.com/api/oauth.v2.access",
#             data={
#                 "client_id": os.environ["SLACK_CLIENT_ID"],
#                 "client_secret": os.environ["SLACK_CLIENT_SECRET"],
#                 "code": code,
#                 "redirect_uri": os.environ["SLACK_REDIRECT_URI"],
#             }
#         )
#         data = response.json()
        
#     if not data.get("ok"):
#         raise HTTPException(status_code=400, detail="Error during OAuth")
#     team_id = data["team"]["id"]
#     access_token = data["access_token"]
#     tokens.append({"team_id": team_id, "access_token": access_token})
#     print("tokens", tokens)
#     return {"Message": "Successful", "team_id": data["team"]["id"], "access": data["access_token"], "team_name": data["team"]["name"]}


# @app.get("/get_tokens")
# async def get_tokens():
#     print("tokens: ", tokens)
#     return tokens

# @app.get("/slack_channel_messages")
# async def get_slack_channel_messages():
#     # print("tokens: ", tokens)
#     client = WebClient(token=tokens[0]["access_token"])
#     bot_channels = get_channels(client)
#     channel_messages = []
#     for bots in bot_channels:
#         messages = fetch_channel_messages(client, bots["id"], 10) 
#         channel_messages.append({"Channel": bots["name"],"messages": messages})
    
#     print(channel_messages)



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
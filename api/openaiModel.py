import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

chat = list()

def get_chat_response():
    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": "What is the capital of the United States?"
        }
        ],
        model= "gpt-3.5-turbo-0125", # "gpt-3.5-turbo-0125
        temperature=0,
        stream=True
    )

    for chunk in chat_completion:
        print(chunk.choices[0].delta.content or "", end="")
        chat.append(chunk.choices[0].delta.content or "")
    
get_chat_response()


# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the capital of the United States?"
#         }
#     ],
#     model = "gpt-3.5-turbo-0125",
#     temperature=0,
#     stream=True
# )

# for chunk in chat_completion:
#     print(chunk.choices[0].delta.content or "", end="")
#     return chunk.choices[0].delta.content or ""
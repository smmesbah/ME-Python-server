from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
# os.environ["OPENAI_API_KEY"] = "sk-proj-J0esYQRZ6rtOIpe33VKHT3BlbkFJiYwWLpXJ4uX0CFIvxFyd"

openai_embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

def get_embedding(text:str) -> list[float]:
    if not text.strip():
        print("Attemted to get embedding for empty text.")
        return []
    
    embedding = openai_embedding_model.embed_query(text)
    return embedding

# text = "This is a test document"

# embedding = openai_embedding_model.embed_query(text)

# print(embedding)
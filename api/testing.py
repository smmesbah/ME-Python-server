from langchain_community.document_loaders import GitHubIssuesLoader
# from dataProcessing import dataset_df
from sentence_transformers import SentenceTransformer

# loader = GitHubIssuesLoader(repo="huggingface/peft", access_token="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", include_prs=False, state="all")

# docs = loader.load()
# print(docs)

# print(dataset_df.head(5))

embedding_model = SentenceTransformer("thenlper/gte-large")

def get_embedding(text:str) -> list[float]:
    if not text.strip():
        print("Attemted to get embedding for empty text.")
        return []
    
    embedding = embedding_model.encode(text)
    return embedding.tolist()

# dataset_df["embedding"] = dataset_df["fullplot"].apply(get_embedding)

# print(dataset_df.head(5))

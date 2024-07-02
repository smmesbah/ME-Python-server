import pymongo
import pymongo.errors
from testing import get_embedding

mongo_uri = "mongodb+srv://Samina:samina@cluster0.grz1bag.mongodb.net/"

def get_mongo_client(mongo_uri):
    """Establish connection to the MongoDB"""

    try: 
        client = pymongo.MongoClient(mongo_uri)
        print("Connected to MongoDB successfully")
        return client
    except pymongo.errors.ConnectionFailure as e: 
        print(f"Connection failed: {e}")
        return None
    
mongo_client = get_mongo_client(mongo_uri)

db  = mongo_client["movies"]

collection = db["moviee_collection_2"]
# collection.delete_many({})

# documents = dataset_df.to_dict("records")
# collection.insert_many(documents)

# print("Data ingestion into MongoDB completed")

def vector_search(user_query, collection):
    """
    Perform a vector search in the MongoDB colelction based on the user query.
    
    Args:
    user_query (str): The user's query string.
    collection (MongoCollection): The MongoDB collection to search.
    
    Returns:
    list: A list of matching documents.
    """
    
    # Generate embedding for the user query
    query_embedding = get_embedding(user_query)
    # print(query_embedding)
    
    if query_embedding is None:
        return "Invalid query or embedding generation failed."
    
    # Define the vector search
    pipeline = [
        {
            "$vectorSearch":{
                "index":"vector_index",
                "queryVector": query_embedding,
                "path":"embedding",
                "numCandidates": 150,
                "limit": 4, # Return top 4 matches
                
            }
        },
        {
            "$project":{
                "_id": 0, # Exclude the _id field
                "fullplot": 1, # Include the plot field
                "title": 1, # Include the title field
                "genres": 1, # Include the genres field
                "score": {"$meta": "vectorSearchScore"}, # Include the search score
            }
        }
    ]
    
    # Execute the search
    results = collection.aggregate(pipeline)
    # print(list(results)) 
    return list(results)


def get_search_result(query, collection):

    get_knowledge = vector_search(query, collection)

    search_result = ""
    for result in get_knowledge:
        search_result += f"Title: {result.get('title', 'N/A')}, Plot: {result.get('fullplot', 'N/A')}\n"
    # print(search_result)
    return search_result

query = "What is the best romantic movie to watch and why?"
source_information = get_search_result(query, collection)

combined_information = (
    f"Query: {query}\nContinue to answer the query by using the Search Results:\n{source_information}."
)

print(combined_information)
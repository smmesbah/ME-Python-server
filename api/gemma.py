from huggingface_hub import InferenceClient

client = InferenceClient(
    "google/gemma-2b-it",
    token="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",
)

# for message in client.chat_completion(
# 	messages=[{"role": "user", "content": "Query: What is my name?\n\n Continue to answer the query by using the Search Results:\n Description: My name is Samina\nDescription: I am a student\nDescription: My friend is Mesbah the goru\n Description: I love sleeping\n."}],
# 	max_tokens=500,
# 	stream=True,
# ):
#     print(message.choices[0].delta.content, end="")
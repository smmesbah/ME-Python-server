from huggingface_hub import HfApi, HfFolder
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

token = "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"

HfFolder.save_token(token)

api = HfApi()
user = api.whoami()

print(f"Logged in as: {user['name']}")

# google/gemma-2b-it

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")

# print("saving the model and tokenizer...")
# save_dir = "./saved_model"
# tokenizer.save_pretrained(save_dir)
# model.save_pretrained(save_dir)
# print("saved the model and tokenizer!!!")


combined_information = "Query: What is my name?\n\n Continue to answer the query by using the Search Results:\nUser_id: 1234567asdf, Description: My name is Samina\nUser_id: 1234567asdf, Description: I am a student\nUser_id: 1234567asdf, Description: My friend is Mesbah the goru\nUser_id: 1234567asdf, Description: I love sleeping\n."
input_ids = tokenizer.encode(combined_information, return_tensors="pt")
# Set the attention mask
attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

# Ensure pad_token_id is set
pad_token_id = tokenizer.eos_token_id

print("Generating response...")
response = model.generate(input_ids, max_new_tokens=10, attention_mask=attention_mask, pad_token_id=pad_token_id)
print("Response generated")
print("response: ", tokenizer.decode(response[0], skip_special_tokens=True))

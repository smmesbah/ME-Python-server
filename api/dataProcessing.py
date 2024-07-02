from datasets import load_dataset
import pandas as pd

dataset = load_dataset("AIatMongoDB/embedded_movies")

dataset_df = pd.DataFrame(dataset["train"])

# print(dataset_df.head(5))

# print(dataset_df.isnull().sum())

dataset_df = dataset_df.dropna(subset=["fullplot"])
print("\nNumber of missing values in each column after removal: ")
print(dataset_df.isnull().sum())

dataset_df = dataset_df.drop(columns=["plot_embedding"])
print(dataset_df.head(5))
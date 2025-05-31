# Query the model with document embeddings
# Following setup in https://ollama.com/blog/embedding-models

import chromadb
import ollama

EMBEDDING_MODEL = "mxbai-embed-large"
QUERY_MODEL = "gemma3:12b"

# Load up the ChromaDB collection
client = chromadb.PersistentClient(path=".chroma")
collection = client.get_collection(name="book_reviews")

# Main question to answer
input = "I love book with fantastical settings. What's a good book with great characters in a unique fantasy setting?"

# Generate an embedding for the input and retrieve the most relevant documents
response = ollama.embed(model=EMBEDDING_MODEL, input=input)
results = collection.query(query_embeddings=response["embeddings"], n_results=1)
metadata = results["metadatas"][0][0]
data = results["documents"][0][0]
distances = results["distances"][0][0]

# List of closest documents that matched
print(metadata["title"])
print(metadata["tags"])
print(distances)

# Use the top documents to generate a response
# prompt = f"Using this data: {data}. Respond to this prompt: {input}"
prompt = f"Using only this data: {data} and this prompt: {input}. Summarize the book review focusing on how it addresses the prompt."
output = ollama.generate(model=QUERY_MODEL, prompt=prompt)

print(output["response"])

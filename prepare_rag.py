# Construct a vector database with document embeddings
# Following setup in https://docs.trychroma.com/docs/overview/getting-started

import chromadb
import feedparser
import ollama
from bs4 import BeautifulSoup

EMBEDDING_MODEL = "mxbai-embed-large"
BLOGFILE = "blog-05-30-2025.xml"

# Parse the blogger output file
d = feedparser.parse(BLOGFILE)

# Instantiate the ChromaDB for storing the RAG
client = chromadb.PersistentClient(path=".chroma")
collection = client.get_or_create_collection(name="book_reviews")

# Loop over entries for specific posts
for i, entry in enumerate(d.entries):
    # Get the tags used and skip any without Books in it
    tag_list = entry.tags
    tag_list = [
        x.get("term") for x in tag_list if not x.get("term", "").endswith("#post")
    ]
    if "Books" not in tag_list:
        continue

    print(f"Processing {i}: {entry.title}")

    # Gather ID
    id = entry.id

    # Gather metadata
    metadata = {
        "title": entry.title,
        "link": entry.link,
        "published": entry.published,
        "tags": ",".join(tag_list),
    }

    # Gather text, without any HTML
    # Get text without any HTML
    soup = BeautifulSoup(entry.summary, "html.parser")
    document = soup.text

    # Generate embeddings
    response = ollama.embed(model=EMBEDDING_MODEL, input=document)
    embeddings = response["embeddings"]

    # Add or update documents
    collection.upsert(
        documents=document, metadatas=metadata, embeddings=embeddings, ids=id
    )

print("RAG complete")

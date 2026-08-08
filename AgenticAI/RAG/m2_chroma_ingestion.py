"""
LAB: Module 2 - Ingestion Pipeline
---------------------------------------------------------
Goal: Extract, chunk, and store the VelocityX Policy.
Learners will see:
1. Recursive Character Text Chunking[cite: 34].
2. OpenAI Embeddings integration[cite: 31].
3. Persistent storage in a Docker-based ChromaDB[cite: 33].
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def print_chunk_diagnostics(chunks, max_chunks_to_print=5):
    """
    Prints sample chunks so learners can understand
    what is being stored in the vector database.
    """

    print("\n================ CHUNK DIAGNOSTICS ================")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Showing first {min(max_chunks_to_print, len(chunks))} chunks\n")

    for i, chunk in enumerate(chunks[:max_chunks_to_print], start=1):
        print(f"---------------- Chunk {i} ----------------")
        print(f"Chunk length: {len(chunk.page_content)} characters")
        print(f"Metadata: {chunk.metadata}")
        print("Chunk preview:")
        print(chunk.page_content[:700])

        if len(chunk.page_content) > 700:
            print("... [truncated]")

        print()


def ingest_data():
    # 1. Load the VelocityX Policy [cite: 165]
    loader = PyPDFLoader("VelocityX Ecommerce Warranty, Returns & Exchange Policy.pdf")
    documents = loader.load()

    print("\n================ DOCUMENT LOAD DIAGNOSTICS ================")
    print(f"Total pages/documents loaded: {len(documents)}")

    if documents:
        print("Sample page metadata:")
        print(documents[0].metadata)
        print("\nSample page content preview:")
        print(documents[0].page_content[:700])
        print("... [truncated]\n")

    # 2. Chunking Strategy: Recursive splitting to maintain context [cite: 34]
    # We use a chunk size of 1000 with 200 overlap to ensure semantics aren't cut.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    # Diagnostic print to inspect the generated chunks
    print_chunk_diagnostics(chunks, max_chunks_to_print=5)

    # 3. Initialize Embeddings and Vector DB [cite: 31, 33]
    embeddings = OpenAIEmbeddings()

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="velocity_x_policy",
        persist_directory="./chroma_db"  # Maps to your local/docker storage
    )

    print("\n================ INGESTION STATUS ================")
    print("Ingestion complete. Data stored in ChromaDB.")
    print("Collection name: velocity_x_policy")
    print("Persist directory: ./chroma_db")


if __name__ == "__main__":
    ingest_data()
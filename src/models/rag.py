import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.tools import tool
from langchain.schema import Document

# Initialize the Chroma vector store
vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    persist_directory="./rag_data/.chromadb"
)

def load_annotation_mappings(filepath):
    """Load annotation mappings and create vector embeddings."""
    with open(filepath, "r") as file:
        data = json.load(file)

    categories = data.get("categories", [])
    docs = []
    for category in categories:
        for attribute in category["attributes"]:
            for value in attribute["values"]:
                doc = Document(
                    page_content=f"{category['name']} {attribute['name']} {value['name']}",
                    metadata={
                        "icon": value["icon"],
                        "color": value["color"]
                    }
                )
                docs.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_docs(docs):
    """Load and split documents, then add them to the vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)


def initialize_rag_database():
    """Initialize the RAG database with annotation mappings."""
    load_annotation_mappings("./src/data/benchmark/annotation_to_icon_mappings.json")
    print("RAG database initialized with annotation mappings.")

def format_docs(docs):
    """Format documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

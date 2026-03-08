from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from modules.utils import load_documents
from config import *

def build_vector_store2():

    docs = load_documents(RAW_DOCS_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)
    print(f"Loaded {len(docs)} documents, split into {len(chunks)} chunks")
    for c in chunks[:3]:
        print(c.page_content[:200])
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    vectordb.persist()

    return vectordb

def build_vector_store():
    print("Loading PDF documents...")
    docs = load_documents("data/raw")
    print(f"Loaded {len(docs)} documents")

    # Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    # Filter
    keywords = ["требования", "ГОСТ", "мера защиты", "политика безопасности"]
    filtered_chunks = [c for c in chunks if any(k.lower() in c.page_content.lower() for k in keywords)]
    print(f"Filtered down to {len(filtered_chunks)} chunks")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Chroma — база создается и сохраняется автоматически
    vectordb = Chroma.from_documents(
        documents=filtered_chunks,
        embedding=embeddings,
        persist_directory="data/vector_store"
    )

    print("Vector database successfully created")


def retrieve_context(query, k=3):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    docs = vectordb.similarity_search(query, k=k)

    # фильтруем по ключевым словам
    keywords = ["требования", "мера защиты", "ГОСТ", "политика безопасности"]
    filtered_docs = []
    for doc in docs:
        text_lower = doc.page_content.lower()
        if any(word.lower() in text_lower for word in keywords):
            filtered_docs.append(doc)

    if not filtered_docs:
        filtered_docs = docs  # если фильтр ничего не дал, берем оригинальные

    # формируем контекст с указанием источника
    context = "\n\n".join(
        [f"Документ: {getattr(d, 'metadata', {}).get('source','unknown')}\n{d.page_content}" for d in filtered_docs]
    )

    return context
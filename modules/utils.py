from langchain_community.document_loaders import PyPDFLoader
import os

def load_documents(path):
    documents = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(path, file))
            docs = loader.load()
            # отбрасываем пустые страницы
            docs = [d for d in docs if d.page_content.strip()]
            # добавляем метаданные с именем файла
            for d in docs:
                d.metadata["source"] = file
            documents.extend(docs)
    return documents
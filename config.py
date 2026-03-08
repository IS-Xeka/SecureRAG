import os
from dotenv import load_dotenv

load_dotenv()

GIGACHAT_MODEL = os.getenv("GIGACHAT_MODEL")
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")

CERT_PATH = os.getenv("CERT_PATH")

VECTOR_DB_PATH = os.getenv("VECTOR_DB")
RAW_DOCS_PATH = os.getenv("RAW_DOCS")

GIGACHAT_AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
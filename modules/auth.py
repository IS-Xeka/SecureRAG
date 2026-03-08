import uuid
import requests
from config import *

def get_access_token():

    headers = {
        "Authorization": f"Basic {GIGACHAT_CREDENTIALS}",
        "RqUID": str(uuid.uuid4()),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "scope": "GIGACHAT_API_PERS"
    }

    response = requests.post(
        GIGACHAT_AUTH_URL,
        headers=headers,
        data=payload,
        verify=CERT_PATH
    )

    response.raise_for_status()

    return response.json()["access_token"]
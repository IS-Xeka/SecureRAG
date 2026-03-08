import requests

from modules.auth import get_access_token
from modules.input_filter import validate_input
from modules.output_filter import validate_output
from modules.rag_core import retrieve_context

from config import *

def ask_gigachat(prompt):

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GIGACHAT_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(
        GIGACHAT_API_URL,
        headers=headers,
        json=payload,
        verify=CERT_PATH
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def secure_rag(query):

    validate_input(query)

    context = retrieve_context(query)

    prompt = f"""
Используй только информацию из контекста.

Контекст:
{context}

Вопрос:
{query}
"""

    answer = ask_gigachat(prompt)

    return validate_output(answer)


def main():

    print("Secure RAG System started")

    while True:

        query = input("\nВведите вопрос: ")

        if query == "exit":
            break

        try:

            response = secure_rag(query)

            print("\nОтвет:")
            print(response)

        except Exception as e:

            print("\nОшибка безопасности:")
            print(e)


if __name__ == "__main__":
    main()
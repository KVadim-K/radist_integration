import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных из .env файла
load_dotenv()

API_KEY = os.getenv('RADIST_API_KEY')
COMPANY_ID = os.getenv('COMPANY_ID')
INTEGRATION_ID = os.getenv('INTEGRATION_ID')

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

app = FastAPI()


# Проверка подключения
@app.get("/")
def root():
    return {"status": "Работает!"}


# Обработка вебхука Radist
@app.post("/webhook")
async def webhook_radist(request: Request):
    data = await request.json()
    logging.info(f"Получен webhook: {data}")

    event = data.get('event')
    chat_id = data['data']['chat']['id']
    connection_id = data['data']['connection']['id']
    message_text = data['data']['message']['text']['body']

    logging.info(f"Новое сообщение в чат {chat_id}: {message_text}")

    # Ответ клиенту
    reply_text = f"Вы написали: {message_text}"

    url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/messaging/chats/{chat_id}/messages"

    payload = {
        "connection_id": connection_id,
        "type": "text",
        "text": {"body": reply_text}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        logging.info("Сообщение отправлено клиенту.")
    else:
        logging.error(f"Ошибка отправки сообщения: {response.text}")

    return {"status": "OK"}

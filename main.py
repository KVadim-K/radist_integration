import os
import logging
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

API_KEY = os.getenv("RADIST_API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")
CONNECTION_ID = os.getenv("CONNECTION_ID")

if not API_KEY or not COMPANY_ID or not CONNECTION_ID:
    raise ValueError("Проверьте, что в .env заданы RADIST_API_KEY, COMPANY_ID, CONNECTION_ID")

app = FastAPI()


# Эндпоинт для проверки работы сервера
@app.get("/")
def root():
    return {"status": "Работает!"}


# Обработка входящих вебхуков от Radist (расширенное логирование)
@app.post("/webhook")
async def webhook_handler(request: Request):
    """
    Обработка входящих вебхуков от Radist.
    Рекомендуется быстро сохранить событие в очередь и вернуть 200.
    """
    try:
        # Лог IP-адрес, порт и заголовки
        client_host = request.client.host
        client_port = request.client.port
        headers_dict = dict(request.headers)

        data = await request.json()
        logger.info("Получен webhook от %s:%s, заголовки=%s, данные=%s",
                    client_host, client_port, headers_dict, data)

    except Exception as e:
        logger.error("Ошибка чтения JSON: %s", e)
        raise HTTPException(status_code=400, detail="Неверный формат JSON")

    return {"status": "OK"}


# Пример эндпоинта для получения списка источников чатов (исправленный URL)
@app.get("/api/radist/chat-sources")
def get_chat_sources():
    import requests

    RADIST_API_KEY = os.getenv("RADIST_API_KEY")
    COMPANY_ID = os.getenv("COMPANY_ID")

    headers = {
        "X-Api-Key": RADIST_API_KEY,
        "Content-Type": "application/json"
    }

    # Добавляем /companies/{COMPANY_ID}/
    url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/messaging/chats/sources/"
    response = requests.get(url, headers=headers)

    logger.info("Get chat sources. Статус: %s, Ответ: %s", response.status_code, response.text)
    return {
        "status": response.status_code,
        "response": response.json()
    }


# Пример эндпоинта для создания чата (исправленный URL)
@app.post("/create_chat")
def create_chat():
    import requests

    RADIST_API_KEY = os.getenv("RADIST_API_KEY")
    COMPANY_ID = os.getenv("COMPANY_ID")
    CONNECTION_ID = os.getenv("CONNECTION_ID")

    headers = {
        "X-Api-Key": RADIST_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "connection_id": int(CONNECTION_ID),
        "contact": {
            # Пример: создаём чат по номеру телефона
            "phone": "+79111234567"
        }
    }

    # Добавляем /companies/{COMPANY_ID}/
    url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/messaging/chats"
    response = requests.post(url, headers=headers, json=payload)

    logger.info("Create chat. Статус: %s, Ответ: %s", response.status_code, response.text)
    return {
        "status": response.status_code,
        "response": response.json()
    }


# Пример эндпоинта для отправки сообщения (исправленный URL)
@app.post("/send_message")
def send_message():
    import requests

    RADIST_API_KEY = os.getenv("RADIST_API_KEY")
    COMPANY_ID = os.getenv("COMPANY_ID")
    CONNECTION_ID = os.getenv("CONNECTION_ID")

    headers = {
        "X-Api-Key": RADIST_API_KEY,
        "Content-Type": "application/json"
    }

    # Нужно получить chat_id из ответа create_chat или из списка чатов
    chat_id = "1234567890"

    payload = {
        "connection_id": int(CONNECTION_ID),
        "chat_id": chat_id,
        "message_type": "text",
        "text": {
            "text": "Привет, это тестовое сообщение!"
        }
    }

    # Добавляем /companies/{COMPANY_ID}/
    url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/messaging/messages"
    response = requests.post(url, headers=headers, json=payload)

    logger.info("Send message. Статус: %s, Ответ: %s", response.status_code, response.text)
    return {
        "status": response.status_code,
        "response": response.json()
    }

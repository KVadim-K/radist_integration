import os
import requests
from dotenv import load_dotenv
from pyngrok import ngrok

# Загрузка переменных окружения
load_dotenv()

RADIST_API_KEY = os.getenv("RADIST_API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")
CONNECTION_ID = os.getenv("CONNECTION_ID")
NGROK_URL = os.getenv("NGROK_URL")  # Если переменная не задана, NGROK_URL будет None

if not RADIST_API_KEY or not COMPANY_ID or not CONNECTION_ID:
    raise ValueError("Проверьте, что в .env заданы RADIST_API_KEY, COMPANY_ID и CONNECTION_ID")

# Если NGROK_URL не задан, запускаем туннель через pyngrok
if not NGROK_URL:
    tunnel = ngrok.connect(8000)
    NGROK_URL = tunnel.public_url
    print("Ngrok tunnel URL:", NGROK_URL)

headers = {
    "X-Api-Key": RADIST_API_KEY,
    "Content-Type": "application/json"
}

# Используем URL с завершающим слэшем, как в Swagger
url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/webhooks/"


# Тело запроса должно содержать обязательные поля:
# - connection_id: ID подключения (канала), для которого вы подписываетесь
# - url: публичный URL для получения уведомлений (должен включать путь /webhook)
# - events: массив типов событий, на которые вы подписываетесь
payload = {
    "connection_id": int(CONNECTION_ID),
    "url": f"{NGROK_URL}/webhook",
    "events": [
        "messages.create",
        "messages.delivery.delivered",
        "messages.delivery.read",
        "messages.delivery.error"
    ]
}

response = requests.post(url, headers=headers, json=payload)

print("Статус-код:", response.status_code)
print("Ответ:", response.text)

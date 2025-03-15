import os
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

API_KEY = os.getenv("RADIST_API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")
INTEGRATION_ID = os.getenv("INTEGRATION_ID")

if not API_KEY or not COMPANY_ID or not INTEGRATION_ID:
    raise ValueError("Проверьте, что в .env заданы RADIST_API_KEY, COMPANY_ID, INTEGRATION_ID")

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# Публичный URL от ngrok – УБЕДИТЬСЯ, ЧТО ОН АКТУАЛЬНЫй !!!!!
PUBLIC_WEBHOOK_URL = "https://0691-104-223-102-25.ngrok-free.app/webhook"

# Формирование payload – в данном варианте не передаем integration_id в теле, так как он уже в URL
payload = {
    "type": "message",      # можно заменить на другой тип, если нужно (например, "conversation")
    "url": PUBLIC_WEBHOOK_URL,
    "description": "Webhook для тестовой интеграции"
}

# Новый URL с указанием идентификатора интеграции
url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/integrations/{INTEGRATION_ID}/webhooks"

response = requests.post(url, headers=headers, json=payload)

print("Статус-код:", response.status_code)
print("Ответ:", response.text)

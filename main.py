import os
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных из .env файла
load_dotenv()

API_KEY = os.getenv("RADIST_API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")
CONNECTION_ID = os.getenv("CONNECTION_ID")


if not API_KEY or not COMPANY_ID or not CONNECTION_ID:
    raise ValueError("Проверьте, что в .env заданы RADIST_API_KEY, COMPANY_ID, CONNECTION_ID")


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
async def webhook_handler(request: Request):
    """
    Обработка входящих вебхуков от Radist.Online.
    Рекомендуется: быстро сохранить событие в очередь, вернуть 200,
    а основную обработку выполнить асинхронно.
    """
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Ошибка чтения JSON: {e}")
        raise HTTPException(status_code=400, detail="Неверный формат JSON")

    logger.info(f"Получен webhook: {data}")

    # Здесь можно добавить логику обработки входящих событий
    # Например, проверить event_type, сохранить данные в БД, отправить уведомление и т.д.

    return {"status": "OK"}
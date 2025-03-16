import os
import time
import requests
import subprocess
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()

RADIST_API_KEY = os.getenv("RADIST_API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")
CONNECTION_ID = os.getenv("CONNECTION_ID")
NGROK_URL = os.getenv("NGROK_URL")  # Если не задан, запустим туннель

if not RADIST_API_KEY or not COMPANY_ID or not CONNECTION_ID:
    raise ValueError("Проверьте, что в .env заданы RADIST_API_KEY, COMPANY_ID, CONNECTION_ID")

# 1) Запускаем uvicorn (сервер FastAPI) в фоне
uvicorn_cmd = ["uvicorn", "main:app", "--reload", "--port", "8000"]
uvicorn_proc = subprocess.Popen(uvicorn_cmd)
print("Запущен uvicorn, PID:", uvicorn_proc.pid)

# 2) Если NGROK_URL не задан, запускаем туннель через pyngrok
if not NGROK_URL:
    tunnel = ngrok.connect(8000)
    NGROK_URL = tunnel.public_url
    print("Ngrok tunnel URL:", NGROK_URL)
else:
    print("Используем указанный NGROK_URL:", NGROK_URL)

# 3) Регистрируем вебхук в Radist
headers = {
    "X-Api-Key": RADIST_API_KEY,
    "Content-Type": "application/json"
}
url = f"https://api.radist.online/v2/companies/{COMPANY_ID}/webhooks/"

payload = {
    "connection_id": int(CONNECTION_ID),
    "url": f"{NGROK_URL}/webhook",
    "events": [
        "messages.create",
        "messages.delivery.delivered",
        "messages.delivery.error",
        "messages.delivery.read"
    ]
}

response = requests.post(url, headers=headers, json=payload)
print("Статус-код:", response.status_code)
print("Ответ:", response.text)

# 4) Держим скрипт "живым", чтобы туннель не закрывался
print("Нажмите Ctrl+C, чтобы остановить скрипт (и закрыть туннель)")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nОстанавливаем сервер и туннель...")
finally:
    # Завершаем uvicorn
    uvicorn_proc.terminate()
    uvicorn_proc.wait(5)

    # Если мы поднимали tunnel через pyngrok, закроем его
    if 'tunnel' in locals():
        ngrok.disconnect(tunnel.public_url)
        ngrok.kill()

    print("Скрипт завершён.")

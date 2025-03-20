# Radist.Online Integration

Данный проект демонстрирует базовую интеграцию с сервисом [Radist.Online](https://radist.online) с использованием [FastAPI](https://fastapi.tiangolo.com/) и автоматической регистрацией вебхуков.  
**Важно**: Сервис Ngrok недоступен из России – вам могут потребоваться альтернативные решения (например, LocalTunnel, либо VPN, либо платная версия Ngrok c европейскими серверами).

## Структура проекта


- **`.env`** – содержит секретные данные и настройки (API-ключ Radist, ID компании, ID подключения и т.д.).
- **`main.py`** – FastAPI-приложение с расширенным логированием. Здесь определены эндпоинты для приёма вебхуков, получения источников чатов, создания чатов и отправки сообщений.
- **`webhook_setup.py`** – скрипт, который автоматически:
  - Запускает uvicorn (сервер FastAPI) в фоне.
  - Поднимает туннель через pyngrok и получает публичный URL.
  - Регистрирует вебхук в Radist.Online по указанному `connection_id`.
  - Удерживает процесс в рабочем состоянии (чтобы туннель не закрывался).
- **`requirements.txt`** – список зависимостей Python.
- **`venv`** – виртуальное окружение (создаётся командой `python -m venv venv`).


## Установка и запуск

1. **Склонируйте репозиторий** (или скопируйте файлы проекта).

2. **Создайте и активируйте виртуальное окружение** (пример для Windows PowerShell):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```
4. **Создайте файл .env в корне проекта и заполните нужными переменными:**
   ```bash
   RADIST_API_KEY=Ваш_API_Ключ_от_Radist
   COMPANY_ID=ID_Компании_в_Radist
   CONNECTION_ID=ID_Подключения_(например_Telegram)
   # NGROK_URL= указывать не обязательно, если скрипт webhook_setup.py сам запускает pyngrok
   ```

5. **(Автоматический способ) Запустите скрипт регистрации вебхука:**

   ```bash
   python webhook_setup.py
   ```
**•** Скрипт запустит Ngrok (через pyngrok), получит публичный URL и выполнит запрос к Radist.Online для регистрации вебхука на указанный `connection_id`.
      В терминале увидите что-то вроде:

    ```arduino
    Ngrok tunnel URL: https://xxxxx.ngrok-free.app
    Статус-код: 200
    Ответ: {"url": "...", "id": "...", ...}
    ```
**•** Это значит, что вебхук успешно зарегистрирован на сторону Radist.Online.

6. **(При необходимости) Запустите Ngrok вручную
**•** Если хотите вручную пробросить порт из терминала:**

   ```bash
   .\ngrok.exe http 8000
   ```

7. **Проверьте получение вебхуков**

    **•** При возникновении события (например, клиент написал в Telegram), Radist.Online отправит POST-запрос на ваш публичный URL (.../webhook).
    
    **•** В консоли (где запущен uvicorn) вы увидите логи, начиная с фразы Получен webhook: {...}.

8. **Тестирование API через PowerShell**

   ```powershell
   curl.exe --ssl-no-revoke -X POST "https://api.radist.online/v2/companies/<Ваш_ID_Компании>/connections/messaging/messages/" `
    -H "Content-Type: application/json" `
    -H "X-Api-Key: <Ваш_API_Ключ>" `
    --data-binary "@C:<Ваш путь к payload.json>"
   ```
   **•** Этот запрос отправляет сообщение (содержащееся в файле payload.json) через Radist API.
   **•** Пример запроса файле payload.json
   ```json
    {
      "connection_id": "<ваш_connection_id>",
      "chat_id": "<ваш_chat_id>",
      "message_type": "text",
      "text": {
        "text": "Привет! Это тестовое сообщение."
      }
    }
   ```
   **•** Выполните команду (укажите полный путь к файлу, если он не находится в текущей директории):

```bash
   curl.exe --ssl-no-revoke -X POST "https://api.radist.online/v2/companies/200509/messaging/messages/" -H "Content-Type: application/json" -H "X-Api-Key: <YOUR_API_KEY>" --data-binary "@C:\ПОЛНЫЙ\ПУТЬ\К\payload.json"
```
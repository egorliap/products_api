**Запуск сервиса со своего устройства**

1. Клонировать репозиторий https://github.com/egorliap/products_api.git
2. Создать виртуальное окружение командой ```python -m venv venv``` и запустить его с помощью ```.\venv\Scripts\activate``` (Windows) ```./venv/bin/activate``` (Linux)
3. Установить в виртуальное окружение зависимости командой ```pip install -r requirements.txt```
4. Создать файл окружения ```.env``` со следующим содержанием:
```
DB_HOST = localhost
DB_PORT = 5432
DB_USER = <ваш postgres юзернэйм>
DB_PASS = <ваш postgres пароль>
DB_NAME = products_db
```
5. Запустить сервис командой ```uvicorn main:app --port 8000```
6. Теперь переходе на http://localhost:8000/docs/ в браузере доступна документация данного api (с возможностью взаимодействовать с бд напрямую)

**Запуск с Docker**

Для запуска сервиса с помощью Docker необходимо запустить docker-compose (2 сервиса: само приложение и сервис бд)
Команда для запуска: ```docker compose up```

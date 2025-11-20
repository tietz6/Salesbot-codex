@echo off
chcp 65001 >nul
setlocal

set ROOT=%~dp0
cd /d %ROOT%

if not exist .venv (
  echo [setup] Создаю виртуальное окружение...
  python -m venv .venv
)

echo [setup] Активирую venv...
call .venv\Scripts\activate

echo [setup] Обновляю pip...
python -m pip install --upgrade pip --quiet

echo [setup] Ставлю зависимости для локального API...
python -m pip install -r _installer\runtime\requirements.txt

echo [run] Поднимаю API на 127.0.0.1:8080 ...
python -m uvicorn _installer.runtime.startup:app --host 127.0.0.1 --port 8080 --reload

import os
import time
import requests

# ============ НАСТРОЙКИ И ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ============

BACKEND_URL = (os.getenv("BACKEND_URL") or "http://127.0.0.1:8080").rstrip("/")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TG_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # можешь не использовать, оставить пустым

if not TOKEN:
    print("❌ Нет TELEGRAM_BOT_TOKEN / TG_BOT_TOKEN. Проверь start_core_api.bat")
    time.sleep(60)  # чтобы окно не сразу закрывалось, если токен не найден
    raise SystemExit(1)

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Память: chat_id -> {"mode": "dialog"/None, "sid": str|None}
SESSIONS: dict[int, dict] = {}


def log(*args):
    """Простой лог в консоль, чтобы видеть работу бота."""
    print("[BOT]", *args)


def send_message(chat_id: int, text: str):
    """Отправка текста в Telegram."""
    try:
        resp = requests.post(
            BASE_URL + "/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
        if not resp.ok:
            log("Ошибка sendMessage:", resp.status_code, resp.text)
    except Exception as e:
        log("Ошибка отправки в Telegram:", e)


def get_session(chat_id: int):
    """Вернуть или создать запись сессии для данного чата."""
    if chat_id not in SESSIONS:
        SESSIONS[chat_id] = {"mode": None, "sid": None}
    return SESSIONS[chat_id]


# ============ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ trainer_dialog_engine ============

def api_start_session(manager_id: str, scenario_id: str = "cold_start_warm") -> dict:
    """
    POST /trainer_dialog_engine/v1/start
    body: {"manager_id": "...", "scenario_id": "..."}
    """
    url = BACKEND_URL + "/trainer_dialog_engine/v1/start"
    log("CALL /start", url, manager_id, scenario_id)
    try:
        r = requests.post(
            url,
            json={"manager_id": manager_id, "scenario_id": scenario_id},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log("Ошибка вызова /start:", e)
        return {"error": str(e)}


def api_turn(sid: str, text: str) -> dict:
    """
    POST /trainer_dialog_engine/v1/turn
    body: {"sid": "...", "text": "..."}
    """
    url = BACKEND_URL + "/trainer_dialog_engine/v1/turn"
    log("CALL /turn", url, sid, "text:", text[:50])
    try:
        r = requests.post(
            url,
            json={"sid": sid, "text": text},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log("Ошибка вызова /turn:", e)
        return {"error": str(e)}


def api_stop(sid: str) -> dict:
    """
    POST /trainer_dialog_engine/v1/stop
    body: {"sid": "..."}
    """
    url = BACKEND_URL + "/trainer_dialog_engine/v1/stop"
    log("CALL /stop", url, sid)
    try:
        r = requests.post(
            url,
            json={"sid": sid},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log("Ошибка вызова /stop:", e)
        return {"error": str(e)}


# ===================== ЛОГИКА КОМАНД =====================

def handle_start_command(chat_id: int, session: dict):
    """Обработка /start."""
    session["mode"] = None
    session["sid"] = None
    send_message(
        chat_id,
        "Привет 🌿 Это тренажёр диалога с клиентом.\n\n"
        "Команды:\n"
        "/train или /dialog — запустить тренажёр (клиент + оценки)\n"
        "/stop_dialog — завершить текущую сессию и получить сводку\n"
    )


def handle_dialog_command(chat_id: int, session: dict):
    """Запуск сессии тренажёра (/train или /dialog)."""
    manager_id = str(chat_id)

    data = api_start_session(manager_id)
    if "error" in data:
        send_message(chat_id, "Не получилось запустить сессию тренажёра 😔 Попробуй позже.")
        return

    sid = data.get("sid") or data.get("session_id")
    if not sid:
        send_message(chat_id, "Сервер не вернул sid, обратитесь к разработчику.")
        return

    session["mode"] = "dialog"
    session["sid"] = sid

    send_message(
        chat_id,
        "Запустил тренировку 🎧\n"
        "Представь, что ты сейчас отвечаешь живому клиенту.\n"
        "Пиши свои ответы — я буду играть роль клиента и параллельно оценивать твои сообщения."
    )


def handle_stop_dialog(chat_id: int, session: dict):
    """Завершение сессии и вывод сводки (/stop_dialog)."""
    sid = session.get("sid")
    if not sid:
        send_message(chat_id, "Активной сессии нет. Чтобы запустить тренажёр, напиши /train.")
        return

    data = api_stop(sid)
    if "error" in data:
        send_message(chat_id, "Не получилось получить итог по сессии 😔 Попробуй позже.")
        return

    summary = data.get("summary", {})
    avg_warmth = summary.get("avg_warmth", 0)
    avg_empathy = summary.get("avg_empathy", 0)
    avg_questions = summary.get("avg_questions", 0)
    tips = data.get("tips", [])

    text_lines = [
        "📊 Итоги сессии:",
        f"Теплота: {avg_warmth}/100",
        f"Эмпатия: {avg_empathy}/100",
        f"Вопросы: {avg_questions}/100",
    ]
    if tips:
        text_lines.append("")
        text_lines.append("Рекомендации:")
        for t in tips:
            text_lines.append(f"• {t}")

    send_message(chat_id, "\n".join(text_lines))

    # Отчёт в админ-чат (как CRM), если нужен
    if ADMIN_CHAT_ID and ADMIN_CHAT_ID != "0":
        try:
            admin_msg = (
                f"👤 Менеджер: {chat_id}\n"
                f"SID: {sid}\n\n" +
                "\n".join(text_lines)
            )
            requests.post(
                BASE_URL + "/sendMessage",
                json={"chat_id": int(ADMIN_CHAT_ID), "text": admin_msg},
                timeout=10,
            )
        except Exception as e:
            log("Ошибка отправки отчёта админу:", e)

    # Сброс сессии
    session["mode"] = None
    session["sid"] = None


def handle_dialog_turn(chat_id: int, text: str, session: dict):
    """Один шаг диалога: менеджер пишет — движок отвечает."""
    sid = session.get("sid")
    if not sid:
        send_message(chat_id, "Сессия ещё не запущена. Напиши /train, чтобы начать 🌿")
        return

    data = api_turn(sid, text)

    if "error" in data:
        if data.get("error") == "session_not_found":
            send_message(chat_id, "Сессия не найдена. Напиши /train, чтобы начать новую.")
            session["mode"] = None
            session["sid"] = None
            return
        send_message(chat_id, f"Ошибка при ходе диалога: {data.get('error')}")
        return

    reply = data.get("reply", "Клиент пока молчит, попробуй ещё раз сформулировать ответ 🫶")
    eval_res = data.get("eval", {})
    scores = eval_res.get("scores", {})
    warmth = scores.get("warmth", 0)
    empathy = scores.get("empathy", 0)
    questions = scores.get("questions", 0)
    tips = eval_res.get("tips") or []

    msg = f"🗣 Клиент:\n{reply}\n"

    msg += "\n📊 Оценка твоего ответа:\n"
    msg += f"Теплота: {warmth}/100\n"
    msg += f"Эмпатия: {empathy}/100\n"
    msg += f"Вопросы: {questions}/100\n"

    if tips:
        msg += "\nРекомендации:\n"
        for t in tips:
            msg += f"• {t}\n"

    send_message(chat_id, msg)


# ===================== ОБРАБОТКА ОБНОВЛЕНИЙ TELEGRAM =====================

def handle_update(update: dict):
    """Обработка одного обновления из Telegram."""
    message = update.get("message") or {}
    if not message:
        return

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if chat_id is None:
        return

    text = (message.get("text") or "").strip()
    if not text:
        return

    log("UPDATE from", chat_id, "text:", text)
    session = get_session(chat_id)

    # Команды
    if text == "/start":
        handle_start_command(chat_id, session)
        return

    if text in ("/train", "/dialog"):
        handle_dialog_command(chat_id, session)
        return

    if text == "/stop_dialog":
        handle_stop_dialog(chat_id, session)
        return

    # Если мы в режиме диалога
    if session.get("mode") == "dialog":
        handle_dialog_turn(chat_id, text, session)
    else:
        send_message(
            chat_id,
            "Чтобы запустить тренажёр диалога, напиши:\n"
            "/train — начать\n"
            "/stop_dialog — закончить и получить сводку"
        )


def main():
    print("✅ simple_telegram_bot (dialog engine) запущен. Ожидаю сообщения...")
    offset = None
    while True:
        try:
            resp = requests.get(
                BASE_URL + "/getUpdates",
                params={"timeout": 50, "offset": offset},
                timeout=60,
            )
            data = resp.json()
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                handle_update(upd)
        except Exception as e:
            log("Ошибка в основном цикле:", e)
            time.sleep(3)


if __name__ == "__main__":
    main()

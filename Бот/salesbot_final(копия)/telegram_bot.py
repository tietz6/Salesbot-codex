import os
import json
from typing import Dict, Any

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from core.state.v1 import StateStore
from core.voice_gateway.v1 import VoicePipeline


# Хранилище состояний в SQLite (salesbot.db)
kv = StateStore("salesbot.db")


def load_session(chat_id: int) -> Dict[str, Any]:
    key = f"tg_session:{chat_id}"
    raw = kv.get(key)
    if not raw:
        return {"stage": "new", "data": {}}
    try:
        return json.loads(raw)
    except Exception:
        return {"stage": "new", "data": {}}


def save_session(chat_id: int, session: Dict[str, Any]) -> None:
    key = f"tg_session:{chat_id}"
    kv.set(key, json.dumps(session, ensure_ascii=False))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка /start — сбрасываем состояние и даём приветствие Софии."""
    chat_id = update.effective_chat.id

    session = {"stage": "who", "data": {}}
    save_session(chat_id, session)

    text = (
        "Добрый день! 🥰 Меня зовут София.\n\n"
        "Мы создаём уникальные песни на заказ по вашей истории — "
        "не по шаблону, а по живым чувствам 🌸\n\n"
        "Кому вы хотите подарить песню и отобразить в музыке ваши эмоции? 💫"
    )
    await update.message.reply_text(text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка обычных текстов в зависимости от стадии диалога."""
    if not update.message:
        return

    chat_id = update.effective_chat.id
    user_text = (update.message.text or "").strip()

    # Загружаем сессию
    session = load_session(chat_id)
    stage = session.get("stage", "new")
    data = session.get("data", {})

    # 1) Если по каким-то причинам стадии нет — начнём с вопроса «кому»
    if stage == "new":
        session = {"stage": "who", "data": {}}
        save_session(chat_id, session)
        await update.message.reply_text(
            "Давайте начнём сначала 🥰\n\n"
            "Кому вы хотите подарить песню и к какому событию она будет? 🌸"
        )
        return

    # 2) Этап: кому песня (who)
    if stage == "who":
        data["target_person_raw"] = user_text
        session["stage"] = "story"
        session["data"] = data
        save_session(chat_id, session)

        reply = (
            "💌 Чтобы написать для вас особенную песню, ответьте, пожалуйста, на несколько вопросов:\n\n"
            "1. Как зовут этого человека? 🥰\n"
            "2. Как давно вы вместе или сколько лет знакомы?\n"
            "3. Есть ли дети или особенные близкие, кого важно упомянуть?\n"
            "4. Есть ли трогательные моменты или фразы, которые обязательно хочется включить в песню? 🌸\n\n"
            "Можете написать всё одним сообщением — я аккуратно соберу это в историю 🫶"
        )
        await update.message.reply_text(reply)
        return

    # 3) Этап: сбор истории (story)
    if stage == "story":
        data["story_raw"] = user_text
        session["stage"] = "ready"
        session["data"] = data
        save_session(chat_id, session)

        # Пробуем красиво пересказать историю через DeepSeek
        vp = VoicePipeline()
        system_prompt = (
            "Ты ассистент проекта «На Счастье».\n"
            "Тебе написали историю для персональной песни.\n"
            "Сделай короткий, тёплый пересказ (3–5 предложений) + подчеркни 2–3 ключевые детали, "
            "чтобы клиент почувствовал: «меня услышали».\n"
            "Не продавай, просто отрази эмоции."
        )
        try:
            summary = vp.llm.chat(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ]
            )
        except Exception:
            summary = (
                "Спасибо вам за такую тёплую историю 🥹💛\n"
                "Я всё сохранила и по ней сделаем текст песни."
            )

        reply_1 = summary
        reply_2 = (
            "\n\nДавайте дальше сделаем всё удобно для вас:\n"
            "Я подготовлю 2 варианта текста по вашей истории — чтобы вы смогли выбрать сердцем 🥰\n"
            "Чуть позже отправлю варианты, а пока можно написать, в каком стиле вам ближе песня: "
            "поп, лирика или что-то более романтичное? 🎶"
        )

        await update.message.reply_text(reply_1)
        await update.message.reply_text(reply_2)
        return

    # 4) Этап: ready — история уже собрана, ведём мягкий диалог с опорой на DeepSeek
    if stage == "ready":
        vp = VoicePipeline()
        system_prompt = (
            "Ты тёплый менеджер проекта «На Счастье» по имени София.\n"
            "История для песни уже собрана, сейчас задача — мягко сопровождать клиента:\n"
            "уточнять стиль, язык, исполнителя, комфортно подводить к началу работы и оплате,\n"
            "без давления, с заботой. Отвечай коротко, человечно, 2–5 предложений."
        )
        try:
            answer = vp.llm.chat(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ]
            )
        except Exception:
            answer = (
                "Я с вами 🌿 У нас уже есть ваша история, "
                "осталось только зафиксировать стиль и исполнителя, и мы начнём 🥰"
            )

        await update.message.reply_text(answer)
        return

    # 5) На всякий случай fallback
    session = {"stage": "who", "data": {}}
    save_session(chat_id, session)
    await update.message.reply_text(
        "Давайте начнём сначала 🥰 Кому вы хотите подарить песню? 🌸"
    )


def main() -> None:
    # Берём токен из ENV (как и для telegram_push)
    token = os.environ.get("TG_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("❌ Не найден TG_BOT_TOKEN / TELEGRAM_BOT_TOKEN в переменных окружения.")
        print("ENV-ключи, которые вижу сейчас:")
        for k, v in os.environ.items():
            if "TG" in k.upper() or "TELEGRAM" in k.upper():
                print(f"  {k} = {v}")
        print("Добавь токен бота в ENV или в .bat, Босс 💛")
        return

    app = ApplicationBuilder().token(token).build()

    # /start → handler
    app.add_handler(CommandHandler("start", start))
    # любой текст → handle_text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Telegram-бот «На Счастье» запущен. Жду сообщения…")
    app.run_polling()


if __name__ == "__main__":
    main()
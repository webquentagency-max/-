import asyncio
import httpx
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.enums import ParseMode

# ==========================================
# ВСТАВЬ СЮДА СВОИ ДАННЫЕ
BOT_TOKEN = "8714144868:AAEWW9b4sDLh_YxP7ubyphms2Ah8_9iy60A"        # токен от @BotFather
ADMIN_ID = 7951440179                  # твой Telegram ID
LISTOK_WEBHOOK = "https://ln1503.listokcrm.ru/cron/tildaLead/32e3dc87a3fe459ac28c096fe0241d75"
# ==========================================

app = FastAPI()
bot = Bot(token=BOT_TOKEN)


@app.post("/webhook")
async def tilda_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = dict(await request.form())

    # Достаём поля из формы
    name = data.get("Name") or data.get("name") or "—"
    phone = data.get("Phone") or data.get("phone") or "—"
    email = data.get("Email") or data.get("email") or "—"

    # 1. Пересылаем в Listok CRM
    try:
        async with httpx.AsyncClient() as client:
            await client.post(LISTOK_WEBHOOK, json=data, timeout=10)
    except Exception as e:
        print(f"Listok error: {e}")

    # 2. Шлём уведомление в Telegram
    text = (
        f'<tg-emoji emoji-id="5870633910337015697">✅</tg-emoji> <b>Новая заявка с сайта</b>\n\n'
        f'<tg-emoji emoji-id="5870994129244131212">👤</tg-emoji> <b>Имя:</b> {name}\n'
        f'<tg-emoji emoji-id="5983150113483134607">⏰</tg-emoji> <b>Телефон:</b> {phone}\n'
        f'<tg-emoji emoji-id="5769289093221454192">🔗</tg-emoji> <b>Email:</b> {email}'
    )

    try:
        await bot.send_message(ADMIN_ID, text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"Telegram error: {e}")

    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "running"}

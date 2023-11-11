from fastapi import FastAPI
from loader import dp, bot
from aiogram import types, Dispatcher, Bot
from data.config import BOT_TOKEN
from utils.notify_admins import on_startup_notify, bot_shutdown

app = FastAPI()
WEBHOOK_PATH=f"/{BOT_TOKEN}/"
WEBHOOK_URL="https://mars-bozor-bot.onrender.com"+WEBHOOK_PATH
@app.on_event('startup')
async def on_startup():
    url = await bot.get_webhook_info()
    if url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL  )
        await on_startup_notify(dp=dp)
@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@app.on_event("shutdown")
async def shutdown():
    await bot_shutdown(dp=dp)
    await bot.get_session().close()
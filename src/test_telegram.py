import asyncio
from src.telegram_notifier import send_telegram_message 

async def main():
    await send_telegram_message("✅ Test Telegram message working!")

asyncio.run(main())

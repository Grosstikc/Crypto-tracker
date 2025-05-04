import asyncio
import time
from src.database import SessionLocal, Alert
from src.data_fetcher import fetch_crypto_data_no_cache
from src.telegram_notifier import send_telegram_message

async def check_price_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).filter(Alert.triggered == False).all()

    for alert in alerts:
        current_data = fetch_crypto_data_no_cache([alert.crypto], alert.currency)
        current_price = current_data[alert.crypto][alert.currency]

        condition_met = False
        if alert.direction == "Above" and current_price >= alert.price:
            condition_met = True
        elif alert.direction == "Below" and current_price <= alert.price:
            condition_met = True

        if condition_met:
            # Still clearly uses chat_id (no change!)
            message = f"🔔 Alert: {alert.crypto.capitalize()} is now {current_price:.2f} {alert.currency.upper()}, {alert.direction} your alert of {alert.price:.2f}!"
            await send_telegram_message(message, alert.user_chat_id)
            alert.triggered = True
            db.commit()

    db.close()

async def run_alert_checker(interval=300):
    while True:
        await check_price_alerts()
        time.sleep(interval)

if __name__ == "__main__":
    asyncio.run(run_alert_checker())

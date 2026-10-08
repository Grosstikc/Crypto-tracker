import asyncio

from src.database import SessionLocal, Alert
from src.data_fetcher import fetch_crypto_data_no_cache
from src.telegram_notifier import send_telegram_message


async def check_price_alerts():
    with SessionLocal() as db:
        alerts = (
            db.query(Alert)
            .filter(Alert.triggered == False)
            .all()
        )

        if not alerts:
            print("No active alerts.")
            return

        # Group alerts by currency
        currencies = set(alert.currency for alert in alerts)

        for currency in currencies:

            currency_alerts = [
                alert for alert in alerts
                if alert.currency == currency
            ]

            # Unique cryptocurrencies only
            crypto_ids = list({
                alert.crypto
                for alert in currency_alerts
            })

            try:
                # ONE request for all cryptocurrencies
                current_data = fetch_crypto_data_no_cache(
                    crypto_ids,
                    currency
                )

            except Exception as e:
                print(
                    f"Error fetching prices for {currency}: {e}"
                )
                continue

            for alert in currency_alerts:

                crypto_data = current_data.get(alert.crypto)

                if not crypto_data:
                    print(
                        f"No data received for {alert.crypto}"
                    )
                    continue

                current_price = crypto_data.get(alert.currency)

                if current_price is None:
                    print(
                        f"No price available for {alert.crypto}"
                    )
                    continue

                condition_met = False

                if (
                    alert.direction == "Above"
                    and current_price >= alert.price
                ):
                    condition_met = True

                elif (
                    alert.direction == "Below"
                    and current_price <= alert.price
                ):
                    condition_met = True

                if condition_met:

                    message = (
                        f"🔔 Price Alert!\n\n"
                        f"{alert.crypto.capitalize()}: "
                        f"{current_price:.2f} "
                        f"{alert.currency.upper()}\n"
                        f"Your target: "
                        f"{alert.direction} "
                        f"{alert.price:.2f}"
                    )

                    try:
                        await send_telegram_message(
                            message,
                            alert.user.chat_id
                        )

                        alert.triggered = True
                        db.commit()

                        print(
                            f"Alert {alert.id} triggered "
                            f"for {alert.crypto}"
                        )

                    except Exception as e:
                        print(
                            f"Error sending alert "
                            f"{alert.id}: {e}"
                        )


async def run_alert_checker(interval=300):

    while True:

        try:
            await check_price_alerts()

        except Exception as e:
            print(f"Alert checker error: {e}")

        await asyncio.sleep(interval)


if __name__ == "__main__":
    asyncio.run(run_alert_checker())
    
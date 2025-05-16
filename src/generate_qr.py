import qrcode

bot_url = "https://t.me/Alert_Cryptocurrency_bot"
img = qrcode.make(bot_url)
img.save("telegram_qr.png")
print("✅ QR code saved as 'telegram_qr.png'")

import aiohttp
from aiogram import types
from config import PAYMENT_API_KEY, CARD_NUMBER, MESSAGES

async def create_payment_link(amount):
    # اینجا باید API درگاه پرداخت (مثل زرین‌پال) رو پیاده‌سازی کنی
    async with aiohttp.ClientSession() as session:
        # نمونه کد برای زرین‌پال
        payload = {
            "merchant_id": PAYMENT_API_KEY,
            "amount": amount * 10000,  # تبدیل به ریال
            "description": "شارژ کیف پول",
            "callback_url": "https://yourdomain.com/callback"
        }
        async with session.post("https://api.zarinpal.com/v4/payment/request.json", json=payload) as resp:
            data = await resp.json()
            return f"https://www.zarinpal.com/pg/StartPay/{data['data']['authority']}"

async def verify_payment(authority):
    # تأیید پرداخت (باید با درگاه هماهنگ بشه)
    return True  # موقتاً

async def send_card_payment_instructions(message: types.Message, price, lang):
    await message.answer(
        MESSAGES[lang]['send_payment'].format(price=price, CARD_NUMBER=CARD_NUMBER)
    )
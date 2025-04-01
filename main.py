from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import API_TOKEN
from handlers import register_handlers
from admin import register_admin_handlers

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="شروع ربات")
    ]
    await bot.set_my_commands(commands)

register_handlers(dp)
register_admin_handlers(dp)

if __name__ == "__main__":
    dp.startup.register(set_bot_commands)  # این خط رو اضافه کن
    dp.run_polling(bot)
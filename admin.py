from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS, MESSAGES
from keyboards import get_admin_menu
from database import db
import logging

logging.basicConfig(level=logging.INFO)

class AdminState(StatesGroup):
    waiting_for_broadcast = State()

def register_admin_handlers(dp: Dispatcher):
    @dp.message(lambda message: message.from_user.id in ADMIN_IDS and message.text == "/admin")
    async def cmd_admin(message: types.Message, state: FSMContext):
        lang = db.get_user(message.from_user.id)[2] or 'fa'
        await message.answer(MESSAGES[lang]['admin_menu'], reply_markup=get_admin_menu(lang))

    @dp.callback_query(lambda c: c.data == "admin_stats")
    async def admin_stats(callback: types.CallbackQuery, state: FSMContext):
        lang = db.get_user(callback.from_user.id)[2] or 'fa'
        total_users, pending_orders, completed_orders = db.get_stats()
        stats_text = f"کاربران: {total_users}\nسفارشات در انتظار: {pending_orders}\nسفارشات تکمیل‌شده: {completed_orders}"
        await callback.message.edit_text(stats_text, reply_markup=get_admin_menu(lang))

    @dp.callback_query(lambda c: c.data == "admin_broadcast")
    async def admin_broadcast(callback: types.CallbackQuery, state: FSMContext):
        lang = db.get_user(callback.from_user.id)[2] or 'fa'
        await callback.message.edit_text("پیام خود را برای ارسال همگانی وارد کنید:")
        await state.set_state(AdminState.waiting_for_broadcast)

    @dp.message(AdminState.waiting_for_broadcast)
    async def process_broadcast(message: types.Message, state: FSMContext):
        lang = db.get_user(message.from_user.id)[2] or 'fa'
        cursor = db.conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()
        for user in users:
            try:
                await message.bot.send_message(user[0], message.text)
            except Exception as e:
                logging.error(f"Failed to send message to {user[0]}: {e}")
        await message.answer("پیام همگانی ارسال شد.", reply_markup=get_admin_menu(lang))
        await state.clear()
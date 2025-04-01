from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import MESSAGES, DEFAULT_LANG, CHANNEL_ID
from keyboards import get_language_keyboard, get_main_menu, get_category_keyboard, get_service_keyboard, get_payment_options, get_settings_menu
from database import db
import logging

logging.basicConfig(level=logging.INFO)

class UserState(StatesGroup):
    waiting_for_lang = State()
    waiting_for_category = State()
    waiting_for_service = State()
    waiting_for_payment = State()
    waiting_for_email = State()
    waiting_for_wallet_charge = State()
    waiting_for_settings = State()

async def check_channel_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

def register_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        print("Debug: /start command received")  # دیباگ برای استارت
        if not await check_channel_membership(message.bot, message.from_user.id):
            await message.answer(MESSAGES[DEFAULT_LANG]['join_channel'].format(channel=CHANNEL_ID))
            return
        db.add_user(message.from_user.id, message.from_user.full_name)
        await state.set_state(UserState.waiting_for_lang)
        await message.answer(MESSAGES[DEFAULT_LANG]['start'], reply_markup=get_language_keyboard())

    @dp.callback_query(lambda c: c.data.startswith("lang_"))
    async def process_language(callback: types.CallbackQuery, state: FSMContext):
        print(f"Debug: Language selected - {callback.data}")  # دیباگ برای انتخاب زبان
        lang = callback.data.split("_")[1]
        await state.update_data(lang=lang)
        db.update_lang(callback.from_user.id, lang)
        await callback.message.edit_text(MESSAGES[lang]['lang_changed'].format(lang=lang), reply_markup=get_main_menu(lang))
        await state.clear()

    @dp.callback_query(lambda c: c.data == "buy")
    async def process_buy(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Buy button pressed")  # دیباگ برای خرید
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['choose_category'], reply_markup=get_category_keyboard(lang))
        await state.set_state(UserState.waiting_for_category)

    @dp.callback_query(lambda c: c.data.startswith("cat_"))
    async def process_category(callback: types.CallbackQuery, state: FSMContext):
        print(f"Debug: Category selected - {callback.data}")  # دیباگ برای دسته‌بندی
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        category = callback.data.split("_")[1]
        await state.update_data(category=category)
        await callback.message.edit_text(MESSAGES[lang]['choose_service'], reply_markup=get_service_keyboard(lang, category))
        await state.set_state(UserState.waiting_for_service)

    @dp.callback_query(lambda c: c.data.startswith("service_"))
    async def process_service(callback: types.CallbackQuery, state: FSMContext):
        print(f"Debug: Service selected - {callback.data}")  # دیباگ برای سرویس
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        product_id = int(callback.data.split("_")[1])
        product = next(p for p in db.get_products_by_category(data["category"], lang) if p[0] == product_id)
        await state.update_data(product_id=product_id, price=product[2])
        await callback.message.edit_text(
            MESSAGES[lang]['service_details'].format(service=product[1], price=product[2], duration=product[3]),
            reply_markup=get_payment_options(lang, product[2])
        )
        await state.set_state(UserState.waiting_for_payment)

    @dp.callback_query(lambda c: c.data == "pay_card")
    async def process_pay_card(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Pay with card selected")  # دیباگ برای پرداخت با کارت
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        price = data["price"]
        await callback.message.edit_text(MESSAGES[lang]['send_payment'].format(price=price, CARD_NUMBER=CARD_NUMBER))
        await state.set_state(UserState.waiting_for_email)

    @dp.message(UserState.waiting_for_email)
    async def process_email(message: types.Message, state: FSMContext):
        print("Debug: Email entered")  # دیباگ برای ورود ایمیل
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        db.add_order(message.from_user.id, data["product_id"], message.text)
        await message.answer(MESSAGES[lang]['thank_you'], reply_markup=get_main_menu(lang))
        await state.clear()

    @dp.callback_query(lambda c: c.data == "wallet")
    async def show_wallet(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Wallet button pressed")  # دیباگ برای کیف پول
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        user = db.get_user(callback.from_user.id)
        builder = InlineKeyboardBuilder()
        builder.button(text="شارژ کیف پول" if lang == 'fa' else "Charge Wallet", callback_data="charge_wallet")
        builder.button(text="🏠 خانه" if lang == 'fa' else "Home", callback_data="home")
        builder.button(text=MESSAGES[lang]['back'], callback_data="back")
        await callback.message.edit_text(MESSAGES[lang]['wallet'].format(balance=user[3]), reply_markup=builder.as_markup())

    @dp.callback_query(lambda c: c.data == "charge_wallet")
    async def charge_wallet(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Charge wallet button pressed")  # دیباگ برای شارژ کیف پول
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['charge_wallet'])
        await state.set_state(UserState.waiting_for_wallet_charge)

    @dp.message(UserState.waiting_for_wallet_charge)
    async def process_wallet_charge(message: types.Message, state: FSMContext):
        print("Debug: Wallet charge amount entered")  # دیباگ برای مقدار شارژ
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        try:
            amount = float(message.text)
            db.update_wallet(message.from_user.id, amount)
            await message.answer(MESSAGES[lang]['wallet'].format(balance=db.get_user(message.from_user.id)[3]), reply_markup=get_main_menu(lang))
            await state.clear()
        except ValueError:
            await message.answer(MESSAGES[lang]['invalid'])

    @dp.callback_query(lambda c: c.data == "settings")
    async def process_settings(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Settings button pressed")  # دیباگ برای تنظیمات
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['settings'].format(lang=lang), reply_markup=get_settings_menu(lang))
        await state.set_state(UserState.waiting_for_settings)

    @dp.callback_query(lambda c: c.data == "change_lang")
    async def process_change_lang(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Change language button pressed")  # دیباگ برای تغییر زبان
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['start'], reply_markup=get_language_keyboard())
        await state.set_state(UserState.waiting_for_lang)

    @dp.callback_query(lambda c: c.data == "support")
    async def process_support(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Support button pressed")  # دیباگ برای پشتیبانی
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['support'], reply_markup=get_main_menu(lang))

    @dp.callback_query(lambda c: c.data == "about")
    async def process_about(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: About button pressed")  # دیباگ برای درباره ما
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['about'], reply_markup=get_main_menu(lang))

    @dp.callback_query(lambda c: c.data == "home")
    async def process_home(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Home button pressed")  # دیباگ برای خانه
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        await callback.message.edit_text(MESSAGES[lang]['lang_changed'].format(lang=lang), reply_markup=get_main_menu(lang))
        await state.clear()

    @dp.callback_query(lambda c: c.data == "back")
    async def process_back(callback: types.CallbackQuery, state: FSMContext):
        print("Debug: Back button pressed")  # دیباگ برای برگشت
        current_state = await state.get_state()
        data = await state.get_data()
        lang = data.get("lang", DEFAULT_LANG)
        if current_state == UserState.waiting_for_category.state:
            await callback.message.edit_text(MESSAGES[lang]['lang_changed'].format(lang=lang), reply_markup=get_main_menu(lang))
            await state.clear()
        elif current_state == UserState.waiting_for_service.state:
            await callback.message.edit_text(MESSAGES[lang]['choose_category'], reply_markup=get_category_keyboard(lang))
            await state.set_state(UserState.waiting_for_category)
        elif current_state == UserState.waiting_for_payment.state:
            product_id = data.get("product_id")
            category = data.get("category")
            product = next(p for p in db.get_products_by_category(category, lang) if p[0] == product_id)
            await callback.message.edit_text(
                MESSAGES[lang]['service_details'].format(service=product[1], price=product[2], duration=product[3]),
                reply_markup=get_service_keyboard(lang, category)
            )
            await state.set_state(UserState.waiting_for_service)
        elif current_state == UserState.waiting_for_settings.state:
            await callback.message.edit_text(MESSAGES[lang]['lang_changed'].format(lang=lang), reply_markup=get_main_menu(lang))
            await state.clear()
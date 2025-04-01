from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import MESSAGES, CATEGORIES, LANGUAGES
from database import db

def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    for code, name in LANGUAGES.items():
        builder.button(text=name, callback_data=f"lang_{code}")
    builder.adjust(2)
    return builder.as_markup()

def get_main_menu(lang):
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 خرید" if lang == 'fa' else "Buy", callback_data="buy")
    builder.button(text="💰 کیف پول" if lang == 'fa' else "Wallet", callback_data="wallet")
    builder.button(text="⚙️ تنظیمات" if lang == 'fa' else "Settings", callback_data="settings")
    builder.button(text="📞 پشتیبانی" if lang == 'fa' else "Support", callback_data="support")
    builder.button(text="ℹ️ درباره ما" if lang == 'fa' else "About", callback_data="about")
    builder.adjust(2)
    return builder.as_markup()

def get_category_keyboard(lang):
    builder = InlineKeyboardBuilder()
    categories = db.get_categories(lang)
    for cat in categories:
        builder.button(text=cat, callback_data=f"cat_{cat}")
    builder.button(text="🏠 خانه" if lang == 'fa' else "Home", callback_data="home")
    builder.button(text=MESSAGES[lang]['back'], callback_data="back")
    builder.adjust(2)
    return builder.as_markup()

def get_service_keyboard(lang, category):
    builder = InlineKeyboardBuilder()
    products = db.get_products_by_category(category, lang)
    for product in products:
        builder.button(text=f"{product[1]} - {product[2]}$", callback_data=f"service_{product[0]}")
    builder.button(text="🏠 خانه" if lang == 'fa' else "Home", callback_data="home")
    builder.button(text=MESSAGES[lang]['back'], callback_data="back")
    builder.adjust(2)
    return builder.as_markup()

def get_payment_options(lang, price):
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 پرداخت با کارت" if lang == 'fa' else "Pay with Card", callback_data="pay_card")
    builder.button(text="💰 پرداخت با کیف پول" if lang == 'fa' else "Pay with Wallet", callback_data="pay_wallet")
    builder.button(text="🌐 پرداخت آنلاین" if lang == 'fa' else "Pay Online", callback_data="pay_online")
    builder.button(text="🏠 خانه" if lang == 'fa' else "Home", callback_data="home")
    builder.button(text=MESSAGES[lang]['back'], callback_data="back")
    builder.adjust(2)
    return builder.as_markup()

def get_admin_menu(lang):
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ افزودن محصول" if lang == 'fa' else "Add Product", callback_data="admin_add_product")
    builder.button(text="📢 پیام همگانی" if lang == 'fa' else "Broadcast", callback_data="admin_broadcast")
    builder.button(text="📊 آمار" if lang == 'fa' else "Stats", callback_data="admin_stats")
    builder.button(text="🏠 خانه" if lang == 'fa' else "Home", callback_data="home")
    builder.adjust(2)
    return builder.as_markup()

def get_settings_menu(lang):
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 تغییر زبان" if lang == 'fa' else "Change Language", callback_data="change_lang")
    builder.button(text="🏠 خانه" if lang == 'fa' else "Home", callback_data="home")
    builder.button(text=MESSAGES[lang]['back'], callback_data="back")
    builder.adjust(2)
    return builder.as_markup()
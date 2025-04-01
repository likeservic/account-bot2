## 🤖 Telegram Multi-language Account Seller Bot | ربات فروش چندزبانه تلگرام

### 🇬🇧 English Description:

This Telegram bot allows users to purchase various digital accounts and licenses (e.g., Spotify, Netflix, Grammarly, Windows, Duolingo, ChatGPT, etc.) in 6 languages: **English, Persian, Arabic, Turkish, French, and Ukrainian**.

#### 🚀 Features:

- Multilingual interface with automatic and manual language switching
- Organized categories and services (e.g., Music, Streaming, Education, VPN, Utilities)
- Dynamic keyboards and step-by-step purchase process
- Manual card payment system and wallet support
- Admin receives detailed order via Telegram
- AI-powered support assistant: Ask Grok! 🧠
- SQLite database integration

#### 🛠️ Tech Stack:

- Python 3 + Aiogram
- FSM (Finite State Machine) for step-by-step user guidance
- SQLite for data storage
- Easy to extend and customize

---

### 🇫🇷 Description Française :

Ce bot Telegram permet aux utilisateurs d'acheter divers comptes et licences numériques (par exemple Spotify, Netflix, Grammarly, Windows, Duolingo, ChatGPT, etc.) dans **6 langues : anglais, persan, arabe, turc, français et ukrainien**.

#### 🚀 Fonctionnalités :

- Interface multilingue avec détection automatique et changement manuel
- Catégories et services organisés (musique, streaming, éducation, VPN, utilitaires)
- Claviers dynamiques et processus d'achat étape par étape
- Paiement manuel via carte bancaire et portefeuille intégré
- L'administrateur reçoit chaque commande avec tous les détails
- Assistant IA intégré : posez vos questions à Grok ! 🧠
- Intégration avec base de données SQLite

#### 🛠️ Technologies :

- Python 3 + Aiogram
- FSM (machine à états finis) pour la gestion des étapes utilisateur
- Base de données SQLite
- Personnalisable et évolutif

---

### 🧪 How to Run / نحوه اجرا:

```bash
pip install -r requirements.txt
python main.py
```

---

### ⚙️ Configuration with `.env` file / پیکربندی با فایل `.env`:

Instead of editing a `config.py`, you can safely store your sensitive information in a `.env` file. Create a `.env` file in the root directory with the following content:

```env
API_TOKEN=your_telegram_bot_token
ADMIN_ID=123456789
CARD_NUMBER=1234-5678-9012-3456
PAYMENT_API_KEY=your_payment_gateway_key
CHANNEL_ID=@your_channel_username
```

🔐 Make sure you add `.env` to your `.gitignore` file if you're pushing this project to GitHub.

📦 Install `python-dotenv` if not already installed:
```bash
pip install python-dotenv
```

Then in your `config.py` or at the top of `main.py`, add:
```python
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CARD_NUMBER = os.getenv("CARD_NUMBER")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
```

---

### 📂 Project Structure / ساختار پروژه:

```
- main.py                # Main bot runner
- handlers.py           # User interaction handlers
- admin.py              # Admin-specific commands
- keyboards.py          # All inline keyboards
- database.py           # SQLite connection and functions
- payments.py           # Payment logic and API
- config.py             # Loads from .env
- .env                  # Your private credentials
- README.md             # This file
```

---

### 📌 To-Do / کارهای آینده:

- Add more payment gateways (Zarinpal, Crypto, etc.)
- Admin web panel or Telegram-based dashboard
- Product management via bot
- Hosting and deployment script

---

### 📬 Contact:

For questions, contact the developer via Telegram: [@kaavooshir](https://t.me/kaavooshir)

---

🛡️ Created with ❤️ using **Python** by [Morteza Delavar]

---

🎯 انجام پروژه‌های برنامه‌نویسی، طراحی ربات، طراحی سایت و سایر خدمات نرم‌افزاری پذیرفته می‌شود.

💸 اگر مایل به حمایت مالی هستید، می‌توانید از طریق کیف پول رمزارز TRC20 زیر دونیت کنید (اختیاری):

```
TXWuKRkG6NtcmSD5DEZDb2JTkwHkqxhNK1
```

🙏 با تشکر از حمایت شما ❤️

---

💸 If you wish to support this project, donations are welcome via **TRC20 wallet** (optional):

```
TXWuKRkG6NtcmSD5DEZDb2JTkwHkqxhNK1
```

Thanks for your support! ❤️

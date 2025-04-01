import sqlite3
from config import CATEGORIES, DATABASE_PATH

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.create_tables()
        self.populate_products()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                lang TEXT DEFAULT 'fa',
                wallet REAL DEFAULT 0.0
            )
        ''')
        # اضافه کردن ستون full_name اگه وجود نداره
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
        except sqlite3.OperationalError:  # اگه ستون از قبل باشه، خطا رو نادیده بگیر
            pass
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name TEXT,
                price REAL,
                duration TEXT,
                lang TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                email TEXT,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, full_name):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
        self.conn.commit()

    def update_lang(self, user_id, lang):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
        self.conn.commit()

    def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

    def update_wallet(self, user_id, amount):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET wallet = wallet + ? WHERE user_id = ?", (amount, user_id))
        self.conn.commit()

    def get_products_by_category(self, category, lang):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE category = ? AND lang = ?", (category, lang))
        return cursor.fetchall()

    def add_order(self, user_id, product_id, email):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, product_id, email) VALUES (?, ?, ?)", (user_id, product_id, email))
        self.conn.commit()

    def populate_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            for lang, categories in CATEGORIES.items():
                for category, products in categories.items():
                    for name, details in products.items():
                        price = float(details['price'].replace('$', ''))
                        duration = details['duration']
                        cursor.execute(
                            "INSERT INTO products (category, name, price, duration, lang) VALUES (?, ?, ?, ?, ?)",
                            (category, name, price, duration, lang)
                        )
            self.conn.commit()
            print("Debug: Products added to database")

    def close(self):
        self.conn.close()

db = Database()
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, chat_id: int):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        phone_number TEXT,
        chat_id INTEGER,
        login TEXT,
        password TEXT
        )
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{chat_id}' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        product_price INTEGER
        username TEXT,
        status TEXT,
        photo TEXT,
        dascription TEXT,
        chat_id INTEGER,
        username TEXT,
        datee TEXT,
        in_not_in TEXT
        )
        """)


        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        product_price INTEGER,
        product_photo TEXT,
        about_product TEXT,
        username TEXT,
        product_date TEXT,
        likes INTEGER,
        status TEXT,
        chat_id INTEGER,
        in_not_in TEXT
        )
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS bozor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        price INTEGER,
        username TEXT,
        about TEXT,
        product_date TEXT,
        status TEXT,
        photo TEXT,
        chat_id TEXT,
        likes INTEGER
        )
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS liked_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        chat_id INTEGER
        )
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{chat_id}history_buys'(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        product_description TEXT,
        product_price INTEGER,
        product_date TEXT,
        product_photo TEXT,
        product_from TEXT
        ) 
        """)

        self.conn.commit()



    def get_user_data(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE chat_id={chat_id}").fetchone()

    def insert_database(self, full_name: str, phone_number: str, chat_id: int, login: str, password: str):
        self.cursor.execute(f"""
INSERT INTO users (full_name, phone_number, chat_id, login, password) VALUES (?,?,?,?,?)
""", (full_name, phone_number, chat_id, login, password))
        self.conn.commit()

    def insert_product(self, chat_id, data: dict):
        product_name = data["name"]
        price = data["price"]
        photo = data["photo"]
        about = data["about"]
        date = data["date"]
        username = data["username"]
        likes = 0
        status = "Mavjud"
        notin = "Bozorda_Emas"
        self.cursor.execute("""
        INSERT INTO products (product_name, product_price, product_photo, about_product, username, product_date, likes, status, chat_id, in_not_in) VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (product_name, price, photo, about, username, date, likes, status, chat_id, notin))

        self.cursor.execute(f"""
        INSERT INTO '{chat_id}' (product_name, product_price, status, photo, dascription, chat_id, username, datee, in_not_in) VALUES (?,?,?,?,?,?,?,?,?)
        """, (product_name, price, status, photo, about, chat_id, username, date, notin))
        self.conn.commit()

    def my_productss(self, chat_id: int):
        return self.cursor.execute(f"""
        SELECT * FROM '{chat_id}'
        """).fetchall()

    def insert_bozor(self, mahsulot, chat_id):
        name = mahsulot[1]
        price = mahsulot[2]
        des = mahsulot[5]
        photo = mahsulot[4]
        username = mahsulot[7]
        date = mahsulot[8]
        likes = 0
        status = "Mavjud"
        self.cursor.execute(f"""
        INSERT INTO bozor (full_name, price, username, about, product_date, status, photo, chat_id, likes) VALUES (?,?,?,?,?,?,?,?,?)
        """, (name, price, username, des, date, status, photo, chat_id, likes))
        self.cursor.execute(f"""
        UPDATE '{chat_id}' SET in_not_in='Bozorda' WHERE product_name='{name}'
        """)
        self.cursor.execute(f"""
        UPDATE products SET in_not_in='Bozorda' WHERE product_name='{name}'
        """)
        self.conn.commit()

    def like_update(self, data: dict):
        likes = self.cursor.execute(f"SELECT likes FROM bozor WHERE full_name='{data['full_name']}'").fetchone()
        self.cursor.execute(f"UPDATE bozor SET likes={likes[0] + 1} WHERE full_name='{data['full_name']}'")
        self.conn.commit()

    def insert_likes(self, data: dict, chat_id):
        self.cursor.execute(f"INSERT INTO liked_products (product_name, chat_id) VALUES (?,?)",(data["full_name"], chat_id))

    def like_or_not(self, chat_id, data):
        return self.cursor.execute(f"SELECT * FROM liked_products WHERE chat_id={chat_id} AND product_name='{data['full_name']}'").fetchall()

    def insert_history(self, product_name, username, date, price, chat_id, des, photo):
        self.cursor.execute(f"""
        INSERT INTO '{chat_id}history_buys' (product_name, product_description, product_price, product_date, product_photo, product_from) VALUES (?,?,?,?,?,?)
        """, (product_name, des, price, date, photo, username))
        self.cursor.execute(f"UPDATE bozor SET status='Mavjud Emas' WHERE full_name='{product_name}'")
        self.conn.commit()

    def search_product(self, message):
        try:
            product = self.cursor.execute(f"SELECT * FROM  bozor WHERE full_name LIKE '%{message}%'")
            return product
            return True
        except Exception as exc:
            print(exc)
            return False

    def delate_product(self, chat_id, id):
        self.cursor.execute(f"DELETE FROM '{chat_id}' WHERE id={id}")
        self.conn.commit()

    def setting_pr(self, id, name):
        self.cursor.execute(f"UPDATE products SET product_name='{name}' WHERE id={id}")
        self.conn.commit()

    def setting_price(self, id, price):
        self.cursor.execute(f"UPDATE products SET product_price={int(price)} WHERE id={id}")
        self.conn.commit()

    def set_desc(self, id, desc):
        self.cursor.execute(f"UPDATE products SET about_product='{desc}' WHERE id={id}")
        self.conn.commit()

    def set_photo(self, id, photo):
        self.cursor.execute(f"UPDATE products SET product_photo='{photo}' WHERE id={id}")
        self.conn.commit()

    def delete_bozor(self, username, mah):
        productt = self.cursor.execute(f"SELECT * FROM products WHERE product_name='{mah}' AND username='{username}'").fetchone()
        self.cursor.execute(f"DELETE FROM bozor WHERE full_name='{productt[1]}' AND username='{productt[5]}'")
        self.cursor.execute(f"UPDATE products SET in_not_in='Bozorda Emas' WHERE product_name   ='{productt[1]}' AND username='{productt[5]}'")
        self.conn.commit()
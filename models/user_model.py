import sqlite3
import hashlib

class UserModel:
    def __init__(self):
        self.db_path = "db/pg_management.db"

    def create_user(self, name, email, phone, address, password):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            password_hashed = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                '''
                INSERT INTO users (name, email, phone, address, password_hashed)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (name, email, phone, address, password_hashed)
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def authenticate_user(self, email, password):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        password_hashed = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute(
            '''
            SELECT id, email FROM users
            WHERE email = ? AND password_hashed = ?
            ''',
            (email, password_hashed)
        )
        user = cursor.fetchone()
        connection.close()

        if user:
            if email == "admin@pg.com":
                return "admin"
            return "guest"
        return None

    def get_all_guests(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute(
                '''
                SELECT id, name, email, phone, address
                FROM users
                WHERE email != "admin@pg.com"
                '''
            )

            guests = cursor.fetchall()
            return guests
        except sqlite3.Error as e:
            print("Database Error:", e)
            return []
        finally:
            connection.close()

    def get_user_details(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT name, email, phone, address
            FROM users
            WHERE id = ?
            ''',
            (user_id,)
        )
        user = cursor.fetchone()
        connection.close()
        return user
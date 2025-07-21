import sqlite3
from app.core.config import settings
from app.core.security import get_hashed_password
from app.schemas.user import UserDataForm


class Users:
    def __init__(self, db_path=settings.DATABASE_URL):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username STRING NOT NULL UNIQUE,
                hashed_password STRING NOT NULL
            )
        ''')

    def add_user(self, username: str, password: str):
        user = self.cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND hashed_password = ?
        ''', (username, get_hashed_password(password))).fetchone()

        if not user:
            self.cursor.execute('''
                INSERT INTO users(username, hashed_password)
                VALUES (?, ?)
            ''', (username, get_hashed_password(password)))
            self.conn.commit()

    def get_user(self, username: str):
        user = self.cursor.execute('''
            SELECT * FROM users
            WHERE username = ?
        ''', (username,)).fetchone()
        return {'username': user[1], 'hashed_password': user[2]}


users = Users()
users.create_tables()

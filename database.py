import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name=os.getenv('DATABASE_NAME', 'bot_data.db')):  # Corrigido: __init__
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        try:
            # Economia
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS economia (
                    user_id INTEGER PRIMARY KEY,
                    saldo INTEGER DEFAULT 100
                )
            ''')

            # XP
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS xp (
                    user_id INTEGER PRIMARY KEY,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1
                )
            ''')

            # Tickets
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    channel_id INTEGER,
                    status TEXT DEFAULT 'aberto'
                )
            ''')

            # Warns
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS warns (
                    user_id INTEGER,
                    moderator_id INTEGER,
                    reason TEXT,
                    timestamp INTEGER
                )
            ''')

            self.conn.commit()
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except Exception as e:
            logger.error(f"Erro na query: {query} | Params: {params} | Erro: {e}")
            return None

    # Métodos para economia
    def get_saldo(self, user_id):
        result = self.execute_query(
            'SELECT saldo FROM economia WHERE user_id = ?',
            (user_id,)
        ).fetchone()
        return result[0] if result else 100

    def update_saldo(self, user_id, quantidade):
        current = self.get_saldo(user_id)
        new_saldo = current + quantidade
        
        if current == 100:
            self.execute_query(
                'INSERT INTO economia (user_id, saldo) VALUES (?, ?)',
                (user_id, new_saldo)
            )
        else:
            self.execute_query(
                'UPDATE economia SET saldo = ? WHERE user_id = ?',
                (new_saldo, user_id)
            )
        return new_saldo
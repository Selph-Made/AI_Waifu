# /database.py

import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = Path("data/chat_data.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_tables()

    def _init_tables(self):
        cursor = self.conn.cursor()
        
        # Chatbot Profiles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chatbot_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User Profiles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat Sessions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT UNIQUE NOT NULL,
                chatbot_profile_id INTEGER NOT NULL,
                user_profile_id INTEGER NOT NULL,
                messages TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(chatbot_profile_id) REFERENCES chatbot_profiles(id),
                FOREIGN KEY(user_profile_id) REFERENCES user_profiles(id)
            )
        ''')
        
        self.conn.commit()

    def get_profiles(self, entity_type):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            SELECT name, data 
            FROM {entity_type}_profiles 
            ORDER BY updated_at DESC
        ''')
        return {row[0]: json.loads(row[1]) for row in cursor.fetchall()}

    def save_profile(self, entity_type, name, data):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            INSERT INTO {entity_type}_profiles (name, data, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(name) DO UPDATE SET
                data = excluded.data,
                updated_at = CURRENT_TIMESTAMP
        ''', (name, json.dumps(data)))
        self.conn.commit()

    def delete_profile(self, entity_type, name):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            DELETE FROM {entity_type}_profiles 
            WHERE name = ?
        ''', (name,))
        self.conn.commit()

    def save_chat_session(self, session_name, chatbot_profile, user_profile, messages):
        cursor = self.conn.cursor()
        
        # Get profile IDs
        cursor.execute('''
            SELECT id FROM chatbot_profiles WHERE name = ?
        ''', (chatbot_profile,))
        chatbot_id = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT id FROM user_profiles WHERE name = ?
        ''', (user_profile,))
        user_id = cursor.fetchone()[0]
        
        # Save session
        cursor.execute('''
            INSERT INTO chat_sessions 
            (session_name, chatbot_profile_id, user_profile_id, messages, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(session_name) DO UPDATE SET
                messages = excluded.messages,
                updated_at = CURRENT_TIMESTAMP
        ''', (session_name, chatbot_id, user_id, json.dumps(messages)))
        
        self.conn.commit()

    def load_chat_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                cs.id,
                cs.session_name,
                cp.name AS chatbot_profile,
                up.name AS user_profile,
                cs.created_at,
                cs.updated_at
            FROM chat_sessions cs
            JOIN chatbot_profiles cp ON cs.chatbot_profile_id = cp.id
            JOIN user_profiles up ON cs.user_profile_id = up.id
            ORDER BY cs.updated_at DESC
        ''')
        return cursor.fetchall()

    def load_chat_messages(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT messages FROM chat_sessions WHERE id = ?
        ''', (session_id,))
        result = cursor.fetchone()
        return json.loads(result[0]) if result else []

    def close(self):
        self.conn.close()


import sqlite3
import re
import os

class BotKVManager:
    @staticmethod
    def import_from_original_file(db_path, original_file_path):
        """
        Автоматически читает исходный файл и вставляет данные в БД
        """
        if not os.path.exists(original_file_path):
            print(f"❌ Файл не найден: {original_file_path}")
            return False
        
        with open(original_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Парсим INSERT
        match = re.search(
            r"VALUES\s*\(\s*'((?:[^']|'')*)'\s*,\s*(\d+)\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*(\w+)\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*\)",
            content,
            re.DOTALL
        )
        
        if not match:
            print("❌ Ошибка парсинга")
            return False
        
        data = {
            'users': match.group(1),
            'downloads': match.group(2),
            'bans': match.group(3),
            'strikes': match.group(4).replace(":''з", ":'з"),
            'users_map': match.group(5).replace(":''з", ":'з"),
            'log_seq_map': match.group(6),
            'bootstrap_done': 'true' if match.group(7).lower() == 'true' else 'false',
            'first_seen': match.group(8),
            'last_seen': match.group(9),
            'stats': match.group(10),
            'user_stats': match.group(11),
            'user_stats_period': match.group(12)
        }
        
        # Подключаемся к БД
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаём таблицу если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_kv (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Вставляем данные
        for key, value in data.items():
            cursor.execute('INSERT OR REPLACE INTO bot_kv (key, value) VALUES (?, ?)', (key, value))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Данные импортированы в {db_path}")
        print(f"📊 Ключи: {', '.join(data.keys())}")
        return True

"""
Модуль для работы с базой данных медицинской платформы.
Используется SQLite — лёгкая встроенная база данных.
"""

import sqlite3
import os
from datetime import datetime

# Путь к файлу базы данных
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "medical.db")


def get_db():
    """Подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # чтобы обращаться к полям по имени
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Создание таблиц при первом запуске"""
    conn = get_db()
    cursor = conn.cursor()

    # Таблица 1: Персональные данные (защищённая информация)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal_data (
            patient_code TEXT PRIMARY KEY,      -- код пациента, например PAT-00123
            full_name TEXT NOT NULL,             -- ФИО
            phone TEXT NOT NULL,                 -- телефон
            birth_date TEXT NOT NULL,            -- дата рождения (ДД.ММ.ГГГГ)
            created_at TEXT NOT NULL             -- дата создания карты
        )
    """)

    # Таблица 2: Медкарта (только медицинские данные, без ФИО)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- номер записи (автоматически)
            patient_code TEXT NOT NULL,             -- код пациента (связь с первой таблицей)
            complaints TEXT DEFAULT '',             -- жалобы
            anamnesis TEXT DEFAULT '',              -- анамнез
            objective_exam TEXT DEFAULT '',         -- объективный осмотр
            diagnosis TEXT DEFAULT '',              -- диагноз (по МКБ)
            treatment_plan TEXT DEFAULT '',         -- план лечения
            treatment_done TEXT DEFAULT '',         -- выполненное лечение
            recommendations TEXT DEFAULT '',        -- рекомендации
            visit_date TEXT NOT NULL,               -- дата приёма
            FOREIGN KEY (patient_code) REFERENCES personal_data(patient_code)
        )
    """)

    conn.commit()
    conn.close()


def generate_patient_code():
    """Автоматическая генерация кода пациента (PAT-001, PAT-002 и т.д.)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT patient_code FROM personal_data ORDER BY patient_code DESC LIMIT 1")
    last = cursor.fetchone()
    conn.close()
    if last is None:
        return "PAT-001"
    # Извлекаем номер из последнего кода, например PAT-042 -> 42
    last_num = int(last["patient_code"].split("-")[1])
    return f"PAT-{last_num + 1:03d}"


# При запуске этого файла — инициализируем базу
if __name__ == "__main__":
    init_db()
    print(f"✅ База данных создана: {DB_PATH}")
    print(f"📁 Таблицы: personal_data, medical_record")

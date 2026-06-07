"""
Модуль для работы с VseGPT API (https://api.vsegpt.ru/v1).
Используется для умного автозаполнения карты пациента.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Загружаем API-ключ из файла .env
load_dotenv()

API_KEY = os.getenv("VSEGPT_API_KEY")
API_URL = "https://api.vsegpt.ru/v1/chat/completions"


def ask_vsegpt(system_prompt: str, user_message: str, model: str = "deepseek/deepseek-chat") -> str:
    """
    Отправляет запрос к VseGPT API и возвращает ответ.
    
    Параметры:
        system_prompt — инструкция для ИИ (системный промпт)
        user_message — сообщение пользователя
        model — модель (по умолчанию deepseek/deepseek-chat)
    """
    if not API_KEY:
        return "❌ Ошибка: не найден API-ключ VseGPT. Проверьте файл .env"

    # Формируем правильный JSON-запрос
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,  # низкая температура — более точные ответы
        "max_tokens": 2000
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        
        # Проверяем статус ответа
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ Ошибка API (код {response.status_code}): {response.text}"
    
    except Exception as e:
        return f"❌ Ошибка соединения: {str(e)}"


# ─── ТЕСТОВЫЙ ЗАПУСК ────────────────────────────────────
if __name__ == "__main__":
    print("🔍 Тестируем подключение к VseGPT API...")
    print(f"   Модель: deepseek/deepseek-chat")
    print(f"   Адрес: {API_URL}")
    print()
    
    # Простой тестовый запрос
    ответ = ask_vsegpt(
        system_prompt="Ты — полезный ассистент. Отвечай кратко и по делу.",
        user_message="Напиши 'Привет! API работает!' если ты меня слышишь."
    )
    
    print(f"📩 Ответ от VseGPT:")
    print(f"   {ответ}")

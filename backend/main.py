import string
import random
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import os
from datetime import datetime

# Инициализация базы данных при запуске
from backend.database import init_db, get_db, generate_key
init_db()

# Функция для генерации кода пациента
def generate_patient_code():
    """Генерирует уникальный код пациента"""
    letters = string.ascii_uppercase
    digits = string.digits
    # Формат: 2 буквы + 4 цифры, например: AB1234
    code = ''.join(random.choices(letters, k=2)) + ''.join(random.choices(digits, k=4))
    return code

app = FastAPI(title="Medical Platform API")

# Путь к frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# ─── СТРАНИЦЫ ───────────────────────────────────────────

@app.get("/")
async def root():
    """Главная страница"""
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Medical Platform</h1><p>Server is running</p>")

@app.post("/api/patients/login")
async def api_patient_login(request: Request):
    """Авторизация пациента"""
    data = await request.json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM personal_data WHERE phone = ? AND patient_code = ?", (data["phone"], data["patient_code"]))
    patient = cursor.fetchone()
    
    if patient:
        return {"success": True, "message": "Успешный вход"}
    else:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Неверные данные"}
        )

@app.post("/api/doctors/login")
async def api_doctor_login(request: Request):
    """Авторизация врача"""
    data = await request.json()
    conn = get_db()
    cursor = conn.cursor()
    
    print(f"Doctor login attempt: {data['username']}")
    
    cursor.execute("SELECT * FROM doctors WHERE username = ? AND password = ?", (data["username"], data["password"]))
    doctor = cursor.fetchone()
    
    if doctor:
        return {"success": True, "message": "Успешный вход"}
    else:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Неверные данные"}
        )

@app.get("/doctor-cabinet")
async def doctor_cabinet():
    """Кабинет врача — карта пациента"""
    return FileResponse(os.path.join(frontend_path, "doctor-cabinet.html"))


# ─── API ДЛЯ РАБОТЫ С ПАЦИЕНТАМИ ────────────────────────

@app.get("/api/generate-code")
async def api_generate_code():
    """Получить новый код пациента"""
    code = generate_patient_code()
    return {"patient_code": code}


@app.post("/api/patients/create")
async def api_create_patient(request: Request):
    """Создать нового пациента (персональные данные)"""
    data = await request.json()
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO personal_data (patient_code, full_name, phone, birth_date, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["patient_code"],
            data["full_name"],
            data["phone"],
            data["birth_date"],
            datetime.now().strftime("%d.%m.%Y")
        ))
        conn.commit()
        return {"success": True, "message": f"Пациент {data['patient_code']} создан"}
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(e)}
        )
    finally:
        conn.close()


@app.post("/api/medical-record/create")
async def api_create_medical_record(request: Request):
    """Создать запись в медкарте"""
    data = await request.json()
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO medical_record (
                patient_code, complaints, anamnesis, objective_exam,
                diagnosis, treatment_plan, treatment_done, recommendations, visit_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["patient_code"],
            data.get("complaints", ""),
            data.get("anamnesis", ""),
            data.get("objective_exam", ""),
            data.get("diagnosis", ""),
            data.get("treatment_plan", ""),
            data.get("treatment_done", ""),
            data.get("recommendations", ""),
            data.get("visit_date", datetime.now().strftime("%d.%m.%Y"))
        ))
        conn.commit()
        return {"success": True, "message": "Запись в медкарте создана"}
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(e)}
        )
    finally:
        conn.close()


@app.get("/api/patients/search")
async def api_search_patients(query: str = ""):
    """Поиск пациентов по коду, ФИО или телефону"""
    conn = get_db()
    cursor = conn.cursor()
    
    if query:
        cursor.execute("""
            SELECT * FROM personal_data 
            WHERE patient_code LIKE ? OR full_name LIKE ? OR phone LIKE ?
            ORDER BY patient_code
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    else:
        cursor.execute("SELECT * FROM personal_data ORDER BY patient_code")
    
    patients = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"patients": patients}


@app.get("/api/medical-record/{patient_code}")
async def api_get_medical_records(patient_code: str):
    """Получить все записи медкарты по коду пациента"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM medical_record 
        WHERE patient_code = ? 
        ORDER BY visit_date DESC
    """, (patient_code,))
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"records": records}


@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API"""
    return {"status": "ok", "message": "Medical Platform API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
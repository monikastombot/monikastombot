from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Medical Platform API")

# Путь к frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def root():
    """Главная страница"""
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/patient-login")
async def patient_login():
    """Страница входа для пациента"""
    return FileResponse(os.path.join(frontend_path, "patient-login.html"))

@app.get("/doctor-login")
async def doctor_login():
    """Страница входа для врача"""
    return FileResponse(os.path.join(frontend_path, "doctor-login.html"))

@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API"""
    return {"status": "ok", "message": "Medical Platform API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

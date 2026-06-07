import sys
import os

# Добавляем текущую папку в путь
sys.path.insert(0, os.path.dirname(__file__))

from backend.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

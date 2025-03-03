from fastapi import FastAPI
import redis
import json

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, db=0)

try:
    r.ping()
    print("✅ Подключено к Redis")
except Exception as e:
    print(f"❌ Ошибка подключения к Redis: {e}")

@app.get("/current_data")
def get_current_data():
    print("⚡ Запрос /current_data")
    data = json.loads(r.get('latest_data') or '[]')
    return {"current_data": data}

@app.get("/failure_warnings")
def get_failure_warnings():
    print("⚡ Запрос /failure_warnings")
    warnings = json.loads(r.get('failure_warnings') or '[]')
    return {"warnings": warnings}

@app.get("/")
def root():
    return {"status": "Equipment Monitoring API is running"}

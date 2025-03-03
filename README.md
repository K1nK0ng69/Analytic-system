# Analytic-system
Когда все файлы и библиотеки установлены, начинаем процесс запуска:
1. Запускаем Redis:
   redis-server
2. Запускаем Mosquitto:
   mosquitto
3.  Запускаем клиента (принимает данные с MQTT):
   python mqtt_sensor_client.py
4. Запускаем API:
   uvicorn api:app --host 0.0.0.0 --port 8000 
5. Проверяем, что всё работает:
   curl http://localhost:8000/current_data


В командной строке прописываешь docker-compose up --build
После этого проект запускается.
Документация доступна в браузере по этой ссылке:  http://localhost:8000/docs

import json
import paho.mqtt.client as mqtt
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        print(f"📥 Получены данные с датчиков: {data}")
        r.rpush('equipment_data', json.dumps(data))
        r.set('latest_data', json.dumps(data))
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга сообщения: {e}, данные: {msg.payload}")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Успешное подключение к брокеру MQTT")
        client.subscribe("equipment/sensors")
    else:
        print(f"❌ Ошибка подключения: {reason_code}")

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()

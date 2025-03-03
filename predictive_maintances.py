import json
import numpy as np
import pandas as pd
import redis
from sklearn.ensemble import IsolationForest

r = redis.Redis(host='localhost', port=6379, db=0)


def fetch_sensor_data():
    data = []
    while r.llen('equipment_data') > 0:
        data.append(json.loads(r.lpop('equipment_data')))
    return pd.DataFrame(data)


def analyze_and_predict(df):
    if df.empty:
        return []

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    features = df[['temperature', 'vibration', 'pressure']]

    model = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly'] = model.fit_predict(features)

    def predict_failure(row):
        if row['anomaly'] == -1:
            return 1
        if row['temperature'] > 85 or row['vibration'] > 6:
            return 1
        return 0

    df['failure_warning'] = df.apply(predict_failure, axis=1)

    warnings = df[df['failure_warning'] == 1].to_dict(orient='records')
    return warnings


def run_analysis():
    data = fetch_sensor_data()
    warnings = analyze_and_predict(data)
    if warnings:
        r.set('failure_warnings', json.dumps(warnings))
    r.set('latest_data', data.tail(1).to_json(orient='records'))


if __name__ == "__main__":
    import time

    while True:
        run_analysis()
        time.sleep(5)

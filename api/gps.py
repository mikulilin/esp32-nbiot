import requests
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

# 用户填写
PRODUCT_ID = "dyLIMxujKq"
DEVICE_NAME = "nbiot"
AUTH_TOKEN = "version=2018-10-31&res=products%2FdyLIMxujKq%2Fdevices%2Fnbiot&et=1798183737&method=md5&sign=w7deU9zmFKjLEVUb4umy6w%3D%3D"

def get_gps_history(product_id, device_name, auth_token, limit=50):
    url = "https://iot-api.heclouds.com/datapoint/history-datapoints"
    params = {
        "product_id": product_id,
        "device_name": device_name,
        "datastream_id": "GPS",
        "limit": limit
    }
    headers = {
        "Authorization": auth_token,
        "Accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    gps_list = []

    if data.get("code") == 0:
        datastreams = data.get("data", {}).get("datastreams", [])
        if datastreams:
            for point in datastreams[0].get("datapoints", []):
                value = point.get("value", {})
                gps_list.append({
                    "time": point.get("at"),
                    "lat": value.get("lat"),
                    "lon": value.get("lon")
                })
    return gps_list

@app.route("/api/gps")
def gps_api():
    gps_data = get_gps_history(PRODUCT_ID, DEVICE_NAME, AUTH_TOKEN)
    return jsonify({"code": 0, "gps": gps_data})

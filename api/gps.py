import json
import requests

PRODUCT_ID = "dyLIMxujKq"      # 替换为你的 OneNET 产品ID
DEVICE_NAME = "nbiot"          # 替换为你的设备名
AUTH_TOKEN = "version=2018-10-31&res=products%2FdyLIMxujKq%2Fdevices%2Fnbiot&et=1798183737&method=md5&sign=w7deU9zmFKjLEVUb4umy6w%3D%3D"  # 替换为你的 token

def handler(request):
    url = "https://iot-api.heclouds.com/datapoint/history-datapoints"
    params = {
        "product_id": PRODUCT_ID,
        "device_name": DEVICE_NAME,
        "datastream_id": "GPS",
        "limit": 10  # 最新10条
    }
    headers = {
        "Authorization": AUTH_TOKEN,
        "Accept": "application/json"
    }

    try:
        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()
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

        return {
            "statusCode": 200,
            "body": json.dumps({"code": 0, "gps": gps_list}),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"code": -1, "error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }

from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse

# OneNET 配置
PRODUCT_ID = "dyLIMxujKq"       # 替换为你的产品ID
DEVICE_NAME = "nbiot"           # 替换为你的设备名称
AUTH_TOKEN = "version=2018-10-31&res=products%2FdyLIMxujKq%2Fdevices%2Fnbiot&et=1798183737&method=md5&sign=w7deU9zmFKjLEVUb4umy6w%3D%3D"

app = FastAPI(title="Vercel FastAPI OneNET GPS", version="1.0.0")


def fetch_gps_history(limit=10):
    url = "https://iot-api.heclouds.com/datapoint/history-datapoints"
    headers = {
        "Authorization": AUTH_TOKEN,
        "Accept": "application/json"
    }
    params = {
        "product_id": PRODUCT_ID,
        "device_name": DEVICE_NAME,
        "datastream_id": "GPS",
        "limit": limit
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        datastreams = data.get("data", {}).get("datastreams", [])
        gps_list = []
        if datastreams:
            points = datastreams[0].get("datapoints", [])
            for p in points:
                val = p.get("value")
                gps_list.append({
                    "time": p.get("at"),
                    "lat": val.get("lat"),
                    "lon": val.get("lon")
                })
        return {"code": 0, "gps": gps_list}
    except Exception as e:
        return {"code": -1, "error": str(e)}


@app.get("/api/gps")
async def api_gps():
    return JSONResponse(content=fetch_gps_history())


@app.get("/")
async def root():
    return {"message": "Vercel FastAPI OneNET GPS API is running"}

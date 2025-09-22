from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from datetime import datetime

app = FastAPI()

ONENET_DEVICE_ID = "你的设备ID"
ONENET_API_KEY = "你的OneNET API Key"
ONENET_DATASTREAM_ID = "GPS"

MAX_HISTORY = 50  # 保留最多50条数据

history_data = []

@app.get("/api/gps")
def get_gps():
    global history_data
    # 请求 OneNET 数据流最新数据
    url = f"https://api.heclouds.com/devices/{ONENET_DEVICE_ID}/datapoints?datastream_id={ONENET_DATASTREAM_ID}&limit=1"
    headers = {"api-key": ONENET_API_KEY}
    
    try:
        r = requests.get(url, headers=headers, timeout=5).json()
        if "data" in r and "datastreams" in r["data"]:
            points = r["data"]["datastreams"][0].get("datapoints", [])
            for p in points:
                gps_point = {
                    "time": p.get("at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    "lat": p["value"]["lat"],
                    "lon": p["value"]["lon"]
                }
                # 避免重复加入相同点
                if len(history_data) == 0 or history_data[-1] != gps_point:
                    history_data.append(gps_point)
                    # 保持最多 MAX_HISTORY 条
                    if len(history_data) > MAX_HISTORY:
                        history_data.pop(0)
    except Exception as e:
        print("OneNET 获取数据失败:", e)

    return JSONResponse({"code": 0, "gps": history_data[::-1]})  # 最新在前

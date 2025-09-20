// api/data.js
import fetch from "node-fetch";

export default async function handler(req, res) {
  // OneNET 固定信息，直接写死
  const PRODUCT_ID = "dyLIMxujKq";      // 你的产品ID
  const DEVICE_NAME = "nbiot";          // 你的设备名
  const API_KEY = "version=2018-10-31&res=products%2FdyLIMxujKq%2Fdevices%2Fnbiot&et=1768250492&method=md5&sign=t5f1pNgczT2aSwuaUZ0ozQ%3D%3D"; // 替换为你的北向API Key

  const url = `https://iot-api.heclouds.com/datapoint/history-datapoints?product_id=${PRODUCT_ID}&device_name=${DEVICE_NAME}&datastream_id=Latitude,Longitude&limit=1&sort=DESC`;

  try {
    const oneRes = await fetch(url, {
      headers: {
        "Authorization": API_KEY
      }
    });
    const data = await oneRes.json();
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: "OneNET API request failed", details: err.message });
  }
}

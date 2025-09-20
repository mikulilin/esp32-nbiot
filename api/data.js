// api/data.js
import fetch from "node-fetch";

export default async function handler(req, res) {
  const PRODUCT_ID = process.env.ONENET_PRODUCT_ID;   // Vercel 环境变量
  const DEVICE_NAME = process.env.ONENET_DEVICE_NAME; // Vercel 环境变量
  const API_KEY = process.env.ONENET_API_KEY;         // OneNET 北向 API Key

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

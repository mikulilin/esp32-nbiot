let latestData = { value: null, time: null };

export default function handler(req, res) {
  if (req.method === "POST") {
    // 从 ESP32/NB-IoT 上传的数据
    const { value } = req.body;
    latestData = { value, time: Date.now() };
    console.log("收到:", latestData);
    res.status(200).json({ ok: true });
  } else if (req.method === "GET") {
    // 给网页读取最新数据
    res.status(200).json(latestData);
  } else {
    res.status(405).json({ error: "Method not allowed" });
  }
}

let latestData = { message: "尚未收到数据" };

export default function handler(req, res) {
  if (req.method === "POST") {
    let body = "";
    req.on("data", chunk => (body += chunk));
    req.on("end", () => {
      try {
        latestData = JSON.parse(body);  // 保存最新的数据
        res.status(200).json({ status: "ok" });
      } catch (err) {
        res.status(400).json({ status: "error", message: err.message });
      }
    });
  } else {
    res.status(200).json(latestData);  // GET 返回最新的数据
  }
}

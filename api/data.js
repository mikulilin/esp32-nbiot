// 简单内存存储，重启会丢失，生产可用数据库
let dataStore = [];

export default function handler(req, res) {
  if (req.method === "POST") {
    const { value } = req.body;
    if (value !== undefined) {
      const record = { value, time: new Date().toISOString() };
      dataStore.push(record);
      return res.status(200).json({ message: "Data received", record });
    }
    return res.status(400).json({ message: "Invalid data" });
  } else if (req.method === "GET") {
    return res.status(200).json(dataStore);
  } else {
    res.setHeader("Allow", ["GET", "POST"]);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

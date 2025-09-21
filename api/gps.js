let lastData = null;

// 这里真实 ESP32 上传时可以 POST 更新 lastData
export default function handler(req, res) {
  // 仅 GET 返回数据
  if (req.method === 'GET') {
    if (lastData) {
      res.status(200).json(lastData);
    } else {
      res.status(200).json({ longitude:null, latitude:null, eventTime:null });
    }
  }
  
  // 可选：模拟 ESP32 POST 上传数据
  if (req.method === 'POST') {
    const { longitude, latitude } = req.body;
    if (longitude != null && latitude != null) {
      lastData = {
        longitude: parseFloat(longitude),
        latitude: parseFloat(latitude),
        eventTime: new Date().toISOString()
      };
      res.status(200).json({ success:true });
    } else {
      res.status(400).json({ success:false, msg:"无效数据" });
    }
  }
}
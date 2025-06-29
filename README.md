# 🚗 YOLOv8 Vehicle Detection System

Real-time vehicle detection system using YOLOv8 with a modern web interface.

## 📁 Project Structure

```
yolnigoh/
├── public/
│   ├── index.html       # HTML-интерфейс
│   └── frame.jpg        # Последний обработанный кадр (обновляется Python'ом)
├── data/
│   └── count.txt        # Число машин (обновляется Python'ом)
├── server.js            # Express-сервер (Node.js)
├── process.py           # YOLOv8 обработчик видео (Python)
├── package.json         # Скрипты запуска Node.js и Python
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip3 install ultralytics opencv-python numpy

# Or use the setup script
npm run setup
```

### 2. Start the System

**Option A: Run components separately**
```bash
# Terminal 1: Start web server
npm start

# Terminal 2: Start vehicle detection
npm run detect
```

**Option B: Run both together**
```bash
npm run both
```

### 3. Open Web Interface

Visit http://localhost:3000 in your browser to see the real-time detection interface.

## 📊 Available Scripts

| Script | Description |
|--------|-------------|
| `npm start` | Start Express web server |
| `npm run dev` | Start server with auto-restart |
| `npm run detect` | Start YOLOv8 detection (webcam) |
| `npm run detect-webcam` | Explicitly use webcam |
| `npm run detect-file` | Detect from video file |
| `npm run both` | Run server + detection together |
| `npm run setup` | Install all dependencies |

## 🎥 Video Sources

### Webcam Detection
```bash
npm run detect
# or
python3 process.py --source 0
```

### Video File Detection
```bash
python3 process.py --source path/to/video.mp4
```

### Custom Options
```bash
python3 process.py --source 0 --model yolov8s.pt --confidence 0.7
```

## 🔧 Configuration

### Python Script Options
- `--source, -s`: Video source (0 for webcam, file path for video)
- `--model, -m`: YOLO model path (default: yolov8n.pt)
- `--confidence, -c`: Detection confidence threshold (default: 0.5)

### Available YOLO Models
- `yolov8n.pt` - Nano (fastest, lowest accuracy)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium  
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (slowest, highest accuracy)

## 🌐 Web Interface Features

- **Real-time vehicle count display**
- **Live video feed with detection overlays**
- **System status monitoring**
- **Automatic updates every second**
- **Responsive design**

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/count` | GET | Current vehicle count |
| `/api/status` | GET | System status |

## 🛠️ Development

### File Updates
- `data/count.txt` - Updated every 5 frames with vehicle count
- `public/frame.jpg` - Updated every 5 frames with annotated image

### Demo Mode
If YOLOv8 is not installed, the system runs in demo mode with random counts for testing.

## 📋 Requirements

### Node.js
- Node.js 14.0.0 or higher
- Express.js

### Python
- Python 3.7 or higher
- ultralytics (YOLOv8)
- opencv-python
- numpy

### System
- Webcam for live detection (optional)
- GPU recommended for better performance (optional)

## 🎯 Vehicle Classes Detected

- Cars
- Motorcycles
- Buses
- Trucks

## 🔄 How It Works

1. **Python script** (`process.py`) captures video frames
2. **YOLOv8** processes frames and detects vehicles
3. **Count and frame** are saved to files every 5 frames
4. **Express server** (`server.js`) serves the web interface
5. **Web page** automatically refreshes data every second

## 🎮 Controls

When the detection window is active:
- Press `q` to quit detection
- Press `s` to save a screenshot

## 🚨 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip3 install ultralytics opencv-python numpy
```

**Webcam not working:**
- Try different source numbers: `--source 1` or `--source 2`
- Check if camera is being used by another application

**Permission denied:**
```bash
sudo chmod +x process.py
```

**Port already in use:**
- Kill existing processes or change port in `server.js`

## 📈 Performance Tips

1. Use smaller YOLO models (yolov8n.pt) for faster processing
2. Adjust confidence threshold for accuracy vs speed
3. Reduce frame update frequency in `process.py`
4. Use GPU acceleration if available

## 📄 License

MIT License - feel free to use and modify! 
import cv2
from ultralytics import YOLO
import time
import numpy as np
import os
from datetime import datetime

# Initialize YOLO model
model = YOLO("yolov8s.pt")  # Lightweight model, downloads automatically

# Initialize video capture - use client's camera
cap = cv2.VideoCapture(0)

# Ensure data directories exist
os.makedirs("public", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Vehicle classes to detect
vehicle_classes = ['car', 'bus', 'truck', 'motorbike']

# Distance parameters for traffic analysis
MAX_DISTANCE = 1000  # Maximum distance (pixels)
MIN_DISTANCE = 200   # Minimum distance (pixels)

# Text positions
text_positions = {
    'count': {'x': 10, 'y': 50},
    'signal': {'x': 10, 'y': 80},
    'intensity': {'x': 10, 'y': 110}
}

# Function to save vehicle count
def save_vehicle_count(count):
    with open("data/count.txt", "w") as f:
        f.write(str(count))

# Function to calculate traffic intensity
def calculate_traffic_intensity(vehicle_count):
    if vehicle_count == 0:
        return "Avtomobil Yo'q"
    elif vehicle_count < 5:
        return "Juda past"
    elif vehicle_count < 15:
        return "Yengil"
    elif vehicle_count < 40:
        return "O'rtacha"
    elif vehicle_count < 70:
        return "Qattiq"
    else:
        return "O'ta qattiq"

# Function to adjust green signal duration
def adjust_green_signal(traffic_intensity):
    intensity_map = {
        "Avtomobil Yo'q": 0,
        "Juda past": 5,
        "Yengil": 15,
        "O'rtacha": 30,
        "Qattiq": 45,
        "O'ta qattiq": 60
    }
    return intensity_map.get(traffic_intensity, 15)

# Function to draw frame border
def draw_frame_border(frame):
    frame_height, frame_width = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (frame_width, frame_height), (0, 255, 0), 20)
    return frame

# Function to draw timestamp
def draw_timestamp(frame):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, f"⏱ {timestamp}", (10, frame.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
    return frame

# Function to draw system status
def draw_system_status(frame, fps, vehicle_count):
    cv2.putText(frame, f"📶 FPS: {fps:.1f} | 🚗 Avtomobillar: {vehicle_count}", 
                (frame.shape[1] - 400, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    return frame

# Main processing loop
try:
    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Pre-process frame
        frame = draw_frame_border(frame)
        frame = draw_timestamp(frame)
        
        # Detect vehicles
        results = model(frame)
        vehicle_count = 0
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                
                if cls_name in vehicle_classes:
                    vehicle_count += 1
                    
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Draw class label
                    cv2.putText(frame, cls_name, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # Calculate traffic metrics
        traffic_intensity = calculate_traffic_intensity(vehicle_count)
        green_signal_time = adjust_green_signal(traffic_intensity)
        
        # Draw traffic information
        cv2.putText(frame, f"Avtomobil Soni: {vehicle_count}", 
                    (text_positions['count']['x'], text_positions['count']['y']), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.putText(frame, f"🟢 Yashil chiroq: {green_signal_time}s", 
                    (text_positions['signal']['x'], text_positions['signal']['y']), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Tirbandlik Holati: {traffic_intensity}", 
                    (text_positions['intensity']['x'], text_positions['intensity']['y']), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 255), 2)
        
        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        # Draw system status
        frame = draw_system_status(frame, fps, vehicle_count)
        
        # Save processed frame
        cv2.imwrite("public/frame.jpg", frame)
        
        # Save vehicle count
        save_vehicle_count(vehicle_count)
        
        # Display in window (optional)
        cv2.imshow("Yo'lNigoh AI - Transport Monitoring", frame)
        
        # Exit on ESC
        if cv2.waitKey(1) == 27:
            break
            
        # Sleep to control processing rate
        time.sleep(0.1)
        
finally:
    # Clean up resources
    cap.release()
    cv2.destroyAllWindows()
    print("System shutdown gracefully")
import cv2
from ultralytics import YOLO
import time
import numpy as np

model = YOLO("yolov8s.pt")  # Лёгкая модель, скачивается автоматически
cap = cv2.VideoCapture(0)   # Или укажи видеофайл, например: "cars.mp4"


# Matnni harakatlantirish uchun boshlang'ich koordinatalar
x, y = 10, 50  # Matnning boshlang'ich joylashuvi
j, z = 10, 80   # Matnning boshlang'ich joylashuvi
b, d = 10, 110    # Matnning boshlang'ich joylashuvi



# Ramka uchun o'zgaruvchilar
frame_thickness = 20  # Ramkaning qalinligi
frame_color = (0, 255, 0)  # Yashil rangda ramka

vehicle_classes = ['car', 'bus', 'truck', 'motorbike']

# Masofa hisoblash uchun parametrlar
max_distance = 1000  # Maksimal masofa (pixellar)
min_distance = 200   # Minimal masofa (pixellar)


def save_vehicle_count(count):
    with open("vehicle_count.txt", "w") as f:
        f.write(str(count))

def calculate_traffic_intensity(vehicle_count):
    # Agar avtomobillar soni belgilangan thresholddan yuqori bo'lsa, "Heavy", aks holda "Smooth"
    heavy_traffic_threshold = 15
    yuqori_avtomobil= 40
    juda_past = 5
    Avtomobil_yuq = 0
    if vehicle_count > heavy_traffic_threshold:
        return "Yuqori"
    elif Avtomobil_yuq == vehicle_count:
        return "Avtomobil Yo'q"
    elif juda_past > vehicle_count:
        return "Juda past"
    elif yuqori_avtomobil < vehicle_count:
        return "O'ta Yuqori"
    else:
        return "O'rtacha"

def adjust_green_signal(traffic_intensity):
    if traffic_intensity == "Yuqori":
        return 30  # Heavy trafik uchun uzunroq yashil chiroq (masalan, 30 soniya)
    elif traffic_intensity == "Avtomobil Yo'q":
        return 0
    elif traffic_intensity == "Juda past":
        return 5        
    elif traffic_intensity == "O'ta Yuqori":
        return 60
    else:
        return 15  # Smooth trafik uchun qisqaroq yashil chiroq (masalan, 15 soniya)
    
    


while True:
    ret, frame = cap.read()
    if not ret:
        break


# Ekran o'lchamlarini olish
    frame_height, frame_width = frame.shape[:2]



# Ekranni yashil ramka bilan o'raladi
    frame_thickness = 20
    frame_color = (0, 255, 0)
    cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), frame_color, frame_thickness)

    # YOLOv8 modelini ishlatish
    results = model(frame)
    vehicle_count = 0
    traffic_intensity = ""

    

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            if cls_name in vehicle_classes:
                vehicle_count += 1

                # Avtomobilning to'liq qutilarini olish
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2


                
   
                
                # Masofa hisoblash (kameraning markazi bilan)
                center_distance = np.sqrt(center_x**2 + center_y**2)  # Kamera markazidan masofa

                # Yashil chiroqni moslashtirish (masofaga qarab)
                if center_distance < min_distance:
                    # Masofa qisqa bo'lsa, avtomobilga tezroq ruxsat berish
                    green_time = 15  # Tez yashil chiroq
                elif center_distance < max_distance:
                    green_time = 25  # O'rta masofa uchun yashil chiroq
                else:
                    green_time = 35  # Uzoq masofa uchun uzun yashil chiroq

                # Ramka va nom yozish
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, cls_name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Traffic intensity va green signal time
    traffic_intensity = calculate_traffic_intensity(vehicle_count)
    green_signal_time = adjust_green_signal(traffic_intensity)

    # Ekranda avtomobil soni va svetofor holatini ko'rsatish
    cv2.putText(frame, f"Avtomobil Soni: {vehicle_count}",(x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Matnni ekranda harakatlantirish

    


 



    # Yashil chiroqni yashil rangda ko'rsatish
    if traffic_intensity == "Yuqori":
        cv2.putText(frame, f"🟢 Yashil chiroq: {green_signal_time}s", (j, z),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Yashil rangda
    else:
        cv2.putText(frame, f"Yashil chiroq: {green_signal_time}s", (j, z),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Yashil rangda
        

    # Ekranda trafik intensivligini ko'rsatish
    cv2.putText(frame, f"Tirbandlik Holati: {traffic_intensity}", (b, d),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 255), 2)
    
     # Matnni harakatlantirish uchun koordinatalarni yangilash
    x += 1  # Gorizontal harakat (matn o'ngga suriladi)
    j += 1  # Gorizontal harakat (matn o'ngga suriladi)
    b += 1  # Gorizontal harakat (matn o'ngga suriladi)
    y += 0  # Vertikal harakat (matn pastga suriladi)

    if x > frame_height:  # Matn ekran chetiga yetganda, uni qayta boshlash
        x -= 5
    if j > frame_height:  # Matn ekran chetiga yetganda, uni qayta boshlash
        j -= 5    
    if b > frame_height:  # Matn ekran chetiga yetganda, uni qayta boshlash
        b -= 5
    # Natijani ko‘rsatish
    #cv2.imshow("Yo'lNigoh AI Startup Software MVP", frame)



    results = model(frame)[0]
    count = len([r for r in results.boxes.cls if int(r) == 2])  # класс 2 = car

    annotated = results.plot()
    cv2.imwrite("public/frame.jpg", annotated)

    with open("data/count.txt", "w") as f:
        f.write(str(vehicle_count))

    time.sleep(1)  # обновление раз в 1 сек



    if cv2.waitKey(1) == 27:  # ESC tugmasi
        break
    

cap.release()
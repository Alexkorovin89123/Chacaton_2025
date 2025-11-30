import cv2
import json
from ultralytics import YOLO
from datetime import timedelta

VIDEO_PATH = 'C:/Users/alex_dextop/PycharmProjects/Yolo_2/rem.mp4'      # путь к видеофайлу
MODEL_PATH = 'yolov8n.pt'          # путь к твоей модели
OUTPUT_JSON = 'violations_report.json'
VIOLATION_CLASSES = {
    0: 'No_Helmet',
    1: 'No_Vest',
    2: 'Unsafe_Position',
    # Добавь свои классы если нужно
}

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
interval = 5  # секунд

results_by_interval = []
frame_num = 0
current_interval_start = 0
interval_violations = []

def save_interval_result(start_frame, detected_violations):
    if not detected_violations:
        return None
    # Сгруппируем классы и объекты
    grouped = {}
    for item in detected_violations:
        key = (item['violation_class'], tuple(item['detected_objects']))
        grouped.setdefault(key, []).append(item)

    result = []
    for (vcls, dobjs), group in grouped.items():
        result.append({
            "violation_class": vcls,
            "number": '',  # Место для распознавания номеров
            "frame": group[0]['frame'],
            "time": f"{group[0]['time']}",
            "detected_objects": list(dobjs),
            "violation_type": "Safety",
            "count": len(group)
        })
    return result

while cap.isOpened():
    ret, frame = cap.read()
    # cv2.line(frame, (750, 715), (625, 170), (0, 0, 255), 2, 2)
    if not ret:
        break
    frame_num += 1
    time_in_sec = frame_num / fps

    # если новый промежуток 5 сек
    if time_in_sec >= current_interval_start + interval:
        v = save_interval_result(current_interval_start, interval_violations)
        if v:
            results_by_interval.extend(v)
        interval_violations = []
        current_interval_start += interval

    results = model(frame)[0]
    for det in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls_id = det
        cls_id = int(cls_id)
        violation_class = VIOLATION_CLASSES.get(cls_id, f'class_{cls_id}')
        objects = ['person'] if violation_class.startswith('No_') or violation_class == 'Unsafe_Position' else []
        time_str = str(timedelta(seconds=int(time_in_sec)))
        violation = {
            "violation_class": violation_class,
            "number": "",  # номер можно дописать если появится модуль чтения номеров
            "frame": frame_num,
            "time": time_str,
            "detected_objects": objects,
            "violation_type": "Safety"
        }
        interval_violations.append(violation)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# сохранение последнего интервала
v = save_interval_result(current_interval_start, interval_violations)
if v:
    results_by_interval.extend(v)

cap.release()

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results_by_interval, f, ensure_ascii=False, indent=4)

print(f"Сохранено {len(results_by_interval)} записей о нарушениях в {OUTPUT_JSON}")

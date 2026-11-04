import cv2
# import mss
import numpy as np
from ultralytics import YOLO
from pathlib import Path

TEST = "C:\\Data\\Slavon\\petprojects\\neurowooll\\dataset\\test"
MODEL = "best.onnx"

model = YOLO(MODEL, task="detect")

for item in Path(f"{TEST}/images").iterdir():
    if item.is_file():
        img = cv2.imread(f"{TEST}/images/{item.name}")
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        results = model.predict(frame, imgsz=500, conf=0.5, verbose=False)

        result = results[0]
        annotated_frame = result.plot()

        cv2.imshow("YOLOv8 Detection", annotated_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




# with mss.mss() as sct:
#     # Пример координат вашего окна 100x100 на экране
#     monitor = {"top": 200, "left": 200, "width": 100, "height": 100}
#
#     while True:
#         # 1. Сверхбыстрый захват кадра
#         screenshot = np.array(sct.grab(monitor))
#         frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)  # Убираем альфа-канал
#
#         # 2. Распознавание всей группы объектов
#         results = model.predict(frame, imgsz=100, conf=0.5, verbose=False)
#
#         # 3. Чтение координат для логики бота
#         for box in results[0].boxes:
#             # Получаем координаты центра объекта, его ширину и высоту
#             x_center, y_center, w, h = box.xywh[0].tolist()
#             class_id = int(box.cls[0].item())
#             confidence = box.conf[0].item()
#
#             # Пример логики: если это враг (класс 0), двигаем мышку/стреляем
#             if class_id == 0:
#                 # Переводим локальные координаты 100x100 в глобальные координаты экрана
#                 screen_x = monitor["left"] + int(x_center)
#                 screen_y = monitor["top"] + int(y_center)
#                 print(f"Цель найдена! Навожусь на: {screen_x}, {screen_y}")
#                 # pydirectinput.click(screen_x, screen_y)

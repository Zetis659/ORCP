from ultralytics import YOLO
import os
import time


start = time.time()

model = YOLO(os.path.join("Models", "Detection", "yolov8x.pt"))

picture = os.path.join('Pictures', '06-10-2023-20-18-29.jpg')


results = model.predict(os.path.join(picture), save=True)


finish = time.time()
total_time = finish - start
print(f"Total time detection: {total_time:.2f}")
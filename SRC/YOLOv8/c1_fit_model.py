from ultralytics import YOLO
import os
import time

start = time.time()

dataset = 'Prepared_photos'

model = YOLO(os.path.join('Models', 'Classification', 'yolov8x-cls.pt'))

model.info()
results = model.train(data=os.path.join('SRC', 'YOLOv8', dataset), epochs=30, imgsz=320)

finish = time.time()
total_time = finish - start
print(f'Total time: {total_time:.2f}')


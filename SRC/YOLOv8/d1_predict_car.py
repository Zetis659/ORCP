from ultralytics import YOLO
import os
import time 
import sys


start = time.time()
picture = os.path.join('Pictures', '06-10-2023-20-18-29.jpg')

model = YOLO(os.path.join('Models', 'Classification', 'ALL_CARS_134.pt'))

results = model.predict(os.path.join(picture), save=True)
finish = time.time()

total_time = finish - start
print(f'Total time: {total_time:.2f}')
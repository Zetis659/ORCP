from ultralytics import YOLO
import os
import time


def yolo_detect(img_path):
    start = time.time()

    model = YOLO(os.path.join("Models", "Detection", "yolov8x.pt"))
    results = model.predict(os.path.join(img_path))

    objects = results[0].boxes.cls
    car = 0

    if "2." in str(objects) or "7." in str(objects):
        print("Есть машина!")
        car = 1
    else:
        print("Нет машины!")

    finish = time.time()
    total_time = finish - start
    print(f"Total time detection: {total_time:.2f}")

    return car

import os
import random
import shutil

source_dir = os.path.join('SRC', 'YOLOv8', 'Selected_photos')
target_dir = os.path.join('SRC', 'YOLOv8', 'Prepared_photos')

train_ratio = 0.7
test_ratio = 0.3

os.makedirs(os.path.join(target_dir, 'train'), exist_ok=True)
os.makedirs(os.path.join(target_dir, 'test'), exist_ok=True)

for root, _, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            rand_num = random.random()
            if rand_num < train_ratio:
                target_subdir = 'train'
            else:
                target_subdir = 'test'

            target_path = os.path.join(
                target_dir, target_subdir, os.path.basename(root))
            os.makedirs(target_path, exist_ok=True)

            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file)
            shutil.copy(source_file, target_file)

print("Готово!")

import requests
import os
import time

start = time.time()

pictures_quantity = 500
picture_size = '456x342n.txt'
car_brand = 'HAVAL'


def download_images_from_file(file_path, download_folder):
    with open(file_path, 'r') as file:
        lines = file.readlines()[:pictures_quantity]

    for idx, url in enumerate(lines):
        url = url.strip()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url.lstrip('/')

        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_name = f'{idx + 1}.jpg'
                image_path = os.path.join(download_folder, image_name)

                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                print(
                    f'Image {idx + 1} downloaded successfully from {file_path}.')

            else:
                print(
                    f'Failed to download image {idx + 1} from {file_path} with status code: {response.status_code}')

        except Exception as e:
            print(
                f'Failed to download image {idx + 1} from {file_path} due to error: {e}')


def process_folders(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(picture_size):
                    file_path = os.path.join(folder_path, file_name)
                    download_folder = os.path.join(
                        'Downloads', car_brand, folder_name, os.path.splitext(file_name)[0])
                    if not os.path.exists(download_folder):
                        os.makedirs(download_folder)

                    download_images_from_file(file_path, download_folder)


if __name__ == '__main__':
    root_folder = os.path.join('SRC/Parsing/Results/Photo_links', car_brand)
    process_folders(root_folder)

end = time.time()

total_time = end - start
print(f'Total time: {total_time:.2f}')

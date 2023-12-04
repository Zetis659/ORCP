from SRC.Parsing.Proxy.a1_preparation_to_parsing_PROXY import dict_headers
from genericpath import exists
import requests
import time
import fake_useragent as fua
import random as rnd
from user_agents import parse
from tqdm import tqdm
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "..", "..", ".."))


start = time.time()
black_list_mobile = ["smartphone", "iphone",
                     "ipad", "ipod", "windows ce", "htc"]

while True:
    user = fua.UserAgent().random
    user_agent_check_mobile = parse(user)
    bl_check = False
    for word in black_list_mobile:
        if word in user.lower():
            bl_check = True
            break
    if user_agent_check_mobile.is_mobile == False and bl_check == False:
        break
dict_headers["User-Agent"] = user

random_port = rnd.randint(9050, 9149)
tor = f"socks5://127.0.0.1:{random_port}"
proxy = {"https": tor}

total_captcha = 0

url = "https://auto.ru/-/ajax/desktop/listing/"
txt_path = os.path.join("SRC", "Parsing", "Results",
                        "Cars", "Brands", "brands.txt")
with open(txt_path, "r", encoding="utf-8") as f:
    brands = f.read()

brands_list = brands.split(",\n")
total_models = 0

parsed_brand_list = []
parsed_model_list = []

for brand in brands_list:
    parsed_brand_list.append(brand)
    data_to_save = [f"parsed_brand_list = {parsed_brand_list}"]

    failure_file_path = os.path.join(
        "SRC", "Parsing", "Results", "Cars", "Parsing_failure", f"Models_fail.txt"
    )
    folder_path = os.path.dirname(failure_file_path)
    if not exists(folder_path):
        os.makedirs(folder_path)
    with open(
        failure_file_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(",\n".join(data_to_save))

    models_list = []

    params = {
        "category": "cars",
        "section": "all",
        "page": 1,
        "catalog_filter": [{"mark": brand}],
        "geo_id": [225],
        "sort": "autoru_exclusive-desc",
    }

    response = requests.post(
        url, json=params, headers=dict_headers, proxies=proxy)

    page_count = response.json()["pagination"]["total_page_count"]
    if page_count > 100:
        print("Разделите данные по годам!!! НЕВОЗМОЖНО спарсить все страницы за раз!!!")
        print(f"Количество страниц: {page_count}")
    else:
        data = response.json()["offers"]
        print(f"Количество страниц: {page_count}")

        random_ip = 0
        for page in tqdm(range(1, page_count + 1)):
            params = {
                "category": "cars",
                "section": "all",
                "page": page,
                "catalog_filter": [{"mark": brand}],
                "geo_id": [225],
                "sort": "autoru_exclusive-desc",
            }

            random_ip += 1

            if random_ip == 2:
                random_port = rnd.randint(9050, 9149)
                tor = f"socks5://127.0.0.1:{random_port}"
                proxy = {"https": tor}

                while True:
                    user = fua.UserAgent().random
                    user_agent_check_mobile = parse(user)
                    bl_check = False
                    for word in black_list_mobile:
                        if word in user.lower():
                            bl_check = True
                            break
                    if user_agent_check_mobile.is_mobile == False and bl_check == False:
                        break
                dict_headers["User-Agent"] = user
                random_ip = 0

            print()
            print(f'UA: {dict_headers["User-Agent"]}')
            print(f"PORT: {tor}")
            print(f"RANDOM IP IN A ROW: {random_ip+1}")

            response = requests.post(
                url, json=params, headers=dict_headers, proxies=proxy
            )

            data = response.json()
            try:
                if data["type"] == "captcha":
                    print("======== CAPTCHA! =========")
                    total_captcha += 1
                    continue
            except:
                data = response.json()["offers"]
                for ad in range(1, len(data)):
                    try:
                        car_model_csv = str(
                            data[ad]["vehicle_info"]["model_info"]["code"]
                        )
                    except:
                        pass

                    if car_model_csv not in models_list:
                        models_list.append(car_model_csv)

                print(f"Page: {page} was parsed!!")
                print(f"Number of models {brand}: {len(models_list)}")

        print(f"{brand} WAS PARSED SUCCESSFULLY!!!")
        print(f"Total Pages: {page_count}")
        print(f"Total {brand} models: {len(models_list)}")
        print(models_list)
        total_models += len(models_list)
        print(f"Models of different brands was parsed: {total_models}")
        print(f"Total CAPTCHA: {total_captcha}")

    txt_file_path = os.path.join(
        "SRC", "Parsing", "Results", "Cars", "Models", f"{brand}.txt"
    )
    folder_path = os.path.dirname(txt_file_path)
    if not exists(folder_path):
        os.makedirs(folder_path)
    with open(
        txt_file_path,
        "a",
        encoding="utf-8",
    ) as file:
        file.write(",\n".join(models_list))
    print(f"{brand} WAS SAVED SUCCESSFULLY!!!")

finish = time.time()
total_time = finish - start
print(f"Total time: {total_time:.2f}")

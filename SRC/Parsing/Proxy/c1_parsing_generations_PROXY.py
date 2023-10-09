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
from SRC.Parsing.Proxy.a1_preparation_to_parsing_PROXY import dict_headers


start = time.time()
black_list_mobile = ["smartphone", "iphone", "ipad", "ipod", "windows ce", "htc"]

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
txt_path = os.path.join("SRC", "Parsing", "Results", "Cars", "Brands", "brands.txt")
with open(txt_path, "r", encoding="utf-8") as f:
    brands = f.read()

brands_list = brands.split(",\n")

parsed_brand_list = []
parsed_model_list = []

total_generations = 0
print(brands_list)
for brand in brands_list:
    print(f"Brand: {brand}")
    parsed_brand_list.append(brand)

    txt_path_models = os.path.join(
        "SRC", "Parsing", "Results", "Cars", "Models", f"{brand}.txt"
    )
    with open(txt_path_models, "r", encoding="utf-8") as file:
        models = file.read()

    models_list = models.split(",\n")

    for model in models_list:
        print(f"Model: {model}")
        parsed_model_list.append(model)

        data_to_save = [
            f"parsed_brand_list = {parsed_brand_list}",
            f"parsed_model_list = {parsed_model_list}",
        ]

        failure_file_path = os.path.join(
            "SRC",
            "Parsing",
            "Results",
            "Cars",
            "Parsing_failure",
            f"Generations_fail.txt",
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

        generations_list = []
        generations_names_list = []

        params = {
            "category": "cars",
            "section": "all",
            "page": 1,
            "catalog_filter": [{"mark": brand, "model": model}],
            "geo_id": [225],
            "sort": "fresh_relevance_1-desc",
        }

        response = requests.post(url, json=params, headers=dict_headers, proxies=proxy)

        page_count = response.json()["pagination"]["total_page_count"]
        if page_count > 100:
            print(
                "Разделите данные по годам!!! НЕВОЗМОЖНО спарсить все страницы за раз!!!"
            )
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
                    "catalog_filter": [{"mark": brand, "model": model}],
                    "geo_id": [225],
                    "sort": "fresh_relevance_1-desc",
                }
                random_ip += 1

                if random_ip == 3:
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
                        if (
                            user_agent_check_mobile.is_mobile == False
                            and bl_check == False
                        ):
                            break
                    dict_headers["User-Agent"] = user
                    random_ip = 0

                print()
                print(f'UA: {dict_headers["User-Agent"]}')
                print(f"PORT: {tor}")
                print(f"RANDOM IP IN A ROW: {random_ip}")

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
                            car_generation_csv = str(
                                data[ad]["vehicle_info"]["super_gen"]["id"]
                            )
                        except:
                            pass

                        try:
                            car_generation_name = str(
                                data[ad]["vehicle_info"]["super_gen"]["name"]
                            )
                        except:
                            pass

                        if car_generation_csv not in generations_list:
                            generations_list.append(car_generation_csv)
                        if car_generation_name not in generations_names_list:
                            generations_names_list.append(car_generation_name)

                    print(f"Page: {page} was parsed!!")
                    print(
                        f"Number of generations {brand} {model}: {len(generations_list)}"
                    )

            print(f"{brand} {model} WAS PARSED SUCCESSFULLY!!!")
            print(f"Total Pages: {page_count}")
            print(f"Total {brand} {model} genes: {len(generations_list)}")
            print(generations_list)
            print(generations_names_list)

            total_generations += len(generations_list)
            print(f"Models of different brands was parsed: {total_generations}")
            print(f"Total CAPTCHA: {total_captcha}")

        txt_file_path = os.path.join(
            "SRC",
            "Parsing",
            "Results",
            "Cars",
            "Generations",
            f"{brand}_{model}.txt",
        )
        folder_path = os.path.dirname(txt_file_path)
        if not exists(folder_path):
            os.makedirs(folder_path)
        with open(
            txt_file_path,
            "a",
            encoding="utf-8",
        ) as file:
            file.write(",\n".join(generations_list))

        txt_file_path = os.path.join(
            "SRC",
            "Parsing",
            "Results",
            "Cars",
            "Generations_names",
            f"{brand}_{model}.txt",
        )
        folder_path = os.path.dirname(txt_file_path)
        if not exists(folder_path):
            os.makedirs(folder_path)
        with open(
            txt_file_path,
            "a",
            encoding="utf-8",
        ) as file:
            file.write(",\n".join(generations_names_list))
        print(f"{brand} {model} WAS SAVED SUCCESSFULLY!!!")
    print(f"ALL {brand} WAS SAVED SUCCESSFULLY!!!!!!!!")


finish = time.time()
total_time = finish - start
print(f"Total time: {total_time:.2f}")

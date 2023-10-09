import sys
import os
from genericpath import exists
import requests
import time
import fake_useragent as fua
from user_agents import parse
from tqdm import tqdm
import random as rnd
import time

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
brands_list = []
params = {
    "category": "cars",
    "section": "all",
    "page": 1,
    "geo_id": [225],
    "sort": "cr_date-desc",
}

response = requests.post(url, json=params, headers=dict_headers, proxies=proxy)
page_count = response.json()

page_count = response.json()["pagination"]["total_page_count"]

data = response.json()["offers"]
print(f"Количество страниц: {page_count}")


random_ip = 0
for page in tqdm(range(1, page_count + 1)):
    params = {
        "category": "cars",
        "section": "all",
        "page": page,
        "geo_id": [225],
        "sort": "cr_date-desc",
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

    response = requests.post(url, json=params, headers=dict_headers, proxies=proxy)
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
                car_brand_csv = str(data[ad]["vehicle_info"]["mark_info"]["code"])
            except:
                pass

            if car_brand_csv not in brands_list:
                brands_list.append(car_brand_csv)

    print(f"Page: {page} was parsed!!")
    print(f"Number of brands: {len(brands_list)}")

print(f"99 PAGES WAS PARSED SUCCESSFULLY!!!")
print(f"Total Pages: {page_count}")
print(f"Total Brands: {len(brands_list)}")
print(f"Total CAPTCHA: {total_captcha}")


txt_file_path = os.path.join(
    "SRC", "Parsing", "Results", "Cars", "Brands", "brands.txt"
)
folder_path = os.path.dirname(txt_file_path)
if not exists(folder_path):
    os.makedirs(folder_path)
with open(txt_file_path, "w", encoding="utf-8") as file:
    file.write(",\n".join(brands_list))
print(brands_list)


finish = time.time()
total_time = finish - start
print(f"Total time: {total_time:.2f}")

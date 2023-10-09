from genericpath import exists
import requests
import time
import fake_useragent as fua
import random as rnd
from user_agents import parse
from tqdm import tqdm
import csv
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

total_captcha = 0

url = "https://auto.ru/-/ajax/desktop/listing/"
txt_path = os.path.join("SRC", "Parsing", "Results", "Cars", "Brands", "brands.txt")
with open(txt_path, "r", encoding="utf-8") as f:
    brands = f.read()

brands_list = brands.split(",\n")
count_brands = 0
count_models = 0
count_gens = 0

parsed_brand_list = []
parsed_model_list = []
parsed_gens_list = []

print(brands_list)
for brand in brands_list:
    count_brands += 1
    print(f"Brand: {brand}")
    parsed_brand_list.append(brand)

    txt_path_models = os.path.join(
        "SRC", "Parsing", "Results", "Cars", "Models", f"{brand}.txt"
    )
    with open(txt_path_models, "r", encoding="utf-8") as file:
        models = file.read()

    models_list = models.split(",\n")

    for model in models_list:
        count_models += 1

        print(f"Model: {model}")
        parsed_model_list.append(model)
        txt_path_generations = os.path.join(
            "SRC", "Parsing", "Results", "Cars", "Generations", f"{brand}_{model}.txt"
        )
        with open(txt_path_generations, "r", encoding="utf-8") as file:
            generations = file.read()

        generation_list = generations.split(",\n")

        for gen in generation_list:
            count_gens += 1

            print(f"GEN: {gen}")
            parsed_gens_list.append(gen)

            data_to_save = [
                f"parsed_brand_list = {parsed_brand_list}",
                f"parsed_model_list = {parsed_model_list}",
                f"parsed_gens_list = {parsed_gens_list}",
            ]

            failure_file_path = os.path.join(
                "SRC",
                "Parsing",
                "Results",
                "Cars",
                "Parsing_failure",
                f"All_cars_fail.txt",
            )
            folder_path = os.path.dirname(failure_file_path)
            if not exists(folder_path):
                os.makedirs(folder_path)
            with open(failure_file_path, "w", encoding="utf-8") as file:
                    file.write(",\n".join(data_to_save))

            params = {
                "category": "cars",
                "section": "all",
                "page": 1,
                "catalog_filter": [{"mark": brand, "model": model, "generation": gen}],
                "geo_id": [225],
                "sort": "year-asc",
            }

            response = requests.post(
                url, json=params, headers=dict_headers
            )

            page_count = response.json()["pagination"]["total_page_count"]
            if page_count > 98:
                print(
                    "Разбить данные по годам, т.к. не поместились все данные в 99 стр!!!"
                )
                print(f"количество страниц: {page_count}")
            else:
                print(f"количество страниц: {page_count}")

                random_agent = 0
                for page in tqdm(range(1, page_count + 1)):
                    params = {
                        "category": "cars",
                        "section": "all",
                        "page": 1,
                        "catalog_filter": [
                            {"mark": brand, "model": model, "generation": gen}
                        ],
                        "geo_id": [225],
                        "sort": "year-asc",
                    }

                    random_agent += 1

                    if random_agent == 3:
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
                        random_agent = 0

                    print()
                    print(f'UA: {dict_headers["User-Agent"]}')
                    print(f"RANDOM AGENT IN A ROW: {random_agent}")

                    response = requests.post(
                        url, json=params, headers=dict_headers
                    )
                    data = response.json()
                    try:
                        if data["type"] == "captcha":
                            print("======== CAPTCHA! =========")
                            total_captcha += 1
                        continue
                    except:
                        data = response.json()["offers"]

                        for ad in range(len(data)):
                            try:
                                car_brand_csv = str(
                                    data[ad]["vehicle_info"]["mark_info"]["name"]
                                )
                            except:
                                car_brand_csv = ""

                            try:
                                car_model_csv = str(
                                    data[ad]["vehicle_info"]["model_info"]["name"]
                                )
                            except:
                                car_model_csv = ""

                            try:
                                year_csv = str(data[ad]["documents"]["year"])
                            except:
                                year_csv = ""

                            try:
                                generation_csv = str(
                                    data[ad]["vehicle_info"]["super_gen"]["name"]
                                )
                            except:
                                generation_csv = ""

                            try:
                                engine_type_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"][
                                        "engine_type"
                                    ]
                                )
                            except:
                                engine_type_csv = ""

                            try:
                                drive_type_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"]["gear_type"]
                                )
                            except:
                                drive_type_csv = ""

                            try:
                                transmission_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"][
                                        "transmission"
                                    ]
                                )
                            except:
                                transmission_csv = ""

                            try:
                                engine_capacity_liters_csv = str(
                                    round(
                                        int(
                                            data[ad]["vehicle_info"]["tech_param"][
                                                "displacement"
                                            ]
                                        )
                                        / 1000,
                                        1,
                                    )
                                )
                            except:
                                engine_capacity_liters_csv = ""

                            try:
                                engine_capacity_cubic_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"][
                                        "displacement"
                                    ]
                                )
                            except:
                                engine_capacity_cubic_csv = ""

                            try:
                                engine_power_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"]["power"]
                                )
                            except:
                                engine_power_csv = ""

                            try:
                                availability_csv = str(data[ad]["availability"])
                            except:
                                availability_csv = ""

                            try:
                                mileage_csv = str(data[ad]["state"]["mileage"])
                            except:
                                mileage_csv = ""

                            try:
                                color_csv = str(data[ad]["color_hex"])
                            except:
                                color_csv = ""

                            try:
                                car_type_csv = str(data[ad]["section"])
                            except:
                                car_type_csv = ""

                            try:
                                condition_csv = str(data[ad]["state"]["condition"])
                            except:
                                condition_csv = ""

                            try:
                                price_csv = str(data[ad]["price_info"]["RUR"])
                            except:
                                price_csv = ""

                            try:
                                price_dollar_csv = str(data[ad]["price_info"]["USD"])
                            except:
                                price_dollar_csv = ""

                            try:
                                price_euro_csv = str(data[ad]["price_info"]["EUR"])
                            except:
                                price_euro_csv = ""

                            try:
                                tax_csv = str(
                                    data[ad]["owner_expenses"]["transport_tax"][
                                        "tax_by_year"
                                    ]
                                )
                            except:
                                tax_csv = ""

                            try:
                                region_csv = str(
                                    data[ad]["seller"]["location"]["region_info"][
                                        "name"
                                    ]
                                )
                            except:
                                region_csv = ""

                            try:
                                car_class_csv = str(
                                    data[ad]["vehicle_info"]["configuration"][
                                        "auto_class"
                                    ]
                                )
                            except:
                                car_class_csv = ""

                            try:
                                body_type_csv = str(
                                    data[ad]["vehicle_info"]["configuration"][
                                        "human_name"
                                    ]
                                )
                            except:
                                body_type_csv = ""

                            try:
                                doors_count_csv = str(
                                    data[ad]["vehicle_info"]["configuration"][
                                        "doors_count"
                                    ]
                                )
                            except:
                                doors_count_csv = ""

                            try:
                                trunk_volume_csv = str(
                                    data[ad]["vehicle_info"]["configuration"][
                                        "trunk_volume_min"
                                    ]
                                )
                            except:
                                trunk_volume_csv = ""

                            try:
                                steering_wheel_csv = str(
                                    data[ad]["vehicle_info"]["steering_wheel"]
                                )
                            except:
                                steering_wheel_csv = ""

                            try:
                                clearance_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"][
                                        "clearance_min"
                                    ]
                                )
                            except:
                                clearance_csv = ""

                            try:
                                acceleration_csv = str(
                                    data[ad]["vehicle_info"]["tech_param"][
                                        "acceleration"
                                    ]
                                )
                            except:
                                acceleration_csv = ""

                            try:
                                vendor_csv = str(data[ad]["vehicle_info"]["vendor"])
                            except:
                                vendor_csv = ""

                            try:
                                customs_csv = str(
                                    data[ad]["documents"]["custom_cleared"]
                                )
                            except:
                                customs_csv = ""

                            try:
                                owners_csv = str(data[ad]["documents"]["owners_number"])
                            except:
                                owners_csv = ""

                            try:
                                pts_csv = str(data[ad]["documents"]["pts"])
                            except:
                                pts_csv = ""

                            try:
                                days_csv = str(
                                    data[ad]["additional_info"]["days_on_sale"]
                                )
                            except:
                                days_csv = ""

                            try:
                                seller_csv = str(data[ad]["seller_type"])
                            except:
                                seller_csv = ""

                            try:
                                price_segment_csv = str(
                                    data[ad]["vehicle_info"]["super_gen"][
                                        "price_segment"
                                    ]
                                )
                            except:
                                price_segment_csv = ""

                            try:
                                year_from_csv = str(
                                    data[ad]["vehicle_info"]["super_gen"]["year_from"]
                                )
                            except:
                                year_from_csv = ""

                            try:
                                year_to_csv = str(
                                    data[ad]["vehicle_info"]["super_gen"]["year_to"]
                                )
                            except:
                                year_to_csv = ""

                            try:
                                price_pred_from_csv = str(
                                    data[ad]["predicted_price_ranges"]["trade_in"][
                                        "from"
                                    ]
                                )
                            except:
                                price_pred_from_csv = ""

                            try:
                                price_pred_to_csv = str(
                                    data[ad]["predicted_price_ranges"]["trade_in"]["to"]
                                )
                            except:
                                price_pred_to_csv = ""

                            try:
                                sale_id_csv = str(data[ad]["saleId"])
                            except:
                                sale_id_csv = ""

                            img_url_1200x900n = []
                            img_url_456x342n = []
                            img_url_320x240 = []

                            for img in data[ad]["state"]["image_urls"]:
                                try:
                                    img_url_1200x900n.append(img["sizes"]["1200x900n"])
                                except:
                                    pass
                                try:
                                    img_url_456x342n.append(img["sizes"]["456x342n"])
                                except:
                                    pass
                                try:
                                    img_url_320x240.append(img["sizes"]["320x240"])
                                except:
                                    pass

                            link_1200x900n = ""
                            link_456x342n = ""
                            link_320x240 = ""

                            for link in img_url_1200x900n:
                                link_1200x900n += str(link) + "\n"

                            for link in img_url_456x342n:
                                link_456x342n += str(link) + "\n"

                            for link in img_url_320x240:
                                link_320x240 += str(link) + "\n"

                            txt_file_path = os.path.join(
                                "SRC",
                                "Parsing",
                                "Results",
                                "Photo_links",
                                brand,
                                model,
                                f"{brand}_{model}_{generation_csv}_{year_from_csv}-{year_to_csv}-1200x900n.txt",
                            )

                            folder_path = os.path.dirname(txt_file_path)
                            if not exists(folder_path):
                                os.makedirs(folder_path)

                            with open(txt_file_path, "a", encoding="utf-8") as file:
                                file.write(link_1200x900n)

                            txt_file_path = os.path.join(
                                "SRC",
                                "Parsing",
                                "Results",
                                "Photo_links",
                                brand,
                                model,
                                f"{brand}_{model}_{generation_csv}_{year_from_csv}-{year_to_csv}-456x342n.txt",
                            )

                            folder_path = os.path.dirname(txt_file_path)
                            if not exists(folder_path):
                                os.makedirs(folder_path)

                            with open(txt_file_path, "a", encoding="utf-8") as file:
                                file.write(link_456x342n)

                            txt_file_path = os.path.join(
                                "SRC",
                                "Parsing",
                                "Results",
                                "Photo_links",
                                brand,
                                model,
                                f"{brand}_{model}_{generation_csv}_{year_from_csv}-{year_to_csv}-320x240.txt",
                            )

                            folder_path = os.path.dirname(txt_file_path)
                            if not exists(folder_path):
                                os.makedirs(folder_path)

                            with open(txt_file_path, "a", encoding="utf-8") as file:
                                file.write(link_320x240)

                            csv_file_path = os.path.join(
                                "SRC", "Parsing", "Results", "Data", "all_cars.csv"
                            )

                            folder_path = os.path.dirname(csv_file_path)
                            if not exists(folder_path):
                                os.makedirs(folder_path)

                            with open(
                                csv_file_path, mode="a", newline="", encoding="utf-8"
                            ) as csvfile:
                                writer = csv.writer(csvfile)
                                is_empty_file = os.path.getsize(csv_file_path) == 0
                                if is_empty_file:
                                    writer.writerow(
                                        [
                                            "brand",
                                            "model",
                                            "year",
                                            "generation",
                                            "engine_type",
                                            "drive_type",
                                            "transmission",
                                            "engine_capacity_liters",
                                            "engine_capacity_cubic",
                                            "engine_power",
                                            "availability",
                                            "mileage",
                                            "color",
                                            "car_type",
                                            "condition",
                                            "price",
                                            "prise_usd",
                                            "price_euro",
                                            "tax",
                                            "region",
                                            "car_class",
                                            "body_type",
                                            "doors_count",
                                            "trunk_volume",
                                            "steering_wheel",
                                            "clearance",
                                            "acceleration",
                                            "vendor",
                                            "customs_cleared",
                                            "owners",
                                            "pts",
                                            "days_on_sale",
                                            "seller",
                                            "price_segment",
                                            "start_sales",
                                            "end_sales",
                                            "price_pred_from",
                                            "price_pred_to",
                                            "id",
                                        ]
                                    )
                                writer.writerow(
                                    [
                                        str(car_brand_csv),
                                        str(car_model_csv),
                                        str(year_csv),
                                        str(generation_csv),
                                        str(engine_type_csv),
                                        str(drive_type_csv),
                                        str(transmission_csv),
                                        str(engine_capacity_liters_csv),
                                        str(engine_capacity_cubic_csv),
                                        str(engine_power_csv),
                                        str(availability_csv),
                                        str(mileage_csv),
                                        str(color_csv),
                                        str(car_type_csv),
                                        str(condition_csv),
                                        str(price_csv),
                                        str(price_dollar_csv),
                                        str(price_euro_csv),
                                        str(tax_csv),
                                        str(region_csv),
                                        str(car_class_csv),
                                        str(body_type_csv),
                                        str(doors_count_csv),
                                        str(trunk_volume_csv),
                                        str(steering_wheel_csv),
                                        str(clearance_csv),
                                        str(acceleration_csv),
                                        str(vendor_csv),
                                        str(customs_csv),
                                        str(owners_csv),
                                        str(pts_csv),
                                        str(days_csv),
                                        str(seller_csv),
                                        str(price_segment_csv),
                                        str(year_from_csv),
                                        str(year_to_csv),
                                        str(price_pred_from_csv),
                                        str(price_pred_to_csv),
                                        str(sale_id_csv),
                                    ]
                                )

                        print(f"Page: {page} - {brand} {model} {generation_csv}")

            print(f"Generation: {brand} {model} {generation_csv} - {gen} was parsed!")
            print(f"Total Gens was parsed: {count_gens}")
        print(f" Model: {brand} {model} was parsed!!!")
        print(f"Total models was parsed {count_models}")
        print(f"Total CAPTCHA: {total_captcha}")
    print(f"--------- ALL Brand: {brand} was parsed!! -----------")
    print(f"Total brands was parsed: {count_brands}")
print("=========== ALL BRANDS WAS PARSED!!! ============")


finish = time.time()

print(count_brands, count_models, count_gens)
total_time = finish - start
print(f"Total time: {total_time:.2f}")

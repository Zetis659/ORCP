from ultralytics import YOLO
import os
import time
import pandas as pd


def yolo_results(img_path):
    start = time.time()
    picture = img_path

    model = YOLO(os.path.join("Models", "Classification", "ALL_CARS_134.pt"))

    results = model.predict(os.path.join(picture))
    names_dict = results[0].names
    probs = results[0].probs
    top = probs.top1
    total_prob = round(float(probs.top1conf) * 100, 2)
    brands_path = os.path.join(
        "SRC", "Parsing", "Results", "Cars", "Brands", "brands.txt"
    )
    with open(brands_path, "r", encoding="utf-8") as f:
        brands = f.read()

    brands_list = brands.split(",\n")

    best_pred = names_dict[top][:-9]
    if best_pred[-1] == "-":
        best_pred = f"{best_pred[:-1]}г - настоящее время"
    else:
        best_pred = f"{best_pred}гг"

    for i in brands_list:
        if i in best_pred:
            my_brand = i

    model_path = os.path.join(
        "SRC", "Parsing", "Results", "Cars", "Models", f"{my_brand}.txt"
    )
    with open(model_path, "r", encoding="utf-8") as f:
        models = f.read()

    double_brands = [
        "SSANG_YONG",
        "LAND_ROVER",
        "GREAT_WALL",
        "ALFA_ROMEO",
        "ROLLS_ROYCE",
    ]
    models_list = models.split(",\n")
    best_pred_list = best_pred.split("_")

    double_brands_flag = 0
    for i in double_brands:
        if i in best_pred:
            double_brands_flag = 1
            break

    if double_brands_flag == 0:
        if len(best_pred_list) == 4:
            car_model = best_pred_list[1]
        elif len(best_pred_list) == 5:
            car_model = f"{best_pred_list[1]}_{best_pred_list[2]}"
        elif len(best_pred_list) == 6:
            car_model = f"{best_pred_list[1]}_{best_pred_list[2]}_{best_pred_list[3]}"
        elif len(best_pred_list) == 7:
            car_model = f"{best_pred_list[1]}_{best_pred_list[2]}_{best_pred_list[3]}_{best_pred_list[4]}"
    else:
        if len(best_pred_list) == 5:
            car_model = best_pred_list[2]
        elif len(best_pred_list) == 6:
            car_model = f"{best_pred_list[2]}_{best_pred_list[3]}"
        elif len(best_pred_list) == 7:
            car_model = f"{best_pred_list[2]}_{best_pred_list[3]}_{best_pred_list[4]}"
        elif len(best_pred_list) == 8:
            car_model = f"{best_pred_list[2]}_{best_pred_list[3]}_{best_pred_list[4]}_{best_pred_list[5]}"

    for i in models_list:
        if i == car_model:
            my_model = i
            break

    gen_path = os.path.join(
        "SRC",
        "Parsing",
        "Results",
        "Cars",
        "Generations_names",
        f"{my_brand}_{my_model}.txt",
    )
    with open(gen_path, "r", encoding="utf-8") as f:
        gens = f.read()

    gens_list = gens.split(",\n")
    my_gen = None

    for i in gens_list:
        for j in best_pred_list:
            if i == j:
                my_gen = i
                break

    if my_gen == "":
        my_gen = None

    years = f"Годы выпуска: {best_pred.split('_')[-1]}"

    if my_brand == "CHERYEXEED":
        my_brand = "EXEED"

    if my_brand == "GREAT_WALL":
        my_brand = "GREAT WALL"

    if my_model == "HOVERH3":
        my_model = "HOVER H3"

    if my_model == "HOVERH5":
        my_model = "HOVER H5"

    if my_model == "HOVER_2005":
        my_model = "HOVER"

    my_model = my_model.replace("_", " ")

    if my_gen is None:
        total = 0
        df = pd.read_csv(os.path.join("Analysis", "Prices", "NBM.csv"))

        new_quartile_25 = None
        new_quartile_75 = None
        try:
            new_quartile_25 = (
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]["25%"]
                .values[0]
            )
            new_quartile_75 = (
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]["75%"]
                .values[0]
            )
        except:
            pass

        if new_quartile_25 == None or new_quartile_75 == None:
            total += 1

        df = pd.read_csv(os.path.join("Analysis", "Prices", "UBM.csv"))

        used_quartile_25 = None
        used_quartile_75 = None

        try:
            used_quartile_25 = (
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]["25%"]
                .values[0]
            )
            used_quartile_75 = (
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]["75%"]
                .values[0]
            )
        except:
            pass

        if used_quartile_25 == None or used_quartile_75 == None:
            total += 2

        if total == 0:
            new_formatted_quartile_25 = "{:,.0f}".format(new_quartile_25).replace(
                ",", "."
            )
            new_formatted_quartile_75 = "{:,.0f}".format(new_quartile_75).replace(
                ",", "."
            )
            used_formatted_quartile_25 = "{:,.0f}".format(used_quartile_25).replace(
                ",", "."
            )
            used_formatted_quartile_75 = "{:,.0f}".format(used_quartile_75).replace(
                ",", "."
            )

            if (
                new_formatted_quartile_25 == new_formatted_quartile_75
                and used_formatted_quartile_25 == used_formatted_quartile_75
            ):
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость нового авто ≈ <b>{new_formatted_quartile_25}</b> ₽\nСредняя стоимость подержанного авто: ≈ <b>{used_formatted_quartile_25}</b> ₽"
            elif new_formatted_quartile_25 == new_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость нового авто ≈ <b>{new_formatted_quartile_25}</b> ₽\nСредняя стоимость подержанного авто: <b>от {used_formatted_quartile_25} до {used_formatted_quartile_75}</b> ₽"
            elif used_formatted_quartile_25 == used_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость нового авто: <b>от {new_formatted_quartile_25} до {new_formatted_quartile_75}</b> ₽\nСредняя стоимость подержанного авто: ≈ <b>{used_formatted_quartile_25}</b> ₽"
            else:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость нового авто: <b>от {new_formatted_quartile_25} до {new_formatted_quartile_75}</b> ₽\nСредняя стоимость подержанного авто: <b>от {used_formatted_quartile_25} до {used_formatted_quartile_75}</b> ₽"

        elif total == 1:
            used_formatted_quartile_25 = "{:,.0f}".format(used_quartile_25).replace(
                ",", "."
            )
            used_formatted_quartile_75 = "{:,.0f}".format(used_quartile_75).replace(
                ",", "."
            )
            if used_formatted_quartile_25 == used_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость подержанного авто: ≈ <b>{used_formatted_quartile_25}</b> ₽"
            else:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость подержанного авто: <b>от {used_formatted_quartile_25} до {used_formatted_quartile_75}</b> ₽"

        elif total == 2:
            new_formatted_quartile_25 = "{:,.0f}".format(new_quartile_25).replace(
                ",", "."
            )
            new_formatted_quartile_75 = "{:,.0f}".format(new_quartile_75).replace(
                ",", "."
            )
            if new_formatted_quartile_75 == new_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость нового авто ≈ <b>{new_formatted_quartile_25}</b> ₽"
            else:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость нового авто: <b>от {new_formatted_quartile_25} до {new_formatted_quartile_75}</b> ₽"

        else:
            df = pd.read_csv(os.path.join("Analysis", "Prices", "BM.csv"))

            quartile_25 = None
            quartile_75 = None

            try:
                quartile_25 = (
                    df.loc[df["brand"] == my_brand]
                    .loc[df["model"] == my_model]["25%"]
                    .values[0]
                )
                quartile_75 = (
                    df.loc[df["brand"] == my_brand]
                    .loc[df["model"] == my_model]["75%"]
                    .values[0]
                )
            except:
                pass

            if quartile_25 == None or quartile_75 == None:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}"
            else:
                formatted_quartile_25 = "{:,.0f}".format(quartile_25).replace(",", ".")
                formatted_quartile_75 = "{:,.0f}".format(quartile_75).replace(",", ".")
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\n{years}\nСредняя стоимость авто: <b>от {formatted_quartile_25} до {formatted_quartile_75}</b> ₽"

    else:
        my_gen = my_gen.upper()
        total = 0

        df = pd.read_csv(os.path.join("Analysis", "Prices", "NBMG.csv"))
        new_quartile_25 = None
        new_quartile_75 = None
        try:
            new_quartile_25 = int(
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]
                .loc[df["generation"] == my_gen]["25%"]
                .values[0]
            )
            new_quartile_75 = int(
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]
                .loc[df["generation"] == my_gen]["75%"]
                .values[0]
            )
        except:
            pass
        if new_quartile_25 == None or new_quartile_75 == None:
            total += 1

        df = pd.read_csv(os.path.join("Analysis", "Prices", "UBMG.csv"))

        used_quartile_25 = None
        used_quartile_75 = None

        try:
            used_quartile_25 = int(
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]
                .loc[df["generation"] == my_gen]["25%"]
                .values[0]
            )
            used_quartile_75 = int(
                df.loc[df["brand"] == my_brand]
                .loc[df["model"] == my_model]
                .loc[df["generation"] == my_gen]["75%"]
                .values[0]
            )
        except:
            pass

        if used_quartile_25 == None or used_quartile_75 == None:
            total += 2

        if total == 0:
            new_formatted_quartile_25 = "{:,.0f}".format(new_quartile_25).replace(
                ",", "."
            )
            new_formatted_quartile_75 = "{:,.0f}".format(new_quartile_75).replace(
                ",", "."
            )
            used_formatted_quartile_25 = "{:,.0f}".format(used_quartile_25).replace(
                ",", "."
            )
            used_formatted_quartile_75 = "{:,.0f}".format(used_quartile_75).replace(
                ",", "."
            )

            if (
                new_formatted_quartile_25 == new_formatted_quartile_75
                and used_formatted_quartile_25 == used_formatted_quartile_75
            ):
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость нового авто ≈ <b>{new_formatted_quartile_25}</b> ₽\nСредняя стоимость подержанного авто: ≈ <b>{used_formatted_quartile_25}</b> ₽"
            elif new_formatted_quartile_25 == new_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость нового авто ≈ <b>{new_formatted_quartile_25}</b> ₽\nСредняя стоимость подержанного авто: <b>от {used_formatted_quartile_25} до {used_formatted_quartile_75}</b> ₽"
            elif used_formatted_quartile_25 == used_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость нового авто: <b>от {new_formatted_quartile_25} до {new_formatted_quartile_75}</b> ₽\nСредняя стоимость подержанного авто: ≈ <b>{used_formatted_quartile_25}</b> ₽"
            else:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость нового авто: <b>от {new_formatted_quartile_25} до {new_formatted_quartile_75}</b> ₽\nСредняя стоимость подержанного авто: <b>от {used_formatted_quartile_25} до {used_formatted_quartile_75}</b> ₽"

        elif total == 1:
            used_formatted_quartile_25 = "{:,.0f}".format(used_quartile_25).replace(
                ",", "."
            )
            used_formatted_quartile_75 = "{:,.0f}".format(used_quartile_75).replace(
                ",", "."
            )

            if used_formatted_quartile_25 == used_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</>\n{years}\nСредняя стоимость подержанного авто: ≈ <b>{used_formatted_quartile_25}</b> ₽"
            else:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость подержанного авто: <b>от {used_formatted_quartile_25} до {used_formatted_quartile_75}</b> ₽"

        elif total == 2:
            new_formatted_quartile_25 = "{:,.0f}".format(used_quartile_25).replace(
                ",", "."
            )
            new_formatted_quartile_75 = "{:,.0f}".format(used_quartile_75).replace(
                ",", "."
            )
            if new_formatted_quartile_75 == new_formatted_quartile_75:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость нового авто ≈ <b>{new_formatted_quartile_25}</b> ₽"
            else:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость нового авто: <b>от {new_formatted_quartile_25} до {new_formatted_quartile_75}</b> ₽"

        else:
            df = pd.read_csv(os.path.join("Analysis", "Prices", "BMG.csv"))

            quartile_25 = None
            quartile_75 = None

            try:
                quartile_25 = int(
                    df.loc[df["brand"] == my_brand]
                    .loc[df["model"] == my_model]
                    .loc[df["generation"] == my_gen]["25%"]
                    .values[0]
                )
                quartile_75 = int(
                    df.loc[df["brand"] == my_brand]
                    .loc[df["model"] == my_model]
                    .loc[df["generation"] == my_gen]["75%"]
                    .values[0]
                )
            except:
                pass

            if quartile_25 == None or quartile_75 == None:
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}"
            else:
                formatted_quartile_25 = "{:,.0f}".format(quartile_25).replace(",", ".")
                formatted_quartile_75 = "{:,.0f}".format(quartile_75).replace(",", ".")
                all_results = f"Вероятность совпадения авто 🚗: {total_prob}% \nБренд: <b>{my_brand}</b>\nМодель: <b>{my_model}</b>\nПоколение: <b>{my_gen}</b>\n{years}\nСредняя стоимость авто: <b>от {formatted_quartile_25} до {formatted_quartile_75}</b> ₽"

    finish = time.time()
    total_time = finish - start
    print(f"Total time prediction: {total_time:.2f}")
    if total_prob >= 80:
        return all_results
    elif total_prob >= 65:
        return (
            f"""
⚠ <b>Вероятность совпадения авто ниже среднего!</b> ⚠ \
Возможно, идентификация этой модели авто <b>неточная</b>!
<b>Для наилучшего результата попробуйте отправить другое фото!</b>
Для просмотра поддерживаемых моделей авто, нажмите кнопку: <b>Инфо о боте</b>🤖\n\n"""
            + all_results
        )
    else:
        return (
            f"""
⚠ <b>Внимание! Вероятность совпадения авто низкая!</b> ⚠ \
Вероятно, данная модель авто <b>НЕ поддерживается</b> ботом или некорректно распознана!
<b>Попробуйте отправить другое фото!</b>
Для просмотра поддерживаемых моделей авто, нажмите кнопку: <b>Инфо о боте</b>🤖\n\n"""
            + all_results
        )

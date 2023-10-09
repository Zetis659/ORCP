import pandas as pd
import numpy as np
import os
import sys
import csv
import re
import time

sys.path.insert(1, os.path.join(sys.path[0], "..", ".."))
start = time.time()
# ==================== BMG =================================

df = pd.read_csv(os.path.join("SRC", "Parsing", "Results", "Data", "all_cars.csv"))

data = df

grouped = data.groupby(["brand", "model", "generation"])


def calculate_quartiles(group):
    quartiles = np.percentile(group["price"], [25, 75])
    return pd.Series({"25%": quartiles[0], "75%": quartiles[1]})


result = grouped.apply(calculate_quartiles).reset_index()

result = result.sort_values(by=["brand", "model", "generation"])

result["brand"] = result["brand"].str.upper()
result["model"] = result["model"].str.upper()
result["generation"] = result["generation"].str.upper()

result.to_csv(os.path.join("Analysis", "Prices", "BMG.csv"), index=False)

filename = os.path.join("Analysis", "Prices", "BMG.csv")

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

for row in data:
    if len(row) >= 2:
        if "BESTURN X80" in row[1]:
            row[1] = row[1].replace("BESTURN X80", "X80")

        if "EMGRAND EC7" in row[1]:
            row[1] = row[1].replace("EMGRAND EC7", "EMGRAND")

        if "E+" in row[1]:
            row[1] = row[1].replace("E+", "EPLUS")

        if "HUNTER PLUS" in row[1]:
            row[1] = row[1].replace("HUNTER PLUS", "HUNTER")

        row[1] = re.sub(r"\s*\([^)]*\)", "", row[1])
        row[1] = row[1].replace("-", " ")

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# ================================= NBMG  =======================================

data = df

filtered_data = data.query("owners == 0")
grouped = filtered_data.groupby(["brand", "model", "generation"])


def calculate_quartiles(group):
    quartiles = np.percentile(group["price"], [25, 75])
    return pd.Series({"25%": quartiles[0], "75%": quartiles[1]})


result = grouped.apply(calculate_quartiles).reset_index()

result = result.sort_values(by=["brand", "model", "generation"])

result["brand"] = result["brand"].str.upper()
result["model"] = result["model"].str.upper()
result["generation"] = result["generation"].str.upper()

result.to_csv(os.path.join("Analysis", "Prices", "NBMG.csv"), index=False)

filename = os.path.join("Analysis", "Prices", "NBMG.csv")

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

for row in data:
    if len(row) >= 2:
        if "BESTURN X80" in row[1]:
            row[1] = row[1].replace("BESTURN X80", "X80")

        if "EMGRAND EC7" in row[1]:
            row[1] = row[1].replace("EMGRAND EC7", "EMGRAND")

        if "E+" in row[1]:
            row[1] = row[1].replace("E+", "EPLUS")

        if "HUNTER PLUS" in row[1]:
            row[1] = row[1].replace("HUNTER PLUS", "HUNTER")

        row[1] = re.sub(r"\s*\([^)]*\)", "", row[1])
        row[1] = row[1].replace("-", " ")

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)


# =============================== UBMG ======================================

data = df

filtered_data = data.query("owners != 0")
grouped = filtered_data.groupby(["brand", "model", "generation"])


def calculate_quartiles(group):
    quartiles = np.percentile(group["price"], [25, 75])
    return pd.Series({"25%": quartiles[0], "75%": quartiles[1]})


result = grouped.apply(calculate_quartiles).reset_index()

result = result.sort_values(by=["brand", "model", "generation"])

result["brand"] = result["brand"].str.upper()
result["model"] = result["model"].str.upper()
result["generation"] = result["generation"].str.upper()

result.to_csv(os.path.join("Analysis", "Prices", "UBMG.csv"), index=False)

filename = os.path.join("Analysis", "Prices", "UBMG.csv")

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

for row in data:
    if len(row) >= 2:
        if "BESTURN X80" in row[1]:
            row[1] = row[1].replace("BESTURN X80", "X80")

        if "EMGRAND EC7" in row[1]:
            row[1] = row[1].replace("EMGRAND EC7", "EMGRAND")

        if "E+" in row[1]:
            row[1] = row[1].replace("E+", "EPLUS")

        if "HUNTER PLUS" in row[1]:
            row[1] = row[1].replace("HUNTER PLUS", "HUNTER")

        row[1] = re.sub(r"\s*\([^)]*\)", "", row[1])
        row[1] = row[1].replace("-", " ")

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)


# =================================== BM =============================

data = df

grouped = data.groupby(["brand", "model"])


def calculate_quartiles(group):
    quartiles = np.percentile(group["price"], [25, 75])
    return pd.Series({"25%": quartiles[0], "75%": quartiles[1]})


result = grouped.apply(calculate_quartiles).reset_index()

result = result.sort_values(by=["brand", "model"])

result["brand"] = result["brand"].str.upper()
result["model"] = result["model"].str.upper()

result.to_csv(os.path.join("Analysis", "Prices", "BM.csv"), index=False)

filename = os.path.join("Analysis", "Prices", "BM.csv")

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

for row in data:
    if len(row) >= 2:
        if "BESTURN X80" in row[1]:
            row[1] = row[1].replace("BESTURN X80", "X80")

        if "EMGRAND EC7" in row[1]:
            row[1] = row[1].replace("EMGRAND EC7", "EMGRAND")

        if "E+" in row[1]:
            row[1] = row[1].replace("E+", "EPLUS")

        if "HUNTER PLUS" in row[1]:
            row[1] = row[1].replace("HUNTER PLUS", "HUNTER")

        row[1] = re.sub(r"\s*\([^)]*\)", "", row[1])
        row[1] = row[1].replace("-", " ")

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# ======================================= NBM ======================

data = df

filtered_data = data.query("owners == 0")

grouped = filtered_data.groupby(["brand", "model"])


def calculate_quartiles(group):
    quartiles = np.percentile(group["price"], [25, 75])
    return pd.Series({"25%": quartiles[0], "75%": quartiles[1]})


result = grouped.apply(calculate_quartiles).reset_index()

result = result.sort_values(by=["brand", "model"])

result["brand"] = result["brand"].str.upper()
result["model"] = result["model"].str.upper()

result.to_csv(os.path.join("Analysis", "Prices", "NBM.csv"), index=False)

filename = os.path.join("Analysis", "Prices", "NBM.csv")

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

for row in data:
    if len(row) >= 2:
        if "BESTURN X80" in row[1]:
            row[1] = row[1].replace("BESTURN X80", "X80")

        if "EMGRAND EC7" in row[1]:
            row[1] = row[1].replace("EMGRAND EC7", "EMGRAND")

        if "E+" in row[1]:
            row[1] = row[1].replace("E+", "EPLUS")

        if "HUNTER PLUS" in row[1]:
            row[1] = row[1].replace("HUNTER PLUS", "HUNTER")

        row[1] = re.sub(r"\s*\([^)]*\)", "", row[1])
        row[1] = row[1].replace("-", " ")

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)


# ====================================== UBM =======================

data = df

filtered_data = data.query("owners != 0")

grouped = filtered_data.groupby(["brand", "model"])


def calculate_quartiles(group):
    quartiles = np.percentile(group["price"], [25, 75])
    return pd.Series({"25%": quartiles[0], "75%": quartiles[1]})


result = grouped.apply(calculate_quartiles).reset_index()

result = result.sort_values(by=["brand", "model"])

result["brand"] = result["brand"].str.upper()
result["model"] = result["model"].str.upper()

result.to_csv(os.path.join("Analysis", "Prices", "UBM.csv"), index=False)

filename = os.path.join("Analysis", "Prices", "UBM.csv")

with open(filename, "r", newline="") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

for row in data:
    if len(row) >= 2:
        if "BESTURN X80" in row[1]:
            row[1] = row[1].replace("BESTURN X80", "X80")

        if "EMGRAND EC7" in row[1]:
            row[1] = row[1].replace("EMGRAND EC7", "EMGRAND")

        if "E+" in row[1]:
            row[1] = row[1].replace("E+", "EPLUS")

        if "HUNTER PLUS" in row[1]:
            row[1] = row[1].replace("HUNTER PLUS", "HUNTER")

        row[1] = re.sub(r"\s*\([^)]*\)", "", row[1])
        row[1] = row[1].replace("-", " ")

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(
    "Программа успешно завершена. Результат сохранен в: BM.csv, BMG.csv, NBM.csv, NBMG.csv, UBM.csv, UBMG.csv"
)
finish = time.time()
total_time = finish - start
print(f"Total time: {total_time:.2f}")

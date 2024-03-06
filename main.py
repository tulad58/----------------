import csv
import pandas as pd
from datetime import datetime


months = {
    "января": "January",
    "февраля": "February",
    "марта": "March",
    "апреля": "April",
    "мая": "May",
    "июня": "June",
    "июля": "July",
    "августа": "August",
    "сентября": "September",
    "октября": "October",
    "ноября": "November",
    "декабря": "December",
}


def read_csv_data(csv_file):
    data = []
    with open(csv_file, "r", encoding="cp1251") as file:
        reader = csv.reader(file, delimiter=";")
        headers = next(reader)
        data.append(headers)
        for row in reader:
            data.append(row)
    return data


def parse_date(date_string):
    for ru_month, en_month in months.items():
        date_string = date_string.replace(ru_month, en_month)
    date_obj = datetime.strptime(date_string, "%d %B %Y г. %H:%M:%S.%f мсек")
    return date_obj


def filter_data(start_time, end_time, aperture_column, csv_file, apperture):
    start_time = parse_date(start_time)
    end_time = parse_date(end_time)

    data = read_csv_data(csv_file)
    filtered_data = [data[0]]

    prev_row = None
    for row in data[1:]:
        timestamp = parse_date(row[1])
        if start_time <= timestamp <= end_time:
            if prev_row is not None:
                diff_check = False
                for col_index in aperture_column:
                    curr_value = float(row[col_index].replace(",", "."))
                    prev_value = float(prev_row[col_index].replace(",", "."))
                    if abs(curr_value - prev_value) > apperture:
                        diff_check = True
                        break
                if diff_check:
                    filtered_data.append(row)
        prev_row = row

    return filtered_data


def write_csv_data(data, output_file):
    with open(output_file, "w", newline="", encoding="cp1251") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(data)


if __name__ == "__main__":
    start_time = "18 августа 2022 г. 00:00:00.000 мсек"
    end_time = "18 августа 2022 г. 08:00:00.000 мсек"
    aperture_column = range(3, 593)
    apperture = 0.5
    input_csv_file = "786442_Ribbon1 Сводная.csv"
    output_csv_file = "output_data4.csv"

    start = datetime.now()
    filtered_data = filter_data(
        start_time, end_time, aperture_column, input_csv_file, apperture
    )
    write_csv_data(filtered_data, output_csv_file)
    df = pd.read_csv(output_csv_file, encoding="cp1251", sep=";")
    df_sorted = df.sort_values(by="Дата и время записи")
    df_sorted.to_csv("output_sorted.csv", encoding="cp1251", sep=";", index=False)
    end = datetime.now()

    print("Время выполнения функции:", end - start)

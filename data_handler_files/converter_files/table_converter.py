import csv
import os

def convert_t(data_list):
    destiny_path=os.path.abspath("converted_csv_datas/csv_table/2021")
    file_xxx = ["json", "csv"]
    csv_name = data_list[0].replace(file_xxx[0], file_xxx[1])
    with open(destiny_path+"/"+csv_name, "w", encoding="utf-8", newline='') as file:
        csv_file = csv.writer(file)
        for i in data_list[1]:
            content = []
            for j in i:
                content.append(j)
            csv_file.writerow(content)
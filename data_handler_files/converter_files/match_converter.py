import csv
import os

def convert_m(data_list):
    destiny_path=os.path.abspath("converted_csv_datas/csv_match")
    file_xxx = ["json", "csv"]
    csv_name = data_list[1].replace(file_xxx[0], file_xxx[1])
    with open(destiny_path+"/"+csv_name, "w", encoding="UTF-8", newline='') as file:
        csv_file = csv.writer(file)
        try:
            id_header = data_list[0]["h"][0]
            csv_file.writerow(id_header)
            for ids in data_list[0].keys():
                for value in range(len(data_list[0][ids])):
                    csv_file.writerow(data_list[0][ids][value].values())
        except IndexError:
            id_header = data_list[0]["a"][0]
            csv_file.writerow(id_header)
            for ids in data_list[0].keys():
                for value in range(len(data_list[0][ids])):
                    csv_file.writerow(data_list[0][ids][value].values())
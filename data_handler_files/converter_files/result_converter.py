import csv
import os

def convert_r(data_list, delim):
    destiny_path=os.path.abspath("converted_csv_datas/csv_result/2021")
    file_xxx = ["json", "csv"]
    csv_name = data_list[0].replace(file_xxx[0], file_xxx[1])
    with open(destiny_path+"/"+csv_name, "w", newline='') as file:
        csv_file = csv.writer(file)
        for number in data_list[1]:
            header = []
            for i in number.keys():
                if isinstance(number[i], dict):
                    for j in number[i].keys():
                        header.append(str(i)+delim+str(j))
                header.append(i)
                if isinstance(number[i], dict):
                    header.remove(i)
        csv_file.writerow(header)
        for number in data_list[1]:
            content = []
            for i in number.keys():
                content.append(number[i])
                if isinstance(number[i], dict):
                    content.remove(number[i])
                    for j in number[i]:
                        content.append(str(number[i][j]))
            csv_file.writerow(content)
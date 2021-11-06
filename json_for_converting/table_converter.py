import file_caller
import csv
import sys
sys.path.append("C:\Repository\FootballScoreAI")


def convert_csv(data_list):
    with open(data_list[0], "w", encoding="utf-8", newline='') as file:
        csv_file = csv.writer(file)
        for i in data_list[1]:
            content = []
            for j in i:
                content.append(j)
            csv_file.writerow(content)


convert_csv(file_caller.caller())

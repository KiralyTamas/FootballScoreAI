import sys
sys.path.append("C:\Repository\FootballScoreAI")
import file_caller,csv

def convert_csv(data_list):
    with open(data_list[0], "w", encoding="UTF-8", newline='') as file:
        csv_file = csv.writer(file)
        id_header = data_list[1]["h"][0]
        csv_file.writerow(id_header)
        for ids in data_list[1].keys():
            for value in range(len(data_list[1][ids])):
                csv_file.writerow(data_list[1][ids][value].values())


convert_csv(file_caller.caller())

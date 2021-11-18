import pandas as pd
import os
import csv
path = os.path.abspath("teams/bundesliga")

cup = input("Melyik bajnokságról van szó?")


def create_team_csv():
    with open(cup, "r") as file:
        csv_file = csv.reader(file)
        df = pd.DataFrame(csv_file)
        for row_index, row in df.iterrows():
            if row_index == 0:
                continue
            else:
                math_id = row[0]
                team_id = [row[2], row[5]]
                teams = row[3], row[6]
                gh = [row[8], row[9]]
                pr = ""
                xg = [row[10], row[11]]
                date = row[12]
                header = ["Dátum", "Meccs-Id", "Hazai-Id", "Hazai Csapat", "Ellenfél-Id", "Ellenfél",
                          "Hazai Gól", "Ellenfél Gól", "Hazai_PR", "Ellenfél_PR", "Hazai XG", "Ellenfél XG"]
                home_data = [date, math_id, team_id[0], teams[0],
                             team_id[1], teams[1], gh[0], gh[1], pr, pr,
                             xg[0], xg[1]]
                against_data = [date, math_id, team_id[1], teams[1],
                                team_id[0], teams[0], gh[1], gh[0], pr, pr,
                                xg[1], xg[0]]
                try:
                    with open(path+"\\"+teams[0]+".csv", "r", newline='', encoding="utf-8") as home_csv_old:
                        home_table_old = csv.reader(home_csv_old)
                        home_old_list = []
                        for home_list in home_table_old:
                            home_old_list.append(home_list)
                        with open(path+"\\"+teams[0]+".csv", "a", newline='', encoding="utf-8") as home_csv:
                            home_table = csv.writer(home_csv)
                            if home_data not in home_old_list:
                                home_table.writerow(home_data)
                except FileNotFoundError:
                    with open(path+"\\"+teams[0]+".csv", "w", newline='', encoding="utf-8") as home_csv:
                        home_table = csv.writer(home_csv)
                        home_table.writerow(header)
                    create_team_csv()
                try:
                    with open(path+"\\"+teams[1]+".csv", "r", newline='', encoding="utf-8") as against_csv_old:
                        against_table_old = csv.reader(against_csv_old)
                        against_old_list = []
                        for against_list in against_table_old:
                            against_old_list.append(against_list)
                        with open(path+"\\"+teams[1]+".csv", "a", newline='', encoding="utf-8") as against_csv:
                            against_table = csv.writer(against_csv)
                            if against_data not in against_old_list:
                                against_table.writerow(against_data)
                except FileNotFoundError:
                    with open(path+"\\"+teams[1]+".csv", "w", newline='', encoding="utf-8") as against_csv:
                        against_table = csv.writer(against_csv)
                        against_table.writerow(header)
                    create_team_csv()


create_team_csv()

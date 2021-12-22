import os
import csv


def next_match():
    print("Egymás elleni elmúlt 5 mérkőzés kigyüjtése.")
    main_fixture_pr = []
    space = ["", ""]
    with open(os.path.abspath("converted_csv_datas\main_fixture\main_fixture_pr.csv"), "r") as fixture_file:
        fixture_file = csv.reader(fixture_file)
        for index,row in enumerate(fixture_file):
                if index==0:
                    continue
                with open(os.path.abspath("converted_csv_datas\main_result\main_pr_result.csv"), "r") as result_file:
                    result_file = csv.reader(result_file)
                    before_matches=[]
                    before_matches.append(space)
                    for r_row in result_file:
                        if (row[2] == r_row[2] and row[3] == r_row[3]) or (row[2] == r_row[3] and row[3] == r_row[2]):
                            r_row_list=[r_row[0], r_row[1], r_row[2], r_row[4], r_row[5], r_row[3]]
                            if len(before_matches) == 6:
                                before_matches.pop(5)
                                before_matches.insert(1, r_row_list)
                            else:
                                before_matches.append(r_row_list)
                    with open(os.path.abspath("converted_csv_datas\\team_stat\\"+str(row[2])+".csv"), "r",encoding='utf-8') as team_stat:
                        team_stat = csv.reader(team_stat)
                        team1_stat = []
                        for i in team_stat:
                            team1_stat.append(i)
                        for j in before_matches:
                            team1_stat.append(j)
                    with open(os.path.abspath("converted_csv_datas\\team_stat\\"+str(row[2])+".csv"), "w", newline='', encoding='utf-8') as file:
                        file = csv.writer(file)
                        file.writerows(team1_stat)
                    with open(os.path.abspath("converted_csv_datas\\team_stat\\"+str(row[3])+".csv"), "r",encoding='utf-8') as team_stat:
                        team_stat = csv.reader(team_stat)
                        team2_stat = []
                        for i in team_stat:
                            team2_stat.append(i)
                        for j in before_matches:
                            team2_stat.append(j)
                    with open(os.path.abspath("converted_csv_datas\\team_stat\\"+str(row[3])+".csv"), "w", newline='', encoding='utf-8') as file:
                        file = csv.writer(file)
                        file.writerows(team2_stat)
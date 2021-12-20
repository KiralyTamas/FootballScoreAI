import csv
import os


def last_10():
    header=["Dátum"]
    start_path = os.path.abspath("converted_csv_datas/teams")
    final_path = os.path.abspath("converted_csv_datas/last_10_match_stat")
    if os.path.exists(final_path) == False:
        os.mkdir(final_path)
    file_name = []
    for(dirpath, dirnames, filenames) in os.walk(start_path):
        file_name.extend(filenames)
    for file in file_name:
        team_name=file[:-4]
        team_list=[]    
        with open(start_path+"\\"+file, "r") as csv_raw_file:
            csv_file = csv.reader(csv_raw_file)
            for index, row in enumerate(csv_file):
                if index == 0:
                    continue
                elif len(team_list) == 10:
                    team_list.pop(0)
                    team_list.insert(9, row)
                else:
                    team_list.append(row)
            score=0
            for row in team_list:
                if team_name in row[2]:
                    score+=int(row[4])
                else:
                    score+=int(row[5])
            space=""
            average_score=[str(score)+":"+str(10)]
        with open(final_path+"\\"+file, "w",newline='',encoding='utf-8') as csv_raw_file:
                csv_raw_file=csv.DictWriter(csv_raw_file,fieldnames=header)
                csv_raw_file.writeheader()
        with open(final_path+"\\"+file, "a",newline='',encoding='utf-8') as file:
            csv_file=csv.writer(file)
            csv_file.writerows(team_list)
            csv_file.writerow(space)
            csv_file.writerow(average_score)

last_10()

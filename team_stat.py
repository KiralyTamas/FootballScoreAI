import csv
import os


def last_10():
    header=["Dátum","Meccs-ID","Hazai-Csapat","Hazai-Gól","Vendég-Gól","Vendég csapat"]
    start_path = os.path.abspath("converted_csv_datas/teams")
    final_path = os.path.abspath("converted_csv_datas/team_stat")
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
                edited_row=[row[0],row[1],row[2],row[4],row[5],row[3],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]]
                if index == 0:
                    continue
                elif len(team_list) == 10:
                    team_list.pop(0)
                    team_list.insert(9, edited_row)
                else:
                    team_list.append(edited_row)
            score=0
            counter_score=0
            for row in team_list:
                if team_name in row[2]:
                    score+=int(row[3])
                    counter_score+=int(row[4])
                else:
                    score+=int(row[4])
                    counter_score+=int(row[3])
            space=["",""]
            team_info=[]
            average_score=["Utolsó 10 meccsen szerzett góljai:",str(score)+":"+str(10),"Utolsó 10 meccsen kapott góljai:",str(counter_score)+":"+str(10)]
            score_per_match=["Meccsenkénti átlag szerzett gólok:",str(int(score)/10),"Meccsenkénti átlag kapott gólok:",str(int(counter_score)/10)]
            team_info.append(space)
            team_info.append(average_score)
            team_info.append(score_per_match)
        with open(final_path+"\\"+file, "w",newline='',encoding='utf-8') as csv_raw_file:
                csv_raw_file=csv.DictWriter(csv_raw_file,fieldnames=header)
                csv_raw_file.writeheader()
        with open(final_path+"\\"+file, "a",newline='',encoding='utf-8') as file:
            csv_file=csv.writer(file)
            csv_file.writerows(team_list)
            csv_file.writerows(team_info)

last_10()

import pandas as pd
import os
import csv
from data_handler_files.converter_files.calculater import calculate as cal

final_path = os.path.abspath("teams")
start_path=input("Mi a konvertálandó fájlok mappájának útvonala: ")

def create_team_csv():
    result_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Ellenfél-Csapat",
                     "Hazai-Gól", "Ellenfél-Gól", "Hazai-XG", "Ellenfél-XG", 
                     "Hazai-PR", "Ellenfél-PR","PR-diff","Hazai-xgPR","Ellenfél-xgPR",
                     "Hazai-Mixed-PR","Ellenfél-Mixed-PR","H%","D%","A%","ForeCast-W",
                     "ForeCast-D","ForeCast-A"]
    team_header=["Dátum","Meccs-Id","Fő-Csapat","Ellenfél-Csapat","Hazai-Gól",
                 "Ellenfél-Gól","Hazai-PR","Ellenfél-PR","Hazai-xgPR",
                 "Ellenfél-xg-PR","Hazai-Mixed-PR","Ellenfél-Mixed-PR"]
    f = []
    g = []
    h = []
    for (dirpath, dirnames, filenames) in os.walk(start_path):
        f.extend(filenames)
        g.extend(dirnames)
        h.append(dirpath)
    for path in h:
        for file in f:
            print(file)
            try:
                with open(path+"\\"+file, "r") as file:
                    csv_file = csv.reader(file)
                    df = pd.DataFrame(csv_file)
                    for row_index, row in df.iterrows():
                        if row_index == 0:
                            with open(os.path.abspath("main_result")+"\\main_result.csv","r",newline='',encoding="utf-8")as main:
                                main_list=csv.reader(main)
                                check_list=[]
                                for i in main_list:
                                    check_list.append(i)
                                    if result_header == check_list[0]:
                                        continue
                                    else:
                                        with open(os.path.abspath("main_result")+"\\main_result.csv","w",newline='',encoding="utf-8")as main:
                                            main_list=csv.writer(main)
                                            main_list.writerow(result_header)
                        else:
                            datas=cal(row,team_header)
                            math_id = row[0]
                            teams = row[3], row[6]
                            score = [row[8], row[9]]
                            xg = [row[10], row[11]]
                            date = row[12]
                            pr_diff=datas[0]-datas[1]
                            pr_diff=("%.4f" % pr_diff)
                            datas[0]=("%.4f" % datas[0])
                            datas[1]=("%.4f" % datas[1])
                            datas[2]=("%.4f" % datas[2])
                            datas[3]=("%.4f" % datas[3])
                            datas[4]=("%.4f" % datas[4])
                            datas[5]=("%.4f" % datas[5])   
                            pr=""
                            forecast=[row[13],row[14],row[15]]
                            main_result=[date,math_id,teams[0],teams[1],score[0],
                                         score[1],xg[0],xg[1],datas[0],datas[1],pr_diff,datas[2],datas[3],datas[4],
                                         datas[5],pr,pr,pr,forecast[0],forecast[1],forecast[2]]
                            home_data = [date, math_id, teams[0],
                                         teams[1], score[0], score[1],datas[0], datas[1],
                                         datas[2],datas[3],datas[4],datas[5]]
                            against_data = [date, math_id, teams[1],
                                            teams[0], score[1], score[0], datas[1], datas[0],
                                            datas[3],datas[2],datas[5],datas[4]]
                            with open(os.path.abspath("main_result")+"\\main_result.csv","a",newline='',encoding="utf-8")as main:
                                main=csv.writer(main)
                                main.writerow(main_result)
                            try:
                                with open(final_path+"\\"+teams[0]+".csv", "r", newline='', encoding="utf-8") as home_csv_old:
                                    home_table_old = csv.reader(home_csv_old)
                                    home_old_list = []
                                    for home_list in home_table_old:
                                        home_old_list.append(home_list)
                                    with open(final_path+"\\"+teams[0]+".csv", "a", newline='', encoding="utf-8") as home_csv:
                                        home_table = csv.writer(home_csv)
                                        if home_data not in home_old_list:
                                            home_table.writerow(home_data)
                            except FileNotFoundError:
                                print("Átküldve1")
                            try:
                                with open(final_path+"\\"+teams[1]+".csv", "r", newline='', encoding="utf-8") as against_csv_old:
                                    against_table_old = csv.reader(
                                        against_csv_old)
                                    against_old_list = []
                                    for against_list in against_table_old:
                                        against_old_list.append(
                                            against_list)
                                    with open(final_path+"\\"+teams[1]+".csv", "a", newline='', encoding="utf-8") as against_csv:
                                        against_table = csv.writer(against_csv)
                                        if against_data not in against_old_list:
                                            against_table.writerow(against_data)
                            except FileNotFoundError:
                                    print("Átküldve2")
                                    if FileNotFoundError == True:
                                        print("Átküldve3")
                                        continue
            except FileNotFoundError:
                if FileNotFoundError == True:
                    print("Szar")
                    continue


create_team_csv()

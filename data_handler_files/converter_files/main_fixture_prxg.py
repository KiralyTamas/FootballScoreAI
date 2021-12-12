import datetime
import os
import csv
from date_time_sorter import date_sorting
from datetime import date as tdate
from datetime import datetime


def fixture_prxg():
    print("fixture_prxg")
    fixture_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Vendég-Csapat", "Hazai-PRXG", "Vendég-PRXG", "PRXG-diff",
        "PRXG-diff-darabszám", "H%", "D%", "A%", "Több mint 3", "3", "2", "1", "0", "-1", "-2", "-3", "Több mint -3"]
    with open(os.path.abspath("..\..\converted_csv_datas\main_fixture\main_fixture_prxg.csv"), "w", newline='', encoding='utf-8') as file:
        new_file = csv.DictWriter(file, dialect='excel',fieldnames=fixture_header)
        new_file.writeheader()
    main_dir = str()
    files = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.abspath("..\..\converted_csv_datas\csv_fixtures")):
        main_dir=dirpath
        files.extend(filenames)
        pr_diff=[]
        home_prxg=[]
        against_prxg=[]
        diff_count=[]
        home_win=[]
        deal_win=[]
        against_win=[]
        score_diff__more = []
        score_diff__3 = []
        score_diff__2 = []
        score_diff__1 = []
        score_diff_0 = []
        score_diff_1 = []
        score_diff_2 = []
        score_diff_3 = []
        score_diff_more =[]
        fixture_row=[]
    for file in files:
        with open(os.path.abspath(main_dir+"/"+file),"r") as file:
            file=csv.reader(file)
            for index,match in enumerate(file):
                if index == 0:
                    continue
                date=match[12]
                match_id=match[0]
                home_team=match[3]
                against_team=match[6]
                with open(os.path.abspath("..\..\converted_csv_datas\main_fixture\main_fixture_prxg.csv"),"r") as file:
                    file=csv.reader(file)
                    fix_table=[]
                    for row in file:
                        fix_table.append(str(row[2]))
                        fix_table.append(str(row[3]))
                        today=tdate.today()
                        date_str1=str(match[-1][:10])
                        date_str2=today.strftime("%Y-%m-%d")
                        date_dt1=datetime.strptime(date_str1, '%Y-%m-%d')
                        date_dt2=datetime.strptime(date_str2, '%Y-%m-%d')
                    if date_dt1<date_dt2:
                        continue
                    if str(home_team) in fix_table:
                        continue
                    elif str(against_team) in fix_table:
                        continue
                    home_team_row=[]
                    with open(os.path.abspath("..\..\converted_csv_datas\\teams"+"/"+match[3]+".csv"),"r") as team:
                        team_table=csv.reader(team)
                        for row in team_table:
                            home_team_row.append(row)
                        home_prxg=home_team_row[-1][16]
                    against_team_row=[]
                    with open(os.path.abspath("..\..\converted_csv_datas\\teams"+"/"+match[6]+".csv"),"r") as team:
                        team_table=csv.reader(team)
                        for row in team_table:
                            against_team_row.append(row)
                        against_prxg=against_team_row[-1][16]
                    pr_diff=float(home_prxg)-float(against_prxg)
                    pr_diff=("%.1f" % pr_diff)    
                    with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv","r") as result:
                        result_table=csv.reader(result)
                        for row in result_table:
                            if pr_diff == row[16]:
                                diff_count=row[17]
                                home_win=row[18]
                                deal_win=row[19]
                                against_win=row[20]
                                score_diff__more = row[21]
                                score_diff__3 = row[22]
                                score_diff__2 = row[23]
                                score_diff__1 = row[24]
                                score_diff_0 = row[25]
                                score_diff_1 = row[26]
                                score_diff_2 = row[27]
                                score_diff_3 = row[28]
                                score_diff_more =row[29]
                                fixture_row=[date,match_id,home_team,against_team,home_prxg,against_prxg,pr_diff,diff_count,
                                            home_win,deal_win,against_win,score_diff_more,score_diff_3,score_diff_2,
                                            score_diff_1,score_diff_0,score_diff__1,score_diff__2,score_diff__3,score_diff__more]
                    with open(os.path.abspath("..\..\converted_csv_datas\main_fixture\main_fixture_prxg.csv"),"a",newline='',encoding="utf-8") as file:
                        file=csv.writer(file, dialect='excel')
                        file.writerow(fixture_row)
    date_sorting("..\..\converted_csv_datas\main_fixture\\main_fixture_prxg.csv")
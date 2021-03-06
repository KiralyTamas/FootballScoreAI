import pandas as pd    # Modulok meghívása
import os
import csv
from data_handler_files.converter_files.calculater import calculate as cal
from data_handler_files.converter_files.pr_percentage_calculate import percentage_calculate as per_cal

# A csapatok mappájának abszolúlt elérési útvonala
final_path = os.path.abspath("converted_csv_datas\\teams")
# Itt kérdezi meg a terminálban az útvonalat, a csv_result mappát kell belehúzni a terminálba.
start_path = os.path.abspath("converted_csv_datas\csv_result")


def create_team_csv(info):  # Függvény kezdete
    result_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Ellenfél-Csapat",  # A main_result és a csapat_csv-k fejlécének elnevezései
                     "Hazai-Gól", "Ellenfél-Gól", "Hazai-XG", "Ellenfél-XG",
                     "Hazai-PR", "Ellenfél-PR", "PR-diff", "Hazai-xgPR", "Ellenfél-xgPR",
                     "XG-diff", "Hazai-Mixed-PR", "Ellenfél-Mixed-PR", "Mixed-PR-diff", "PR-diff-darabszám", "H%", "D%", "A%", "Több mint 3", "3", "2", "1", "0", "-1", "-2", "-3", "Több mint -3", "ForeCast-W",
                     "ForeCast-D", "ForeCast-A"]
    team_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Vendég-Csapat", "Hazai-Gól",
                   "Ellenfél-Gól", "Hazai-XG", "Ellenfél-XG", "Ellenfél-PR", "Meccs-Előtti-PR", "Meccs-Utáni-PR", "Vendég-xgPR", "Meccs-Előtti-xgPR",
                   "Meccs-Utáni-xgPR", "Vendég-Mixed_PR", "Meccs-Előtti-Mixed_PR", "Meccs-Utáni-Mixed_PR"]
    f = []  # A "h" tárolja a mappa útvonalakat, az "f" a mappákban lévő fájlok neveit
    g = []
    path = []
    #season=input("Add meg a konvertálni kívánt szezon évszámát: ")
    # Az os.walk iterál végig a csv_result mappa almappáin és az azokban lévő fájlokon.
    for (dirpath, dirnames, filenames) in os.walk(start_path):
        f.extend(filenames)
        g.extend(dirnames)
        path.append(dirpath)
    # Az első "for" a mappákon iterál végig, a második "for" a mappákban lévő fájlokon.
    for dir_results in g:
        for file in f:
            if str(info) not in file:
                continue
            print(file)
            try:
                # Megnyitja a "for" által megadott aktuális csv_result fájlt, "df" változóba kilistázza, aztán végigiterál rajta.
                with open(path[0]+"\\"+dir_results+"\\"+file, "r") as file:
                    csv_file = csv.reader(file)
                    df = pd.DataFrame(csv_file)
                    for row_index, row in df.iterrows():
                        # Minden fájlban van fejléc. Az új fájl 0-adik indexén a fejléc van.
                        if row_index == 0:
                            # Ha ennél a sornál jár az iteráció, megvizsgálja, hogy létezik-e a main_result csv fájl.
                            if os.path.exists(os.path.abspath("converted_csv_datas\main_result")+"\\main_result.csv") == False:
                                # Ha létezik, akkor szimplán átugorja ezt az iterált sort. Ha nem, akkor létrehozza a fájlt és beírja
                                with open(os.path.abspath("converted_csv_datas\main_result")+"\\main_result.csv", "w", newline='', encoding="utf-8") as main:
                                    # Az előzőleg a result_header változóba eltárolt fejlecet.
                                    main_list = csv.writer(main, dialect='excel')
                                    main_list.writerow(result_header)
                        else:
                            # A cal(row, team_header) meghívásával átadjuk az aktuálisan iterált csv_result fájl sorát és a csapat_csv fejlécét.
                            datas = cal(row, team_header)
                            # Visszaérkeznek a "calculater" által küldött "datas" adatok.
                            pr = "-"
                            # A csv_result-ből kivett adatok "row"-ként vannak behívva, a calculater adatai "datas"-ként szerepel,
                            datas[0] = ("%.3f" % datas[0])
                            datas[1] = ("%.3f" % datas[1])
                            datas[2] = ("%.3f" % datas[2])
                            datas[3] = ("%.3f" % datas[3])
                            datas[4] = ("%.3f" % datas[4])
                            datas[5] = ("%.3f" % datas[5])
                            datas[6] = ("%.3f" % datas[6])
                            datas[7] = ("%.3f" % datas[7])
                            datas[8] = ("%.3f" % datas[8])
                            date = row[12]
                            math_id = row[0]
                            teams = row[3], row[6]
                            score_h = row[8]
                            score_a = row[9]
                            xg = [row[10], row[11]]
                            pr_diff = float(datas[0])-float(datas[1])
                            xg_diff = float(datas[2])-float(datas[3])
                            prxg_diff = float(datas[4])-float(datas[5])
                            new_hpr=(float(datas[0])+float(datas[6]))
                            new_apr=(float(datas[1])-float(datas[6]))
                            new_hxg=(float(datas[2])+float(datas[7]))
                            new_axg=(float(datas[3])-float(datas[7]))
                            new_hprxg=(float(datas[4])+float(datas[8]))
                            new_aprxg=(float(datas[5])-float(datas[8]))
                            new_hpr=("%.3f" % new_hpr)
                            new_apr=("%.3f" % new_apr)
                            new_hxg=("%.3f" % new_hxg)
                            new_axg=("%.3f" % new_axg)
                            new_hprxg=("%.3f" % new_hprxg)
                            new_aprxg=("%.3f" % new_aprxg)
                            if pr_diff == -0 or -0.0:  # Itt van javítva a -0 anomália
                                pr_diff = 0
                            if xg_diff == -0 or -0.0:
                                xg_diff = 0
                            if prxg_diff == -0 or -0.0:
                                prxg_diff = 0
                            # Itt vannak beállítva a tizedesjegyek hossza
                            pr_diff = ("%.1f" % pr_diff)
                            xg_diff = ("%.1f" % xg_diff)
                            prxg_diff = ("%.1f" % prxg_diff)     # Itt van kitöltve a main_result és a hazai--vendég csapatok kitöltési dataszerkezete attól függően, hazai vagy vendég
                            forecast = [row[13], row[14], row[15]]
                            main_result = [date, math_id, teams[0], teams[1], score_h,
                                           score_a, xg[0], xg[1], datas[0], datas[1], pr_diff, datas[2], datas[3], xg_diff, datas[4],
                                           datas[5], prxg_diff, pr, pr, pr, pr, pr, pr, pr, pr, pr, pr, pr, pr, pr, forecast[0], forecast[1], forecast[2]]
                            home_data = [date, math_id, "(H) "+teams[0],
                                         "(V) " +
                                         teams[1], score_h, score_a, xg[0], xg[1], datas[1], datas[0], new_hpr,
                                         datas[3], datas[2], new_hxg, datas[5], datas[4], new_hprxg]
                            against_data = [date, math_id,"(H) " +teams[0],
                                            "(V) "+teams[1], score_h,score_a, xg[1], xg[0], datas[0], datas[1], new_apr,
                                            datas[2], datas[3], new_axg, datas[4], datas[5], new_aprxg]
                            with open(os.path.abspath("converted_csv_datas\main_result")+"\\main_result.csv", "r") as read_main:
                                read_main = csv.reader(read_main)
                                list_id = []
                                for index, i in enumerate(read_main):
                                    if index == 0:
                                        continue
                                    list_id.append(int(i[1]))
                                if int(main_result[1]) in list_id:
                                    continue
                                else:
                                    with open(os.path.abspath("converted_csv_datas\main_result")+"\\main_result.csv", "a", newline='', encoding="utf-8")as main:
                                        main = csv.writer(main, dialect='excel')
                                        main.writerow(main_result)
                                with open(final_path+"\\"+teams[0]+".csv", "r", newline='', encoding="utf-8") as home_csv_old:
                                    home_table_old = csv.reader(home_csv_old)
                                    home_old_date=[]
                                    for home_list in home_table_old:
                                        home_old_date.append(home_list[0])
                                    if home_data[0] not in home_old_date:
                                        with open(final_path+"\\"+teams[0]+".csv", "a", newline='', encoding="utf-8") as home_csv:
                                            home_table = csv.writer(home_csv, dialect='excel')
                                            home_table.writerow(home_data)
                                with open(final_path+"\\"+teams[1]+".csv", "r", newline='', encoding="utf-8") as against_csv_old:
                                    against_table_old = csv.reader(against_csv_old)
                                    against_old_date=[]
                                    for against_list in against_table_old:
                                        against_old_date.append(against_list[0])
                                    if against_data[0] not in against_old_date:
                                        with open(final_path+"\\"+teams[1]+".csv", "a", newline='', encoding="utf-8") as against_csv:
                                            against_table = csv.writer(against_csv, dialect='excel')
                                            against_table.writerow(against_data)
            except FileNotFoundError:
                continue
    per_cal("converted_csv_datas\main_result\\main_result.csv",result_header)




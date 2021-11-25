# Modulok meghívása
import pandas as pd
import os
import csv
# A kalkulátor fájl behívása
from data_handler_files.converter_files.calculater import calculate as cal

# A csapatok mappájának abszolúlt elérési útvonala
final_path = os.path.abspath("teams")
# Itt kérdezi meg a terminálban az útvonalat, a csv_result mappát kell belehúzni a terminálba.
start_path = os.path.abspath("converted_csv_datas\csv_result")

# Függvény kezdete
def create_team_csv():
# A main_result és a csapat_csv-k fejlécének elnevezései
  result_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Ellenfél-Csapat",
                  "Hazai-Gól", "Ellenfél-Gól", "Hazai-XG", "Ellenfél-XG",
                  "Hazai-PR", "Ellenfél-PR", "PR-diff", "Hazai-xgPR", "Ellenfél-xgPR",
                  "XG-diff","Hazai-Mixed-PR", "Ellenfél-Mixed-PR","Mixed-PR-diff", "H%", "D%", "A%", "ForeCast-W",
                  "ForeCast-D", "ForeCast-A"]
  team_header = ["Dátum", "Meccs-Id", "Fő-Csapat", "Ellenfél-Csapat", "Hazai-Gól",
                "Ellenfél-Gól", "Meccs-Előtti-PR", "Meccs-Utáni-PR", "Meccs-Előtti-xgPR",
                "Meccs-Utáni-xgPR", "Meccs-Előtti-Mixed_PR", "Meccs-Utáni-Mixed_PR"]
# Az os.walk iterál végig a csv_result mappa almappáin és az azokban lévő fájlokon.
# A "h" tárolja a mappa útvonalakat, az "f" a mappákban lévő fájlok neveit
  f = []
  g = []
  h = []
  for (dirpath, dirnames, filenames) in os.walk(start_path):
    f.extend(filenames)
    g.extend(dirnames)
    h.append(dirpath)
# Az első "for" a mappákon iterál végig, a második "for" a mappákban lévő fájlokon.
  for path in h:
    for file in f:
      print(file)
      try:
# Megnyitja a "for" által megadott aktuális csv_result fájlt, "df" változóba kilistázza, aztán végigiterál rajta.
        with open(path+"\\"+file, "r") as file:
          csv_file = csv.reader(file)
          df = pd.DataFrame(csv_file)
          for row_index, row in df.iterrows():
# Minden fájlban van fejléc. Az új fájl 0-adik indexén a fejléc van.
# Ha ennél a sornál jár az iteráció, megvizsgálja, hogy létezik-e a main_result csv fájl.
# Ha létezik, akkor szimplán átugorja ezt az iterált sort. Ha nem, akkor létrehozza a fájlt és beírja
# Az előzőleg a result_header változóba eltárolt fejlecet.
            if row_index == 0:
              if os.path.exists(os.path.abspath("main_result")+"\\main_result.csv") == False:
                with open(os.path.abspath("main_result")+"\\main_result.csv", "w", newline='',encoding="utf-8") as main:
                  main_list = csv.writer(main, dialect='excel')
                  main_list.writerow(result_header)
            else:
# A cal(row, team_header) meghívásával átadjuk az aktuálisan iterált csv_result fájl sorát és a csapat_csv fejlécét.
                datas = cal(row, team_header)
# Visszaérkeznek a "calculater" által küldött "datas" adatok.
# A csv_result-ből kivett adatok "row"-ként vannak behívva, a calculater adatai "datas"-ként szerepel,
                pr = ""
                date = row[12]
                math_id = row[0]
                teams = row[3], row[6]
                score = [row[8], row[9]]
                xg = [row[10], row[11]]
                pr_diff = datas[6]-datas[7]
                xg_diff=datas[8]-datas[9]
                prxg_diff=datas[10]-datas[11]
# Itt van javítva a -0 anomália
                if pr_diff == -0 or -0.0:
                  pr_diff=0
                if xg_diff == -0 or -0.0:
                  xg_diff=0
                if prxg_diff == -0 or -0.0:
                  prxg_diff=0
# Itt vannak beállítva a tizedesjegyek hossza
                pr_diff = ("%.2f" % pr_diff)
                xg_diff = ("%.2f" % xg_diff)
                prxg_diff = ("%.2f" % prxg_diff)
                datas[0] = ("%.4f" % datas[0])
                datas[1] = ("%.4f" % datas[1])
                datas[2] = ("%.4f" % datas[2])
                datas[3] = ("%.4f" % datas[3])
                datas[4] = ("%.4f" % datas[4])
                datas[5] = ("%.4f" % datas[5])
# Itt van kitöltve a main_result és a hazai--vendég csapatok kitöltési dataszerkezete attól függően, hazai vagy vendég
                forecast = [row[13], row[14], row[15]]
                main_result = [date, math_id, teams[0], teams[1], score[0],
                              score[1], xg[0], xg[1], datas[6], datas[7], pr_diff, datas[8], datas[9],pr_diff, datas[10],
                              datas[11],pr_diff, pr, pr, pr, forecast[0], forecast[1], forecast[2]]
                home_data = [date, math_id, teams[0],
                            teams[1], score[0], score[1], datas[6], datas[0],
                            datas[8], datas[2], datas[10], datas[4]]
                against_data = [date, math_id, teams[1],
                              teams[0], score[1], score[0], datas[7], datas[1],
                              datas[9], datas[3], datas[11], datas[5]]
# Ha a main_resultben már szerepel az aktuális adatsor Pl: Bővítés esetén, nem duplikálja a sort és a csapatfájlokba
# se engedi beírni az adatokat, ezáltal sehol sem duplikál.
                with open(os.path.abspath("main_result")+"\\main_result.csv", "r") as read_main:
                  read_main = csv.reader(read_main)
                  list_match_id = []
                  list_main=[]
                  for index,i in enumerate(read_main):
                    if main_result[1] in i:
                      print(index)
                      continue
                  else:
                    with open(os.path.abspath("main_result")+"\\main_result.csv", "a", newline='',encoding="utf-8")as main:
                      main = csv.writer(main, dialect='excel')
                      main.writerow(main_result)
                with open(final_path+"\\"+teams[0]+".csv", "r", newline='', encoding="utf-8") as home_csv_old:
                  home_table_old = csv.reader(home_csv_old)
                  home_old_list = []
                  for home_list in home_table_old:
                    home_old_list.append(home_list)
                  if [home_data] not in home_old_list:
                    with open(final_path+"\\"+teams[0]+".csv", "a", newline='', encoding="utf-8") as home_csv:
                      home_table = csv.writer(home_csv, dialect='excel')
                      home_table.writerow(home_data)
                with open(final_path+"\\"+teams[1]+".csv", "r", newline='', encoding="utf-8") as against_csv_old:
                  against_table_old = csv.reader(against_csv_old)
                  against_old_list = []
                  for against_list in against_table_old:
                    against_old_list.append(
                    against_list)
                with open(final_path+"\\"+teams[1]+".csv", "a", newline='', encoding="utf-8") as against_csv:
                  against_table = csv.writer(against_csv, dialect='excel')
                  if against_data not in against_old_list:
                    against_table.writerow(against_data)
      except FileNotFoundError:
        if FileNotFoundError == True:
          print("Szar")
          continue

create_team_csv()

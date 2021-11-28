# Modulok meghívása
import pandas as pd
import os
import csv
# A kalkulátor fájl behívása
from calculater import calculate as cal

# A csapatok mappájának abszolúlt elérési útvonala
final_path = os.path.abspath("..\..\converted_csv_datas\\teams")
# Itt kérdezi meg a terminálban az útvonalat, a csv_result mappát kell belehúzni a terminálba.
start_path = os.path.abspath("..\..\converted_csv_datas\csv_result")
print(start_path)

# Függvény kezdete
def create_team_csv():
# A main_result és a csapat_csv-k fejlécének elnevezései
  result_header = ["Dátum", "Meccs-Id", "Hazai-Csapat", "Ellenfél-Csapat",
                  "Hazai-Gól", "Ellenfél-Gól", "Hazai-XG", "Ellenfél-XG",
                  "Hazai-PR", "Ellenfél-PR", "PR-diff", "Hazai-xgPR", "Ellenfél-xgPR",
                  "XG-diff","Hazai-Mixed-PR", "Ellenfél-Mixed-PR","Mixed-PR-diff", "H%", "D%", "A%", "ForeCast-W",
                  "ForeCast-D", "ForeCast-A"]
  team_header = ["Dátum", "Meccs-Id", "Fő-Csapat", "Ellenfél-Csapat","Hazai-Gól",
                "Ellenfél-Gól","Hazai-XG","Ellenfél-XG", "Meccs-Előtti-PR", "Meccs-Utáni-PR", "Meccs-Előtti-xgPR",
                "Meccs-Utáni-xgPR", "Meccs-Előtti-Mixed_PR", "Meccs-Utáni-Mixed_PR"]
# Az os.walk iterál végig a csv_result mappa almappáin és az azokban lévő fájlokon.
# A "h" tárolja a mappa útvonalakat, az "f" a mappákban lévő fájlok neveit
  f = []
  g = []
  path = []
  for (dirpath, dirnames, filenames) in os.walk(start_path):
    f.extend(filenames)
    g.extend(dirnames)
    path.append(dirpath)
# Az első "for" a mappákon iterál végig, a második "for" a mappákban lévő fájlokon.
  for dir_results in g:
    for file in f:
      print(file)
# Megnyitja a "for" által megadott aktuális csv_result fájlt, "df" változóba kilistázza, aztán végigiterál rajta.
      try:
        with open(path[0]+"\\"+dir_results+"\\"+file, "r") as file:
          csv_file = csv.reader(file)
          df = pd.DataFrame(csv_file)
          for row_index, row in df.iterrows():
# Minden fájlban van fejléc. Az új fájl 0-adik indexén a fejléc van.
# Ha ennél a sornál jár az iteráció, megvizsgálja, hogy létezik-e a main_result csv fájl.
# Ha létezik, akkor szimplán átugorja ezt az iterált sort. Ha nem, akkor létrehozza a fájlt és beírja
# Az előzőleg a result_header változóba eltárolt fejlecet.
            if row_index == 0:
              if os.path.exists(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv") == False:
                with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "w", newline='',encoding="utf-8") as main:
                  main_list = csv.writer(main, dialect='excel')
                  main_list.writerow(result_header)
            else:
# A cal(row, team_header) meghívásával átadjuk az aktuálisan iterált csv_result fájl sorát és a csapat_csv fejlécét.
                datas=cal(row, team_header)
# Visszaérkeznek a "calculater" által küldött "datas" adatok.
# A csv_result-ből kivett adatok "row"-ként vannak behívva, a calculater adatai "datas"-ként szerepel,
                pr = ""
                date = row[12]
                math_id = row[0]
                teams = row[3], row[6]
                score_h = row[8]
                score_a=row[9]
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
                pr_diff = ("%.1f" % pr_diff)
                xg_diff = ("%.1f" % xg_diff)
                prxg_diff = ("%.1f" % prxg_diff)
                datas[0] = ("%.4f" % datas[0])
                datas[1] = ("%.4f" % datas[1])
                datas[2] = ("%.4f" % datas[2])
                datas[3] = ("%.4f" % datas[3])
                datas[4] = ("%.4f" % datas[4])
                datas[5] = ("%.4f" % datas[5])
# Itt van kitöltve a main_result és a hazai--vendég csapatok kitöltési dataszerkezete attól függően, hazai vagy vendég
                forecast = [row[13], row[14], row[15]]
                main_result = [date, math_id, teams[0], teams[1], score_h,
                              score_a, xg[0], xg[1], datas[6], datas[7], pr_diff, datas[8], datas[9],xg_diff, datas[10],
                              datas[11],prxg_diff, pr, pr, pr, forecast[0], forecast[1], forecast[2]]
                home_data = [date, math_id,"(H) "+teams[0],
                            "(V) "+teams[1], score_h, score_a,xg[0], xg[1], datas[6], datas[0],
                            datas[8], datas[2], datas[10], datas[4]]
                against_data = [date, math_id,"(V) "+teams[1],
                              "(H) "+teams[0], score_a, score_h,xg[1], xg[0], datas[7], datas[1],
                              datas[9], datas[3], datas[11], datas[5]]
# Ha a main_resultben már szerepel az aktuális adatsor Pl: Bővítés esetén, nem duplikálja a sort és a csapatfájlokba
# se engedi beírni az adatokat, ezáltal sehol sem duplikál.
                with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "r") as read_main:
                  read_main = csv.reader(read_main)
                  list_id=[]
                  count=0
                  home_count=0
                  deal_count=0
                  against_count=0
                  for i in read_main:
                    try:
                      list_id.append(int(i[1]))
                      if main_result[10] == i[10]:
                        count+=1
                        final_score=int(i[4])-int(i[5])
                        if int(final_score) > 0:
                          home_count+=1
                        elif int(final_score) < 0:
                          against_count+=1
                        else:
                          deal_count+=1
                    except ValueError:
                      continue
                  try:
                      home_percentage=(home_count/count)*100
                      deal_percentage=(deal_count/count)*100
                      against_percentage=(against_count/count)*100
                  except ZeroDivisionError:
                      home_percentage=0
                      deal_percentage=0
                      against_percentage=0
                if int(main_result[1]) in list_id:
                  continue
                else:
                  with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "a", newline='',encoding="utf-8")as main:
                    main = csv.writer(main, dialect='excel')
                    home_percentage= ("%.2f" % home_percentage)
                    deal_percentage= ("%.2f" % deal_percentage)
                    against_percentage= ("%.2f" % against_percentage)
                    main_result.pop(-6)
                    main_result.insert(-5,str(home_percentage)+"%")
                    main_result.pop(-5)
                    main_result.insert(-4,str(deal_percentage)+"%")
                    main_result.pop(-4)
                    main_result.insert(-3,str(against_percentage)+"%")
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
        continue
create_team_csv()

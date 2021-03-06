# Szükséges modulok meghívva
import os
import csv

# A csapatok mappájának abszolúlt elérési útvonala
final_path = os.path.abspath("converted_csv_datas\\teams")


# Az info tartalmazza az átküldött iterált csv_result sort, a team_header magáért beszél :)
def calculate(info, team_header):
    fix_num = 0.5, 0.25, 10  # Fix számok elmentése 0,1,2 indexxel hivatkozunk majd rájuk
    # Ha a info[3]:Hazai CSapat és info[6]:Vendég Csapat által visszaadott csapatnév alapján nincs csv fájl,
    if os.path.exists(final_path+"\\"+info[3]+".csv") == False:
        # akkor létrehozza a fájlt és az áthozott team_header adatait beírja fejlécként.
        with open(final_path+"\\"+info[3]+".csv", "w", newline='', encoding="utf-8") as hdata:
            header = csv.writer(hdata, dialect='excel')
            header.writerow(team_header)
    if os.path.exists(final_path+"\\"+info[6]+".csv") == False:
        with open(final_path+"\\"+info[6]+".csv", "w", newline='', encoding="utf-8") as adata:
            header = csv.writer(adata, dialect='excel')
            header.writerow(team_header)
    # Az info[3] és info[6] csapatok fájljait megnyitja, beolvassa és beiterálja a row_hlist és row_alist változókba.
    with open(final_path+"\\"+info[3]+".csv", "r", encoding="utf-8") as hdata:
        data_hlist = csv.reader(hdata)
        row_hlist = []
        for hrow in data_hlist:
            row_hlist.append(hrow)
    with open(final_path+"\\"+info[6]+".csv", "r", encoding="utf-8") as adata:
        data_alist = csv.reader(adata)
        row_alist = []
        for arow in data_alist:
            row_alist.append(arow)
    # Innentől kezdődik a tényleges számítás. "if":mindkét csapat csak a fejléccel rendelkezik.
    if len(row_hlist) == 1 and len(row_alist) == 1:
        # Ez csak a 2014-es év elején fordul elő, mikor minden csapat egymással az első meccsüket játszák.
        pr_changing = (
            ((int(info[8])-int(info[9]))-(fix_num[2]-fix_num[2]))-fix_num[0])*fix_num[1]
        # ekkor csaka az iterált sorból dolgozik és a kezdeti 10-es értéket a fix_num[2] bekéréssel számolja.
        xg_changing = (((float(info[10])-float(info[11])) -(fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
        prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
        # Itt az eredménnyel módosítjuk a "régi értéket", jelen esetben csak a 10-es kezdő értéket.
        pr_changing = ("%.3f" % pr_changing)
        xg_changing = ("%.3f" % xg_changing)
        prxg_changing = ("%.3f" % prxg_changing)
        datas = [fix_num[2], fix_num[2], fix_num[2], fix_num[2],fix_num[2], fix_num[2],float(pr_changing),float(xg_changing),float(prxg_changing)]  # Itt előkészítjük az eredményeket egy "datas" változóba és a return paranccsal visszaadjuk
        # ezt a "datas" adatokat a team_collector fájlnak.
        return (datas)
    if len(row_hlist) == 1:  # Innentől a folyamat lényegében ugyanaz.
        # Az első "elif" csinálja a számítást, ha a hazai csapat érkezett újjonnan a bajnokságba
        pr_changing = (
            ((int(info[8])-int(info[9]))-(fix_num[2]-float(row_alist[-1][10])))-fix_num[0])*fix_num[1]
        # A második "elif" értelemszerüen ha a vendég csapat az új, vagyis nincs mit kiemelni a saját fájljából.
        xg_changing = (((float(info[10])-float(info[11])) -(fix_num[2]-float(row_alist[-1][13])))-fix_num[0])*fix_num[1]
        # Az "else" csinálja a "régi" csapatok számítását. Ekkor nem csak az iterált csv_resultot használja
        prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(
            info[11]))-(fix_num[2]-float(row_alist[-1][16])))-fix_num[0])*fix_num[1]
        # hanem a két csapat fájljaiból is ki tudja emelni az előző mérkőzésük változásait.
        new_hpr = fix_num[2]+float(pr_changing)
        # Természetesen csak az egyik feltétel fut le iterálásonként, mindegyik a maga "datas" adatait küldi vissza.
        pr_changing = ("%.3f" % pr_changing)
        xg_changing = ("%.3f" % xg_changing)
        prxg_changing = ("%.3f" % prxg_changing)
        old_apr = float(row_alist[-1][10])
        old_axg = float(row_alist[-1][13])
        old_aprxg = float(row_alist[-1][16])
        datas = [fix_num[2], old_apr, fix_num[2], old_axg, fix_num[2],old_aprxg, float(pr_changing),float(xg_changing),float(prxg_changing)]
        return (datas)
    if len(row_alist) == 1:
        pr_changing = (
            ((int(info[8])-int(info[9]))-(float(row_hlist[-1][10])-fix_num[2]))-fix_num[0])*fix_num[1]
        xg_changing = (((float(info[10])-float(info[11])) -(float(row_hlist[-1][13])-fix_num[2]))-fix_num[0])*fix_num[1]
        prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(
            info[11]))-(float(row_hlist[-1][16])-fix_num[2]))-fix_num[0])*fix_num[1]
        pr_changing = ("%.3f" % pr_changing)
        xg_changing = ("%.3f" % xg_changing)
        prxg_changing = ("%.3f" % prxg_changing)
        old_hpr = float(row_hlist[-1][10])
        old_hxg = float(row_hlist[-1][13])
        old_hprxg = float(row_hlist[-1][16])
        datas = [old_hpr, fix_num[2], old_hxg, fix_num[2], old_hprxg, fix_num[2],float(pr_changing),float(xg_changing),float(prxg_changing)]
        return (datas)
    else:
        pr_changing = (((int(info[8])-int(info[9]))-(float(row_hlist[-1][10])-float(row_alist[-1][10])))-fix_num[0])*fix_num[1]
        xg_changing = ((float(info[10])-float(info[11]))-(
            float(row_hlist[-1][13])-float(row_alist[-1][13]))-fix_num[0])*fix_num[1]
        prxg_changing = ((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(
            float(row_hlist[-1][16])-float(row_alist[-1][16]))-fix_num[0])*fix_num[1]
        pr_changing = ("%.3f" % pr_changing)
        xg_changing = ("%.3f" % xg_changing)
        prxg_changing = ("%.3f" % prxg_changing)
        old_hpr = float(row_hlist[-1][10])
        old_apr = float(row_alist[-1][10])
        old_hxg = float(row_hlist[-1][13])
        old_axg = float(row_alist[-1][13])
        old_hprxg = float(row_hlist[-1][16])
        old_aprxg = float(row_alist[-1][16])
        datas = [old_hpr, old_apr, old_hxg, old_axg, old_hprxg, old_aprxg,float(pr_changing),float(xg_changing),float(prxg_changing)]
        return (datas)

# Szükséges modulok meghívva
import os
import csv

# A csapatok mappájának abszolúlt elérési útvonala
final_path = os.path.abspath("..\..\converted_csv_datas\\teams")

# Függvény kezdete
# Az info tartalmazza az átküldött iterált csv_result sort, a team_header magáért beszél :)
def calculate(info, team_header):
# Fix számok elmentése 0,1,2 indexxel hivatkozunk majd rájuk
	fix_num = 0.5, 0.25, 10
# Ha a info[3]:Hazai CSapat és info[6]:Vendég Csapat által visszaadott csapatnév alapján nincs csv fájl,
# akkor létrehozza a fájlt és az áthozott team_header adatait beírja fejlécként.
	if os.path.exists(final_path+"\\"+info[3]+".csv") == False:
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
# Ez csak a 2014-es év elején fordul elő, mikor minden csapat egymással az első meccsüket játszák.
# ekkor csaka az iterált sorból dolgozik és a kezdeti 10-es értéket a fix_num[2] bekéréssel számolja.
	if len(row_hlist) and len(row_alist) == 1:
		pr_changing = (((int(info[8])-int(info[9]))-(fix_num[2]-fix_num[2]))-fix_num[0])*fix_num[1]
		xg_changing = (((float(info[10])-float(info[11])) -(fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
		prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
# Itt az eredménnyel módosítjuk a "régi értéket", jelen esetben csak a 10-es kezdő értéket.
		new_hpr = fix_num[2]+float(pr_changing)
		new_apr = fix_num[2]-float(pr_changing)
		new_hxg = fix_num[2]+float(xg_changing)
		new_axg = fix_num[2]-float(xg_changing)
		new_hprxg = fix_num[2]+float(prxg_changing)
		new_aprxg = fix_num[2]-float(prxg_changing)
# Itt előkészítjük az eredményeket egy "datas" változóba és a return paranccsal visszaadjuk
# ezt a "datas" adatokat a team_collector fájlnak.
		datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,fix_num[2], fix_num[2], fix_num[2], fix_num[2], fix_num[2], fix_num[2]]
		return (datas)
# Innentől a folyamat lényegében ugyanaz.
# Az első "elif" csinálja a számítást, ha a hazai csapat érkezett újjonnan a bajnokságba
# A második "elif" értelemszerüen ha a vendég csapat az új, vagyis nincs mit kiemelni a saját fájljából.
# Az "else" csinálja a "régi" csapatok számítását. Ekkor ne mcsak az iterált csv_resultot használja
# hanem a két csapat fájljaiból is ki tudja emelni az előző mérkőzésük változásait.
# Természetesen csak az egyik feltétel fut le iterálásonként, mindegyik a maga "datas" adatait küldi vissza.
	elif len(row_hlist) == 1:
		pr_changing = (((int(info[8])-int(info[9]))-(fix_num[2]-float(row_alist[-1][6])))-fix_num[0])*fix_num[1]
		xg_changing = (((float(info[10])-float(info[11]))-(fix_num[2]-float(row_alist[-1][6])))-fix_num[0])*fix_num[1]
		prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(fix_num[2]-float(row_alist[-1][6])))-fix_num[0])*fix_num[1]
		new_hpr = fix_num[2]+float(pr_changing)
		old_apr = float(row_alist[-1][7])
		new_apr = old_apr-float(pr_changing)
		new_hxg = fix_num[2]+float(xg_changing)
		old_axg = float(row_alist[-1][9])
		new_axg = old_axg-float(xg_changing)
		new_hprxg = fix_num[2]+float(prxg_changing)
		old_aprxg = float(row_alist[-1][11])
		new_aprxg = old_aprxg-float(prxg_changing)
		datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,fix_num[2], old_apr, fix_num[2], old_axg, fix_num[2], old_aprxg]
		return (datas)
	elif len(row_alist) == 1:
		pr_changing = (((int(info[8])-int(info[9]))-(float(row_hlist[-1][6])-fix_num[2]))-fix_num[0])*fix_num[1]
		xg_changing = (((float(info[10])-float(info[11]))-(float(row_hlist[-1][6])-fix_num[2]))-fix_num[0])*fix_num[1]
		prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(float(row_alist[-1][6])-fix_num[2]))-fix_num[0])*fix_num[1]
		old_hpr = float(row_hlist[-1][7])
		new_hpr = old_hpr+float(pr_changing)
		new_apr = fix_num[2]-float(pr_changing)
		old_hxg = float(row_hlist[-1][9])
		new_hxg = old_hxg+float(xg_changing)
		new_axg = fix_num[2]-float(xg_changing)
		old_hprxg = float(row_hlist[-1][11])
		new_hprxg = old_hprxg+float(prxg_changing)
		new_aprxg = fix_num[2]-float(prxg_changing)
		datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,old_hpr, fix_num[2], old_hxg, fix_num[2], old_hprxg, fix_num[2]]
		return (datas)
	else:
			pr_changing = ((int(info[8])-int(info[9]))-(float(row_hlist[-1][6])-float(row_alist[-1][6]))-fix_num[0])*fix_num[1]
			xg_changing = ((float(info[10])-float(info[11]))-(float(row_hlist[-1][6])-float(row_alist[-1][6]))-fix_num[0])*fix_num[1]
			prxg_changing = ((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(float(row_hlist[-1][6])-float(row_alist[-1][6]))-fix_num[0])*fix_num[1]
			old_hpr = float(row_hlist[-1][7])
			new_hpr = old_hpr+float(pr_changing)
			old_apr = float(row_alist[-1][7])
			new_apr = old_apr-float(pr_changing)
			old_hxg = float(row_hlist[-1][9])
			new_hxg = old_hxg+float(xg_changing)
			old_axg = float(row_alist[-1][9])
			new_axg = old_axg-float(xg_changing)
			old_hprxg = float(row_hlist[-1][11])
			new_hprxg = old_hprxg+float(prxg_changing)
			old_aprxg = float(row_alist[-1][11])
			new_aprxg = old_aprxg-float(prxg_changing)
			datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,old_hpr, old_apr, old_hxg, old_axg, old_hprxg, old_aprxg]
			return (datas)

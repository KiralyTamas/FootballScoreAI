# Szükséges modulok meghívva
import os
import csv

final_path = os.path.abspath("..\..\converted_csv_datas\\teams") # A csapatok mappájának abszolúlt elérési útvonala


def calculate(info, team_header): # Az info tartalmazza az átküldött iterált csv_result sort, a team_header magáért beszél :)
	fix_num = 0.5, 0.25, 10 # Fix számok elmentése 0,1,2 indexxel hivatkozunk majd rájuk
	if os.path.exists(final_path+"\\"+info[3]+".csv") == False:   # Ha a info[3]:Hazai CSapat és info[6]:Vendég Csapat által visszaadott csapatnév alapján nincs csv fájl,
		with open(final_path+"\\"+info[3]+".csv", "w", newline='', encoding="utf-8") as hdata: # akkor létrehozza a fájlt és az áthozott team_header adatait beírja fejlécként.
			header = csv.writer(hdata, dialect='excel')
			header.writerow(team_header)
	if os.path.exists(final_path+"\\"+info[6]+".csv") == False:
		with open(final_path+"\\"+info[6]+".csv", "w", newline='', encoding="utf-8") as adata:
			header = csv.writer(adata, dialect='excel')
			header.writerow(team_header)
	with open(final_path+"\\"+info[3]+".csv", "r", encoding="utf-8") as hdata: # Az info[3] és info[6] csapatok fájljait megnyitja, beolvassa és beiterálja a row_hlist és row_alist változókba.
		data_hlist = csv.reader(hdata)
		row_hlist = []
		for hrow in data_hlist:
			row_hlist.append(hrow)
	with open(final_path+"\\"+info[6]+".csv", "r", encoding="utf-8") as adata:
		data_alist = csv.reader(adata)
		row_alist = []
		for arow in data_alist:
			row_alist.append(arow)
	if len(row_hlist) and len(row_alist) == 1: # Innentől kezdődik a tényleges számítás. "if":mindkét csapat csak a fejléccel rendelkezik.
		pr_changing = (((int(info[8])-int(info[9]))-(fix_num[2]-fix_num[2]))-fix_num[0])*fix_num[1]  # Ez csak a 2014-es év elején fordul elő, mikor minden csapat egymással az első meccsüket játszák.
		xg_changing = (((float(info[10])-float(info[11])) -(fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])   # ekkor csaka az iterált sorból dolgozik és a kezdeti 10-es értéket a fix_num[2] bekéréssel számolja.
		prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
		new_hpr = fix_num[2]+float(pr_changing)  # Itt az eredménnyel módosítjuk a "régi értéket", jelen esetben csak a 10-es kezdő értéket.
		new_apr = fix_num[2]-float(pr_changing)
		new_hxg = fix_num[2]+float(xg_changing)
		new_axg = fix_num[2]-float(xg_changing)
		new_hprxg = fix_num[2]+float(prxg_changing)
		new_aprxg = fix_num[2]-float(prxg_changing)
		datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,fix_num[2], fix_num[2], fix_num[2], fix_num[2], fix_num[2], fix_num[2]] # Itt előkészítjük az eredményeket egy "datas" változóba és a return paranccsal visszaadjuk
		return (datas)           # ezt a "datas" adatokat a team_collector fájlnak.
	elif len(row_hlist) == 1: # Innentől a folyamat lényegében ugyanaz.
		pr_changing = (((int(info[8])-int(info[9]))-(fix_num[2]-float(row_alist[-1][9])))-fix_num[0])*fix_num[1]  # Az első "elif" csinálja a számítást, ha a hazai csapat érkezett újjonnan a bajnokságba
		xg_changing = (((float(info[10])-float(info[11]))-(fix_num[2]-float(row_alist[-1][9])))-fix_num[0])*fix_num[1]   # A második "elif" értelemszerüen ha a vendég csapat az új, vagyis nincs mit kiemelni a saját fájljából.
		prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(fix_num[2]-float(row_alist[-1][9])))-fix_num[0])*fix_num[1]   # Az "else" csinálja a "régi" csapatok számítását. Ekkor nem csak az iterált csv_resultot használja
		new_hpr = fix_num[2]+float(pr_changing)   # hanem a két csapat fájljaiból is ki tudja emelni az előző mérkőzésük változásait.
		old_apr = float(row_alist[-1][10])    # Természetesen csak az egyik feltétel fut le iterálásonként, mindegyik a maga "datas" adatait küldi vissza.
		new_apr = old_apr-float(pr_changing)
		new_hxg = fix_num[2]+float(xg_changing)
		old_axg = float(row_alist[-1][12])
		new_axg = old_axg-float(xg_changing)
		new_hprxg = fix_num[2]+float(prxg_changing)
		old_aprxg = float(row_alist[-1][14])
		new_aprxg = old_aprxg-float(prxg_changing)
		datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,fix_num[2], old_apr, fix_num[2], old_axg, fix_num[2], old_aprxg]
		return (datas)
	elif len(row_alist) == 1:
		pr_changing = (((int(info[8])-int(info[9]))-(float(row_hlist[-1][9])-fix_num[2]))-fix_num[0])*fix_num[1]
		xg_changing = (((float(info[10])-float(info[11]))-(float(row_hlist[-1][9])-fix_num[2]))-fix_num[0])*fix_num[1]
		prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(float(row_alist[-1][9])-fix_num[2]))-fix_num[0])*fix_num[1]
		old_hpr = float(row_hlist[-1][10])
		new_hpr = old_hpr+float(pr_changing)
		new_apr = fix_num[2]-float(pr_changing)
		old_hxg = float(row_hlist[-1][12])
		new_hxg = old_hxg+float(xg_changing)
		new_axg = fix_num[2]-float(xg_changing)
		old_hprxg = float(row_hlist[-1][14])
		new_hprxg = old_hprxg+float(prxg_changing)
		new_aprxg = fix_num[2]-float(prxg_changing)
		datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,old_hpr, fix_num[2], old_hxg, fix_num[2], old_hprxg, fix_num[2]]
		return (datas)
	else:
			pr_changing = ((int(info[8])-int(info[9]))-(float(row_hlist[-1][9])-float(row_alist[-1][9]))-fix_num[0])*fix_num[1]
			xg_changing = ((float(info[10])-float(info[11]))-(float(row_hlist[-1][9])-float(row_alist[-1][9]))-fix_num[0])*fix_num[1]
			prxg_changing = ((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(float(row_hlist[-1][9])-float(row_alist[-1][9]))-fix_num[0])*fix_num[1]
			old_hpr = float(row_hlist[-1][10])
			new_hpr = old_hpr+float(pr_changing)
			old_apr = float(row_alist[-1][10])
			new_apr = old_apr-float(pr_changing)
			old_hxg = float(row_hlist[-1][12])
			new_hxg = old_hxg+float(xg_changing)
			old_axg = float(row_alist[-1][12])
			new_axg = old_axg-float(xg_changing)
			old_hprxg = float(row_hlist[-1][14])
			new_hprxg = old_hprxg+float(prxg_changing)
			old_aprxg = float(row_alist[-1][14])
			new_aprxg = old_aprxg-float(prxg_changing)
			datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,old_hpr, old_apr, old_hxg, old_axg, old_hprxg, old_aprxg]
			return (datas)

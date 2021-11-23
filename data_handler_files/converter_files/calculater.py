import os
import csv

final_path = os.path.abspath("teams")


def calculate(info, team_header):
    fix_num = 0.5, 0.25, 10
    if os.path.exists(final_path+"\\"+info[3]+".csv") == False:
        with open(final_path+"\\"+info[3]+".csv", "w",newline='', encoding="utf-8") as hdata:
            header = csv.writer(hdata)
            header.writerow(team_header)
    if os.path.exists(final_path+"\\"+info[6]+".csv") == False:
        with open(final_path+"\\"+info[6]+".csv", "w",newline='', encoding="utf-8") as adata:
            header = csv.writer(adata)
            header.writerow(team_header)
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
    if len(row_hlist) and len(row_alist) == 1:
        pr_changing = (
            ((int(info[8])-int(info[9]))-(fix_num[2]-fix_num[2]))-fix_num[0])*fix_num[1]
        xg_changing = (((float(info[10])-float(info[11])) -
                       (fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
        prxg_changing = (((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(
            fix_num[2]-fix_num[2]))-float(fix_num[0]))*float(fix_num[1])
        new_hpr = fix_num[2]+float(pr_changing)
        new_apr = fix_num[2]-float(pr_changing)
        new_hxg = fix_num[2]+float(xg_changing)
        new_axg = fix_num[2]-float(xg_changing)
        new_hprxg = fix_num[2]+float(prxg_changing)
        new_aprxg = fix_num[2]-float(prxg_changing)
        datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,
                 fix_num[2], fix_num[2], fix_num[2], fix_num[2], fix_num[2], fix_num[2]]
        return (datas)
    else:
        pr_changing = ((int(info[8])-int(info[9]))-(float(row_hlist[-1]
                       [6])-float(row_alist[-1][6]))-fix_num[0])*fix_num[1]
        xg_changing = ((float(info[10])-float(info[11]))-(float(row_hlist[-1][6])-float(
            row_alist[-1][6]))-float(fix_num[0]))*float(fix_num[1])
        prxg_changing = ((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(
            float(row_hlist[-1][6])-float(row_alist[-1][6]))-float(fix_num[0]))*float(fix_num[1])
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
        datas = [new_hpr, new_apr, new_hxg, new_axg, new_hprxg, new_aprxg,
                 old_hpr, old_apr, old_hxg, old_axg, old_hprxg, old_aprxg]
        return (datas)

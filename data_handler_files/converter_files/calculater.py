import os
import csv

final_path = os.path.abspath("teams")

def calculate(info):
  fix_numbers = 0.5, 0.25
  try:
      with open(final_path+"\\"+info[3]+".csv","r",encoding="utf-8") as hdata:
        data_hlist=csv.reader(hdata)
        row_hlist=[]
        for hrow in data_hlist:
          row_hlist.append(hrow)
      with open(final_path+"\\"+info[6]+".csv","r",encoding="utf-8") as adata:
        data_alist=csv.reader(adata)
        row_alist=[]
        for arow in data_alist:
          row_alist.append(arow)
      pr_changing = ((int(info[8])-int(info[9]))-(float(row_hlist[-1][6])-float(row_alist[-1][6]))-fix_numbers[0])*fix_numbers[1]
      xg_changing = ((float(info[10])-float(info[11]))-(float(row_hlist[-1][6])-float(row_alist[-1][6]))-float(fix_numbers[0]))*float(fix_numbers[1])
      prxg_changing = ((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(float(row_hlist[-1][6])-float(row_alist[-1][6]))-float(fix_numbers[0]))*float(fix_numbers[1])
      pr_changing=  ("%.4f" % pr_changing)
      xg_changing = ("%.4f" % xg_changing)
      prxg_changing = ("%.4f" % prxg_changing)
      new_hpr=float(row_hlist[-1][6])+float(pr_changing)
      new_apr=float(row_alist[-1][6])-float(pr_changing)
      new_hxg=float(row_hlist[-1][8])+float(xg_changing)
      new_axg=float(row_alist[-1][8])-float(xg_changing)
      new_hprxg=float(row_hlist[-1][10])+float(prxg_changing)
      new_aprxg=float(row_alist[-1][10])-float(prxg_changing)
      datas=[new_hpr,new_apr,new_hxg,new_axg,new_hprxg,new_aprxg]
      return (datas)
  except FileNotFoundError:
      pr=10
      pr_changing = ((int(info[8])-int(info[9]))-(pr-pr)-fix_numbers[0])*fix_numbers[1]
      xg_changing = ((float(info[10])-float(info[11]))-(pr-pr)-fix_numbers[0])*fix_numbers[1]
      prxg_changing = ((int(info[8])-int(info[9]))-(float(info[10])-float(info[11]))-(pr-pr)-fix_numbers[0])*fix_numbers[1]
      pr_changing=  ("%.4f" % pr_changing)
      xg_changing = ("%.4f" % xg_changing)
      prxg_changing = ("%.4f" % prxg_changing)
      new_hpr=pr+float(pr_changing)
      new_apr=pr-float(pr_changing)
      new_hxg=pr+float(xg_changing)
      new_axg=pr-float(xg_changing)
      new_hprxg=pr+float(prxg_changing)
      new_aprxg=pr-float(prxg_changing)
      datas=[new_hpr,new_apr,new_hxg,new_axg,new_hprxg,new_aprxg]
      return (datas)
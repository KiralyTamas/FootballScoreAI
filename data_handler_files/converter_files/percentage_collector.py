import csv
import os

def per_col():
  pr_diff=[]
  with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv","r") as file:
    file=csv.reader(file)
    for index,row in enumerate(file):
      if index == 0:
        continue
      if float(row[10]) not in pr_diff:
        pr_diff.append(float(row[10]))
  pr_diff = sorted(pr_diff, key=lambda line:line, reverse=False)
per_col()
import csv

with open("C:\Repository\FootballScoreAI\converted_csv_datas\csv_table\\2014\\tablebundesliga2014.csv","r",encoding="utf-8") as data:
  data_list=csv.reader(data)
  row_list=[]
  for row in data_list:
    row_list.append(row)
  print(row_list[-1][0])
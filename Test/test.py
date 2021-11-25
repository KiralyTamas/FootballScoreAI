import csv

with open("test.csv","r") as list:
  csv_list=csv.reader(list)
  for i,num in enumerate(csv_list):
    if str(15) in num:
      print(i)
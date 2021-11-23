import csv

with open("test.csv","r") as file:
  csv_file=csv.reader(file)
  list_of_num=[]
  for num in csv_file:
    list_of_num.append(num)
  print(list_of_num)
  for i,ch in enumerate(range(1,17)) :
    if [str(ch)] in list_of_num:
      print(ch)
    else:
      list_of_num.insert(i,[str(ch)])
with open("test.csv","w",newline='',encoding="utf-8")as file:
  csv_file=csv.writer(file)
  csv_file.writerows(list_of_num)
import csv

with open("D:\Repository\FootballScoreAI\data_handler_files\\requester_files\match_ids.csv","r") as list:
  csv_list=csv.reader(list)
  num_list=[]
  for num in csv_list:
    int_num=int(num)
    num_list.append(int_num)
print(num_list)
import os
import csv

def id_collect():
  source_dir=os.path.abspath("converted_csv_datas\csv_match")
  print(source_dir)
  f = []
  for (dirpath, dirnames, filenames) in os.walk(source_dir):
      f.extend(filenames)
      break
  number_list = []
  check_list=[]
  p_path=os.path.abspath("data_handler_files\\requester_files")
  for match_id in f:
    match_num_1 = match_id.replace("match", '')
    match_num_2=int(match_num_1.replace(".csv", ''))
    number_list.append(match_num_2)
  for num in range(1,20001):
      if num not in number_list:
        check_list.append(num)
  with open(p_path+"\match_ids.csv", "w", newline='') as file:
    csv_file=csv.writer(file, dialect='excel')
    csv_file.writerow(check_list)
  return print("Kész")
import os
import csv

source_dir=os.path.abspath("converted_csv_datas\csv_match")
f = []
for (dirpath, dirnames, filenames) in os.walk(source_dir):
    f.extend(filenames)
    break

file_name = []
match_id=["match_id"]
p_path=os.path.abspath("data_handler_files\\requester_files")
for i in f:
  number = []
  file_name = i
  new_file_name = file_name.replace("match", '')
  number.append(int(new_file_name.replace(".csv", '')))
print(type(number))
with open(p_path+"\match_ids.csv", "a", newline='') as file:
  csv_file=csv.writer(file, dialect='excel')
  check_list=[]
  for j in range(1,20001,1):
    if j not in [number]:
      check_list.append(j)
      csv_file.writerow(check_list)
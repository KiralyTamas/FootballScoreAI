import os
import csv
path_dir=os.path.abspath("converted_csv_datas\csv_match")
f = []
for (dirpath, dirnames, filenames) in os.walk(os.path.relpath(path_dir)):
    f.extend(filenames)
    break

file_name = []
match_id=["match_id"]
p_path=os.path.abspath("converted_csv_datas\csv_match_ids")
try:
  os.mkdir(p_path)
except FileExistsError:
    print("Ez a mappa már létezik")
with open(p_path+"\match_ids.csv", "w", newline='') as file:
  csv_file=csv.writer(file)
  csv_file.writerow(match_id)
  for i in f:
    number = []
    file_name = str(i)
    new_file_name = file_name.replace("match", '')
    number.append(new_file_name.replace(".csv", ''))
    csv_file.writerow(number)
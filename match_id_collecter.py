import os
import csv
path_dir="C:\Repository\FootballScoreAI\datas_for_converting\match"
f = []
for (dirpath, dirnames, filenames) in os.walk(os.path.relpath(path_dir)):
    f.extend(filenames)
    break

file_name = []
match_id=["match_id"]
make_dir="datas_for_converting\match_ids"
p_path=os.path.relpath("C:\Repository\FootballScoreAI")
try:
  path=os.path.join(p_path,make_dir)
  os.mkdir(path)
except FileExistsError:
    print("Ez a mappa már létezik")
with open(path+"\match_ids.csv", "w", newline='') as file:
  csv_file=csv.writer(file)
  csv_file.writerow(match_id)
  for i in f:
    number = []
    file_name = str(i)
    new_file_name = file_name.replace("match", '')
    number.append(new_file_name.replace(".csv", ''))
    csv_file.writerow(number)
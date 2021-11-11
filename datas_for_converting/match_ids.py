import os
import csv

f = []
for (dirpath, dirnames, filenames) in os.walk("C:\Repository\FootballScoreAI\datas_for_converting\match"):
    f.extend(filenames)
    break

file_name = []
match_id=["match_id"]
make_dir="match_ids"
p_path="C:\Repository\FootballScoreAI\datas_for_converting"
try:
  path=os.path.join(p_path,make_dir)
  os.mkdir(path)
except FileExistsError:
    print("Ez a mappa már létezik")
with open("match_ids\match_ids.csv", "w", newline='') as file:
  csv_file=csv.writer(file)
  csv_file.writerow(match_id)
  for i in f:
    number = []
    if i[-4:]==".csv":
      continue
    file_name = str(i)
    new_file_name = file_name.replace("match", '')
    number.append(new_file_name.replace(".json", ''))
    csv_file.writerow(number)
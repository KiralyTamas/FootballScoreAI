from os import walk
import csv

f = []
for (dirpath, dirnames, filenames) in walk("C:\Repository\FootballScoreAI\datas_for_converting\match"):
    f.extend(filenames)
    break

file_name = []
match_id=["match_id"]
with open("match_ids.csv", "w", newline='') as file:
  csv_file=csv.writer(file)
  csv_file.writerow(match_id)
  for i in f:
    number = []
    file_name = str(i)
    new_file_name = file_name.replace("match", '')
    number.append(new_file_name.replace(".json", ''))
    csv_file.writerow(number)
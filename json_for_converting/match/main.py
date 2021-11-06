import csv
import json
from pathlib import Path

path=input("Mi a konvertálandó fájl útvonala: ")
file_name=Path(path).name
source = open(file_name, "r",encoding="utf-8")
data = []
data = json.load(source)
source.close()
file_xxx=['json','csv']
csv_path = file_name.replace(file_xxx[0],file_xxx[1])

def convert_csv():
  with open(csv_path,"w",encoding="UTF-8",newline='') as file:
    csv_file=csv.writer(file)
    id_header=data["h"][0]
    csv_file.writerow(id_header)
    for ids in data.keys():
        for value in range(len(data[ids])):
          csv_file.writerow(data[ids][value].values())

convert_csv()
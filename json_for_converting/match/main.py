import csv
import json

old = "json"
new = "csv"
data = []
path="match16000.json"
#path=input("Mi a konvertálandó fájl útvonala: ")
source = open(path, "r",encoding="utf-8")
data = json.load(source)
source.close()
csv_path = path.replace(old, new)

def convert_csv():
  with open(csv_path,"w",encoding="UTF-8",newline='') as file:
    csv_file=csv.writer(file)
    for ids in data.keys():
        csv_file.writerow(data[ids][0])
        for value in range(len(data[ids])):
          csv_file.writerow(data[ids][value].values())

convert_csv()
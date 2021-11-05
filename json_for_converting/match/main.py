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
    for a in data:
      adat=data[a]
      for c in data:
          print("lista")
          csv_file.writerow(a)
          csv_file.writerow(data[a])
          if isinstance(data[a], list):
            for b in data[a]:
              csv_file.writerow(data[a][1].values())
    

convert_csv()
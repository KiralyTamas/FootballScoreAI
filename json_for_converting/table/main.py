import csv
import json

old = "json"
new = "csv"
data = []
path=input("Mi a konvertálandó fájl útvonala: ")
source = open(path, "r")
data = json.load(source)
source.close()
csv_path = path.replace(old, new)

def convert_csv(data):
  with open(csv_path,"w",newline='') as file:
    csv_file=csv.writer(file)
    for i in data:
      content=[]
      for j in i:
        content.append(j)
      csv_file.writerow(content)

convert_csv(data)
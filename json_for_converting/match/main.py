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
  u=[]
  for a in data:
    u.append(a)
  f=iter(data)
  for i in f:
    print(data[i])
    x=iter(data[i])
    print(u)

convert_csv()
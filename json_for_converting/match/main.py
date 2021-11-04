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
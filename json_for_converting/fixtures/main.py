import json
import csv

old = "json"
new = "csv"
data = []
path=input("Mi a konvertálandó fájl útvonala: ")
source = open(path, "r")
data = json.load(source)
source.close()
csv_path = path.replace(old, new)


def convert_header(data, delim):
    with open(csv_path, "w", newline='') as file:
        csv_file = csv.writer(file)
        for number in data:
            header = []
            for i in number.keys():
                if isinstance(number[i], dict):
                    for j in number[i].keys():
                        header.append(str(i)+delim+str(j))
                header.append(i)
                if isinstance(number[i], dict):
                    header.remove(i)
        csv_file.writerow(header)
        for number in data:
          content = []
          for i in number.keys():
            content.append(number[i])
            if isinstance(number[i], dict):
                content.remove(number[i])
                for j in number[i]:
                    content.append(str(number[i][j]))
          csv_file.writerow(content)

convert_header(data, "_")

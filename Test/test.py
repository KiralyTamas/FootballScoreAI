import csv
import os
list = [["1", "alma", "narancs", "dió", "kókusz"],
        ["2", "kocsi", "bicikli", "hajó", "repülő"],
        ["3", "nadrág", "kabát", "cipő", "sapka"],
        ["4", "fiú", "lány", "férfi", "nő"],
        ["5", "fekete", "fehér", "piros", "sárga"],
        ["6", "cápa", "delfin", "bálna", "kardhal"],
        ["7", "NewYork", "Tokyo", "London", "Texas"]]


def write():
    try:
        with open("proba.csv", "w", encoding="utf-8", newline='') as file:
            write_csv = csv.writer(file)
            for item in reversed(list):
                item.insert(1, "univerzum")
                if item == list:
                    continue
                else:
                    write_csv.writerow(item)
    except OSError:
        print("szar")
        write()


def search():

  f = []
  g = []
  h = []
  for (dirpath, dirnames, filenames) in os.walk(input("Mi a konvertálandó fájlok mappájának útvonala: ")):
    f.extend(filenames)
    g.extend(dirnames)
    h.append(dirpath)
  print(f)
  print(g)
  print(h)

search()
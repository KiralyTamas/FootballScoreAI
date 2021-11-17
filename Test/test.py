import csv
list = [["1", "alma", "narancs", "dió", "kókusz"],
        ["2", "kocsi", "bicikli", "hajó", "repülő"],
        ["3", "nadrág", "kabát", "cipő", "sapka"],
        ["4", "fiú", "lány", "férfi", "nő"],
        ["5", "fekete", "fehér", "piros", "sárga"],
        ["6","cápa","delfin","bálna","kardhal"],
        ["7","NewYork","Tokyo","London","Texas"]]

def read():
  data=[]
  for item in list:
    if "proba.csv":
      with open("proba.csv","r",encoding="utf-8", newline='') as file:
        read_file=csv.reader(file)
        data.append(item)
  return data

def write(list):
  with open("proba.csv","w",encoding="utf-8", newline='') as file:
    write_csv=csv.writer(file)
    for item in reversed(list):
      if item == list:
        continue
      else:
        write_csv.writerow(item)

write(read())
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
  for index,item in enumerate(list):
    if "proba.csv":
      prev_num=int(list[index-1][0])
      new_num=int(item[0])+int(prev_num)
      item.insert(1,new_num)
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
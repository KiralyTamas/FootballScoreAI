import os
import csv


def id_collect():
    source_dir = os.path.abspath("converted_csv_datas\csv_fixtures")
    f = []
    e = []
    id_list=[]
    for (dirpath, dirnames, filenames) in os.walk(source_dir):
        e.extend(dirpath)
        f.extend(filenames)
        for i in f:
            with open(source_dir+"/"+i,"r") as file:
                file_list=csv.reader(file)
                for index,row in enumerate(file_list):
                    if index==0:
                        continue
                    id_list.append(row[0])
    return(id_list)

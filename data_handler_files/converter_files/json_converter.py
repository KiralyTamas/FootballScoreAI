import csv
import json
import os


def make_json():
    start_path=os.path.abspath("..\..\converted_csv_datas\main_fixture")
    finish_path=os.path.abspath("..\..\converted_json_datas\main_fixture")
    file_names=[]
    dir_names=[]
    dir_path=[]
    for (dirpath, dirnames, filenames) in os.walk(start_path):
        file_names.extend(filenames)
        dir_names.extend(dirnames)
        dir_path.append(dirpath)
    print(dir_path)
    print(file_names)
    data = {}
    for file in file_names:
        with open(start_path+"\\"+file, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for index,rows in enumerate(csvReader):
                key = index+1
                data[key] = rows
        if os.path.exists(os.path.abspath("..\..\converted_json_datas"))==False:
            os.mkdir(os.path.abspath("..\..\converted_json_datas"))
        if os.path.exists(finish_path)==False:
            os.mkdir(finish_path)
        with open(finish_path+"\\"+file.replace('.csv', '.json'), 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

make_json()
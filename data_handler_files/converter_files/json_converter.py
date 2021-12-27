import csv
import json
import os


def make_json():
    print("Adatok json-ba konvertálása Web-felülethez.")
    start_fixture_path=os.path.abspath("converted_csv_datas\main_fixture")
    finish_fixture_path=os.path.abspath("converted_json_datas\main_fixture")
    file_names=[]
    dir_names=[]
    dir_path=[]
    for (dirpath, dirnames, filenames) in os.walk(start_fixture_path):
        file_names.extend(filenames)
        dir_names.extend(dirnames)
        dir_path.append(dirpath)
    data = {}
    for file in file_names:
        with open(start_fixture_path+"\\"+file, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for index,rows in enumerate(csvReader):
                key = index+1
                data[key]=rows
        if os.path.exists(os.path.abspath("converted_json_datas"))==False:
            os.mkdir(os.path.abspath("converted_json_datas"))
        if os.path.exists(finish_fixture_path)==False:
            os.mkdir(finish_fixture_path)
        with open(finish_fixture_path+"\\"+file.replace('.csv', '.json'), 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
    start_teams_path=os.path.abspath("converted_csv_datas\\teams")
    finish_teams_path=os.path.abspath("converted_json_datas\\teams")
    file_names=[]
    dir_names=[]
    dir_path=[]
    for (dirpath, dirnames, filenames) in os.walk(start_teams_path):
        file_names.extend(filenames)
        dir_names.extend(dirnames)
        dir_path.append(dirpath)
    data = {}
    for file in file_names:
        with open(start_teams_path+"\\"+file, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for index,rows in enumerate(csvReader):
                key = index+1
                data[key]=rows
        if os.path.exists(finish_teams_path)==False:
            os.mkdir(finish_teams_path)
        with open(finish_teams_path+"\\"+file.replace('.csv', '.json'), 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
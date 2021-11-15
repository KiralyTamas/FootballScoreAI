import json
import os


def caller(path,csv_path):
    last_four=path[-4:]
    if last_four == ".csv":
        data_list=[last_four,"_"]
        return data_list
    else:
        relative_path = os.path.relpath(path)
        source = open(relative_path, "r")
        data = json.load(source)
        file_xxx = ["json", "csv"]
        csv_path = csv_path.replace(file_xxx[0], file_xxx[1])
        source.close()
        data_list = [csv_path, data]
        return data_list
import json
import os


def caller(path,file_name):
    last_four=path[-4:]
    if last_four == ".csv":
        data_list=[last_four,"_"]
        return data_list
    else:
        relative_path = os.path.relpath(path)
        source = open(relative_path, "r")
        data = json.load(source)
        source.close()
        data_list = [file_name, data]
        return data_list
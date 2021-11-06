import json
import os


def caller():
    path = input("Mi a konvertálandó fájl útvonala: ")
    relative_path = os.path.relpath(path)
    source = open(relative_path, "r")
    data = json.load(source)
    file_xxx = ["json", "csv"]
    csv_path = relative_path.replace(file_xxx[0], file_xxx[1])
    source.close()
    data_list = [csv_path, data]
    return data_list

import csv
import os


def date_sorting():
    try:
        with open((os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv"), "r", encoding="utf-8") as data:
            data = csv.reader(data)
            sample = []
            for i in data:
                sample.append(i)
            poped = sample.pop(0)
            list_correct = sorted(
                sample, key=lambda date: date[0], reverse=False)
            list_correct.insert(0, poped)
        with open((os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv"), "w", newline='', encoding="utf-8") as data:
            data = csv.writer(data, dialect='excel')
            data.writerows(list_correct)
    except FileNotFoundError:
        print('')

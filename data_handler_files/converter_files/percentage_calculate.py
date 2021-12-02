import pandas as pd
import os
import csv
from date_time_sorter import date_sorting as date


def percentage_calculate():
    date()
    with open((os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv"), "r") as file:
        file = csv.reader(file)
        row_list = []
        for row in file:
            row_list.append(row)
        poped = row_list.pop(0)
        new_list = []
        for row_index, row in enumerate(row_list):
            if row[0][:10] in row_list:
                row.pop(-6)
                row.insert(-5, row_list[-1][-6])
                row.pop(-5)
                row.insert(-4, row_list[-1][-5])
                row.pop(-4)
                row.insert(-3, row_list[-1][-4])

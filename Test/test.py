import csv
import os

with open("D:\Repository\FootballScoreAI\converted_csv_datas\main_result\main_result.csv", "r")as file:
    file = csv.reader(file)
    all_len = []
    for i in file:
        all_len.append(i)
    for index, i in enumerate(all_len):
        if index >= len(all_len)-200:
            print(index)
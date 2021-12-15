import csv
import os
from data_handler_files.converter_files.xg_percentage_collector import xg_per_col as xg_col

def pr_per_col():
    print("PR Százalék összegyüjtése")
    pr_diff = []
    checking_list=[]
    line_len=0
    path=os.path.abspath(
        ("converted_csv_datas\main_diff"))
    if os.path.exists(path)==False:
        os.mkdir(path)
    diff_home_table = "\main_pr_diff_home.csv"
    diff_deal_table = "\main_pr_diff_deal.csv"
    diff_against_table = "\main_pr_diff_against.csv"
    with open(os.path.abspath("converted_csv_datas\main_result")+"\\main_pr_result.csv", "r") as file:
        file = csv.reader(file)
        for index, row in enumerate(file):
            fragment=[]
            if index == 0:
                continue
            fragment=[row[10],row[18],row[19],row[20]]
            checking_list.append(fragment)
            if float(row[10]) not in pr_diff:
                pr_diff.append(float(row[10]))
        pr_diff = sorted(pr_diff, key=lambda line: line, reverse=False)
    with open(path+diff_home_table,"w",newline='', encoding='utf-8')as file:
            csv_file=csv.DictWriter(file,dialect='excel', fieldnames=pr_diff)
            csv_file.writeheader()
    with open(path+diff_deal_table,"w",newline='', encoding='utf-8')as file:
            csv_file=csv.DictWriter(file,dialect='excel', fieldnames=pr_diff)
            csv_file.writeheader()
    with open(path+diff_against_table,"w",newline='', encoding='utf-8')as file:
            csv_file=csv.DictWriter(file,dialect='excel', fieldnames=pr_diff)
            csv_file.writeheader()
    list_len=0
    full_home=[]
    full_deal=[]
    full_against=[]
    for num in pr_diff:
        num_home=[]
        num_deal=[]
        num_against=[]
        hit=0
        for checking in checking_list:
            if float(num) == float(checking[0]):
                hit+=1
                if hit>list_len:
                    list_len+=1
                num_home.append(checking[1])
                num_deal.append(checking[2])
                num_against.append(checking[3])
        full_home.append(num_home)
        full_deal.append(num_deal)
        full_against.append(num_against)
    for line in range(list_len):
        finish_home_list=[]
        finish_deal_list=[]
        finish_against_list=[]
        for row in full_home:
            try:
                finish_home_list.append(row[line])
            except IndexError:
                finish_home_list.append("")
        with open(path+diff_home_table,"a",newline='', encoding='utf-8')as file:
            csv_file=csv.writer(file)
            csv_file.writerow(finish_home_list)
        for row in full_deal:
            try:
                finish_deal_list.append(row[line])
            except IndexError:
                finish_deal_list.append("")
        with open(path+diff_deal_table,"a",newline='', encoding='utf-8')as file:
            csv_file=csv.writer(file)
            csv_file.writerow(finish_deal_list)
        for row in full_against:
            try:
                finish_against_list.append(row[line])
            except IndexError:
                finish_against_list.append("")
        with open(path+diff_against_table,"a",newline='', encoding='utf-8')as file:
            csv_file=csv.writer(file)
            csv_file.writerow(finish_against_list)
    xg_col()
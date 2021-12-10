import csv
import os


def per_col():
    pr_diff = []
    checking_list=[]
    percentage_home_list=[]
    percentage_deal_list=[]
    percentage_against_list=[]
    line_len=0
    path=os.path.abspath(
        ("..\..\converted_csv_datas\main_diff"))
    diff_home_table = "\main_diff_home.csv"
    diff_deal_table = "\main_diff_deal.csv"
    diff_against_table = "\main_diff_against.csv"
    with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "r") as file:
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
    if os.path.exists(path+diff_home_table)==True:
        os.remove(path+diff_home_table)
    with open(path+diff_home_table,"a",newline='', encoding='utf-8') as m_file:
        m_file=csv.writer(m_file)
        num_home=[]
        num_deal=[]
        num_against=[]
        hit=0        
    print(checking_list)

per_col()
import csv
import os


def per_col():
    pr_diff = []
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
            if index == 0:
                continue
            if float(row[10]) not in pr_diff:
                pr_diff.append(float(row[10]))
    pr_diff = sorted(pr_diff, key=lambda line: line, reverse=False)
    if os.path.exists(path+diff_home_table)==True:
        os.remove(path+diff_home_table)
    with open(path+diff_home_table,"a",newline='', encoding='utf-8') as m_file:
        m_file=csv.writer(m_file)
        with open(os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv", "r") as file:
            file = csv.reader(file)
            for num in pr_diff:
                num_home=[]
                num_deal=[]
                num_against=[]
                hit=0
                for index, row in enumerate(file):
                    if index == 0:
                        continue
                    if str(num) == str(row[10]):
                        line_len+=1
                        hit+=1
                        if line_len<hit:
                            line_len+=1
                        num_home.append(row[18])
                        num_deal.append(row[19])
                        num_against.append(row[20])
                print(num_home)    
                m_file.writerow(num_home)
    

per_col()
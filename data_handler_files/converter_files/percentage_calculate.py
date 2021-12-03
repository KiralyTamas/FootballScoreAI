import pandas as pd
import os
import csv
from date_time_sorter import date_sorting as date


def percentage_calculate():
    date()
    with open((os.path.abspath("..\..\converted_csv_datas\main_result")+"\\main_result.csv"), "r") as file:
        file = csv.reader(file)
        row_list = []
        header=[]
        for row in file:
            count=0
            home_count=0
            deal_count=0
            against_count=0
            score_diff__more:0
            score_diff__3:0
            score_diff__2:0
            score_diff__1:0
            score_diff_0:0
            score_diff_1:0
            score_diff_2:0
            score_diff_3:0
            score_diff_more:0
            if len(row_list) ==0:
                header.append(row)
            else:
                if (row[0][:10] not in row_list) or ((row[0][:10] and row[10]) not in row_list):
                    for i in row_list:
                        if float(row[10]) == float(i[10]):
                            count+=1
                            score=i[4]-i[5]
                            if score < -3:
                                score_diff__more+=1
                                against_count+=1
                            if score == -3:
                                score_diff__3+=1
                                against_count+=1
                            if score == -2:
                                score_diff__2+=1
                                against_count+=1
                            if score == -1:
                                score_diff__1+=1
                                against_count+=1
                            if score == 0:
                                deal_count+=1
                                score_diff_0+=1
                            if score == 1:
                                home_count+=1
                                score_diff_1+=1
                            if score == 2:
                                home_count+=1
                                score_diff_2+=1
                            if score == 3:
                                home_count+=1
                                score_diff_3+=1
                            if score > 3:
                                home_count+=1
                                score_diff_more+=1
                    home_percentage=(home_count/count)*100
                    deal_percentage=(deal_count/count)*100
                    against_percentage=(against_count/count)*100
                    percentage__more=(score_diff__more/count)*100
                    percentage__3=(score_diff__3/count)*100
                    percentage__2=(score_diff__2/count)*100
                    percentage__1=(score_diff__1/count)*100
                    percentage_0=(score_diff_0/count)*100
                    percentage_1=(score_diff_1/count)*100
                    percentage_2=(score_diff_2/count)*100
                    percentage_3=(score_diff_3/count)*100
                    percentage_more=(score_diff_more/count)*100
                    row.pop(17)
                    row.insert(17, count)
                    row.pop(18)
                    row.insert(18, home_percentage)
                    row.pop(19)
                    row.insert(19, deal_percentage)
                    row.pop(20)
                    row.insert(20, against_percentage)
                    row.pop(21)
                    row.insert(21, percentage__more)
                    row.pop(22)
                    row.insert(22, percentage__3)
                    row.pop(23)
                    row.insert(23, percentage__2)
                    row.pop(24)
                    row.insert(24, percentage__1)
                    row.pop(25)
                    row.insert(25, percentage_0)
                    row.pop(26)
                    row.insert(26, percentage_1)
                    row.pop(27)
                    row.insert(27, percentage_2)
                    row.pop(28)
                    row.insert(28, percentage_3)
                    row.pop(29)
                    row.insert(29, percentage_more)
                else:
                    for i in row_list:
                        if row[0][:10] == i[0][:10] and row[10] == i[10]:
                            row.pop(18)
                            row.insert(18, i[-1][18])
                            row.pop(19)
                            row.insert(19, i[-1][19])
                            row.pop(20)
                            row.insert(20, i[-1][20])
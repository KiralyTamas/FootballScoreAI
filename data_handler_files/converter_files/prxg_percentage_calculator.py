import pandas as pd
import os
import csv
from data_handler_files.converter_files.date_time_sorter import date_sorting as date
from data_handler_files.converter_files.main_fixture_pr import fixture_pr as pr
from data_handler_files.converter_files.pr_percentage_collector import pr_per_col as pr_col

def prxg_percentage_calculate(header,main_result):
    print("prxg_percentage_calculate")
    main_result_list=date(main_result)
    main_list=[]
    calculated_list=[]
    id_list=[]
    with open((os.path.abspath("converted_csv_datas\main_result")+"\\main_prxg_result.csv"), "r", encoding='utf-8') as file:
        file = csv.reader(file)
        row_list = []
        for row in file:
            main_list.append(row)
    for row in main_list:
        if row[20] != "-":
            id_list.append(row[1])
            calculated_list.append(row)
    for row_id in main_result_list:
        if row_id[1] not in id_list:
            main_list.append(row_id)
    for row in main_list[len(calculated_list):]:
        count = 0
        home_count = 0
        deal_count = 0
        against_count = 0
        score_diff__more = 0
        score_diff__3 = 0
        score_diff__2 = 0
        score_diff__1 = 0
        score_diff_0 = 0
        score_diff_1 = 0
        score_diff_2 = 0
        score_diff_3 = 0
        score_diff_more = 0
        if (row[0][:10] not in calculated_list):
            for index,i in enumerate(calculated_list):
                if index == 0:
                    continue
                if float(row[16]) == float(i[16]):
                    count += 1
                    score = int(i[4])-int(i[5])
                    if score < -3:
                        score_diff__more += 1
                        against_count += 1
                    if score == -3:
                        score_diff__3 += 1
                        against_count += 1
                    if score == -2:
                        score_diff__2 += 1
                        against_count += 1
                    if score == -1:
                        score_diff__1 += 1
                        against_count += 1
                    if score == 0:
                        deal_count += 1
                        score_diff_0 += 1
                    if score == 1:
                        home_count += 1
                        score_diff_1 += 1
                    if score == 2:
                        home_count += 1
                        score_diff_2 += 1
                    if score == 3:
                        home_count += 1
                        score_diff_3 += 1
                    if score > 3:
                        home_count += 1
                        score_diff_more += 1
            try:
                home_percentage = "{:.0%}".format(home_count/count)
                deal_percentage = "{:.0%}".format(deal_count/count)
                against_percentage = "{:.0%}".format(against_count/count)
                percentage__more = "{:.0%}".format(score_diff__more/count)
                percentage__3 = "{:.0%}".format(score_diff__3/count)
                percentage__2 = "{:.0%}".format(score_diff__2/count)
                percentage__1 = "{:.0%}".format(score_diff__1/count)
                percentage_0 = "{:.0%}".format(score_diff_0/count)
                percentage_1 = "{:.0%}".format(score_diff_1/count)
                percentage_2 = "{:.0%}".format(score_diff_2/count)
                percentage_3 = "{:.0%}".format(score_diff_3/count)
                percentage_more = "{:.0%}".format(score_diff_more/count)
  #              home_percentage = ("%.2f" % home_percentage)
   #             deal_percentage = ("%.2f" % deal_percentage)
    #            against_percentage = ("%.2f" % against_percentage)
     #           percentage__more = ("%.2f" % percentage__more)
      #          percentage__3 = ("%.2f" % percentage__3)
       #         percentage__2 = ("%.2f" % percentage__2)
        #        percentage__1 = ("%.2f" % percentage__1)
         #       percentage_0 = ("%.2f" % percentage_0)
           #     percentage_1 = ("%.2f" % percentage_1)
            #    percentage_2 = ("%.2f" % percentage_2)
             #   percentage_3 = ("%.2f" % percentage_3)
              #  percentage_more = ("%.2f" % percentage_more)
                row.pop(17)
                row.insert(17, count)
                row.pop(18)
                row.insert(18, home_percentage)
                row.pop(19)
                row.insert(19, deal_percentage)
                row.pop(20)
                row.insert(20, against_percentage)
                row.pop(21)
                row.insert(21, percentage_more)
                row.pop(22)
                row.insert(22, percentage_3)
                row.pop(23)
                row.insert(23, percentage_2)
                row.pop(24)
                row.insert(24, percentage_1)
                row.pop(25)
                row.insert(25, percentage_0)
                row.pop(26)
                row.insert(26, percentage__1)
                row.pop(27)
                row.insert(27, percentage__2)
                row.pop(28)
                row.insert(28, percentage__3)
                row.pop(29)
                row.insert(29, percentage__more)
                calculated_list.append(row)
            except ZeroDivisionError:
                zero=0
                home_percentage = "{:.0%}".format(zero)
                deal_percentage = "{:.0%}".format(zero)
                against_percentage = "{:.0%}".format(zero)
                percentage__more = "{:.0%}".format(zero)
                percentage__3 = "{:.0%}".format(zero)
                percentage__2 = "{:.0%}".format(zero)
                percentage__1 = "{:.0%}".format(zero)
                percentage_0 = "{:.0%}".format(zero)
                percentage_1 = "{:.0%}".format(zero)
                percentage_2 = "{:.0%}".format(zero)
                percentage_3 = "{:.0%}".format(zero)
                percentage_more = "{:.0%}".format(zero)
                row.pop(17)
                row.insert(17, count)
                row.pop(18)
                row.insert(18, home_percentage)
                row.pop(19)
                row.insert(19, deal_percentage)
                row.pop(20)
                row.insert(20, against_percentage)
                row.pop(21)
                row.insert(21, percentage_more)
                row.pop(22)
                row.insert(22, percentage_3)
                row.pop(23)
                row.insert(23, percentage_2)
                row.pop(24)
                row.insert(24, percentage_1)
                row.pop(25)
                row.insert(25, percentage_0)
                row.pop(26)
                row.insert(26, percentage__1)
                row.pop(27)
                row.insert(27, percentage__2)
                row.pop(28)
                row.insert(28, percentage__3)
                row.pop(29)
                row.insert(29, percentage__more)
                calculated_list.append(row)
        else:
            for i in calculated_list:
                if (row[0][:10] == i[0][:10]) and (row[16] == i[16]):
                    print(row)
                    print(i)
                    row.pop(17)
                    row.insert(17, i[17])
                    row.pop(18)
                    row.insert(18, i[18])
                    row.pop(19)
                    row.insert(19, i[19])
                    row.pop(20)
                    row.insert(20, i[20])
                    row.pop(21)
                    row.insert(21, i[21])
                    row.pop(22)
                    row.insert(22, i[22])
                    row.pop(23)
                    row.insert(23, i[23])
                    row.pop(24)
                    row.insert(24, i[24])
                    row.pop(25)
                    row.insert(25, i[25])
                    row.pop(26)
                    row.insert(26, i[26])
                    row.pop(27)
                    row.insert(27, i[27])
                    row.pop(28)
                    row.insert(28, i[28])
                    row.pop(29)
                    row.insert(29, i[29])
                    calculated_list.append(row)
    poped=calculated_list.pop(0)
    with open(os.path.abspath("converted_csv_datas\main_result")+"\\main_prxg_result.csv", "w", newline='', encoding='utf-8') as file:
        new_file = csv.DictWriter(file, dialect='excel',fieldnames=header)
        new_file.writeheader()
    with open(os.path.abspath("converted_csv_datas\main_result")+"\\main_prxg_result.csv", "a", newline='', encoding='utf-8') as file:
        new_file = csv.writer(file, dialect='excel')
        new_file.writerows(calculated_list)
    pr_col()
    pr()

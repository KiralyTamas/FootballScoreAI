import os
from datas_for_converting.file_caller import caller
from datas_for_converting.fixtures_result_converter import convert_fr
from datas_for_converting.match_converter import convert_m
from datas_for_converting.table_converter import convert_t

f = []
for (dirpath, dirnames, filenames) in os.walk(input("Mi a konvertálandó fájlok mappájának útvonala: ")):
    f.extend(filenames)
    break


def convert():
  main_path=f
  for i in main_path:
    all_path=str(dirpath)+"\\"+str(i)
    recall= caller(all_path)
    if recall[0] == all_path[-4:]:
      continue
    if "fixtures" in recall[0]:
      convert_fr(recall,"_")
    if "result" in recall[0]:
      convert_fr(recall,"_")
    if "match" in recall[0]:
      convert_m(recall)
    if "table" in recall[0]:
      convert_t(recall)
convert()
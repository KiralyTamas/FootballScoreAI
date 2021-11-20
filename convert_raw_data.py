import os
from data_handler_files.converter_files.file_caller import caller
from data_handler_files.converter_files.fixtures_converter import convert_f
from data_handler_files.converter_files.result_converter import convert_r
from data_handler_files.converter_files.match_converter import convert_m
from data_handler_files.converter_files.table_converter import convert_t
from data_handler_files.converter_files.epl_converter import convert_epl

f = []
for (dirpath, dirnames, filenames) in os.walk(input("Mi a konvertálandó fájlok mappájának útvonala: ")):
    f.extend(filenames)
    break


def convert():
  csv_path=os.path.abspath("converted_csv_datas")
  main_path=f
  for i in main_path:
    all_path=str(dirpath)+"\\"+str(i)
    recall= caller(all_path,i)
    if recall[0] == all_path[-4:]:
      continue
    if "fixtures" in recall[0]:
      convert_f(recall,"_")
      os.remove(all_path)
    if "epl_" in recall[0]:
      convert_epl(recall,"_")
      os.remove(all_path)
    if "result" in recall[0]:
      convert_r(recall,"_")
      os.remove(all_path)
    if "match" in recall[0]:
      try:
        convert_m(recall)
        os.remove(all_path)
      except IndexError:
        if IndexError == True:
          continue
    if "table" in recall[0]:
      convert_t(recall)
      os.remove(all_path)
convert()
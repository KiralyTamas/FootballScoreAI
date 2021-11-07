from datas_for_converting.file_caller import caller
from datas_for_converting.fixtures_result_converter import convert_fr
from datas_for_converting.match_converter import convert_m
from datas_for_converting.table_converter import convert_t

main_path=""
def convert():
  main_path=input("Mi a konvertálandó fájl útvonala: ")
  recall= caller(main_path)
  if "fixtures" in recall[0]:
    convert_fr(recall,"_")
  if "result" in recall[0]:
    convert_fr(recall,"_")
  if "match" in recall[0]:
    convert_m(recall)
  if "table" in recall[0]:
    convert_t(recall)
convert()
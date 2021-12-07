import os
from data_handler_files.converter_files.file_caller import caller
from data_handler_files.converter_files.fixtures_converter import convert_f
from data_handler_files.converter_files.result_converter import convert_r
from data_handler_files.converter_files.match_converter import convert_m
from data_handler_files.converter_files.table_converter import convert_t
from data_handler_files.converter_files.epl_converter import convert_epl




def convert():
  f = []
  g=[]
  h=[]
  for (dirpath, dirnames, filenames) in os.walk("raw_json_datas"):
    f.extend(filenames)
    g.extend(dirnames)
    h.append(dirpath)
  for i in h:
    for j in g:
      for k in f:
        try:
          current_path=os.path.abspath(i+"/"+j+"/"+k)
          recall= caller(current_path,k)
          if "fixtures" in k:
            convert_f(recall,"_",k)
            os.remove(current_path)
            continue
          if "epl_" in k:
            convert_epl(recall,"_")
            os.remove(current_path)
            continue
          if "result" in k:
            convert_r(recall,"_")
            os.remove(current_path)
            continue
          if "match" in k:
            convert_m(recall)
            os.remove(current_path)
            continue
          if "table" in k:
            convert_t(recall)
            os.remove(current_path)
        except TypeError:
          if TypeError==True:
            continue
          
convert()
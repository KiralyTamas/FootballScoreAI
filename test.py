import os

destiny=os.path.abspath("converted_csv_datas")
start=os.path.abspath("raw_json_datas\match")
path=os.path.relpath(start,destiny)
print(destiny)
print(start)
print(path)
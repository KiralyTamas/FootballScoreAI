import csv

with open("main_fixture.csv","r",encoding="utf-8") as data:
  data=csv.reader(data)
  list_correct=sorted(data, key=lambda date:date[12], reverse=True)
with open("main_fixture.csv","w",newline='', encoding="utf-8") as data:
  data=csv.writer(data)
  data.writerows(list_correct)
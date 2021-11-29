import csv

def date_sorting(letter):
  try:
    input_info=input("Növekvő sorrend: 'n', Csökkenő sorrend: 'c'")
    with open("main_result.csv","r",encoding="utf-8") as data:
      data=csv.reader(data)
      sample=[]
      for i in data:
        sample.append(i)
      poped=sample.pop(0)
      if input_info== str(letter):
        list_correct=sorted(sample, key=lambda date:date[0], reverse=False)
      else:
        list_correct=sorted(sample, key=lambda date:date[0], reverse=True)
      list_correct.insert(0,poped)
    with open("main_result.csv","w",newline='', encoding="utf-8") as data:
      data=csv.writer(data)
      data.writerows(list_correct)
  except FileNotFoundError:
    return
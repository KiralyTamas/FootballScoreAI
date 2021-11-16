import pandas as pd
import os
import csv
path=os.path.abspath("teams/bundesliga")

def create_team_csv():
    cup = input("Melyik bajnokságról van szó?")
    with open(cup, "r") as file:
        csv_file = csv.reader(file)
        df = pd.DataFrame(csv_file)
        for row_index,row in df.iterrows():
            if row_index==0:
                continue
            date=row[12],row[1]
            h_team=row[3]
            a_team=row[6]
            h_gol = row[8]
            a_gol = row[9]
            score = int(h_gol)-int(a_gol)
            data=date[0],date[1],h_team,h_gol,a_team,a_gol,score
            if path+"\\"+h_team+".csv" == True:
                with open(path+"\\"+h_team+".csv","r",newline='') as team_csv:
                    csv_data=csv.reader(team_csv)
                    for lines in csv_data:
                        raw_data=[]
                        raw_data.extend(lines)
                    raw_data.insert(0,data)
                with open(path+"\\"+h_team+".csv","a",newline='') as team_csv:
                    team_file=csv.writer(team_csv)
                    team_file.writerow(raw_data)
            else:    
                with open(path+"\\"+h_team+".csv","w",newline='') as team_csv:
                    team_file=csv.writer(team_csv)
                    team_file.writerow(data)
            
                

create_team_csv()
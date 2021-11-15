import pandas as pd
import os
cup=input("Melyik bajnokságról van szó?")
folder=input("Hova legyenek elmentve a fájlok?")
f = []
for (dirpath, dirnames, filenames) in os.walk(os.path.abspath(folder)):
    f.extend(filenames)
    break


def create_team_csv():
    df = pd.read_csv(cup)
    h_title = df["h_title"]
    a_title = df["a_title"]
    for i in range(len(h_title)):
        if (h_title[i]+".csv") not in f:
            with open(folder+"/"+h_title[i]+".csv", "w"):
                continue
        elif (a_title[i]+".csv") not in f:
            with open(folder+"/"+a_title[i]+".csv", "w"):
                continue

create_team_csv()
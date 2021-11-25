import asyncio
import json
import os
import csv
import xlsxwriter
import aiohttp
from understat import Understat


async def main():
    raw_matches=os.path.abspath("../../raw_json_datas/match")
    # Ez a két sor megkérdezi, hogy melyik ID-től melyik ID-ig fusson le a lekérdezés. Manuálisan kell a terminálban megadni a számokat.
    with open("match_ids.csv","r") as file:
        list_of_num=csv.reader(file)
        number=[]
        for num in list_of_num:
            number.append(num)
    # A for ciklus használja az előzőleg megadott értékeket. Ha 1-et és 200-at adsz meg, akkor a ciklus ideiglenesen készít 199darab "page" változót, amibe alapértelmezetten 1-egy növekedve eltárolja a két megadott érték közötti számokat. 
    # minden ciklus lefutása után autómatikusan a következő "page" változót illeszti be a folyamatba.
    for page in num:
        # try függvény. A try fügvény "megpróbálja" futtatni a benne szereplő kódot.
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                understat = Understat(session)
                match = await understat.get_match_shots(page)
                f = open(raw_matches+"\match"+str(page)+".json", "w")
                f.write(json.dumps(match))
                f.close()
        # A try függvényt csak az except fügvénnyel együtt lehet alkalmazni
        # Ha a try hibára fut, akkor "el lehet kapni a hibakódot" -UnboundLocalError- és a konkrét hiba esetén más folyamatot lehet elindítani.
        # Mivel jelen esetben "ID hiány" miatt megszakad a lekérdezés, ezért UnboundLocalError kódot eredményez.
        except UnboundLocalError:
        # A hiba létrejötte esetén a lenti szöveget kiiratom a konsole-ba az aktuális ID számmal: str(page). Az itt látható page a for ciklusnak köszönhetően mindíg az aktuálisan vizsgált-lekérdezett ID-számot képviseli
            print("Nem találtam az "+str(page)+" Id számmal mach információkat!")
        # Ez a sor egy feltétel. Ha az UnboundLocalError igaz, vagyis fennál a hiba, akkor a "continue" paranccsal átléptetem a folyamatot a következő for ciklusra. 
            if UnboundLocalError == True:
                continue
        # Ezt az "if-continue" kapcsolatot csak for cikluson belül lehet használni. Máskülönben nem tudja ez a kapcsolat, hogy hova kellene továbbléptetni a folyamatot és hibára fog futni.

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
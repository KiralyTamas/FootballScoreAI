import asyncio
import json
import os
import xlsxwriter
import aiohttp
from understat import Understat


async def main():
    caller_path=os.getcwd()
    final_path=os.path.abspath(input("Hova legyenek letöltve a fájlok? "))
    final=os.path.relpath(final_path,caller_path)
    # Ez a két sor megkérdezi, hogy melyik ID-től melyik ID-ig fusson le a lekérdezés. Manuálisan kell a terminálban megadni a számokat.
    page_start = int(input("Mi az Id szám, ahonnan a lekérdezés induljon?:")) # Példa: 1
    page_end=int(input("Mi az Id szám, ameddig a lekérdezés tartson?:")) # Példa: 200
    # A for ciklus használja az előzőleg megadott értékeket. Ha 1-et és 200-at adsz meg, akkor a ciklus ideiglenesen készít 199darab "page" változót, amibe alapértelmezetten 1-egy növekedve eltárolja a két megadott érték közötti számokat. 
    # minden ciklus lefutása után autómatikusan a következő "page" változót illeszti be a folyamatba.
    for page in range(page_start,page_end):
        # try függvény. A try fügvény "megpróbálja" futtatni a benne szereplő kódot.
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                understat = Understat(session)
                players = await understat.get_match_shots(page)
                f = open(final+"\match"+str(page)+".json", "w")
                f.write(json.dumps(players))
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
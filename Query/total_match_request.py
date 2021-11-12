import asyncio
import json

import xlsxwriter

import aiohttp

from understat import Understat

async def main():
    page_start = int(input("Mi az Id szám, ahonnan a lekérdezés induljon?:"))
    page_end=int(input("Mi az Id szám, ameddig a lekérdezés tartson?:"))
    for page in range(page_start,page_end,1):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                understat = Understat(session)
                players = await understat.get_match_shots(page)
                f = open(f"C:\Repository\FootballScoreAI\datas_for_converting\match\match{page}.json", "w")
                f.write(json.dumps(players))
                f.close()
        except UnboundLocalError:
            print("Nem találtam az "+str(page)+" Id számmal mach információkat!")
            if UnboundLocalError == True:
                continue

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
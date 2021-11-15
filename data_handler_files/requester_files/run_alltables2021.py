import asyncio
import json
import os
import xlsxwriter

import aiohttp

from understat import Understat


async def main():
    raw_tables=os.path.abspath("../../raw_json_datas/table/2021")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        understat = Understat(session)
        tableepl = await understat.get_league_table("epl", 2021)
        tablelaliga = await understat.get_league_table("la_liga", 2021)
        tablebundesliga = await understat.get_league_table("bundesliga", 2021)
        tableseriea = await understat.get_league_table("serie_a", 2021)
        tableligue1 = await understat.get_league_table("ligue_1", 2021)
        tablerfpl = await understat.get_league_table("rfpl", 2021)

        f = open(raw_tables+"/tableepl2021.json", "w")
        f.write(json.dumps(tableepl))

        f = open(raw_tables+"/tablelaliga2021.json", "w")
        f.write(json.dumps(tablelaliga))

        f = open(raw_tables+"/tablebundesliga2021.json", "w")
        f.write(json.dumps(tablebundesliga))

        f = open(raw_tables+"/tableseriea2021.json", "w")
        f.write(json.dumps(tableseriea))

        f = open(raw_tables+"/tableligueOne2021.json", "w")
        f.write(json.dumps(tableligue1))

        f = open(raw_tables+"/tablerfpl2021.json", "w")
        f.write(json.dumps(tablerfpl))
        f.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
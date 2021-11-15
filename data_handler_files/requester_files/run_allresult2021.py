import asyncio
import json

import xlsxwriter

import aiohttp

from understat import Understat


async def main():
    raw_result=os.path.abspath("../../raw_json_datas/result/2021")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        understat = Understat(session)
        tableepl = await understat.get_league_results("epl", 2021)
        tablelaliga = await understat.get_league_results("la_liga", 2021)
        tablebundesliga = await understat.get_league_results("bundesliga", 2021)
        tableseriea = await understat.get_league_results("serie_a", 2021)
        tableligue1 = await understat.get_league_results("ligue_1", 2021)
        tablerfpl = await understat.get_league_results("rfpl", 2021)

        f = open(raw_result+"/resultepl2021.json", "w")
        f.write(json.dumps(tableepl))

        f = open(raw_result+"/resultlaliga2021.json", "w")
        f.write(json.dumps(tablelaliga))

        f = open(raw_result+"/resultbundesliga2021.json", "w")
        f.write(json.dumps(tablebundesliga))

        f = open(raw_result+"/resultseriea2021.json", "w")
        f.write(json.dumps(tableseriea))

        f = open(raw_result+"/resultligueOne2021.json", "w")
        f.write(json.dumps(tableligue1))

        f = open(raw_result+"/resultrfpl2021.json", "w")
        f.write(json.dumps(tablerfpl))
        f.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
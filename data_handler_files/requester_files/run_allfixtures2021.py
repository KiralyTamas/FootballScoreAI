import asyncio
import json

import xlsxwriter
import os
import aiohttp

from understat import Understat


async def main():
    raw_tables=os.path.abspath("../../raw_json_datas")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        understat = Understat(session)
        fixturesepl = await understat.get_league_fixtures("epl", 2021)
        fixtureslaliga = await understat.get_league_fixtures("la_liga", 2021)
        fixturesbundesliga = await understat.get_league_fixtures("bundesliga", 2021)
        fixturesseriea = await understat.get_league_fixtures("serie_a", 2021)
        fixturesligue1 = await understat.get_league_fixtures("ligue_1", 2021)
        fixturesrfpl = await understat.get_league_fixtures("rfpl", 2021)

        f = open(raw_tables+"/fixtures/fixturesepl.json", "w")
        f.write(json.dumps(fixturesepl))

        f = open(raw_tables+"/fixtures/fixtureslaliga.json", "w")
        f.write(json.dumps(fixtureslaliga))

        f = open(raw_tables+"/fixtures/fixturesbundesliga.json", "w")
        f.write(json.dumps(fixturesbundesliga))

        f = open(raw_tables+"/fixtures/fixturesseriea.json", "w")
        f.write(json.dumps(fixturesseriea))

        f = open(raw_tables+"/fixtures/fixturesligue1.json", "w")
        f.write(json.dumps(fixturesligue1))

        f = open(raw_tables+"/fixtures/fixturesrfpl.json", "w")
        f.write(json.dumps(fixturesrfpl))
        f.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
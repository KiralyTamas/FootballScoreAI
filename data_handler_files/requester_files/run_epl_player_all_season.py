import asyncio
import json
import os
import xlsxwriter

import aiohttp

from understat import Understat


async def main():
    eplplayer_path=os.path.abspath("../../raw_json_datas/epl_player")
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        understat = Understat(session)
        player2021 = await understat.get_league_players("epl", 2021)
        player2020 = await understat.get_league_players("epl", 2020)
        player2019 = await understat.get_league_players("epl", 2019)
        player2018 = await understat.get_league_players("epl", 2018)
        player2017 = await understat.get_league_players("epl", 2017)
        player2016 = await understat.get_league_players("epl", 2016)
        player2015 = await understat.get_league_players("epl", 2015)
        player2014 = await understat.get_league_players("epl", 2014)

        f = open(eplplayer_path+"/epl_player2021.json", "w")
        f.write(json.dumps(player2021))

        f = open(eplplayer_path+"/epl_player2020.json", "w")
        f.write(json.dumps(player2020))

        f = open(eplplayer_path+"/epl_player2019.json", "w")
        f.write(json.dumps(player2019))

        f = open(eplplayer_path+"/epl_player2018.json", "w")
        f.write(json.dumps(player2018))

        f = open(eplplayer_path+"/epl_player2017.json", "w")
        f.write(json.dumps(player2017))

        f = open(eplplayer_path+"/epl_player2016.json", "w")
        f.write(json.dumps(player2016))

        f = open(eplplayer_path+"/epl_player2015.json", "w")
        f.write(json.dumps(player2015))

        f = open(eplplayer_path+"/epl_player2014.json", "w")
        f.write(json.dumps(player2014))

        f.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
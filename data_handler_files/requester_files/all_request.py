import asyncio
import json
import xlsxwriter
import os
import csv
import aiohttp
from understat import Understat
from data_handler_files.requester_files.match_id_collector import id_collect as coll
from data_handler_files.converter_files.convert_raw_data import convert as con


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        raw_fixtures = os.path.abspath("raw_json_datas/fixtures")
        if os.path.exists('raw_json_datas') == False:
            os.mkdir('raw_json_datas')
        if os.path.exists(raw_fixtures) == False:
            os.mkdir(raw_fixtures)
        raw_tables = os.path.abspath("raw_json_datas/table/2021")
        if os.path.exists(raw_tables) ==False:
            os.mkdir(os.path.abspath("raw_json_datas/table"))
            os.mkdir(raw_tables)
        raw_result = os.path.abspath("raw_json_datas/result/2021")
        if os.path.exists(raw_result) ==False:
            os.mkdir(os.path.abspath("raw_json_datas/result"))
            os.mkdir(raw_result)
        player = os.path.abspath("raw_json_datas/player")
        if os.path.exists(player) ==False:
            os.mkdir(player)
        raw_matches = os.path.abspath("raw_json_datas/match")
        if os.path.exists(raw_matches) ==False:
            os.mkdir(raw_matches)
        understat = Understat(session)
        fixturesepl = await understat.get_league_fixtures("epl", 2021)
        fixtureslaliga = await understat.get_league_fixtures("la_liga", 2021)
        fixturesbundesliga = await understat.get_league_fixtures("bundesliga", 2021)
        fixturesseriea = await understat.get_league_fixtures("serie_a", 2021)
        fixturesligue1 = await understat.get_league_fixtures("ligue_1", 2021)
        fixturesrfpl = await understat.get_league_fixtures("rfpl", 2021)
        tableepl = await understat.get_league_table("epl", 2021)
        tablelaliga = await understat.get_league_table("la_liga", 2021)
        tablebundesliga = await understat.get_league_table("bundesliga", 2021)
        tableseriea = await understat.get_league_table("serie_a", 2021)
        tableligue1 = await understat.get_league_table("ligue_1", 2021)
        tablerfpl = await understat.get_league_table("rfpl", 2021)
        resultepl = await understat.get_league_results("epl", 2021)
        resultlaliga = await understat.get_league_results("la_liga", 2021)
        resultbundesliga = await understat.get_league_results("bundesliga", 2021)
        resultseriea = await understat.get_league_results("serie_a", 2021)
        resultligue1 = await understat.get_league_results("ligue_1", 2021)
        resultrfpl = await understat.get_league_results("rfpl", 2021)
        epl_2021 = await understat.get_league_players("epl", 2021)
        la_liga_2021 = await understat.get_league_players("la_liga", 2021)
        bundesliga_2021 = await understat.get_league_players("bundesliga", 2021)
        serie_a_2021 = await understat.get_league_players("serie_a", 2021)
        ligue_1_2021 = await understat.get_league_players("ligue_1", 2021)
        rfpl_2021 = await understat.get_league_players("rfpl", 2021)

        with open(raw_tables+"/tableepl2021.json", "w") as file:
            file.write(json.dumps(tableepl))
        with open(raw_tables+"/tablelaliga2021.json", "w") as file:
            file.write(json.dumps(tablelaliga))
        with open(raw_tables+"/tablebundesliga2021.json", "w") as file:
            file.write(json.dumps(tablebundesliga))
        with open(raw_tables+"/tableseriea2021.json", "w") as file:
            file.write(json.dumps(tableseriea))
        with open(raw_tables+"/tableligueOne2021.json", "w") as file:
            file.write(json.dumps(tableligue1))
        with open(raw_tables+"/tablerfpl2021.json", "w") as file:
            file.write(json.dumps(tablerfpl))
        with open(raw_fixtures+"/fixturesepl.json", "w") as file:
            file.write(json.dumps(fixturesepl))
        with open(raw_fixtures+"/fixtureslaliga.json", "w") as file:
            file.write(json.dumps(fixtureslaliga))
        with open(raw_fixtures+"/fixturesbundesliga.json", "w") as file:
            file.write(json.dumps(fixturesbundesliga))
        with open(raw_fixtures+"/fixturesseriea.json", "w") as file:
            file.write(json.dumps(fixturesseriea))
        with open(raw_fixtures+"/fixturesligue1.json", "w") as file:
            file.write(json.dumps(fixturesligue1))
        with open(raw_fixtures+"/fixturesrfpl.json", "w") as file:
            file.write(json.dumps(fixturesrfpl))
        with open(raw_result+"/resultepl2021.json", "w") as file:
            file.write(json.dumps(resultepl))
        with open(raw_result+"/resultlaliga2021.json", "w") as file:
            file.write(json.dumps(resultlaliga))
        with open(raw_result+"/resultbundesliga2021.json", "w") as file:
            file.write(json.dumps(resultbundesliga))
        with open(raw_result+"/resultseriea2021.json", "w") as file:
            file.write(json.dumps(resultseriea))
        with open(raw_result+"/resultligueOne2021.json", "w") as file:
            file.write(json.dumps(resultligue1))
        with open(raw_result+"/resultrfpl2021.json", "w") as file:
            file.write(json.dumps(resultrfpl))
        with open(player+"/epl_player2021.json", "w") as file:
            file.write(json.dumps(epl_2021))
        with open(player+"/la_liga_player2021.json", "w") as file:
            file.write(json.dumps(la_liga_2021))
        with open(player+"/bundesliga_player2021.json", "w") as file:
            file.write(json.dumps(bundesliga_2021))
        with open(player+"/serie_a_player2021.json", "w") as file:
            file.write(json.dumps(serie_a_2021))
        with open(player+"/ligue_1_player2021.json", "w") as file:
            file.write(json.dumps(ligue_1_2021))
        with open(player+"/rfpl_player2021.json", "w") as file:
            file.write(json.dumps(rfpl_2021))

        id_list=coll()
        for page in id_list:
            try:
                understat = Understat(session)
                match = await understat.get_match_shots(page)
                f = open(raw_matches+"\match"+str(page)+".json", "w")
                f.write(json.dumps(match))
                f.close()
                if page == id_list[-1]:
                    con()
            except UnboundLocalError:
                print("Nem találtam az "+str(page) +" Id számmal mach információkat!")
                if page == id_list[-1]:
                    con()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
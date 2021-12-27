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
        eplplayer = os.path.abspath("raw_json_datas/epl_player")
        if os.path.exists(eplplayer) ==False:
            os.mkdir(eplplayer)
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
        player2021 = await understat.get_league_players("epl", 2021)
        player2020 = await understat.get_league_players("epl", 2020)
        player2019 = await understat.get_league_players("epl", 2019)
        player2018 = await understat.get_league_players("epl", 2018)
        player2017 = await understat.get_league_players("epl", 2017)
        player2016 = await understat.get_league_players("epl", 2016)
        player2015 = await understat.get_league_players("epl", 2015)
        player2014 = await understat.get_league_players("epl", 2014)
        laliga2021 = await understat.get_league_players("la_liga", 2021)

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
        with open(eplplayer+"/epl_player2021.json", "w") as file:
            file.write(json.dumps(player2021))
        with open(eplplayer+"/epl_player2020.json", "w") as file:
            file.write(json.dumps(player2020))
        with open(eplplayer+"/epl_player2019.json", "w") as file:
            file.write(json.dumps(player2019))
        with open(eplplayer+"/epl_player2018.json", "w") as file:
            file.write(json.dumps(player2018))
        with open(eplplayer+"/epl_player2017.json", "w") as file:
            file.write(json.dumps(player2017))
        with open(eplplayer+"/epl_player2016.json", "w") as file:
            file.write(json.dumps(player2016))
        with open(eplplayer+"/epl_player2015.json", "w") as file:
            file.write(json.dumps(player2015))
        with open(eplplayer+"/epl_player2014.json", "w") as file:
            file.write(json.dumps(player2014))
        with open(eplplayer+"/la_liga_player2021.json", "w") as file:
            file.write(json.dumps(laliga2021))

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
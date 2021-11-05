import json
import os

from sqlalchemy import create_engine

from endpoint_caller import EndpointCaller
from OBSOLETE.dataPuller import ApiMediator, filter_leagues, filter_leagues_with_odds
import pandas as pd

from response_converter import ResponseConverter

from config import *
from verifiers import Verifiers

pd.set_option('display.max_columns', None)

####################################################################
# Script used to create large CSVs, to fill an empty database with #
####################################################################

endpointCaller = EndpointCaller(API_KEY, HOST_URL, is_rapid_api=False)
apiMediator = ApiMediator(endpointCaller)


def get_cached_file(filename):
    file_path = os.path.join("cache", filename)
    with open(file_path, "r", encoding="utf-8") as cacheFile:
        cache = json.loads(cacheFile.read())
    return cache


def download_fixtures():
    leagues = apiMediator.retrieve_leagues()
    all_leagues = filter_leagues(leagues)
    fixtures = apiMediator.retrieve_fixtures(all_leagues, caching=True)
    fixtures.to_csv("fixtures_all.csv")


def download_odds():
    dfs = []
    for file in os.listdir(os.path.join("cache")):
        print(file)
        df = ResponseConverter.get_odds(get_cached_file(file))
        if df is not None:
            dfs.append(df)
    pd.concat(dfs).to_csv("all_odds2.csv")


def get_fixture_extras(fixture_id):
    response = endpointCaller.call("/fixtures/id/{}?timezone=Europe/Budapest".format(fixture_id))
    with open(os.path.join("extras_responses", str(fixture_id) + ".json"), "w+", encoding="utf-8") as file:  # save response
        file.write(json.dumps(response))
    is_good = Verifiers.verify_extras_fixture(response)
    if is_good:
        print(fixture_id)
        print(response)
        return None, None, None, None, None
    df_fixture = ResponseConverter.get_extras_fixture(response)
    df_event = ResponseConverter.get_events(response)
    df_statistics = ResponseConverter.get_statistics(response)
    df_players = ResponseConverter.get_players(response)
    df_lineups = ResponseConverter.get_lineups(response)
    return df_fixture, df_event, df_statistics, df_players, df_lineups


def download_additional_fixture_data(fixture_ids):
    df_fixtures = []
    df_events = []
    df_statistics = []
    df_players = []
    df_lineups = []

    for fixture_id in fixture_ids:
        df_fixture, df_event, df_statistic, df_player, df_lineup = get_fixture_extras(fixture_id)
        print(fixture_id)
        if df_fixture is not None:
            df_fixtures.append(df_fixture)
        if df_event is not None:
            df_events.append(df_event)
        if df_statistic is not None:
            df_statistics.append(df_statistic)
        if df_player is not None:
            df_players.append(df_player)
        if df_lineup is not None:
            df_lineups.append(df_lineup)

    if len(df_fixtures) > 0:
        pd.concat(df_fixtures).to_csv("fixtures_extra_all.csv")
    if len(df_events) > 0:
        pd.concat(df_events).to_csv("events_all.csv")
    if len(df_statistics) > 0:
        pd.concat(df_statistics).to_csv("statistics_all.csv")
    if len(df_players) > 0:
        pd.concat(df_players).to_csv("players_all.csv")
    if len(df_lineups) > 0:
        pd.concat(df_lineups).to_csv("lineups_all.csv")


engine = create_engine('mssql+pyodbc://football:G3Ff2C63gvB@football2020.database.windows.net/football-db?driver=SQL+Server')
df = pd.read_sql_query("select [fixture.fixture_id] from odds group by [fixture.fixture_id]", con=engine)
fixture_ids_with_odds = df["fixture.fixture_id"]
download_additional_fixture_data(fixture_ids_with_odds)

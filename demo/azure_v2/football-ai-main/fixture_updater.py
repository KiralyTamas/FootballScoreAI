import logging

import pandas as pd
from datetime import date, timedelta

from api_mediator import ApiMediator
from config import *
from database_mediator import DatabaseMediator
from endpoint_caller import EndpointCaller

endpointCaller = EndpointCaller(API_KEY, HOST_URL, is_rapid_api=False)
api_mediator = ApiMediator(endpointCaller)
database_mediator = DatabaseMediator("football2020.database.windows.net",
                                     user="football",
                                     password="G3Ff2C63gvB",
                                     database="football-db")


def get_past_dates_to_update(latest_insert):
    latest_insert = pd.to_datetime(latest_insert).date()
    todays_date = date.today()
    days = pd.date_range(latest_insert - timedelta(days=1), todays_date, freq="d")
    dates_to_update = [day.strftime("%Y-%m-%d") for day in days]
    return dates_to_update


def get_future_dates_to_update():
    todays_date = date.today()
    days = pd.date_range(todays_date + timedelta(days=1), todays_date + timedelta(days=2), freq="d")
    dates_to_update = [day.strftime("%Y-%m-%d") for day in days]
    dates_to_update.append((todays_date + timedelta(days=7)).strftime("%Y-%m-%d"))
    return dates_to_update


logging.getLogger().setLevel(logging.INFO)
logging.info('Starting fixture updater')

# update leagues too, while we're at it
df_leagues = api_mediator.retrieve_leagues(retries=2)
df_leagues = df_leagues[df_leagues["type"] == "League"]
database_mediator.write_leagues_overwrite(df_leagues)

# get dates
latest_insert = database_mediator.get_latest_fixture_insert()
past_dates_to_update = get_past_dates_to_update(latest_insert)
future_dates_to_update = get_future_dates_to_update()

# get extras
df_past = api_mediator.retrieve_fixtures_for_dates(past_dates_to_update, retries=2)
fixture_ids = df_past.reset_index()["fixture_id"]
dfs_extrafixtures, dfs_events, dfs_statistics, dfs_players, dfs_lineups = api_mediator.retrieve_extras_for_fixtures(fixture_ids, retries=2)

# get fixtures
df_future = api_mediator.retrieve_fixtures_for_dates(future_dates_to_update, retries=2)
df = pd.concat([df_past, df_future])

# get predictions
fixture_ids = df.reset_index()["fixture_id"]
df_predictions = api_mediator.retrieve_predictions_for_fixtures(fixture_ids)

# write to db
database_mediator.write_fixture_overwrite(df)
database_mediator.write_fixture_extras_overwrite(dfs_extrafixtures, dfs_events, dfs_statistics, dfs_players, dfs_lineups)
database_mediator.write_predictions(df_predictions)

import json
import os

from sqlalchemy import create_engine, event

from endpoint_caller import EndpointCaller
import pandas as pd

from response_converter import ResponseConverter

from config import *
from verifiers import Verifiers

pd.set_option('display.max_columns', None)


############################################
# This file currently is only for drafting #
############################################



engine = create_engine('mssql+pyodbc://football:G3Ff2C63gvB@football2020.database.windows.net/football-db?driver=SQL+Server')
df = pd.read_sql_query("select [fixture.fixture_id] from odds group by [fixture.fixture_id]", con=engine)
for fixture in df["fixture.fixture_id"].values:
    print(fixture)
    exit()
print(df)
exit()


df = pd.read_csv("fixtures_all.csv")
df = df.set_index("fixture_id", verify_integrity=True)
df["event_date"] = pd.to_datetime(df["event_date"])
del df["Unnamed: 0"]
print(df.shape)


exit()


endpointCaller = EndpointCaller(API_KEY, HOST_URL, is_rapid_api=False)
engine = create_engine('mssql+pyodbc://football:G3Ff2C63gvB@football2020.database.windows.net/football-db?driver=SQL+Server')
fixture_id = 654100
response = endpointCaller.call("/fixtures/id/654100?timezone=Europe/Budapest")
is_good = Verifiers.verify_extras_fixture(response)
if is_good:
    print(response)
    exit()
df = ResponseConverter.get_extras_fixture(response)
df_event = ResponseConverter.get_events(response)
df_statistics = ResponseConverter.get_statistics(response)
df_players = ResponseConverter.get_players(response)
df_lineups = ResponseConverter.get_lineups(response)

response = endpointCaller.call("/predictions/654100")
df_predictions = ResponseConverter.get_predictions(response, fixture_id)
df_h2h_prediction = ResponseConverter.get_h2h_prediction(response)

response = endpointCaller.call("/odds/fixture/652100")
df_odds = ResponseConverter.get_odds(response)

#print(pd.io.sql.get_schema(df.reset_index(), "fixtures"))
#print(pd.io.sql.get_schema(df_event.reset_index(), "events"))
#print(pd.io.sql.get_schema(df_statistics.reset_index(), "statistics"))
#print(pd.io.sql.get_schema(df_players.reset_index(), "players"))
#print(pd.io.sql.get_schema(df_lineups.reset_index(), "lineups"))
#print(pd.io.sql.get_schema(df_predictions.reset_index(), "predictions"))
#print(pd.io.sql.get_schema(df_h2h_prediction.reset_index(), "h2h_prediction"))
#print(pd.io.sql.get_schema(df_odds.reset_index(), "odds"))
#df.to_csv("fixtures.csv")
#df_event.to_csv("events.csv")
#df_statistics.to_csv("statistics.csv")
#df_players.to_csv("players.csv")
#df_lineups.to_csv("lineups.csv")
#df_predictions.to_csv("predictions.csv")
#df_h2h_prediction.to_csv("h2h_prediction.csv")
#df_odds.to_csv("odds.csv")

#df.to_sql("fixtures", con=engine, if_exists='append')
df_event.to_sql("events", con=engine, if_exists='append', index=False)
#df_statistics.to_sql("statistics", con=engine, if_exists='append')
#df_players.to_sql("players", con=engine, if_exists='append')
#df_lineups.to_sql("lineups", con=engine, if_exists='append')
#df_predictions.to_sql("predictions", con=engine, if_exists='append')
#df_h2h_prediction.to_sql("h2h_prediction", con=engine, if_exists='append')
#df_odds.to_sql("odds", con=engine, if_exists='append', index=False)


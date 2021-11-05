import logging

from api_mediator import ApiMediator
from config import *
from database_mediator import DatabaseMediator
from endpoint_caller import EndpointCaller


logging.getLogger().setLevel(logging.INFO)
logging.info('Starting odds updater')

endpointCaller = EndpointCaller(API_KEY, HOST_URL, is_rapid_api=False)
api_mediator = ApiMediator(endpointCaller)
database_mediator = DatabaseMediator("football2020.database.windows.net",
                                     user="football",
                                     password="G3Ff2C63gvB",
                                     database="football-db")

df_odds_mappings = api_mediator.retrieve_odds_mappings()
database_mediator.write_odds_mappings(df_odds_mappings)
fixture_ids = database_mediator.get_notupdated_fixtureids_from_oddsmappings()
df_odds = api_mediator.retrieve_odds_for_fixtures(fixture_ids, retries=2)
database_mediator.write_firstodds(df_odds)
database_mediator.write_odds(df_odds)
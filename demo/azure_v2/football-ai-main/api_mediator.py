import logging
import time

import pandas as pd

from config import BOOKMAKER_ID
from response_converter import ResponseConverter
from verifiers import Verifiers


class ApiMediator:
    def __init__(self, endpoint_caller):
        self.endpoint_caller = endpoint_caller
        self.logger = logging.getLogger(__name__)

    def retrieve_leagues(self, retries=1):
        response = self.__call_endpoint_with_retries("/leagues/", Verifiers.verify_leagues, retries)
        if response is not None:
            return ResponseConverter.get_leagues(response)

    def retrieve_fixtures_for_dates(self, dates, retries=1):
        dfs = []
        for date in dates:
            response = self.__call_endpoint_with_retries("/fixtures/date/{}?timezone=Europe/Budapest".format(date),
                                                         Verifiers.verify_base_fixture,
                                                         retries)
            if response is not None:
                df = ResponseConverter.get_base_fixture(response)
                if df is not None:
                    dfs.append(df)
        return pd.concat(dfs) if len(dfs) > 0 else None

    def retrieve_odds_for_fixtures(self, fixture_ids, retries=1):
        dfs = []
        for fixture_id in fixture_ids:
            response = self.__call_paged_endpoint_with_retries("/odds/fixture/{}/bookmaker/{}".format(fixture_id, BOOKMAKER_ID),
                                                               Verifiers.verify_odds,
                                                               retries, "odds")
            if response is not None:
                df = ResponseConverter.get_odds(response)
                if df is not None:
                    dfs.append(df)
        return pd.concat(dfs) if len(dfs) > 0 else None

    def retrieve_extras_for_fixtures(self, fixture_ids, retries=1):
        dfs_extrafixtures = []
        dfs_events = []
        dfs_statistics = []
        dfs_players = []
        dfs_lineups = []
        for fixture_id in fixture_ids:
            response = self.__call_endpoint_with_retries("/fixtures/id/{}?timezone=Europe/Budapest".format(fixture_id),
                                                         Verifiers.verify_extras_fixture,
                                                         retries)
            if response is not None:
                df_extrafixtures = ResponseConverter.get_extras_fixture(response)
                df_events = ResponseConverter.get_events(response)
                df_statistics = ResponseConverter.get_statistics(response)
                df_players = ResponseConverter.get_players(response)
                df_lineups = ResponseConverter.get_lineups(response)

                if df_extrafixtures is not None:
                    dfs_extrafixtures.append(df_extrafixtures)
                if df_events is not None:
                    dfs_events.append(df_events)
                if df_statistics is not None:
                    dfs_statistics.append(df_statistics)
                if df_players is not None:
                    dfs_players.append(df_players)
                if df_lineups is not None:
                    dfs_lineups.append(df_lineups)

        dfs_extrafixtures = pd.concat(dfs_extrafixtures) if len(dfs_extrafixtures) > 0 else None
        dfs_events = pd.concat(dfs_events) if len(dfs_events) > 0 else None
        dfs_statistics = pd.concat(dfs_statistics) if len(dfs_statistics) > 0 else None
        dfs_players = pd.concat(dfs_players) if len(dfs_players) > 0 else None
        dfs_lineups = pd.concat(dfs_lineups) if len(dfs_lineups) > 0 else None
        return dfs_extrafixtures, dfs_events, dfs_statistics, dfs_players, dfs_lineups

    def retrieve_predictions_for_fixtures(self, fixture_ids, retries=1):
        dfs = []
        for fixture_id in fixture_ids:
            response = self.__call_endpoint_with_retries("/predictions/{}".format(fixture_id),
                                                               Verifiers.verify_predictions,
                                                               retries)
            if response is not None:
                df = ResponseConverter.get_predictions(response, fixture_id)
                if df is not None:
                    dfs.append(df)
        return pd.concat(dfs) if len(dfs) > 0 else None

    def retrieve_odds_mappings(self, retries=1):
        response = self.__call_paged_endpoint_with_retries("/odds/mapping", Verifiers.verify_odds_mappings,
                                                           retries, "mapping")
        if response is None:
            return None
        df = ResponseConverter.get_odds_mappings(response)
        return df

    def __call_endpoint_with_retries(self, endpoint, verifier, retries):
        response = None
        for _ in range(retries+1):
            response = self.endpoint_caller.call(endpoint)
            if verifier(response):
                return response
            self.__sleep_if_too_many_requests(response)
        self.logger.error("Failed to retrieve endpoint: " + " " + endpoint)
        self.logger.error(response)
        return None

    def __call_paged_endpoint_with_retries(self, endpoint, verifier, retries, data_key):
        response = self.__call_endpoint_with_retries(endpoint + "?page=1", verifier, retries)
        if response is None:
            return None
        max_pages = response["api"]["paging"]["total"]
        for i in range(2, max_pages + 1):
            part_response = self.__call_endpoint_with_retries(endpoint + "?page=" + str(i), verifier, retries)
            if part_response is not None:
                response["api"][data_key].extend(part_response["api"][data_key])
        response["api"].pop("paging")
        return response

    def __sleep_if_too_many_requests(self, response):
        if "api" in response:
            if "status" in response["api"]:
                if "Too many requests" in response["api"]["status"]:
                    time.sleep(5)

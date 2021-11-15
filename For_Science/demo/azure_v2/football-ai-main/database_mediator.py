import logging

import pandas as pd
from sqlalchemy import create_engine


class DatabaseMediator:
    def __init__(self, host, user, password, database, retries=2):
        self.engine = create_engine('mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server'.format(user, password, host, database),
                                    fast_executemany=True)
        self.retries = retries
        self.logger = logging.getLogger(__name__)

    def write_leagues_overwrite(self, df_leagues):
        self.__to_sql_with_retry(df_leagues, "leagues", if_exists='replace', chunksize=30, index=True)

    def write_fixture_overwrite(self, df_fixture):
        self.__write_fixture_data(df_fixture, "fixtures")

    def write_fixture_extras_overwrite(self, dfs_extrafixtures, dfs_events, dfs_statistics, dfs_players, dfs_lineups):
        self.__write_fixture_data(dfs_extrafixtures, "fixtures")
        self.__write_fixture_data(dfs_events, "events", index=False)
        self.__write_fixture_data(dfs_statistics, "fixture_statistics")
        self.__write_fixture_data(dfs_players, "players")
        self.__write_fixture_data(dfs_lineups, "lineups")

    def write_predictions(self, df_predictions):
        self.__write_fixture_data(df_predictions, "predictions")

    def write_odds_mappings(self, df_odds_mappings):
        ids = df_odds_mappings.reset_index()["fixture_id"].astype(str).str.cat(sep=", ")
        odds_mappings_to_update = self.__read_sql_with_retry("select fixture_id, updateAt from odds_mappings "
                                                             "WHERE fixture_id in ({})".format(ids))
        odds_mappings_to_update = odds_mappings_to_update.rename(columns={"updateAt": "lastUpdateAt"})
        df_odds_mappings = df_odds_mappings.join(odds_mappings_to_update.set_index("fixture_id"),
                                                 on="fixture_id", how="left")
        self.__to_sql_with_retry(df_odds_mappings, "odds_mappings", if_exists='replace', index=False, chunksize=200)

    def write_odds(self, df_odds):
        ids = df_odds.reset_index()["fixture.fixture_id"].drop_duplicates().astype(str).str.cat(sep=", ")
        self.__execute_sql_with_retry("DELETE FROM odds WHERE [fixture.fixture_id] in ({})".format(ids))
        self.__to_sql_with_retry(df_odds, "odds", if_exists='append', chunksize=200)

    def write_firstodds(self, df_odds):
        fixture_ids = self.__read_sql_with_retry("select [fixture.fixture_id] from first_odds "
                                                 "group by [fixture.fixture_id]")
        fixture_ids = fixture_ids["fixture.fixture_id"]
        df_odds = df_odds.reset_index()
        df_newodds = df_odds[~df_odds["fixture.fixture_id"].isin(fixture_ids)]
        self.__to_sql_with_retry(df_newodds, "first_odds", if_exists='append', index=False, chunksize=200)

    def write_prs(self, df_pr):
        self.__to_sql_with_retry(df_pr, "fixture_pr", if_exists='replace', chunksize=None)

    def write_pr_stats(self, df_pr):
        self.__to_sql_with_retry(df_pr, "fixture_pr_stats", if_exists='replace', chunksize=None)

    def write_pr_odds_stats(self, df_pr):
        self.__to_sql_with_retry(df_pr, "fixture_pr_odds_stats", if_exists='replace', chunksize=None)

    def get_notupdated_fixtureids_from_oddsmappings(self):
        fixture_ids = self.__read_sql_with_retry("select fixture_id from odds_mappings "
                                                 "where updateAt != lastUpdateAt or lastUpdateAt is null")
        return fixture_ids["fixture_id"]

    def get_latest_fixture_insert(self):
        df = self.__read_sql_with_retry("select CONVERT(DATE, max(insert_date)) as latest_insert from fixtures")
        return df["latest_insert"].item()

    def get_pivoted_odds(self):
        df = self.__read_sql_with_retry("select * from retrieve_formatted_odds()")  # its a server function, it only returns 3 labels
        return df

    def get_fixtures_and_leagues_for_pr(self):
        df = self.__read_sql_with_retry("select leagues.league_id, leagues.season, fixture_id, event_timestamp, "
                                        "[homeTeam.team_id], [awayTeam.team_id], goalsHomeTeam, goalsAwayTeam "
                                        "from fixtures "
                                        "join leagues on leagues.league_id=fixtures.league_id")
        return df.set_index("fixture_id")

    def get_fixtures_for_pr_calculation(self):
        df = self.__read_sql_with_retry("select * from retrieve_fixtures_without_first_n_matches(5)")
        return df

    def get_fixtures_for_pr_odds_calculation(self):
        df_fixtures = self.__read_sql_with_retry("select * from retrieve_fixtures_without_first_n_matches(5)")
        df_odds = self.__read_sql_with_retry("select * from retrieve_formatted_label1_odds()")
        df = df_fixtures.merge(df_odds, on="fixture_id", how="inner")
        return df

    def get_leagues(self):
        df = self.__read_sql_with_retry("select * from leagues")
        return df

    def __write_fixture_data(self, df, tablename, index=True):
        ids = df.reset_index()["fixture_id"].astype(str).str.cat(sep=", ")
        self.__execute_sql_with_retry("DELETE FROM {} WHERE fixture_id in ({})".format(tablename, ids))
        chunksize = 1500 // len(df.columns)
        self.__to_sql_with_retry(df, tablename, if_exists='append', chunksize=chunksize, index=index)

    def __to_sql_with_retry(self, df, tablename, chunksize=None, index=True, if_exists='append'):
        for i in range(self.retries+1):
            try:
                if chunksize is not None:
                    df.to_sql(tablename, con=self.engine, if_exists=if_exists, method='multi', chunksize=chunksize, index=index)
                else:
                    df.to_sql(tablename, con=self.engine, if_exists=if_exists, index=index)
                return
            except Exception as e:
                self.logger.error(tablename)
                self.logger.error(e, exc_info=True)
        raise Exception("Failed after {} retries".format(self.retries))

    def __execute_sql_with_retry(self, query):
        for i in range(self.retries+1):
            try:
                with self.engine.connect() as con:
                    con.execute(query)
                return
            except Exception as e:
                self.logger.error(query)
                self.logger.error(e, exc_info=True)
        raise Exception("Failed after {} retries".format(self.retries))

    def __read_sql_with_retry(self, query):
        for i in range(self.retries+1):
            try:
                return pd.read_sql_query(query, con=self.engine)
            except Exception as e:
                self.logger.error(query)
                self.logger.error(e, exc_info=True)
        raise Exception("Failed after {} retries".format(self.retries))

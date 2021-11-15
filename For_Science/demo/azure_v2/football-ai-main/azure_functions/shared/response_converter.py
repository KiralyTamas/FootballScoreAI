import logging

import pandas as pd


class ResponseConverter:

    class _Decorators:
        @classmethod
        def catch_errors(cls, func):
            def inner(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.getLogger(__name__).exception(e)
                    return None
            return inner

    @staticmethod
    @_Decorators.catch_errors
    def get_leagues(response):
        df = pd.json_normalize(response["api"]["leagues"])
        df = df.set_index("league_id")
        return df

    @staticmethod
    @_Decorators.catch_errors
    def get_base_fixture(response):
        df = pd.json_normalize(response["api"]["fixtures"])
        df = df.set_index("fixture_id")
        df["event_date"] = pd.to_datetime(df["event_date"])
        return df

    @staticmethod
    @_Decorators.catch_errors
    def get_extras_fixture(response):
        fixtures = []
        for fixture in response["api"]["fixtures"]:
            fixtures.append(ResponseConverter.generalize_lineup_teamnames(fixture))
        df = pd.json_normalize(fixtures)
        df = df.set_index("fixture_id")
        df["event_date"] = pd.to_datetime(df["event_date"])
        df = df.drop(["events"], axis=1, errors='ignore')
        df = df.drop(["players"], axis=1, errors='ignore')
        df = df[[col for col in df.columns if 'statistics' not in col]]
        df = df.drop(["lineups.homeTeam.startXI"], axis=1, errors='ignore')
        df = df.drop(["lineups.homeTeam.substitutes"], axis=1, errors='ignore')
        df = df.drop(["lineups.awayTeam.startXI"], axis=1, errors='ignore')
        df = df.drop(["lineups.awayTeam.substitutes"], axis=1, errors='ignore')
        return df

    @staticmethod
    @_Decorators.catch_errors
    def get_events(response):
        dfs = []
        for fixture in response["api"]["fixtures"]:
            if fixture["events"] is not None:
                df = pd.json_normalize(fixture["events"])
                df["fixture_id"] = fixture["fixture_id"]
                df["elapsed_plus"] = df["elapsed_plus"].astype(str)
                dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs)

    @staticmethod
    @_Decorators.catch_errors
    def get_statistics(response):
        dfs = []
        for fixture in response["api"]["fixtures"]:
            if fixture["statistics"] is not None:
                df = pd.json_normalize(fixture["statistics"])
                df["fixture_id"] = fixture["fixture_id"]
                df = df.set_index("fixture_id")
                #df = df.fillna(0)
                df = df.apply(pd.to_numeric, errors="ignore", downcast="integer")
                df = ResponseConverter.convert_percentage_columns(df, ["Ball Possession.home", "Ball Possession.away",
                                                                       "Passes %.home", "Passes %.away"])
                df = ResponseConverter.format_column_names(df)
                dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs)

    @staticmethod
    @_Decorators.catch_errors
    def get_players(response):
        dfs = []
        for fixture in response["api"]["fixtures"]:
            if fixture["players"] is not None:
                df = pd.json_normalize(fixture["players"])
                df = df.dropna(subset=['player_id'])
                df = df.rename(columns={"event_id": "fixture_id"})
                df = df.set_index(["fixture_id", "player_id"])
                df["substitute"] = df["substitute"].map({"True": True, "False": False})  # TODO: integer?
                df["captain"] = df["captain"].map({"True": True, "False": False})
                df["rating"] = df["rating"].apply(pd.to_numeric, args=("coerce",))
                dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs)

    @staticmethod
    @_Decorators.catch_errors
    def get_lineups(response):
        dfs = []
        for fixture in response["api"]["fixtures"]:
            if fixture["lineups"] is not None:
                generalized_fixture = ResponseConverter.generalize_lineup_teamnames(fixture)
                for is_home_team in (False, True):
                    for is_start_xi in (False, True):
                        team_key = "homeTeam" if is_home_team else "awayTeam"
                        start_xi_key = "startXI" if is_start_xi else "substitutes"
                        if start_xi_key in generalized_fixture["lineups"][team_key]:
                            df = pd.json_normalize(generalized_fixture["lineups"][team_key][start_xi_key])
                            df["is_homeTeam"] = is_home_team
                            df["is_startXI"] = is_start_xi
                            df["is_homeTeam"] = df["is_homeTeam"].astype(int)
                            df["is_startXI"] = df["is_startXI"].astype(int)
                            df["fixture_id"] = fixture["fixture_id"]
                            df = df.dropna(subset=['player_id'])
                            df = df.set_index(["fixture_id", "player_id"])
                            dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs)

    @staticmethod
    @_Decorators.catch_errors
    def get_h2h_prediction(response):
        dfs = []
        for prediction in response["api"]["predictions"]:
            df = pd.json_normalize(prediction["h2h"])  # TODO
            dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs)

    @staticmethod
    @_Decorators.catch_errors
    def get_predictions(response, fixture_id):
        dfs = []
        for prediction in response["api"]["predictions"]:
            df = pd.json_normalize(prediction)
            percetage_cols = [col for col in df.columns if 'winning_percent' in col or 'last_5_matches.forme' in col
                              or 'last_5_matches.att' in col or 'last_5_matches.def' in col or 'comparison' in col]
            df = ResponseConverter.convert_percentage_columns(df, percetage_cols)
            nonnumeric_cols = [col for col in df.columns if 'all_last_matches.goalsAvg' in col or 'under_over' in col
                               or 'goals_home' in col or 'goals_away' in col]
            df[nonnumeric_cols] = df[nonnumeric_cols].apply(pd.to_numeric)
            del df["h2h"]
            df["fixture_id"] = fixture_id
            df = df.set_index("fixture_id")
            dfs.append(df)
        if not dfs:
            return None
        return pd.concat(dfs)

    @staticmethod
    @_Decorators.catch_errors
    def get_odds(response):
        dfs = []
        for odds in response["api"]["odds"]:
            for bookmaker in odds["bookmakers"]:
                for bet in bookmaker["bets"]:
                    df_values = pd.json_normalize(bet, "values")
                    df_values["label_id"] = bet["label_id"]
                    df_values["label_name"] = bet["label_name"]
                    df_values["bookmaker_id"] = bookmaker["bookmaker_id"]
                    df_values["bookmaker_name"] = bookmaker["bookmaker_name"]
                    df_values["fixture.league_id"] = odds["fixture"]["league_id"]
                    df_values["fixture.fixture_id"] = odds["fixture"]["fixture_id"]
                    df_values["fixture.updateAt"] = odds["fixture"]["updateAt"]
                    dfs.append(df_values)
        if not dfs:
            return None
        result = pd.concat(dfs)
        result["odd"] = result["odd"].apply(pd.to_numeric)
        result[["value", "label_name", "bookmaker_name"]] = result[["value", "label_name", "bookmaker_name"]].astype(str)
        result = result.set_index(["fixture.fixture_id", "fixture.updateAt", "bookmaker_id", "label_id"])
        return result

    @staticmethod
    @_Decorators.catch_errors
    def get_odds_mappings(response):
        return pd.json_normalize(response["api"]["mapping"])

    @staticmethod
    def format_column_names(df):
        mapping = {}
        for column in df:
            new = column.replace(" ", "")
            mapping[column] = new
        return df.rename(columns=mapping)

    @staticmethod
    def convert_percentage_columns(df, columns):
        df[columns] = df[columns].applymap(lambda x: float(x.strip('%')) / 100 if not pd.isna(x) else x)
        return df

    @staticmethod
    def generalize_lineup_teamnames(response):
        if response["lineups"] is None:
            result = response.copy()
            result.pop("lineups")
            return result
        rename = {}
        home_team_name = response["homeTeam"]["team_name"]
        away_team_name = response["awayTeam"]["team_name"]
        keys = list(response["lineups"].keys())
        if keys[0] == home_team_name or keys[1] == away_team_name:
            rename[keys[0]] = "homeTeam"
            rename[keys[1]] = "awayTeam"
        if keys[0] == away_team_name or keys[1] == home_team_name:
            rename[keys[1]] = "homeTeam"
            rename[keys[0]] = "awayTeam"
        for key in rename:
            new_name = rename[key]
            response["lineups"][new_name] = response["lineups"].pop(key)
        return response

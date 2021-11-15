import numpy as np
import pandas as pd


class StatCalculator:
    # expected columns: league_id int, fixture_id int, event_timestamp int,
    # goalsHomeTeam int, goalsAwayTeam int, [homeTeam.PowerRating] real, [awayTeam.PowerRating] real
    def calculate_pr_percentage(self, df_fixtures_with_prs):
        home_counts = {}
        draw_counts = {}
        away_counts = {}
        df_fixtures_with_prs = df_fixtures_with_prs.sort_values(by="event_timestamp")
        for index, row in df_fixtures_with_prs.iterrows():
            pr_diff = np.around(row["homeTeam.PowerRating"] - row["awayTeam.PowerRating"], 1)
            league_id = row["league_id"]
            goals_home_team = row["goalsHomeTeam"]
            goals_away_team = row["goalsAwayTeam"]
            home_counts = self.__fill_missing_keys(home_counts, pr_diff, league_id)
            draw_counts = self.__fill_missing_keys(draw_counts, pr_diff, league_id)
            away_counts = self.__fill_missing_keys(away_counts, pr_diff, league_id)
            sum_of_all_counts = home_counts[pr_diff][league_id] + draw_counts[pr_diff][league_id] + away_counts[pr_diff][league_id]
            df_fixtures_with_prs.at[index, "prHomeWinPercent"] = home_counts[pr_diff][league_id] / sum_of_all_counts if sum_of_all_counts is not 0 else 0
            df_fixtures_with_prs.at[index, "prDrawWinPercent"] = draw_counts[pr_diff][league_id] / sum_of_all_counts if sum_of_all_counts is not 0 else 0
            df_fixtures_with_prs.at[index, "prAwayWinPercent"] = away_counts[pr_diff][league_id] / sum_of_all_counts if sum_of_all_counts is not 0 else 0
            if not pd.isnull(goals_home_team) and not pd.isnull(goals_away_team):
                if goals_home_team > goals_away_team:
                    home_counts[pr_diff][league_id] += 1
                if goals_home_team == goals_away_team:
                    draw_counts[pr_diff][league_id] += 1
                if goals_home_team < goals_away_team:
                    away_counts[pr_diff][league_id] += 1

        return df_fixtures_with_prs.set_index("fixture_id")[["prHomeWinPercent", "prDrawWinPercent", "prAwayWinPercent"]]

    # expected columns: league_id int, fixture_id int, event_timestamp int,
    # goalsHomeTeam int, goalsAwayTeam int, [homeTeam.PowerRating] real, [awayTeam.PowerRating] real,
    # [Match_Winner.Home] real, [Match_Winner.Draw] real, [Match_Winner.Away] real
    def calculate_pr_odds_percentage(self, df_fixtures_with_prs):
        home_win_count = {}
        home_lose_count = {}
        draw_win_count = {}
        draw_lose_count = {}
        away_win_count = {}
        away_lose_count = {}
        df_fixtures_with_prs = df_fixtures_with_prs.sort_values(by="event_timestamp")
        for index, row in df_fixtures_with_prs.iterrows():
            pr_diff = np.around(row["homeTeam.PowerRating"] - row["awayTeam.PowerRating"], 1)
            home_odd = np.around(row["Match_Winner.Home"], 1)
            draw_odd = np.around(row["Match_Winner.Draw"], 1)
            away_odd = np.around(row["Match_Winner.Away"], 1)
            goals_home_team = row["goalsHomeTeam"]
            goals_away_team = row["goalsAwayTeam"]
            home_win_count = self.__fill_missing_keys(home_win_count, pr_diff, home_odd)
            home_lose_count = self.__fill_missing_keys(home_lose_count, pr_diff, home_odd)
            draw_win_count = self.__fill_missing_keys(draw_win_count, pr_diff, draw_odd)
            draw_lose_count = self.__fill_missing_keys(draw_lose_count, pr_diff, draw_odd)
            away_win_count = self.__fill_missing_keys(away_win_count, pr_diff, away_odd)
            away_lose_count = self.__fill_missing_keys(away_lose_count, pr_diff, away_odd)
            df_fixtures_with_prs.at[index, "Match_Winner.Home.winCount"] = home_win_count[pr_diff][home_odd]
            df_fixtures_with_prs.at[index, "Match_Winner.Draw.winCount"] = draw_win_count[pr_diff][draw_odd]
            df_fixtures_with_prs.at[index, "Match_Winner.Away.winCount"] = away_win_count[pr_diff][away_odd]
            df_fixtures_with_prs.at[index, "Match_Winner.Home.loseCount"] = home_lose_count[pr_diff][home_odd]
            df_fixtures_with_prs.at[index, "Match_Winner.Draw.loseCount"] = draw_lose_count[pr_diff][draw_odd]
            df_fixtures_with_prs.at[index, "Match_Winner.Away.loseCount"] = away_lose_count[pr_diff][away_odd]

            if not pd.isnull(goals_home_team) and not pd.isnull(goals_away_team):
                if goals_home_team > goals_away_team:
                    home_win_count[pr_diff][home_odd] += 1
                    draw_lose_count[pr_diff][draw_odd] += 1
                    away_lose_count[pr_diff][away_odd] += 1
                if goals_home_team == goals_away_team:
                    home_lose_count[pr_diff][home_odd] += 1
                    draw_win_count[pr_diff][draw_odd] += 1
                    away_lose_count[pr_diff][away_odd] += 1
                if goals_home_team < goals_away_team:
                    home_lose_count[pr_diff][home_odd] += 1
                    draw_lose_count[pr_diff][draw_odd] += 1
                    away_win_count[pr_diff][away_odd] += 1

        return df_fixtures_with_prs.set_index("fixture_id")[["Match_Winner.Home.winCount", "Match_Winner.Draw.winCount",
                                                            "Match_Winner.Away.winCount", "Match_Winner.Home.loseCount",
                                                             "Match_Winner.Draw.loseCount", "Match_Winner.Away.loseCount"]]

    def __fill_missing_keys(self, counts, key1, key2):
        if key1 not in counts:
            counts[key1] = {}
        if key2 not in counts[key1]:
            counts[key1][key2] = 0
        return counts

import numpy as np
import pandas as pd


class PRCalculator:
    def calculate_power_ratings(self, fixtures_leagues_odds):
        fixtures_leagues_odds["homeTeam.PowerRating"] = np.full(len(fixtures_leagues_odds), 10.0)
        fixtures_leagues_odds["awayTeam.PowerRating"] = np.full(len(fixtures_leagues_odds), 10.0)
        seasons = fixtures_leagues_odds["season"].unique()
        for season in seasons:
            fixtures_leagues_odds = self.__calculate_power_ratings_for_season(fixtures_leagues_odds, season)
        return fixtures_leagues_odds

    def __calculate_power_ratings_for_season(self, fixtures_leagues_odds, season=None):
        season_fixtures = fixtures_leagues_odds.sort_values(by="event_timestamp")
        if season is not None:
            season_fixtures = season_fixtures[season_fixtures["season"] == season]
        adjuster = 0.25
        home_teams = set(season_fixtures["homeTeam.team_id"].unique())
        away_teams = set(season_fixtures["awayTeam.team_id"].unique())
        unique_teams = home_teams.union(away_teams)
        current_team_ratings = {team: 10 for team in unique_teams}
        for index, row in season_fixtures.iterrows():
            home_team_name = row["homeTeam.team_id"]
            home_team_goals = row["goalsHomeTeam"]
            home_team_rating = current_team_ratings[home_team_name]
            away_team_name = row["awayTeam.team_id"]
            away_team_goals = row["goalsAwayTeam"]
            away_team_rating = current_team_ratings[away_team_name]
############################ez miért or? nem and?
            if home_team_goals is None or away_team_goals is None:
                home_power_rating_change = 0
                away_power_rating_change = 0
            else:
                home_power_rating_change = self.__power_rating(home_team_goals - away_team_goals, home_team_rating - away_team_rating, adjuster)
                away_power_rating_change = -1 * home_power_rating_change

            if pd.isnull(home_power_rating_change):
                home_power_rating_change = 0
                away_power_rating_change = 0

            current_team_ratings[home_team_name] += home_power_rating_change
            current_team_ratings[away_team_name] += away_power_rating_change
            fixtures_leagues_odds.at[index, "homeTeam.PowerRating"] = home_team_rating
            fixtures_leagues_odds.at[index, "awayTeam.PowerRating"] = away_team_rating

        return fixtures_leagues_odds

    def __power_rating(self, goal_difference, rating_difference, adjuster):
        return (goal_difference - rating_difference - adjuster * 2) * adjuster

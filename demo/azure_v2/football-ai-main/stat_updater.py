import logging

from database_mediator import DatabaseMediator
from stat_calculator import StatCalculator

logging.getLogger().setLevel(logging.INFO)
logging.info('Starting stat updater')

database_mediator = DatabaseMediator("football2020.database.windows.net",
                                     user="football",
                                     password="G3Ff2C63gvB",
                                     database="football-db")
stat_calculator = StatCalculator()
df_fixtures_with_prs = database_mediator.get_fixtures_for_pr_calculation()
df_pr_percentage = stat_calculator.calculate_pr_percentage(df_fixtures_with_prs)
database_mediator.write_pr_stats(df_pr_percentage)

df_fixtures_odds_with_prs = database_mediator.get_fixtures_for_pr_odds_calculation()
df_pr_odds_percentage = stat_calculator.calculate_pr_odds_percentage(df_fixtures_odds_with_prs)
database_mediator.write_pr_odds_stats(df_pr_odds_percentage)



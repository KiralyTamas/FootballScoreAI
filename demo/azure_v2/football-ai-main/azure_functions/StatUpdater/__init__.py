import datetime
import logging

import azure.functions as func
from shared.database_mediator import DatabaseMediator
from shared.stat_calculator import StatCalculator

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

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


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

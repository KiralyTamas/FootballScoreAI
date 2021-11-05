import datetime
import logging

import azure.functions as func
from shared.database_mediator import DatabaseMediator
from shared.pr_calculator import PRCalculator


def main(mytimer: func.TimerRequest) -> None:
    logging.getLogger().setLevel(logging.INFO)
    logging.info('Starting pr updater')

    database_mediator = DatabaseMediator("football2020.database.windows.net",
                                        user="football",
                                        password="G3Ff2C63gvB",
                                        database="football-db")

    logging.info("Retrieving fixtures and leagues")
    df_fixtures_leagues = database_mediator.get_fixtures_and_leagues_for_pr()
    logging.info("Retrieved {} rows".format(len(df_fixtures_leagues)))

    logging.info("Starting PR calculation")
    pr_calculator = PRCalculator()
    df_pr = pr_calculator.calculate_power_ratings(df_fixtures_leagues)
    df_pr = df_pr[["homeTeam.PowerRating", "awayTeam.PowerRating"]]
    logging.info("PR calculation finished")

    logging.info("Writing {} rows to database".format(len(df_pr)))
    database_mediator.write_prs(df_pr)
    logging.info("PR updating is done")

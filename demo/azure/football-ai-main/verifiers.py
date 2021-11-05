class Verifiers:
    @staticmethod
    def verify_leagues(json):
        if "api" not in json:
            return False
        if "leagues" not in json["api"]:
            return False
        if json["api"]["leagues"] is None:
            return False
        return True

    @staticmethod
    def verify_base_fixture(json):
        if "api" not in json:
            return False
        if "fixtures" not in json["api"]:
            return False
        if json["api"]["fixtures"] is None:
            return False
        return True

    @staticmethod
    def verify_extras_fixture(json):
        if "api" not in json:
            return False
        if "fixtures" not in json["api"]:
            return False
        if len(json["api"]["fixtures"]) == 0:
            return False
        for fixture in json["api"]["fixtures"]:
            if "events" not in fixture or "statistics" not in fixture or \
                    "lineups" not in fixture or "players" not in fixture:
                return False
        return True

    @staticmethod
    def verify_odds(json):
        if "api" not in json:
            return False
        if "paging" not in json["api"]:
            return False
        if "odds" not in json["api"]:
            return False
        if len(json["api"]["odds"]) == 0:
            return False
        for odd in json["api"]["odds"]:
            if "fixture" not in odd or "bookmakers" not in odd:
                return False
        return True

    @staticmethod
    def verify_odds_mappings(json):
        if "api" not in json:
            return False
        if "paging" not in json["api"]:
            return False
        if "mapping" not in json["api"]:
            return False
        return True

    @staticmethod
    def verify_predictions(json):
        if "api" not in json:
            return False
        if "predictions" not in json["api"]:
            return False
        if json["api"]["predictions"] is None:
            return False
        return True

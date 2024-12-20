import calendar
import json

from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import *

import pytz
import requests

from pprint import pp

NHL_API_ENDPOINT = "https://api-web.nhle.com/v1/"

NHL_URLS = {"team_season_schedule": "club-schedule-season/{team}/{season}"}

NHL_TEAMS = [
    { "name": "Anaheim Ducks", "abbreviation": "ANA" },
    { "name": "Arizona Coyotes", "abbreviation": "ARI" },
    { "name": "Boston Bruins", "abbreviation": "BOS" },
    { "name": "Buffalo Sabres", "abbreviation": "BUF" },
    { "name": "Calgary Flames", "abbreviation": "CGY" },
    { "name": "Carolina Hurricanes", "abbreviation": "CAR" },
    { "name": "Chicago Blackhawks", "abbreviation": "CHI" },
    { "name": "Colorado Avalanche", "abbreviation": "COL" },
    { "name": "Columbus Blue Jackets", "abbreviation": "CBJ" },
    { "name": "Dallas Stars", "abbreviation": "DAL" },
    { "name": "Detroit Red Wings", "abbreviation": "DET" },
    { "name": "Edmonton Oilers", "abbreviation": "EDM" },
    { "name": "Florida Panthers", "abbreviation": "FLA" },
    { "name": "Los Angeles Kings", "abbreviation": "LAK" },
    { "name": "Minnesota Wild", "abbreviation": "MIN" },
    { "name": "Montreal Canadiens", "abbreviation": "MTL" },
    { "name": "Nashville Predators", "abbreviation": "NSH" },
    { "name": "New Jersey Devils", "abbreviation": "NJD" },
    { "name": "New York Islanders", "abbreviation": "NYI" },
    { "name": "New York Rangers", "abbreviation": "NYR" },
    { "name": "Ottawa Senators", "abbreviation": "OTT" },
    { "name": "Philadelphia Flyers", "abbreviation": "PHI" },
    { "name": "Pittsburgh Penguins", "abbreviation": "PIT" },
    { "name": "San Jose Sharks", "abbreviation": "SJS" },
    { "name": "Seattle Kraken", "abbreviation": "SEA" },
    { "name": "St. Louis Blues", "abbreviation": "STL" },
    { "name": "Tampa Bay Lightning", "abbreviation": "TBL" },
    { "name": "Toronto Maple Leafs", "abbreviation": "TOR" },
    { "name": "Vancouver Canucks", "abbreviation": "VAN" },
    { "name": "Vegas Golden Knights", "abbreviation": "VGK" },
    { "name": "Washington Capitals", "abbreviation": "WSH" },
    { "name": "Winnipeg Jets", "abbreviation": "WPG" },
]

def _parse_datetime_string(str_in: str) -> datetime:
    return parser.isoparse(str_in)


def get_full_season_by_team(team: str, season: str) -> list[dict]:
    """
    Returns a team's schedule for the given season. The data returned from the endpoint will be filtered to just what this app needs.

    Args:
        team (str): Three letter team designation
        season (str): Season in YYYYYYYY format, where the first four digits represent the start year of the season, and the last four digits represent the end year. Current season can be specified with "now".
    Returns:
        list[dict]: List of the games scheduled for the team in the selected season.
    """
    schedule = []
    req = requests.get(
        NHL_API_ENDPOINT
        + NHL_URLS["team_season_schedule"].format(team=team, season=season)
    )
    decoded_payload = req.json()
    for game in decoded_payload["games"]:
        game_data = {
            "datetime": _parse_datetime_string(game["startTimeUTC"]),
            "home": game["homeTeam"].copy(),
            "away": game["awayTeam"].copy(),
            "venue": game["venue"]["default"],
            "network": [x["network"] for x in game["tvBroadcasts"]],
            "three_minute_recap": game.get("threeMinRecap", ""),
            "game_center_link": game.get("gameCenterLink", ""),
            "state": game["gameState"],
        }
        schedule.append(game_data)
    return schedule

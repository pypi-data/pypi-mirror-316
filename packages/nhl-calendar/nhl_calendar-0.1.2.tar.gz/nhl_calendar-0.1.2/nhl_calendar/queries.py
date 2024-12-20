import calendar
import json

from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import *

import pytz
import requests

from pprint import pp

NHL_API_URLS = {
    "team_list": "https://api.nhle.com/stats/rest/en/team",
    "team_season_schedule": "https://api-web.nhle.com/v1/club-schedule-season/{team}/{season}",
}

# `id`s for all active NHL teams, kind of frustrating that this isn't provided in the API
ACTIVE_NHL_TEAMS = [
    8,
    7,
    2,
    28,
    29,
    5,
    13,
    12,
    54,
    25,
    52,
    14,
    59,
    18,
    4,
    1,
    9,
    17,
    21,
    55,
    15,
    24,
    26,
    23,
    30,
    10,
    3,
    22,
    20,
    6,
    19,
    16,
]


def get_teams() -> list[dict]:
    teams = []
    req = requests.get(NHL_API_URLS["team_list"])
    decoded_payload = req.json()
    for team in decoded_payload["data"]:
        active = True if team["id"] in ACTIVE_NHL_TEAMS else False
        teams.append(
            {
                "name": team["fullName"],
                "franchiseId": team["franchiseId"],
                "triCode": team["triCode"],
                "active": active,
            }
        )
    sort_by_name = lambda x: x["name"]
    return sorted(teams, key=sort_by_name)


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
        NHL_API_URLS["team_season_schedule"].format(team=team, season=season)
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

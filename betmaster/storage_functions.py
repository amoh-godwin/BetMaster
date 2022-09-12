# 12th September, 2022
# Amoh-Gyebi Ampofo

from typing import List
import json


def temp_store_games(team: str, games: List) -> None:
    fn = team + '_games.json'
    data = {team: games}
    with open(fn, 'w') as jp:
        json.dump(data, jp)

def get_store_team_games(team: str) -> List:
    fn = team + '_games.json'

    with open(fn, 'r') as jp:
        data = json.load(jp)

    return data[team]

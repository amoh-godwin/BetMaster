# 12th September, 2022
# Amoh-Gyebi Ampofo

import os
from typing import List
import json


FOLDER_NAME = './team_sheets'


def get_store_team_games(team: str) -> List:
    fn = team + '_games.json'
    fn = os.path.join(FOLDER_NAME, fn)

    with open(fn, 'r') as jp:
        data = json.load(jp)

    return data[team]


def get_file(fileName: str) -> str:
    fn = os.path.join(FOLDER_NAME, fileName)
    if os.path.exists(fn):
        with open(fn, 'rb') as fp:
            conts = fp.read()
        return str(conts, 'utf-8')
    else:
        return ''


def temp_store_games(team: str, games: List) -> None:
    fn = team + '_games.json'
    fn = os.path.join(FOLDER_NAME, fn)
    data = {team: games}
    with open(fn, 'w') as jp:
        json.dump(data, jp)




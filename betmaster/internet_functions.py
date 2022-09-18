# 12th September, 2022
# Amoh-Gyebi Ampofo

import requests
import os
from datetime import date

from storage_functions import get_file


def get_team_data(team_name: str) -> str:
    fn = team_name + "_goals.txt"

    conts = get_file(fn)

    if not conts:
        req = requests.get(f'http://www.footlive.com/team/{team_name}/')
        conts = req.text

        with open("./team_sheets/"+fn, 'wb') as fb:
            fb.write(req.content)

    return conts


def get_not_started() -> str:

    today = str(date.today())
    fileName = 'not_started_' + today + '.txt'
    conts = get_file(fileName)

    if not conts:
        req = requests.get(f'http://www.footlive.com/scores-results/{today}/')
        conts = req.content

        with open("./team_sheets/"+fileName, 'wb') as fp:
            fp.write(conts)
        conts = str(conts, 'utf-8')

    return conts

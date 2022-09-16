# 12th September, 2022
# Amoh-Gyebi Ampofo

import requests
import os
from datetime import date


def get_team_data(team_name: str) -> str:
    fn = team_name + "_goals.txt"

    if os.path.exists(fn):
        with open(fn, 'r') as fr:
            conts = fr.read()
    else:
        req = requests.get(f'http://www.footlive.com/team/{team_name}/')
        conts = req.text

        with open(fn, 'wb') as fb:
            fb.write(req.content)

    return conts


def get_not_started() -> str:

    today = date.today()
    fileName = 'not_started_' + str(today) + '.txt'

    if os.path.exists(fileName):
        with open(fileName, 'r') as fp:
            conts = fp.read()
    else:
        req = requests.get('http://www.footlive.com/')
        conts = req.text

        with open(fileName, 'w') as fp:
            fp.write(conts)

    return conts

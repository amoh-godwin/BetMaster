# 11th September, 2022
# Amoh-Gyebi Ampofo
import requests
import re
from dataclasses import dataclass
from typing import List

# from bs4 import BeautifulSoup


@dataclass
class Team:
    id: int
    name: str
    date: int


def extract_footlive_notstarted() -> List:
    teams = []
    #req = requests.get('http://www.footlive.com/tomorrow/')
    #conts = req.text

    """ with open('ff.txt', 'wb') as fb:
        fb.write(req.content) """

    with open('ff.txt', 'r') as fr:
        conts = fr.read()

    reg = r"data-id=['|\"].*?['|\"] data-date=['|\"].*?['|\"] "
    reg += r"data-team1=['|\"].*?['|\"] data-team2=['|\"].*?['|\"]"
    all = re.findall(reg, conts)
    for x in all:
        teams.extend(extract_team_data(x))
    
    print(teams)


def extract_team_data(div: str) -> List:
    br = div.replace('\\', '')
    id = re.findall(r"id=['|\"].*?['|\"]", br)[0][4:-1]
    date = re.findall(r"date=['|\"].*?['|\"]", br)[0][6:-1]
    t1 = re.findall(r"team1=['|\"].*?['|\"]", br)[0][7:-1]
    t2 = re.findall(r"team2=['|\"].*?['|\"]", br)[0][7:-1]
    teams = [Team(int(id), t1, int(date)), Team(int(id), t2, int(date))]
    return teams




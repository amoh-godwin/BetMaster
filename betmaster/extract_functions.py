# 11th September, 2022
# Amoh-Gyebi Ampofo
from pprint import pp
import requests
import re
from dataclasses import dataclass
from typing import List, Tuple

# from bs4 import BeautifulSoup


@dataclass
class Match:
    id: int
    date: int
    name: str
    team1: str
    team2: str
    score1: int
    score2: int


@dataclass
class Team:
    id: int
    name: str
    date: int


@dataclass
class Scores:
    name: int
    gf: tuple
    ga: tuple


def extract_data(div: str) -> Tuple[int, int, int, int, str, str]:
    br = div.replace('\\', '')
    id = re.findall(r"id=['|\"].*?['|\"]", br)[0][4:-1]
    date = re.findall(r"date=['|\"].*?['|\"]", br)[0][6:-1]
    s1 = re.findall(r"score1=['|\"].*?['|\"]", br)[0][8:-1]
    s2 = re.findall(r"score2=['|\"].*?['|\"]", br)[0][8:-1]
    t1 = re.findall(r"slug1=['|\"].*?['|\"]", br)[0][7:-1]
    t2 = re.findall(r"slug2=['|\"].*?['|\"]", br)[0][7:-1]

    return (int(id), int(date), int(s1), int(s2), t1, t2)


def extract_footlive_tomorrow() -> List:
    teams = []
    #req = requests.get('http://www.footlive.com/tomorrow/')
    #conts = req.text

    """ with open('ff.txt', 'wb') as fb:
        fb.write(req.content) """

    with open('ff.txt', 'r') as fr:
        conts = fr.read()

    reg = r"data-id=['|\"].*?['|\"] data-date=['|\"].*?['|\"] "
    reg += r"data-slug1=['|\"].*?['|\"] data-slug2=['|\"].*?['|\"]"
    all = re.findall(reg, conts)
    for x in all:
        teams.extend(extract_team_data(x))

    print(teams)


def extract_goals(div: str, team_name: str) -> Tuple:
    _, _, s1, s2, t1, t2 = extract_data(div)

    if team_name == t1:
        gf = s1
        ga = s2
    else:
        gf = s2
        ga = s1

    return (int(gf), int(ga))


def extract_matches(div: str, team_name: str) -> Match:
    id, date, s1, s2, t1, t2 = extract_data(div)
    return Match(id, date, team_name, t1, t2, s1, s2)


def extract_team_data(div: str) -> List:
    id, date, s1, s2, t1, t2 = extract_data(div)
    teams = [Team(int(id), t1, int(date)), Team(int(id), t2, int(date))]
    return teams


def extract_team_scores(name: str) -> Scores:
    scores = []
    sgf = []
    sga = []
    """ req = requests.get(f'http://www.footlive.com/team/{name}/')
    conts = req.text

    with open('goals.txt', 'wb') as fb:
        fb.write(req.content) """

    with open('goals.txt', 'r') as fr:
        conts = fr.read()

    reg = r"data-id=['|\"].*?['|\"] data-status=['|\"]FT['|\"]"
    reg += r".*?data-slug2=['|\"].*?['|\"]"
    all = re.findall(reg, conts)
    for x in all:
        gf, ga = extract_goals(x, name)
        sgf.append(gf)
        sga.append(ga)


    return Scores(name, tuple(sgf), tuple(sga))



# 11th September, 2022
# Amoh-Gyebi Ampofo
import requests
import re
from datetime import datetime
from dataclasses import asdict, dataclass
from typing import List, Tuple, Dict

from storage_functions import temp_store_games, get_store_team_games
from internet_functions import get_team_data


@dataclass
class Game:
    id: int
    date: int
    name: str
    team1: str
    team2: str
    score1: int
    score2: int


@dataclass
class HomeAwayScore:
    name: str
    home_gf: list
    home_ga: list
    away_gf: list
    away_ga: list


@dataclass
class H2HVictory:
    name: str
    home: list
    away: list

@dataclass
class TeamVictory:
    name: str
    home: list
    away: list


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
    req = requests.get('http://www.footlive.com/tomorrow/')
    conts = req.text

    with open('ff.txt', 'wb') as fb:
        fb.write(req.content)

    """ with open('ff.txt', 'r') as fr:
        conts = fr.read() """

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


def extract_game(div: str, team_name: str) -> Game:
    id, date, s1, s2, t1, t2 = extract_data(div)
    return Game(id, date, team_name, t1, t2, s1, s2)


def extract_h2h(team1: str, team2: str, low_year: int = 2020) -> Tuple[List, Dict]:
    team_names = (team1, team2)
    t1_games = get_store_team_games(team1)
    t2_games = get_store_team_games(team2)
    t1_ids = set()
    t2_ids = set()
    home_games = HomeAwayScore(team1, [], [], [], [])
    away_games = HomeAwayScore(team2, [], [], [], [])
    team1_h2h_victory = H2HVictory(team1, [], [])
    team2_h2h_victory = H2HVictory(team2, [], [])
    h2h_ids = set()
    games = []
    team_goals = {team1: set(), team2: set() }

    today = int(datetime.now().timestamp())

    for x in t1_games:
        # if x['id'] in inter:
        if x['team1'] in team_names and x['team2'] in team_names:
            
            year = int(datetime.fromtimestamp(x['date']).year)
            if x['id'] not in h2h_ids and x['date'] < today and year > low_year:
                h2h_ids.add(x['id'])
                extract_homeaway_goals(x, team1, home_games, away_games, team1_h2h_victory, team2_h2h_victory)
                team_goals[x['team1']].add(x['score1'])
                team_goals[x['team2']].add(x['score2'])
                games.append((x['score1'], x['score2']))

    for x in t2_games:
        if x['team1'] in team_names and x['team2'] in team_names:
            
            year = int(datetime.fromtimestamp(x['date']).year)
            if x['id'] not in h2h_ids and x['date'] < today and year > low_year:
                h2h_ids.add(x['id'])
                extract_homeaway_goals(x, team1, home_games, away_games, team1_h2h_victory, team2_h2h_victory)
                team_goals[x['team1']].add(x['score1'])
                team_goals[x['team2']].add(x['score2'])
                games.append((x['score1'], x['score2']))

    return (games, team_goals, home_games, away_games, (team1_h2h_victory, team2_h2h_victory))


def extract_homeaway_goals(
    x: Dict, team1: str,
    home_games: Dict, away_games: Dict,
    team1_vict: Dict, team2_vict: Dict):
    # Home / Away extraction
    if team1 == x['team1']:
        home_games.home_gf.append(x['score1'])
        away_games.away_ga.append(x['score1'])
        home_games.home_ga.append(x['score2'])
        away_games.away_gf.append(x['score2'])

        # Victory extraction
        if x['score1'] > x['score2']:
            team1_vict.home.append('W')
            team2_vict.away.append('L')
        elif x['score1'] < x['score2']:
            team1_vict.home.append('L')
            team2_vict.away.append('W')
        else:
            team1_vict.home.append('D')
            team2_vict.away.append('D')

    elif team1 == x['team2']:
        home_games.away_gf.append(x['score2'])
        away_games.home_ga.append(x['score2'])
        home_games.away_ga.append(x['score1'])
        away_games.home_gf.append(x['score1'])

        # Victory extraction
        if x['score1'] > x['score2']:
            team1_vict.away.append('W')
            team2_vict.home.append('L')
        elif x['score1'] < x['score2']:
            team1_vict.away.append('L')
            team2_vict.home.append('W')
        else:
            team1_vict.away.append('D')
            team2_vict.home.append('D')


def extract_team_victory(name: str) -> Dict:
    """
    Return the Win, Draw or Loss as W, D or L
    """

    team_victory = TeamVictory(name, [], [])

    games = get_store_team_games(name)

    for score in games:
        if name == score['team1']:

            if score['score1'] > score['score2']:
                victory = 'W'
            elif score['score1'] < score['score2']:
                victory = 'L'
            else:
                victory = 'D'

            team_victory.home.append(victory)

        elif name == score['team2']:
            if score['score1'] > score['score2']:
                victory = 'L'
            elif score['score1'] < score['score2']:
                victory = 'W'
            else:
                victory = 'D'

            team_victory.away.append(victory)
    
    return team_victory


def extract_team_data(div: str) -> List:
    id, date, s1, s2, t1, t2 = extract_data(div)
    teams = [Team(int(id), t1, int(date)), Team(int(id), t2, int(date))]
    return teams


def extract_team_scores(name: str) -> Scores:
    scores = []
    games = []
    sgf = []
    sga = []

    conts = get_team_data(name)

    reg = r"data-id=['|\"].*?['|\"] data-status=['|\"]FT['|\"]"
    reg += r".*?data-slug2=['|\"].*?['|\"]"
    all = re.findall(reg, conts)
    for x in all:
        gf, ga = extract_goals(x, name)
        sgf.append(gf)
        sga.append(ga)
        games.append(asdict(extract_game(x, name)))

    temp_store_games(name, games)

    return Scores(name, tuple(sgf), tuple(sga))



# 11th September, 2022
# Amoh-Gyebi Ampofo
from re import L
from threading import local
from typing import Dict

from extract_functions import extract_h2h, extract_team_victory, extract_team_combined_victory, extract_team_scores
from calculate_functions import *
from algorithms import *


def main_summary(team1: str, team2: str) -> Dict:
    summary = {'1x2': '', 'HomeGoal': 0, 'AwayGoal': 0, 'RHG': 0, 'RAG': 0}
    final_summary = {}
    team1_sum = team_summary(team1, 'home')
    team2_sum = team_summary(team2, 'away')
    h2h = h2h_summary(team1, team2)

    victory_sum = victory_summary(team1_sum, team2_sum, h2h)

    # Total games
    summary['HomeGames'] = team1_sum['Games']
    summary['AwayGames'] = team2_sum['Games']

    if victory_sum['home'] > 59:
        summary['1x2'] += 'Home'
    if victory_sum['away'] > 50:
        summary['1x2'] += 'Away'
    if victory_sum['draw'] > 50:
        summary['1x2'] += 'Draw'
    if not summary['1x2']:
        summary['1x2'] = 'Uncertain'

    if 'Predicted GF AVG' in team1_sum and 'Predicted GA AVG' in team2_sum:
        avg = (team1_sum['Predicted GF AVG'] + team2_sum['Predicted GA AVG']) / 2
        over = avg - 0.5
        summary['HomeOver'] = round(over, 2)

    if 'Predicted GF AVG' in team2_sum and 'Predicted GA AVG' in team1_sum:
        avg = (team2_sum['Predicted GF AVG'] + team1_sum['Predicted GA AVG']) / 2
        over = avg - 0.5
        summary['AwayOver'] = round(over, 2)

    if 'Updated Predicted GF(3)' in team1_sum and 'Updated Predicted GA(3)' in team2_sum:
        updated1 = team1_sum['Updated Predicted GF(3)'] + team2_sum['Updated Predicted GA(3)']
        summary['home_gf_avg'] = round(updated1 / 2, 2)
    if 'Updated Predicted GF(3)' in team2_sum and 'Updated Predicted GA(3)' in team1_sum:
        updated2 = team2_sum['Updated Predicted GF(3)'] + team1_sum['Updated Predicted GA(3)']
        summary['away_gf_avg'] = round(updated2 / 2, 2)

    t1_gf = int((team1_sum['GF'] + team2_sum['GA']) / 2)
    t2_gf = int((team1_sum['GA'] + team2_sum['GF']) / 2)
    if t1_gf > 80:
        summary['HomeGoal'] = t1_gf
    if t2_gf > 80:
        summary['AwayGoal'] = t2_gf

    # Recent
    rt1_gf = int((team1_sum['Recent GF'] + team2_sum['Recent GA']) / 2)
    rt2_gf = int((team1_sum['Recent GA'] + team2_sum['Recent GF']) / 2)
    summary['RHG'] = rt1_gf
    summary['RAG'] = rt2_gf

    if 'HomeOver' in summary and 'AwayOver' in summary:
        summary['Over'] = round((summary['HomeOver'] + summary['AwayOver']) - 0.5, 2)

    algo_map = {'Away': away_algorithm, 'Home': home_algorithm, 'Draw': draw_algorithm}
    try:
        final_summary = algo_map[summary['1x2']](summary)
    except:
        final_summary = summary

    return summary | final_summary


def h2h_summary(team1: str, team2: str) -> Dict:
    summary_keys = (
        'H2H_over_under', 'Home_over_under',
        'Away_over_under', 'local_home_1x2',
        'local_away_1x2', 'combined_home_1x2',
        'combined_away_1x2')
    summary = {}
    goals, team_goals, home, away, ha_victory = extract_h2h(team1, team2)
    if team_goals[team1]:
        # mou = match_over_under_evaluation(goals)
        team1_ou = predict_over_under(tuple(team_goals[team1]))
        team2_ou = predict_over_under(tuple(team_goals[team2]))
        team1_h2h_gf =  predict_over_under(tuple(home.home_gf))
        team1_h2h_ga =  predict_over_under(tuple(home.home_ga))
        team2_h2h_gf =  predict_over_under(tuple(away.away_gf))
        team2_h2h_ga =  predict_over_under(tuple(away.away_ga))
        team1_h2h_w = home_away_evaluation(ha_victory[0])
        team2_h2h_w = home_away_evaluation(ha_victory[1])
        gou = predict_game_over_under(goals)

        # check if over/under for at least 5 matches
        per = (team1_ou[0].count(None) / len(team1_ou[0])) * 100
        if per < 33:
            summary['H2H_over_under'] = gou
            summary['Home_over_under'] = team1_ou
            summary['Away_over_under'] = team2_ou

        # for location based 1x2
        locals = []
        local_h2hs = (team1_h2h_w['home'], team2_h2h_w['away'])
        for y in local_h2hs:
            local_1x2 = ''
            highest = 0

            for x in y:
                if y[x] > highest:
                    highest = y[x]
                    local_1x2 = x
                elif y[x] == highest:
                    local_1x2 += x

            locals.append(local_1x2)

        # for the combined 1x2
        combineds = []
        for y in (team1_h2h_w, team2_h2h_w):
            tt = list(y['home'].values())
            tt.extend(list(y['away'].values()))
            tt = [x or 0 for x in tt]
            t_c = {}
            t_c['W'] = tt[0] + tt[3]
            t_c['D'] = tt[1] + tt[4]
            t_c['L'] = tt[2] + tt[5]

            combined_1x2 = ''
            highest = 0
            for x in t_c:
                if t_c[x] > highest:
                    highest = t_c[x]
                    combined_1x2 = x
                elif t_c[x] == highest:
                    combined_1x2 += x

            combineds.append(combined_1x2)

        summary['local_home_1x2'] = locals[0]
        summary['local_away_1x2'] = locals[1]
        summary['combined_home_1x2'] = combineds[0]
        summary['combined_away_1x2'] = combineds[1]

    return summary


def over_under_summary(team_name) -> Dict:

    """ {
        'GF': gfou, 'GA': gaou,
        'Recent GF(5)': mrgf_5, 'Recent GF(10)': mrgf_10, 
        'Recent GA(5)': mrga_5, 'Recent GA(10)': mrga_10,
        'Predicted GF(5)': p5, 'Predicted GF(10)': p10,
        'Predicted GA(5)': pa5, 'Predicted GA(10)': pa10,
        'Updated Predicted GF(3)': p3, 'Updated Predicted GA(3)': pa3} """

    summary = {}
    over_under_keys = (
        'GF', 'GA',
        'Recent GF', 'Recent GF',
        'Recent GA', 'Recent GA',
        'Predicted GF(5)', 'Predicted GF(10)',
        'Predicted GA(5)', 'Predicted GA(10)',
        'Predicted GF AVG', 'Predicted GA AVG')
    scores = extract_team_scores(team_name)
    gfou = over_under_evaluation(scores.gf)
    gaou = over_under_evaluation(scores.ga)
    mrgf_5, mrgf_10 = most_recent_over_under(scores.gf)
    mrga_5, mrga_10 = most_recent_over_under(scores.ga)
    p3, p5, p10 = predict_over_under(scores.gf)
    pa3, pa5, pa10 = predict_over_under(scores.ga)
    pgf_avg = final_predict_over_under(p5[-1], p10[-1])
    pga_avg = final_predict_over_under(pa5[-1], pa10[-1])

    # Summary
    summary['GF'] = gfou
    summary['GA'] = gaou
    if pgf_avg >= 1.0:
        summary['Predicted GF AVG'] = pgf_avg
        summary['Predicted GF(10)'] = p10
    if pga_avg >= 1.0:
        summary['Predicted GA AVG'] = pga_avg
        summary['Predicted GA(10)'] = pa10
    
    if p3[-1] >= 1.0:
        summary['Updated Predicted GF(3)']: p3[-1]
    if pa3[-1] >= 1.0:
        summary['Updated Predicted GA(3)']: pa3[-1]

    summary['Recent GF'] = int((mrgf_5 + mrgf_10) / 2)
    summary['Recent GA'] = int((mrga_5 + mrga_10) / 2)

    return summary


def team_summary(team_name: str, location: str) -> Dict:
    team_summary_keys = ('GF', 'GA', 'W')
    t1_ous = over_under_summary(team_name)
    vic = extract_team_victory(team_name)
    t_ha_eval = home_away_evaluation(vic)
    t_ha_eval = t_ha_eval[location]
    summary = t1_ous

    # Count games
    total_games = []
    total_games.extend(vic.home)
    total_games.extend(vic.away)
    summary = summary | {'Games': len(total_games)}

    # for location based win
    local_1x2 = ''
    highest = 0
    for x in t_ha_eval:
        if t_ha_eval[x] > highest:
            highest = t_ha_eval[x]
            local_1x2 = x
        elif t_ha_eval[x] == highest:
            local_1x2 += x

    summary = summary | {'local_1x2': local_1x2}

    c_vic = extract_team_combined_victory(team_name)

    vivv = range_matches_evaluation(c_vic)

    # for the overal win rate
    combined_1x2 = ''
    highest = 0
    for x in vivv:
        if vivv[x] > highest:
            highest = vivv[x]
            combined_1x2 = x
        elif vivv[x] == highest:
            combined_1x2 += x
    
    summary = summary | {'combined_1x2': combined_1x2}

    return summary


def victory_summary(team1_summary: Dict, team2_summary: Dict, h2h_summary: Dict) -> Dict:
    h2h_win_score = {'home': 0, 'draw': 0, 'away': 0}
    t1_local_1x2 = team1_summary['local_1x2']
    t1_combined_1x2 = team1_summary['combined_1x2']
    t2_local_1x2 = team2_summary['local_1x2']
    t2_combined_1x2 = team2_summary['combined_1x2']

    if h2h_summary:
        home_1x2 = h2h_summary['local_home_1x2']
        combined_home_1x2 = h2h_summary['combined_home_1x2']
        away_1x2 = h2h_summary['local_away_1x2']
        combined_away_1x2 = h2h_summary['combined_away_1x2']

        if combined_home_1x2 == 'W':
            h2h_win_score['home'] += 30
        if combined_away_1x2 == 'W':
            h2h_win_score['away'] += 30
        if home_1x2 == 'W':
            h2h_win_score['home'] += 20
        if away_1x2 == 'W':
            h2h_win_score['away'] += 20

        if combined_home_1x2 == 'D':
            h2h_win_score['draw'] += 15
        if combined_away_1x2 == 'D':
            h2h_win_score['draw'] += 15
        if home_1x2 == 'D':
            h2h_win_score['draw'] += 10
        if away_1x2 == 'D':
            h2h_win_score['draw'] += 10
        
        if combined_home_1x2 in ('WD', 'DW'):
            h2h_win_score['home'] += 15
            h2h_win_score['draw'] += 15
        if combined_away_1x2 in ('WD', 'DW'):
            h2h_win_score['away'] += 15
            h2h_win_score['draw'] += 15
        if home_1x2 in ('WD', 'DW'):
            h2h_win_score['home'] += 10
            h2h_win_score['draw'] += 10
        if away_1x2 in ('WD', 'DW'):
            h2h_win_score['away'] += 10
            h2h_win_score['draw'] += 10

    if t1_local_1x2 == 'W':
        h2h_win_score['home'] += 30
    if t2_local_1x2 == 'W':
        h2h_win_score['away'] += 30
    if t1_combined_1x2 == 'W':
        h2h_win_score['home'] += 20
    if t2_combined_1x2 == 'W':
        h2h_win_score['away'] += 20

    if t1_local_1x2 == 'D':
        h2h_win_score['draw'] += 15
    if t2_local_1x2 == 'D':
        h2h_win_score['draw'] += 15
    if t1_combined_1x2 == 'D':
        h2h_win_score['draw'] += 10
    if t2_combined_1x2 == 'D':
        h2h_win_score['draw'] += 10

    if t1_local_1x2 in ('WD', 'DW'):
        h2h_win_score['home'] += 15
        h2h_win_score['draw'] += 15
    if t2_local_1x2 in ('WD', 'DW'):
        h2h_win_score['away'] += 15
        h2h_win_score['draw'] += 15
    if t1_combined_1x2 in ('WD', 'DW'):
        h2h_win_score['home'] += 10
        h2h_win_score['draw'] += 10
    if t2_combined_1x2 in ('WD', 'DW'):
        h2h_win_score['away'] += 10
        h2h_win_score['draw'] += 10

    return h2h_win_score


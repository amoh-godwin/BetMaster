# 11th September, 2022
# Amoh-Gyebi Ampofo
from typing import Dict

from extract_functions import extract_h2h
from calculate_functions import *


def over_under_summary(scores) -> Dict:
    gfou = over_under_evaluation(scores.gf)
    gaou = over_under_evaluation(scores.ga)
    mrgf_5, mrgf_10 = most_recent_over_under(scores.gf)
    mrga_5, mrga_10 = most_recent_over_under(scores.ga)
    p5, p10 = predict_over_under(scores.gf)
    pa5, pa10 = predict_over_under(scores.ga)
    return {
        'GF': gfou, 'GA': gaou,
        'Recent GF(5)': mrgf_5, 'Recent GF(10)': mrgf_10, 
        'Recent GA(5)': mrga_5, 'Recent GA(10)': mrga_10,
        'Predicted GF(5)': p5, 'Predicted GF(10)': p10,
        'Predicted GA(5)': pa5, 'Predicted GA(10)': pa10}


def h2h_summary(team1: str, team2: str) -> Dict:
    goals, team_goals, home, away = extract_h2h(team1, team2)
    # mou = match_over_under_evaluation(goals)
    team1_ou = predict_over_under(tuple(team_goals[team1]))
    team2_ou = predict_over_under(tuple(team_goals[team2]))
    team1_h2h_gf =  predict_over_under(tuple(home.home_gf))
    team1_h2h_ga =  predict_over_under(tuple(home.home_ga))
    team2_h2h_gf =  predict_over_under(tuple(away.away_gf))
    team2_h2h_ga =  predict_over_under(tuple(away.away_ga))
    gou = predict_game_over_under(goals)
    # return {team1: team1_ou, team2: team2_ou, 'gou': gou}
    return (team1_h2h_gf, team1_h2h_ga, team2_h2h_gf, team2_h2h_ga, gou)

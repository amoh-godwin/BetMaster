# 16th September, 2022
# Amoh-Gyebi Ampofo
from typing import Dict


def draw_algorithm(summary: Dict) -> Dict:
    final_sum = {}
    if 'HomeOver' in summary and 'AwayOver' in summary:
        if int(summary['HomeOver']) == int(summary['AwayOver']):
            final_sum['1x2'] = 'Draw'
        else:
            final_sum['1x2'] = 'Uncertain'
    elif 'HomeOver' not in summary and 'AwayOver' not in summary:
        final_sum['1x2'] = 'Draw'
    else:
        final_sum['1x2'] = 'Uncertain'

    return final_sum


def away_algorithm(summary: Dict) -> Dict:
    final_sum = {}
    if 'HomeOver' in summary:
        final_sum['1x2'] = 'Uncertain'
    elif 'AwayOver' in summary:
        final_sum['1x2'] = 'Away'
    else:
        final_sum['1x2'] = 'Uncertain'

    return final_sum


def home_algorithm(summary: Dict) -> Dict:
    final_sum = {}
    if 'AwayOver' in summary:
        final_sum['1x2'] = 'Uncertain'
    elif 'HomeOver' in summary:
        final_sum['1x2'] = 'Home'
    else:
        final_sum['1x2'] = 'Uncertain'

    return final_sum

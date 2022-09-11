# 11th September, 2022
# Amoh-Gyebi Ampofo
from typing import Dict

from calculate_functions import over_under_evaluation, most_recent_over_under

def over_under_summary(scores) -> Dict:
    gfou = over_under_evaluation(scores.gf)
    gaou = over_under_evaluation(scores.ga)
    mrgf_5, mrgf_10 = most_recent_over_under(scores.gf)
    mrga_5, mrga_10 = most_recent_over_under(scores.ga)
    return {
        'GF': gfou, 'GA': gaou, 
        'Recent GF(5)': mrgf_5, 'Recent GF(10)': mrgf_10, 
        'Recent GA(5)': mrga_5, 'Recent GA(10)': mrga_10}

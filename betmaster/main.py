# 11th September, 2022
# Amoh-Gyebi Ampofo
import requests

from extract_functions import extract_footlive_tomorrow, extract_team_scores
from calculate_functions import over_under_evaluation, most_recent_over_under

scores = extract_team_scores('bkma-yerevan')
ev = over_under_evaluation(scores.ga)
most_recent_over_under(scores.ga)

print(ev)


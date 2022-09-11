# 11th September, 2022
# Amoh-Gyebi Ampofo
import requests

from extract_functions import extract_footlive_tomorrow, extract_team_scores
from summary_functions import over_under_summary

scores = extract_team_scores('bkma-yerevan')
bkma_sum = over_under_summary(scores)

print(bkma_sum)


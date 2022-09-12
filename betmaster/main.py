# 11th September, 2022
# Amoh-Gyebi Ampofo
import requests

from extract_functions import extract_footlive_tomorrow, extract_team_scores, extract_h2h
from summary_functions import over_under_summary, h2h_summary

scores = extract_team_scores('ararat-yerevan')
scores_2 = extract_team_scores('bkma-yerevan')
bkma_sum = over_under_summary(scores_2)
ararat_sum = over_under_summary(scores)

h2h_summary('ararat-yerevan', 'bkma-yerevan')

print(bkma_sum)
print(ararat_sum)

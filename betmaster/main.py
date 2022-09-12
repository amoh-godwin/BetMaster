# 11th September, 2022
# Amoh-Gyebi Ampofo
import requests

from extract_functions import extract_footlive_tomorrow, extract_team_scores, extract_h2h
from summary_functions import over_under_summary

# scores = extract_team_scores('ararat-yerevan')
# bkma_sum = over_under_summary(scores)

extract_h2h('bkma-yerevan', 'ararat-yerevan')

# print(bkma_sum)


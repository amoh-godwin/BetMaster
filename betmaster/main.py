# 11th September, 2022
# Amoh-Gyebi Ampofo

from ast import main
from msilib.schema import Error
from summary_functions import main_summary
from extract_functions import extract_not_started



""" summ = main_summary('cd-luis-angel-firpo', 'cd-aguila')
print(summ, '\n')
 """
matches = extract_not_started()

for x in matches:
    try:
        one = main_summary(x.home, x.away)
    except Exception:
        one = 'Error while processing'

    """ if 'HomeOver' not in one or 'AwayOver' not in one:
        continue

    if one['Over'] < 1.99:
        continue """

    if 'Over' not in one:
        continue

    if one['Over'] < 1.59 and one['Under'] == 0:
        continue

    print(f'\n{x.home_name} vs {x.away_name} : {one}\n')
    print(f'*****************\n')

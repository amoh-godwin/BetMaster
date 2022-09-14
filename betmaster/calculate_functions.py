# 11th September, 2022
# Amoh-Gyebi 
from cgi import test
from collections import Counter
from typing import Tuple, List, Dict
from unittest import result

OVER_ADD = 1.5
UNDER_MINUS = 0.5


def home_away_evaluation(scores: Dict) -> Dict:
    results = {}
    home = tuple(scores.home)
    away = tuple(scores.away)
    hw = home.count('W')
    hd = home.count('D')
    hl = home.count('L')
    aw = away.count('W')
    ad = away.count('D')
    al = away.count('L')
    if home:
        hwp = int((hw / len(home)) * 100)
        hdp = int((hd / len(home)) * 100)
        hlp = int((hl / len(home)) * 100)
    else:
        hwp, hdp, hlp = (None, None, None)
    if away:
        awp = int((aw / len(away)) * 100)
        adp = int((ad / len(away)) * 100)
        alp = int((al / len(away)) * 100)
    else:
        awp, adp, alp = (None, None, None)

    results['home'] = {'W': hwp, 'D': hdp, 'L': hlp}
    results['away'] = {'W': awp, 'D': adp, 'L': alp}
    return results

def range_matches_evaluation(scores: Dict, length: int = 0) -> Dict:
    if length == 0:
        length = len(scores.victories)

    ha = scores.victories[0:length]

    total = len(ha)

    w = round((ha.count('W') / total) * 100)
    d = round((ha.count('D') / total) * 100)
    l = round((ha.count('L') / total) * 100)

    return {'W': w, 'D': d, 'L': l}

def match_over_under_evaluation(scores: tuple) -> Tuple[bool, bool]:
    # check the score in groups of 2
    # to see if the predictions were accurate
    # Most recent scores fewer than 2
    # are not included in evaluation
    two = set()
    under_rate = False # max
    unders = []
    under_percent = 0
    over_rate = False # min
    overs = []
    over_percent = 0
    counter = 0
    overall_index = 0
    for x in scores:
        two.add(x)
        counter += 1
        if counter == 2:
            try:
                test_score = scores[overall_index + 1]
            except:
                test_score = -1
            under_rate, over_rate = min_max(two, test_score)
            unders.append(under_rate)
            overs.append(over_rate)
            # rating.append((under_rate, over_rate))
            two = set()

            counter = 0

        overall_index += 1

    count = Counter(overs)
    count_u = Counter(unders)

    over_percent = (count.get(True) / len(overs)) * 100
    under_percent = (count_u.get(True) / len(unders)) * 100

    return (over_percent, under_percent)


def over_under_evaluation(scores: tuple) -> Tuple[bool, bool]:
    # check the score in groups of 5 and 10
    # to see if the predictions were accurate
    # Most recent scores fewer than 5 and 10
    # are not included in evaluation
    five = set()
    ten = set()
    rating = []
    under_rate = False # max
    unders = []
    under_percent = 0
    over_rate = False # min
    overs = []
    over_percent = 0
    counter = 0
    ten_counter = 0
    overall_index = 0
    for x in scores:
        five.add(x)
        ten.add(x)
        counter += 1
        ten_counter += 1
        if counter == 5:
            try:
                test_score = scores[overall_index + 1]
            except:
                test_score = -1
            under_rate, over_rate = min_max(five, test_score)
            unders.append(under_rate)
            overs.append(over_rate)
            # rating.append((under_rate, over_rate))
            five = set()

            counter = 0

        if ten_counter == 10:
            try:
                test_score = scores[overall_index + 1]
            except:
                test_score = -1
            under_rate, over_rate = min_max(ten, test_score)
            ten_counter = 0
            rating.append((under_rate, over_rate))
            ten = set()

        overall_index += 1
    
    count = Counter(overs)
    count_u = Counter(unders)

    over_percent = (count.get(True) / len(overs)) * 100
    under_percent = (count_u.get(True) / len(unders)) * 100
    per = (over_percent + under_percent) / 2

    return (per)


def min_max(group_score: tuple, test_score: int) -> Tuple[bool, bool]:
    # Get the under and over of the predicted scores
    # and see which of the prediction was True

    if test_score < 0:
        return (None, None)

    maxx = max(group_score) + OVER_ADD
    minn = min(group_score) - UNDER_MINUS
    under_rate, over_rate = (False, False)
    if test_score < maxx:
        under_rate = True
    if test_score > minn:
        over_rate = True

    return (under_rate, over_rate)


def most_recent_over_under(scores: tuple) -> Tuple:
    # Get the most recent prediction
    # and see it it was True
    l = len(scores)
    five = set(scores[l-5:])
    ten = set(scores[l-10:])
    t_five = scores[l-6]
    t_ten = scores[l-11]
    f_min_max = min_max(five, t_five)
    t_min_max = min_max(ten, t_ten)
    f_per = (f_min_max.count(True) / len(f_min_max)) * 100
    t_per = (t_min_max.count(True) / len(t_min_max)) * 100
    return f_per, t_per


def predict_game_over_under(scores: list):

    pred = []

    for x in scores:
        maxx = max(x) + OVER_ADD
        minn = min(x) - UNDER_MINUS
        pred.extend([maxx, minn])

    pred = set(pred)
    low = min(pred)
    high = max(pred)

    return (low, high)


def predict_over_under(scores: tuple) -> List[Tuple[float, float]]:
    l = len(scores)
    five = set(scores[l-5:])
    ten = set(scores[l-10:])

    maxx = max(five) + OVER_ADD
    minn = min(five) - UNDER_MINUS

    t_maxx = max(ten) + OVER_ADD
    t_minn = min(ten) - UNDER_MINUS

    return [(maxx, minn), (t_maxx, t_minn)]

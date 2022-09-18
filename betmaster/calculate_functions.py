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
        hwp, hdp, hlp = (0, 0, 0)
    if away:
        awp = int((aw / len(away)) * 100)
        adp = int((ad / len(away)) * 100)
        alp = int((al / len(away)) * 100)
    else:
        awp, adp, alp = (0, 0, 0)

    results['home'] = {'W': hwp, 'D': hdp, 'L': hlp}
    results['away'] = {'W': awp, 'D': adp, 'L': alp}
    return results

def range_matches_evaluation(scores: Dict, length: int = 0) -> Dict:
    if length == 0:
        length = len(scores.victories)

    ha = scores.victories[0:length]

    total = len(ha)
    if total:
        w = round((ha.count('W') / total) * 100)
        d = round((ha.count('D') / total) * 100)
        l = round((ha.count('L') / total) * 100)
    else:
        w, d, l = (0, 0, 0) # for now

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
    five = []
    ten = []
    under_rate = False # max
    unders = []
    ten_unders = []
    under_percent = 0
    over_rate = False # min
    overs = []
    ten_overs = []
    over_percent = 0
    counter = 0
    ten_counter = 0
    overall_index = 0

    for x in scores:
        five.append(x)
        ten.append(x)
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
            five = []

            counter = 0

        if ten_counter == 10:
            try:
                test_score = scores[overall_index + 1]
            except:
                test_score = -1
            under_rate, over_rate = min_max(ten, test_score)
            ten_counter = 0
            ten_overs.append(over_rate)
            ten_unders.append(under_rate)
            ten = []

        overall_index += 1

    if not overs or not unders:
        per = 0
    else:
        over_percent = round((overs.count(True) / len(overs)) * 100)
        under_percent = round((unders.count(True) / len(unders)) * 100)
        per = round((over_percent + under_percent) / 2)

    if not ten_overs or not ten_unders:
        ten_per = 0
    else:
        ten_o_per = round((ten_overs.count(True) / len(ten_overs)) * 100)
        ten_u_per = round((ten_unders.count(True) / len(ten_unders)) * 100)
        ten_per = round((ten_o_per + ten_u_per) / 2)

    return round((per + ten_per) / 2)


def min_max(group_score: tuple, test_score: int) -> Tuple[bool, bool]:
    # Get the under and over of the predicted scores
    # and see which of the prediction was True

    if test_score < 0:
        return (False, False)

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
    five = tuple(scores[l-5:])
    ten = tuple(scores[l-10:])
    try:
        t_five = scores[l-6]
    except:
        t_five = -1
    try:
        t_ten = scores[l-11]
    except:
        t_ten = -1
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
    if pred:
        low = min(pred)
        high = max(pred)
    else:
        low = -100.5
        high = 100.5

    return (high, low)


def predict_over_under(scores: tuple) -> List[Tuple[float, float]]:
    l = len(scores)
    three = scores[l-3:]
    five = scores[l-5:]
    ten = scores[l-10:]

    if l > 2:
        tri_max = max(three) + OVER_ADD
        tri_min = min(three) - UNDER_MINUS
        tri_avgg = sum(three) / 3
    else:
        tri_max, tri_min, tri_avgg = 0, 0, 0

    if l > 4:
        maxx = max(five) + OVER_ADD
        minn = min(five) - UNDER_MINUS
        avgg = sum(five) / 5
    else:
        maxx, minn, avgg = 0, 0, 0

    if l > 9:
        t_maxx = max(ten) + OVER_ADD
        t_minn = min(ten) - UNDER_MINUS
        t_avgg = sum(ten) / 10
    else:
        t_maxx, t_minn, t_avgg = 0, 0, 0

    return [(tri_max, tri_min, tri_avgg), (maxx, minn, avgg), (t_maxx, t_minn, t_avgg)]


def final_predict_over_under(five_avg: int, ten_avg: int) -> int:
    # find the average of the average
    if not five_avg or not ten_avg:
        return 0
    return abs((five_avg + ten_avg) / 2)

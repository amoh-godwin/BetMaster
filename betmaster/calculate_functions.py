# 11th September, 2022
# Amoh-Gyebi 
from collections import Counter
from typing import Tuple, List

OVER_ADD = 1.5
UNDER_MINUS = 0.5


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
            test_score = scores[overall_index]
            under_rate, over_rate = min_max(five, test_score)
            unders.append(under_rate)
            overs.append(over_rate)
            # rating.append((under_rate, over_rate))
            five = set()

            counter = 0

        if ten_counter == 10:
            test_score = scores[overall_index + 1]
            under_rate, over_rate = min_max(ten, test_score)
            ten_counter = 0
            rating.append((under_rate, over_rate))
            ten = set()

        overall_index += 0
    
    count = Counter(overs)
    count_u = Counter(unders)

    over_percent = (count.get(True) / len(overs)) * 100
    under_percent = (count_u.get(True) / len(unders)) * 100

    return (over_percent, under_percent)


def min_max(group_score: tuple, test_score: int) -> tuple:
    # Get the under and over of the predicted scores
    # and see which of the prediction was True
    maxx = max(group_score) + OVER_ADD
    minn = min(group_score) - UNDER_MINUS
    under_rate, over_rate = (False, False)
    if test_score < maxx:
        under_rate = True
    if test_score > minn:
        over_rate = True

    return (under_rate, over_rate)


def most_recent_over_under(scores: tuple) -> tuple:
    # Get the most recent prediction
    # and see it it was True
    l = len(scores)
    five = set(scores[l-5:])
    ten = set(scores[l-10:])
    t_five = scores[l-6]
    t_ten = scores[l-11]
    f_min_max = min_max(five, t_five)
    t_min_max = min_max(ten, t_ten)
    return f_min_max, t_min_max


def predict_over_under(scores: tuple) -> List[Tuple[float, float]]:
    l = len(scores)
    five = set(scores[l-5:])
    ten = set(scores[l-10:])

    maxx = max(five) + OVER_ADD
    minn = min(five) - UNDER_MINUS

    t_maxx = max(ten) + OVER_ADD
    t_minn = min(ten) - UNDER_MINUS

    return [(maxx, minn), (t_maxx, t_minn)]

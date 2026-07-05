from find_figure.settings import UPPER_LIMIT, LOWER_LIMIT


def algorithm_1(fact_color):
    for i in 0, 1, 2:
        if not UPPER_LIMIT > fact_color[i] > LOWER_LIMIT:
            return False
    return True


def algorithm_2(fact_color):
    color = list(filter(None, fact_color[:3]))
    print(color)
    if len(color) > 1:
        a = max(color)
        b = min(color)
        dif = a / b
        if dif <= 2:
            return True
        else:
            return False


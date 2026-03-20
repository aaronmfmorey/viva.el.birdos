# Fangraphs doesn't publicize their formula, but Baseball Reference uses 1.83 as the exponent
EXPONENT = 1.83


def calculate_pythag_wins(rs: int, ra: int, exponent: int = None, games: int = 162):
    if exponent is None:
        exponent = EXPONENT

    if exponent < 0 or rs < 0 or ra < 0 or games < 0:
        raise Exception("Pythag cannot operate on negative numbers")

    expected_win_percentage = (rs**exponent) / ((ra**exponent) + rs**exponent)

    return expected_win_percentage * games

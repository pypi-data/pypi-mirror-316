from datalib.statistics import calculate_mean, calculate_median

def test_calculate_mean():
    data = [1, 2, 3, 4, 5]
    assert calculate_mean(data) == 3


def test_calculate_median():
    data = [1, 2, 3, 4, 5]
    assert calculate_median(data) == 3

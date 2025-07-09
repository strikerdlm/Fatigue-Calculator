import pytest
from fatigue_calculator import core

def test_simulate_cognitive_performance_length():
    hours = 24
    sleep_start = 22
    sleep_end = 6
    sleep_quality = 0.8
    sleep_quantity = 7
    work_start = 9
    work_end = 17
    load_rating = 2
    t, c, e = core.simulate_cognitive_performance(hours, sleep_start, sleep_end, sleep_quality, sleep_quantity, work_start, work_end, load_rating)
    assert len(t) == hours
    assert len(c) == hours
    assert len(e) == hours 
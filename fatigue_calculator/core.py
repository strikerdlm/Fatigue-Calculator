# Core logic for Fatigue Calculator
# (Moved from FatigueCalc3.py)

import math
import pandas as pd

def homeostatic_process(t, prev_reservoir_level, asleep, ai, sleep_quality, sleep_quantity):
    K = 0.5
    K_adjusted = K * (1 + (8 - sleep_quantity) * 0.1)
    as_factor = 0.235
    tau1 = 1
    tau2 = 1
    delta_t = 1

    if asleep:
        recovery_factor = sleep_quality * (1 - math.exp(-delta_t / tau1))
        return as_factor + recovery_factor * prev_reservoir_level + (1 - math.exp(-delta_t / tau2)) * (ai - as_factor)
    else:
        return prev_reservoir_level - K_adjusted * t

def circadian_process(t):
    p = 18
    p_prime = 3
    beta = 0.5

    return math.cos(2 * math.pi * (t - p) / 24) + beta * math.cos(4 * math.pi * (t - p_prime) / 24)

def sleep_inertia(t):
    Imax = 5
    i = 0.04

    if t < 2:
        return Imax * math.exp(-t / i)
    else:
        return 0

def cognitive_performance(t, Rt, Ct, It):
    a1 = 7
    a2 = 5
    Rc = 2880

    return 100 * (Rt / Rc) + (a1 + a2 * (Rc - Rt) / Rc) * Ct + It

def workload(t, Wt_prev, load_rating, asleep):
    Wc = 75
    Wd = 1.14
    Wr = 11

    if asleep:
        return Wt_prev + Wr
    else:
        return Wt_prev - Wd * (1 + load_rating)

def cognitive_performance_with_workload(t, Rt, Ct, It, Wt, Wc):
    Et_base = cognitive_performance(t, Rt, Ct, It)
    return Et_base * (Wc - Wt) / Wc

def simulate_cognitive_performance(hours, sleep_start, sleep_end, sleep_quality, sleep_quantity, work_start, work_end, load_rating):
    Wt_prev = 0
    Wc = 75
    time_points = []
    circadian_rhythms = []
    cognitive_performances = []

    for t in range(hours):
        asleep = sleep_start <= t % 24 < sleep_end
        at_work = work_start <= t % 24 < work_end

        if t == 0:
            prev_reservoir_level = 2400
            ai = 1
        else:
            prev_reservoir_level = Rt
            ai = 1

        Rt = homeostatic_process(t, prev_reservoir_level, asleep, ai, sleep_quality, sleep_quantity)
        Ct = circadian_process(t)
        It = sleep_inertia(t)

        if at_work:
            Wt = workload(t, Wt_prev, load_rating, asleep)
            E_t = cognitive_performance_with_workload(t, Rt, Ct, It, Wt, Wc)
        else:
            E_t = cognitive_performance(t, Rt, Ct, It)

        time_points.append(t)
        circadian_rhythms.append(Ct)
        cognitive_performances.append(E_t)

    return time_points, circadian_rhythms, cognitive_performances 
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:02:27 2023

@author: DiegoMalpica
"""
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

def main():
    # Gather user input
    sleep_start = int(input("Enter sleep start time (0-23): "))
    sleep_end = int(input("Enter sleep end time (0-23): "))
    sleep_quality = float(input("Enter sleep quality (0-1): "))
    sleep_quantity = float(input("Enter sleep quantity (in hours): "))
    work_start = int(input("Enter work start time (0-23): "))
    work_end = int(input("Enter work end time (0-23): "))
    load_rating = int(input("Enter workload rating (0-3): "))

    # Calculate cognitive performance for the next 48 hours
    hours = 48
    time_points, circadian_rhythms, cognitive_performances = simulate_cognitive_performance(
        hours, sleep_start, sleep_end, sleep_quality, sleep_quantity, work_start, work_end, load_rating)

    # Save cognitive performance data to an Excel file
    def categorize(score):
        if score < 60:
            return "Low"
        elif score < 80:
            return "Moderate"
        else:
            return "High"

    categories = [categorize(s) for s in cognitive_performances]

    data = {
        "Time of Day": [(t % 24) for t in time_points],
        "Predicted Cognitive Performance": cognitive_performances,
        "Performance Category": categories,
    }
    df = pd.DataFrame(data)
    df.to_excel("cognitive_performance_data.xlsx", index=False)

    # Console summary based on scientific thresholds
    average_perf = sum(cognitive_performances) / len(cognitive_performances)
    min_perf = min(cognitive_performances)
    max_perf = max(cognitive_performances)
    time_min = time_points[cognitive_performances.index(min_perf)] % 24
    time_max = time_points[cognitive_performances.index(max_perf)] % 24
    low_periods = sum(1 for s in cognitive_performances if s < 60)
    moderate_periods = sum(1 for s in cognitive_performances if 60 <= s < 80)

    print("Cognitive performance data saved to 'cognitive_performance_data.xlsx'")
    print("\n===== Scientific Summary =====")
    print(f"Average predicted performance: {average_perf:.1f}")
    print(f"Peak performance of {max_perf:.1f} expected around hour {time_max}")
    print(f"Lowest performance of {min_perf:.1f} expected around hour {time_min}")
    print(f"Number of low-performance hours (<60): {low_periods}")
    print(f"Number of moderate-performance hours (60-80): {moderate_periods}")

if __name__ == "__main__":
    main()


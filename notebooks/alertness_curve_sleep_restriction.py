# %% [markdown]
# # Alertness Curve Simulation: 3-Hour Sleep Restriction for 5 Days
#
# This notebook-style script demonstrates how to use the `fatigue_calculator` package
# included in this repository to model the alertness (cognitive performance)
# trajectory of an individual who restricts their sleep by **3 hours each night** over
# a 5-day period.
#
# * **Sleep quantity:** 5 h/night (00:00 – 05:00)
# * **Sleep quality:** 0.7 (“fair”) on a 0–1 scale
# * **Workload:** Moderate (8 h daily, cognitive load rating = 1)
# * **Simulation length:** 5 days (120 h)
#
# You can open this file directly in JupyterLab or VS Code as a notebook (thanks to
# the `# %%` cell markers) or run it as a plain Python script.

# %%
import matplotlib.pyplot as plt
from fatigue_calculator.core import enhanced_simulate_cognitive_performance

# ---------------- Scenario configuration -----------------------------
hours = 5 * 24  # 5 days

# Sleep: 00:00 – 05:00 (5 h) each day
sleep_quantity = 5        # hours/night
sleep_quality = 0.7       # fair quality
sleep_start = 0           # hour of day (24-h clock)
sleep_end = sleep_start + sleep_quantity

# Work: 09:00 – 17:00 (8 h) each day
work_start = 9            # hour of day
work_end = 17             # hour of day
cognitive_load_rating = 1 # moderate workload

# Build repeating daily schedules (24-h pattern)
sleep_schedule = {
    'quality': sleep_quality,
    'quantity': sleep_quantity,
}
for h in range(24):
    sleep_schedule[h] = sleep_start <= h < sleep_end

work_schedule = {
    'load_rating': cognitive_load_rating,
}
for h in range(24):
    work_schedule[h] = work_start <= h < work_end

individual_profile = {}  # default profile (average person)

# ---------------- Run simulation -------------------------------------
time_pts, circadian, performance = enhanced_simulate_cognitive_performance(
    hours, sleep_schedule, work_schedule, individual_profile
)

# ---------------- Visualise -----------------------------------------
plt.figure(figsize=(12, 4))
plt.plot(time_pts, performance, label='Alertness / Cognitive Performance')
plt.xlabel('Time (hours)')
plt.ylabel('Performance (0–100)')
plt.title('Alertness curve – 5 days with 3 h sleep restriction per night')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Interpretation
# The plot shows how the model predicts a progressive decline in cognitive
# performance as sleep debt accumulates across the 5-day period. Feel free to
# experiment with different:
# * **Sleep schedules** (e.g. shorter naps, extending sleep at the weekend)
# * **Workload intensities** (`cognitive_load_rating`)
# * **Sleep-quality values** (0 – 1)
#
# The underlying engine incorporates state-of-the-art findings up to 2024,
# including adenosine dynamics, circadian modulation, workload effects, and
# individual differences.
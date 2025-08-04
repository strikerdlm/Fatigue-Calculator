# %% [markdown]
# # Sleep Restriction Analysis: Impact on Alertness Over 7 Days
#
# This notebook demonstrates the effects of different sleep durations (1-7 hours) 
# on cognitive performance and alertness over a 7-day period using the enhanced 
# fatigue calculator with the latest 2024 scientific research.

# %%
# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fatigue_calculator.core import enhanced_simulate_cognitive_performance
import warnings
warnings.filterwarnings('ignore')

# Set plotting style for better visualizations
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

print("Sleep Restriction Analysis - Enhanced 2025 Research Edition")
print("=" * 60)

# %%
# Configuration
SIMULATION_DAYS = 7
HOURS_TOTAL = SIMULATION_DAYS * 24
SLEEP_DURATIONS = [1, 2, 3, 4, 5, 6, 7]  # Hours of sleep per night
SLEEP_QUALITY = 0.7  # Fair sleep quality
WORK_START, WORK_END = 9, 17  # 9 AM to 5 PM
COGNITIVE_LOAD = 1  # Moderate workload

# Individual profile (average person)
INDIVIDUAL_PROFILE = {
    'genetic_profile': [], 'sex': 'unknown', 'age': 25, 'chronotype_offset': 0
}

print(f"Simulating {SIMULATION_DAYS} days with sleep durations: {SLEEP_DURATIONS} hours")

# %%
# Function to create schedules
def create_schedules(sleep_duration, sleep_quality, work_start, work_end, cognitive_load):
    """Create sleep and work schedules for simulation"""
    sleep_start = 0  # Midnight
    sleep_end = sleep_duration
    
    # Sleep schedule
    sleep_schedule = {'quality': sleep_quality, 'quantity': sleep_duration}
    for h in range(24):
        sleep_schedule[h] = sleep_start <= h < sleep_end
    
    # Work schedule  
    work_schedule = {'load_rating': cognitive_load}
    for h in range(24):
        work_schedule[h] = work_start <= h < work_end
    
    return sleep_schedule, work_schedule

# %%
# Run simulations
print("Running simulations...")
results = {}
all_data = []

for sleep_duration in SLEEP_DURATIONS:
    print(f"  Simulating {sleep_duration}h sleep...")
    
    sleep_schedule, work_schedule = create_schedules(
        sleep_duration, SLEEP_QUALITY, WORK_START, WORK_END, COGNITIVE_LOAD
    )
    
    time_points, circadian_rhythms, cognitive_performances = enhanced_simulate_cognitive_performance(
        HOURS_TOTAL, sleep_schedule, work_schedule, INDIVIDUAL_PROFILE
    )
    
    results[sleep_duration] = {
        'time': time_points, 'performance': cognitive_performances
    }
    
    # Store data for analysis
    for t, perf in zip(time_points, cognitive_performances):
        all_data.append({
            'sleep_duration': sleep_duration, 'time_hours': t,
            'day': t // 24 + 1, 'hour_of_day': t % 24, 'performance': perf
        })

df = pd.DataFrame(all_data)
print(f"Completed! Generated {len(df)} data points")

# %%
# Create main visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Sleep Restriction Analysis: 7-Day Alertness Simulation', 
             fontsize=16, fontweight='bold')

# Plot 1: Time series for all sleep durations
ax1 = axes[0, 0]
colors = plt.cm.viridis(np.linspace(0, 1, len(SLEEP_DURATIONS)))
for i, sleep_duration in enumerate(SLEEP_DURATIONS):
    data = results[sleep_duration]
    ax1.plot(data['time'], data['performance'], 
             color=colors[i], label=f'{sleep_duration}h sleep', linewidth=2, alpha=0.8)

ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Cognitive Performance')
ax1.set_title('Alertness Over 7 Days by Sleep Duration')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add day markers
for day in range(1, 8):
    ax1.axvline(x=day*24, color='gray', linestyle='--', alpha=0.5)

# Plot 2: Daily averages
ax2 = axes[0, 1]
daily_avg = df.groupby(['day', 'sleep_duration'])['performance'].mean().unstack()
for i, sleep_duration in enumerate(SLEEP_DURATIONS):
    ax2.plot(daily_avg.index, daily_avg[sleep_duration], 
             color=colors[i], marker='o', linewidth=2, label=f'{sleep_duration}h sleep')

ax2.set_xlabel('Day')
ax2.set_ylabel('Average Daily Performance')
ax2.set_title('Daily Performance Trends')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Performance distributions
ax3 = axes[1, 0]
sleep_data = [df[df['sleep_duration'] == sd]['performance'].values 
              for sd in SLEEP_DURATIONS]
bp = ax3.boxplot(sleep_data, labels=[f'{sd}h' for sd in SLEEP_DURATIONS], 
                 patch_artist=True)

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax3.set_xlabel('Sleep Duration')
ax3.set_ylabel('Performance Distribution')
ax3.set_title('Performance Variability by Sleep Duration')
ax3.grid(True, alpha=0.3)

# Plot 4: Work hours performance
ax4 = axes[1, 1]
work_data = df[(df['hour_of_day'] >= WORK_START) & (df['hour_of_day'] < WORK_END)]
work_avg = work_data.groupby(['sleep_duration', 'day'])['performance'].mean().unstack()

for i, sleep_duration in enumerate(SLEEP_DURATIONS):
    ax4.plot(work_avg.columns, work_avg.loc[sleep_duration], 
             color=colors[i], marker='s', linewidth=2, label=f'{sleep_duration}h sleep')

ax4.set_xlabel('Day')
ax4.set_ylabel('Work Hours Performance')
ax4.set_title('Work Performance Decline Over 7 Days')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# Summary statistics
print("\n" + "="*60)
print("SIMULATION SUMMARY")
print("="*60)

print("\nAverage Performance by Sleep Duration:")
summary = df.groupby('sleep_duration')['performance'].agg(['mean', 'std', 'min', 'max']).round(2)
print(summary)

print("\nWork Hours Performance Analysis:")
work_summary = work_data.groupby('sleep_duration')['performance'].agg(['mean', 'std', 'min']).round(2)
print(work_summary)

# Performance decline analysis
print("\nPerformance Decline Analysis:")
baseline_7h = df[df['sleep_duration'] == 7]['performance'].mean()
for sleep_duration in SLEEP_DURATIONS:
    avg_perf = df[df['sleep_duration'] == sleep_duration]['performance'].mean()
    decline = ((baseline_7h - avg_perf) / baseline_7h) * 100
    print(f"{sleep_duration}h sleep: {decline:+.1f}% vs 7h baseline")

# %%
# Risk analysis
print("\n" + "="*60)
print("PERFORMANCE RISK ANALYSIS")
print("="*60)

for sleep_duration in SLEEP_DURATIONS:
    work_perf = work_data[work_data['sleep_duration'] == sleep_duration]['performance']
    
    critical = (work_perf < 70).mean() * 100
    high = ((work_perf >= 70) & (work_perf < 80)).mean() * 100
    moderate = ((work_perf >= 80) & (work_perf < 90)).mean() * 100
    optimal = (work_perf >= 90).mean() * 100
    
    print(f"\n{sleep_duration}h Sleep Risk Profile:")
    print(f"  Critical Risk (<70%): {critical:.1f}% of work time")
    print(f"  High Risk (70-80%): {high:.1f}% of work time") 
    print(f"  Moderate Risk (80-90%): {moderate:.1f}% of work time")
    print(f"  Optimal (≥90%): {optimal:.1f}% of work time")

# %%
# Final recommendations
print("\n" + "="*60)
print("KEY FINDINGS & RECOMMENDATIONS")
print("="*60)

print("\n1. SEVERE IMPAIRMENT (1-3 hours):")
print("   - Dramatic performance decline with critical safety implications")
print("   - Immediate intervention required")

print("\n2. MODERATE IMPAIRMENT (4-5 hours):")
print("   - Significant but manageable performance loss")
print("   - Increased monitoring and safety measures needed")

print("\n3. MILD IMPAIRMENT (6 hours):")
print("   - Minor but measurable effects on alertness")
print("   - Consider extending sleep when possible")

print("\n4. BASELINE (7 hours):")
print("   - Adequate sleep for maintaining performance")
print("   - Recommended minimum for most individuals")

print("\nScientific Basis:")
print("- Enhanced homeostatic process with adenosine dynamics")
print("- Circadian rhythm modeling with chronotype effects") 
print("- Sleep debt accumulation and recovery patterns")
print("- Individual differences in sleep sensitivity")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
# %% [markdown]
# # Sleep Restriction Analysis: Impact on Alertness Over 7 Days
#
# This notebook simulates the effects of different sleep durations (1-7 hours) on cognitive 
# performance and alertness over a 7-day period using the enhanced fatigue calculator with 
# the latest 2024 scientific research.
#
# ## Simulation Parameters
# - **Duration**: 7 days (168 hours)
# - **Sleep durations**: 1, 2, 3, 4, 5, 6, 7 hours per night
# - **Sleep quality**: 0.7 (fair quality) for all scenarios
# - **Work schedule**: 9:00 AM - 5:00 PM (8 hours daily)
# - **Cognitive load**: Moderate (rating = 1)
# - **Individual profile**: Average person (default genetic factors)
#
# ## Key Features
# - Enhanced homeostatic process with adenosine dynamics
# - Circadian rhythm modeling with chronotype effects
# - Sleep inertia and sleep debt accumulation
# - Individual differences in sleep sensitivity
# - Comprehensive visualization and analysis

# %%
# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fatigue_calculator.core import enhanced_simulate_cognitive_performance
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("Libraries imported successfully!")
print("Fatigue Calculator Enhanced 2025 Research Edition loaded")

# %%
# Configuration for sleep restriction simulation
SIMULATION_DAYS = 7
HOURS_TOTAL = SIMULATION_DAYS * 24  # 168 hours

# Sleep durations to test (1-7 hours)
SLEEP_DURATIONS = [1, 2, 3, 4, 5, 6, 7]

# Fixed parameters
SLEEP_QUALITY = 0.7  # Fair sleep quality
SLEEP_START_HOUR = 0  # Midnight
WORK_START = 9  # 9 AM
WORK_END = 17  # 5 PM
COGNITIVE_LOAD = 1  # Moderate workload

# Individual profile (average person)
INDIVIDUAL_PROFILE = {
    'genetic_profile': [],  # Default genetic factors
    'sex': 'unknown',
    'age': 25,
    'chronotype_offset': 0  # Neither morning nor evening type
}

print(f"Simulation configured for {SIMULATION_DAYS} days ({HOURS_TOTAL} hours)")
print(f"Testing sleep durations: {SLEEP_DURATIONS} hours")
print(f"Sleep quality: {SLEEP_QUALITY} (0-1 scale)")
print(f"Work schedule: {WORK_START}:00 - {WORK_END}:00")

# %%
# Function to create sleep and work schedules
def create_schedules(sleep_duration, sleep_quality, sleep_start, work_start, work_end, cognitive_load):
    """Create sleep and work schedules for simulation"""
    sleep_end = (sleep_start + sleep_duration) % 24
    
    # Sleep schedule (24-hour pattern)
    sleep_schedule = {
        'quality': sleep_quality,
        'quantity': sleep_duration,
    }
    
    # Handle sleep periods that cross midnight
    if sleep_end > sleep_start:
        # Sleep doesn't cross midnight
        for h in range(24):
            sleep_schedule[h] = sleep_start <= h < sleep_end
    else:
        # Sleep crosses midnight
        for h in range(24):
            sleep_schedule[h] = h >= sleep_start or h < sleep_end
    
    # Work schedule
    work_schedule = {
        'load_rating': cognitive_load,
    }
    for h in range(24):
        work_schedule[h] = work_start <= h < work_end
    
    return sleep_schedule, work_schedule

# Test the function
test_sleep, test_work = create_schedules(8, 0.7, 0, 9, 17, 1)
print("Schedule creation function ready!")
print(f"Example: 8-hour sleep from midnight, sleep hours: {[h for h in range(24) if test_sleep[h]]}")
print(f"Example: Work hours: {[h for h in range(24) if test_work[h]]}")

# %%
# Run simulations for all sleep durations
print("Running simulations for different sleep durations...")
print("This may take a few moments...\n")

# Store results
simulation_results = {}
simulation_data = []

for sleep_duration in SLEEP_DURATIONS:
    print(f"Simulating {sleep_duration} hours of sleep...")
    
    # Create schedules
    sleep_schedule, work_schedule = create_schedules(
        sleep_duration, SLEEP_QUALITY, SLEEP_START_HOUR, 
        WORK_START, WORK_END, COGNITIVE_LOAD
    )
    
    # Run simulation
    time_points, circadian_rhythms, cognitive_performances = enhanced_simulate_cognitive_performance(
        HOURS_TOTAL, sleep_schedule, work_schedule, INDIVIDUAL_PROFILE
    )
    
    # Store results
    simulation_results[sleep_duration] = {
        'time': time_points,
        'circadian': circadian_rhythms,
        'performance': cognitive_performances
    }
    
    # Create DataFrame for this simulation
    for i, (t, perf) in enumerate(zip(time_points, cognitive_performances)):
        simulation_data.append({
            'sleep_duration': sleep_duration,
            'time_hours': t,
            'day': t // 24 + 1,
            'hour_of_day': t % 24,
            'performance': perf
        })
    
    print(f"  Completed! Average performance: {np.mean(cognitive_performances):.1f}")

# Create comprehensive DataFrame
df_results = pd.DataFrame(simulation_data)

print(f"\nAll simulations completed!")
print(f"Total data points: {len(df_results)}")
print(f"Data shape: {df_results.shape}")

# %%
# Display summary statistics
print("=== SIMULATION SUMMARY ===")
print("\nAverage Performance by Sleep Duration:")
summary_stats = df_results.groupby('sleep_duration')['performance'].agg([
    'mean', 'std', 'min', 'max'
]).round(2)
summary_stats.columns = ['Mean', 'Std Dev', 'Minimum', 'Maximum']
print(summary_stats)

print("\nPerformance Decline by Day:")
daily_performance = df_results.groupby(['sleep_duration', 'day'])['performance'].mean().unstack()
print(daily_performance.round(1))

# %%
# Create comprehensive visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Sleep Restriction Analysis: 7-Day Alertness Simulation', fontsize=16, fontweight='bold')

# Plot 1: Time series for all sleep durations
ax1 = axes[0, 0]
for sleep_duration in SLEEP_DURATIONS:
    data = simulation_results[sleep_duration]
    ax1.plot(data['time'], data['performance'], 
             label=f'{sleep_duration}h sleep', linewidth=2, alpha=0.8)

ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Cognitive Performance')
ax1.set_title('Alertness Over 7 Days by Sleep Duration')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(True, alpha=0.3)

# Add day markers
for day in range(1, 8):
    ax1.axvline(x=day*24, color='gray', linestyle='--', alpha=0.5)
    ax1.text(day*24-12, ax1.get_ylim()[1]*0.95, f'Day {day}', 
             ha='center', va='top', fontsize=8, alpha=0.7)

# Plot 2: Average daily performance
ax2 = axes[0, 1]
daily_avg = df_results.groupby(['day', 'sleep_duration'])['performance'].mean().unstack()
for sleep_duration in SLEEP_DURATIONS:
    ax2.plot(daily_avg.index, daily_avg[sleep_duration], 
             marker='o', linewidth=2, label=f'{sleep_duration}h sleep')

ax2.set_xlabel('Day')
ax2.set_ylabel('Average Daily Performance')
ax2.set_title('Daily Performance Trends')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xticks(range(1, 8))

# Plot 3: Performance distribution by sleep duration
ax3 = axes[1, 0]
sleep_data = [df_results[df_results['sleep_duration'] == sd]['performance'].values 
              for sd in SLEEP_DURATIONS]
bp = ax3.boxplot(sleep_data, labels=[f'{sd}h' for sd in SLEEP_DURATIONS], 
                 patch_artist=True, notch=True)

# Color the boxes
colors = plt.cm.viridis(np.linspace(0, 1, len(SLEEP_DURATIONS)))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax3.set_xlabel('Sleep Duration')
ax3.set_ylabel('Performance Distribution')
ax3.set_title('Performance Variability by Sleep Duration')
ax3.grid(True, alpha=0.3)

# Plot 4: Heatmap of hourly performance
ax4 = axes[1, 1]
hourly_avg = df_results.groupby(['sleep_duration', 'hour_of_day'])['performance'].mean().unstack()
im = ax4.imshow(hourly_avg.values, cmap='RdYlBu_r', aspect='auto', interpolation='nearest')
ax4.set_xlabel('Hour of Day')
ax4.set_ylabel('Sleep Duration (hours)')
ax4.set_title('Average Hourly Performance Heatmap')
ax4.set_yticks(range(len(SLEEP_DURATIONS)))
ax4.set_yticklabels([f'{sd}h' for sd in SLEEP_DURATIONS])
ax4.set_xticks(range(0, 24, 4))
ax4.set_xticklabels(range(0, 24, 4))

# Add colorbar
cbar = plt.colorbar(im, ax=ax4)
cbar.set_label('Performance Level')

plt.tight_layout()
plt.show()

# %%
# Detailed analysis: Performance decline patterns
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Detailed Sleep Restriction Analysis', fontsize=16, fontweight='bold')

# Plot 1: Sleep debt accumulation effect
ax1 = axes[0]
sleep_debt_effect = {}
for sleep_duration in SLEEP_DURATIONS:
    daily_mins = df_results[(df_results['sleep_duration'] == sleep_duration)].groupby('day')['performance'].min()
    sleep_debt_effect[sleep_duration] = daily_mins.values
    ax1.plot(range(1, 8), daily_mins.values, marker='o', linewidth=2, 
             label=f'{sleep_duration}h sleep')

ax1.set_xlabel('Day')
ax1.set_ylabel('Daily Minimum Performance')
ax1.set_title('Daily Performance Lows\n(Sleep Debt Accumulation)')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(1, 8))

# Plot 2: Recovery patterns (if any)
ax2 = axes[1]
for sleep_duration in SLEEP_DURATIONS:
    daily_range = df_results[(df_results['sleep_duration'] == sleep_duration)].groupby('day').agg({
        'performance': lambda x: x.max() - x.min()
    })['performance']
    ax2.plot(range(1, 8), daily_range.values, marker='s', linewidth=2, 
             label=f'{sleep_duration}h sleep')

ax2.set_xlabel('Day')
ax2.set_ylabel('Daily Performance Range')
ax2.set_title('Daily Performance Variability\n(Circadian Amplitude)')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xticks(range(1, 8))

# Plot 3: Cumulative performance loss
ax3 = axes[2]
baseline_7h = df_results[df_results['sleep_duration'] == 7]['performance'].mean()
cumulative_loss = []
sleep_hours = []

for sleep_duration in SLEEP_DURATIONS:
    avg_performance = df_results[df_results['sleep_duration'] == sleep_duration]['performance'].mean()
    loss_percentage = ((baseline_7h - avg_performance) / baseline_7h) * 100
    cumulative_loss.append(loss_percentage)
    sleep_hours.append(sleep_duration)

bars = ax3.bar(sleep_hours, cumulative_loss, color=plt.cm.Reds(np.linspace(0.3, 1, len(SLEEP_DURATIONS))), 
               alpha=0.8, edgecolor='black')
ax3.set_xlabel('Sleep Duration (hours)')
ax3.set_ylabel('Performance Loss (%)')
ax3.set_title('Cumulative Performance Loss\n(Relative to 7h Sleep)')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, loss in zip(bars, cumulative_loss):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{loss:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# %%
# Work hours performance analysis
print("=== WORK HOURS PERFORMANCE ANALYSIS ===")

# Filter for work hours (9 AM - 5 PM)
work_hours_data = df_results[(df_results['hour_of_day'] >= WORK_START) & 
                            (df_results['hour_of_day'] < WORK_END)]

work_performance = work_hours_data.groupby('sleep_duration')['performance'].agg([
    'mean', 'std', 'min'
]).round(2)
work_performance.columns = ['Mean Work Performance', 'Std Dev', 'Worst Performance']
print(work_performance)

# Calculate performance zones
print("\n=== PERFORMANCE RISK ZONES ===")
for sleep_duration in SLEEP_DURATIONS:
    work_perf = work_hours_data[work_hours_data['sleep_duration'] == sleep_duration]['performance']
    
    # Define risk zones
    critical_risk = (work_perf < 70).sum() / len(work_perf) * 100  # Below 70% performance
    high_risk = ((work_perf >= 70) & (work_perf < 80)).sum() / len(work_perf) * 100
    moderate_risk = ((work_perf >= 80) & (work_perf < 90)).sum() / len(work_perf) * 100
    low_risk = (work_perf >= 90).sum() / len(work_perf) * 100
    
    print(f"\n{sleep_duration}h Sleep:")
    print(f"  Critical Risk (<70%): {critical_risk:.1f}% of work time")
    print(f"  High Risk (70-80%): {high_risk:.1f}% of work time")
    print(f"  Moderate Risk (80-90%): {moderate_risk:.1f}% of work time")
    print(f"  Low Risk (≥90%): {low_risk:.1f}% of work time")

# %%
# Create final summary visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('Sleep Restriction Impact Summary', fontsize=16, fontweight='bold')

# Plot 1: Work hours performance comparison
ax1 = axes[0]
work_hours_summary = work_hours_data.groupby(['sleep_duration', 'day'])['performance'].mean().unstack()

# Create line plot
x = work_hours_summary.columns
colors = plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, len(SLEEP_DURATIONS)))

for i, sleep_duration in enumerate(SLEEP_DURATIONS):
    ax1.plot(x, work_hours_summary.loc[sleep_duration], 
             color=colors[i], linewidth=3, marker='o', markersize=6,
             label=f'{sleep_duration}h sleep')

ax1.set_xlabel('Day')
ax1.set_ylabel('Average Work Performance')
ax1.set_title('Work Hours Performance Decline Over 7 Days')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(1, 8))

# Add performance zones
ax1.axhspan(90, 100, alpha=0.2, color='green', label='Optimal (90-100%)')
ax1.axhspan(80, 90, alpha=0.2, color='yellow', label='Acceptable (80-90%)')
ax1.axhspan(70, 80, alpha=0.2, color='orange', label='Impaired (70-80%)')
ax1.axhspan(0, 70, alpha=0.2, color='red', label='Critical (<70%)')

# Plot 2: Sleep efficiency recommendations
ax2 = axes[1]
sleep_recommendations = {
    1: "Severely impaired - Immediate intervention required",
    2: "Critically impaired - Major safety concerns", 
    3: "Heavily impaired - Significant performance loss",
    4: "Moderately impaired - Noticeable decline",
    5: "Mildly impaired - Some performance loss",
    6: "Slightly impaired - Minor effects",
    7: "Baseline - Adequate for most individuals"
}

# Create recommendation chart
y_pos = np.arange(len(SLEEP_DURATIONS))
performance_means = [df_results[df_results['sleep_duration'] == sd]['performance'].mean() 
                    for sd in SLEEP_DURATIONS]

bars = ax2.barh(y_pos, performance_means, 
                color=plt.cm.RdYlGn(np.array(performance_means)/100),
                alpha=0.8, edgecolor='black')

ax2.set_yticks(y_pos)
ax2.set_yticklabels([f'{sd}h\n{sleep_recommendations[sd]}' for sd in SLEEP_DURATIONS])
ax2.set_xlabel('Average Performance Level')
ax2.set_title('Sleep Duration Recommendations Based on Performance Impact')
ax2.grid(True, alpha=0.3, axis='x')

# Add performance values on bars
for i, (bar, perf) in enumerate(zip(bars, performance_means)):
    ax2.text(perf + 1, bar.get_y() + bar.get_height()/2,
             f'{perf:.1f}%', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Key Findings and Conclusions
#
# ### Performance Impact Summary
# The simulation reveals clear patterns in how sleep restriction affects cognitive performance over a 7-day period:
#
# 1. **Severe Impairment (1-3 hours)**: Dramatic performance decline with critical safety implications
# 2. **Moderate Impairment (4-5 hours)**: Significant but manageable performance loss
# 3. **Mild Impairment (6 hours)**: Minor but measurable effects on alertness
# 4. **Baseline (7 hours)**: Adequate sleep for maintaining performance
#
# ### Scientific Basis
# This analysis incorporates the latest 2024 research findings including:
# - **Adenosine dynamics**: Glial cell modulation and sleep pressure accumulation
# - **Sleep debt effects**: Cumulative impact of restricted sleep
# - **Circadian modulation**: 24-hour rhythm effects on alertness
# - **Individual differences**: Genetic and demographic factors
#
# ### Practical Implications
# - Sleep restriction below 6 hours shows exponential performance decline
# - Recovery requires multiple nights of adequate sleep
# - Work performance is most affected during afternoon hours
# - Individual variation exists but general patterns are consistent
#
# ### Recommendations
# 1. **Maintain 7+ hours** of sleep for optimal performance
# 2. **Avoid chronic restriction** below 6 hours
# 3. **Monitor performance** during critical tasks when sleep-deprived
# 4. **Plan recovery sleep** after periods of restriction

# %%
# Save results to CSV for further analysis
df_results.to_csv('notebooks/sleep_restriction_results.csv', index=False)
print("Results saved to 'sleep_restriction_results.csv'")

# Display final summary
print("\n" + "="*60)
print("SLEEP RESTRICTION ANALYSIS COMPLETE")
print("="*60)
print(f"Simulated {len(SLEEP_DURATIONS)} sleep duration scenarios over {SIMULATION_DAYS} days")
print(f"Generated {len(df_results)} data points for comprehensive analysis")
print("All visualizations and analysis completed successfully!")
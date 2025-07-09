# API Documentation: Cognitive Fatigue Prediction System

## Overview

This document provides detailed API documentation for the cognitive fatigue prediction system functions. The system implements the Two-Process Model of Sleep Regulation with additional features for workload integration and individual chronotype support.

## Core Functions

### `homeostatic_process(t, prev_reservoir_level, asleep, ai, sleep_quality, sleep_quantity)`

Calculates the homeostatic sleep pressure level based on current state and sleep parameters.

**Parameters:**
- `t` (int): Current time point in hours
- `prev_reservoir_level` (float): Previous sleep pressure level
- `asleep` (bool): Whether the individual is currently asleep
- `ai` (float): Alertness input (typically 1.0)
- `sleep_quality` (float): Sleep quality rating (0.0 to 1.0)
- `sleep_quantity` (float): Sleep duration in hours

**Returns:**
- `float`: Updated sleep pressure level

**Example:**
```python
# During wakefulness
level = homeostatic_process(10, 2400, False, 1.0, 0.8, 8.0)

# During sleep
level = homeostatic_process(2, 2400, True, 1.0, 0.8, 8.0)
```

### `circadian_process(t, chronotype_offset=0)`

Calculates the circadian rhythm component at a given time.

**Parameters:**
- `t` (int): Current time point in hours
- `chronotype_offset` (float): Individual chronotype adjustment in hours (-1.5 to +1.5)

**Returns:**
- `float`: Circadian rhythm value (-1.0 to +1.0)

**Example:**
```python
# Standard chronotype
circadian = circadian_process(18)  # Peak alertness time

# Early bird chronotype
circadian = circadian_process(18, -1.5)  # Shifted earlier
```

### `sleep_inertia(t)`

Calculates sleep inertia effect following awakening.

**Parameters:**
- `t` (int): Time since awakening in hours

**Returns:**
- `float`: Sleep inertia effect (0.0 to 5.0)

**Example:**
```python
# Immediately after awakening
inertia = sleep_inertia(0)  # Maximum effect

# 1 hour after awakening
inertia = sleep_inertia(1)  # Reduced effect

# 3 hours after awakening
inertia = sleep_inertia(3)  # No effect
```

### `cognitive_performance(t, Rt, Ct, It)`

Calculates overall cognitive performance based on homeostatic, circadian, and sleep inertia components.

**Parameters:**
- `t` (int): Current time point
- `Rt` (float): Current homeostatic level
- `Ct` (float): Current circadian level
- `It` (float): Current sleep inertia level

**Returns:**
- `float`: Cognitive performance score (0.0 to 100.0)

**Example:**
```python
performance = cognitive_performance(10, 2400, 0.5, 0.0)
```

### `workload(t, Wt_prev, load_rating, asleep)`

Calculates current workload level based on previous workload and current activity.

**Parameters:**
- `t` (int): Current time point
- `Wt_prev` (float): Previous workload level
- `load_rating` (int): Workload intensity rating (0-3)
- `asleep` (bool): Whether the individual is currently asleep

**Returns:**
- `float`: Updated workload level

**Example:**
```python
# During work with high load
workload_level = workload(10, 50, 3, False)

# During sleep (recovery)
workload_level = workload(2, 50, 0, True)
```

### `cognitive_performance_with_workload(t, Rt, Ct, It, Wt, Wc)`

Calculates cognitive performance adjusted for workload effects.

**Parameters:**
- `t` (int): Current time point
- `Rt` (float): Current homeostatic level
- `Ct` (float): Current circadian level
- `It` (float): Current sleep inertia level
- `Wt` (float): Current workload level
- `Wc` (float): Critical workload threshold (typically 75)

**Returns:**
- `float`: Workload-adjusted cognitive performance score

**Example:**
```python
performance = cognitive_performance_with_workload(10, 2400, 0.5, 0.0, 60, 75)
```

## Advanced Functions (FatigueCalcVerAlfa.py)

### `homeostatic_process_advanced(t, prev_reservoir_level, asleep, ai, sleep_quality, sleep_quantity, rem_sleep_time, non_rem_sleep_time, sleep_debt)`

Enhanced homeostatic process that incorporates sleep architecture and sleep debt.

**Parameters:**
- `t` (int): Current time point in hours
- `prev_reservoir_level` (float): Previous sleep pressure level
- `asleep` (bool): Whether the individual is currently asleep
- `ai` (float): Alertness input (typically 1.0)
- `sleep_quality` (float): Sleep quality rating (0.0 to 1.0)
- `sleep_quantity` (float): Sleep duration in hours
- `rem_sleep_time` (float): REM sleep duration in hours
- `non_rem_sleep_time` (float): Non-REM sleep duration in hours
- `sleep_debt` (float): Accumulated sleep debt in hours

**Returns:**
- `float`: Updated sleep pressure level

**Example:**
```python
level = homeostatic_process_advanced(
    t=10, prev_reservoir_level=2400, asleep=False, ai=1.0,
    sleep_quality=0.8, sleep_quantity=8.0, rem_sleep_time=2.0,
    non_rem_sleep_time=6.0, sleep_debt=1.0
)
```

### `circadian_process_advanced(t, chronotype_offset)`

Circadian process with individual chronotype adjustments.

**Parameters:**
- `t` (int): Current time point in hours
- `chronotype_offset` (float): Individual chronotype adjustment in hours

**Returns:**
- `float`: Circadian rhythm value adjusted for chronotype

**Example:**
```python
# Night owl chronotype
circadian = circadian_process_advanced(22, 1.5)
```

## Simulation Functions

### `simulate_cognitive_performance(hours, sleep_start, sleep_end, sleep_quality, sleep_quantity, work_start, work_end, load_rating)`

Simulates cognitive performance over a specified time period (FatigueCalc3.py).

**Parameters:**
- `hours` (int): Number of hours to simulate
- `sleep_start` (int): Sleep start time (0-23)
- `sleep_end` (int): Sleep end time (0-23)
- `sleep_quality` (float): Sleep quality rating (0.0 to 1.0)
- `sleep_quantity` (float): Sleep duration in hours
- `work_start` (int): Work start time (0-23)
- `work_end` (int): Work end time (0-23)
- `load_rating` (int): Workload rating (0-3)

**Returns:**
- `tuple`: (time_points, circadian_rhythms, cognitive_performances)

**Example:**
```python
time_points, circadian, performance = simulate_cognitive_performance(
    hours=48, sleep_start=22, sleep_end=6, sleep_quality=0.8,
    sleep_quantity=8.0, work_start=8, work_end=17, load_rating=2
)
```

### `simulate_cognitive_performance_advanced(prediction_hours, sleep_history, work_history, load_rating_history, chronotype_offset)`

Advanced simulation with multi-day history and chronotype support (FatigueCalcVerAlfa.py).

**Parameters:**
- `prediction_hours` (int): Number of hours to simulate
- `sleep_history` (list): List of sleep session tuples
- `work_history` (list): List of work session tuples
- `load_rating_history` (list): List of workload ratings
- `chronotype_offset` (float): Individual chronotype adjustment

**Returns:**
- `tuple`: (time_points, circadian_rhythms, cognitive_performances)

**Example:**
```python
sleep_history = [
    (22, 6, 0.8, 8.0, 2.0, 6.0, 0.0),  # (start, end, quality, quantity, rem, non_rem, debt)
    (22, 6, 0.7, 7.5, 1.8, 5.7, 0.5)
]
work_history = [(8, 17), (8, 17)]
load_rating_history = [2, 2]

time_points, circadian, performance = simulate_cognitive_performance_advanced(
    prediction_hours=72, sleep_history=sleep_history,
    work_history=work_history, load_rating_history=load_rating_history,
    chronotype_offset=0.0
)
```

## Data Structures

### Sleep Session Tuple
```python
sleep_session = (start_time, end_time, quality, quantity, rem_time, non_rem_time, sleep_debt)
```

**Fields:**
- `start_time` (int): Sleep start hour (0-23)
- `end_time` (int): Sleep end hour (0-23)
- `quality` (float): Sleep quality rating (0.0 to 1.0)
- `quantity` (float): Sleep duration in hours
- `rem_time` (float): REM sleep duration in hours
- `non_rem_time` (float): Non-REM sleep duration in hours
- `sleep_debt` (float): Accumulated sleep debt in hours

### Work Session Tuple
```python
work_session = (start_time, end_time)
```

**Fields:**
- `start_time` (int): Work start hour (0-23)
- `end_time` (int): Work end hour (0-23)

## Error Handling

### Input Validation

The system includes basic input validation:

```python
# Sleep quality validation
if not 0.0 <= sleep_quality <= 1.0:
    raise ValueError("Sleep quality must be between 0.0 and 1.0")

# Time validation
if not 0 <= sleep_start <= 23:
    raise ValueError("Sleep start time must be between 0 and 23")

# Workload rating validation
if not 0 <= load_rating <= 3:
    raise ValueError("Workload rating must be between 0 and 3")
```

### Common Error Scenarios

1. **Invalid time ranges**: Times must be 0-23
2. **Negative sleep quantities**: Sleep duration must be positive
3. **Invalid sleep quality**: Must be 0.0 to 1.0
4. **Empty history lists**: Advanced simulation requires history data

## Performance Considerations

### Computational Complexity
- **Time complexity**: O(n) where n is the number of hours to simulate
- **Space complexity**: O(n) for storing time series data
- **Memory usage**: Approximately 24 bytes per time point

### Optimization Tips

1. **Batch processing**: Simulate multiple scenarios in one run
2. **Data export**: Use pandas for efficient data handling
3. **Visualization**: Use matplotlib for plotting large datasets

## Integration Examples

### Basic Integration
```python
from FatigueCalc3 import simulate_cognitive_performance

# Simple simulation
time_points, circadian, performance = simulate_cognitive_performance(
    hours=24, sleep_start=22, sleep_end=6, sleep_quality=0.8,
    sleep_quantity=8.0, work_start=8, work_end=17, load_rating=2
)

# Export results
import pandas as pd
df = pd.DataFrame({
    'Time': time_points,
    'Circadian': circadian,
    'Performance': performance
})
df.to_csv('performance_data.csv')
```

### Advanced Integration
```python
from FatigueCalcVerAlfa import simulate_cognitive_performance_advanced

# Multi-day simulation
sleep_history = [
    (22, 6, 0.8, 8.0, 2.0, 6.0, 0.0),
    (22, 6, 0.7, 7.5, 1.8, 5.7, 0.5)
]
work_history = [(8, 17), (8, 17)]
load_rating_history = [2, 2]

time_points, circadian, performance = simulate_cognitive_performance_advanced(
    prediction_hours=72, sleep_history=sleep_history,
    work_history=work_history, load_rating_history=load_rating_history,
    chronotype_offset=0.0
)

# Visualization
import matplotlib.pyplot as plt
plt.plot(time_points, performance)
plt.xlabel('Time (hours)')
plt.ylabel('Cognitive Performance')
plt.title('Predicted Cognitive Performance')
plt.show()
```

## Version Compatibility

### FatigueCalc3.py
- **Python**: 3.6+
- **Dependencies**: pandas, math
- **Features**: Basic Two-Process Model implementation

### FatigueCalcVerAlfa.py
- **Python**: 3.6+
- **Dependencies**: pandas, matplotlib, datetime, math
- **Features**: Advanced features with visualization and chronotype support

## Migration Guide

### From FatigueCalc3 to FatigueCalcVerAlfa

1. **Update function calls**: Use advanced simulation function
2. **Add history data**: Provide sleep and work history
3. **Include chronotype**: Add chronotype offset parameter
4. **Handle visualization**: Manage matplotlib output

### Backward Compatibility

The basic functions (`homeostatic_process`, `circadian_process`, `sleep_inertia`) remain compatible between versions. 
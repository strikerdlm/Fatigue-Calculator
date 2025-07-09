# Technical Documentation: Cognitive Fatigue Prediction System

## Scientific Background

### Two-Process Model of Sleep Regulation

The cognitive fatigue prediction system is based on the Two-Process Model of Sleep Regulation, first proposed by Borbély (1982). This model describes sleep regulation through two independent but interacting processes:

#### Process S: Homeostatic Process
The homeostatic process represents the accumulation and dissipation of sleep pressure. During wakefulness, sleep pressure (S) increases exponentially, while during sleep, it decreases according to a recovery function.

**Mathematical Formulation:**
```
S(t) = S(t-1) - K * t  (during wakefulness)
S(t) = S0 + (S(t-1) - S0) * exp(-t/τ)  (during sleep)
```

Where:
- `K`: Sleep pressure accumulation rate
- `S0`: Asymptotic level of sleep pressure
- `τ`: Recovery time constant

#### Process C: Circadian Process
The circadian process represents the endogenous circadian rhythm that modulates alertness and performance throughout the day.

**Mathematical Formulation:**
```
C(t) = cos(2π(t - p)/24) + β * cos(4π(t - p')/24)
```

Where:
- `p`: Primary peak time (typically 18:00)
- `p'`: Secondary peak time (typically 03:00)
- `β`: Amplitude of secondary oscillation

### Sleep Inertia
Sleep inertia represents the temporary impairment in cognitive performance immediately following awakening.

**Mathematical Formulation:**
```
I(t) = Imax * exp(-t/i)  (for t < 2 hours after awakening)
I(t) = 0  (for t ≥ 2 hours)
```

Where:
- `Imax`: Maximum sleep inertia effect (5)
- `i`: Sleep inertia time constant (0.04)

## Implementation Details

### Core Functions

#### `homeostatic_process()`
```python
def homeostatic_process(t, prev_reservoir_level, asleep, ai, sleep_quality, sleep_quantity):
```

**Parameters:**
- `t`: Current time point
- `prev_reservoir_level`: Previous sleep pressure level
- `asleep`: Boolean indicating sleep state
- `ai`: Alertness input (typically 1)
- `sleep_quality`: Sleep quality rating (0-1)
- `sleep_quantity`: Sleep duration in hours

**Implementation Logic:**
1. **Wakefulness**: Sleep pressure decreases linearly with time
2. **Sleep**: Sleep pressure recovers exponentially based on sleep quality
3. **Sleep quantity adjustment**: K_adjusted accounts for sleep deprivation effects

#### `circadian_process()`
```python
def circadian_process(t, chronotype_offset=0):
```

**Parameters:**
- `t`: Current time point
- `chronotype_offset`: Individual chronotype adjustment (-1.5 to +1.5 hours)

**Implementation Logic:**
1. Primary circadian oscillation with 24-hour period
2. Secondary oscillation with 12-hour period
3. Chronotype adjustment shifts peak times

#### `sleep_inertia()`
```python
def sleep_inertia(t):
```

**Implementation Logic:**
1. Exponential decay function for first 2 hours after awakening
2. Zero effect after 2 hours
3. Maximum effect of 5 performance units

#### `cognitive_performance()`
```python
def cognitive_performance(t, Rt, Ct, It):
```

**Parameters:**
- `Rt`: Current homeostatic level
- `Ct`: Current circadian level
- `It`: Current sleep inertia level

**Implementation Logic:**
1. Base performance from homeostatic level (0-100 scale)
2. Circadian modulation based on sleep pressure
3. Sleep inertia subtraction

### Advanced Features (FatigueCalcVerAlfa.py)

#### Sleep Architecture Modeling
The advanced version incorporates REM and non-REM sleep effects:

```python
sleep_recovery = (rem_sleep_time * rem_factor + non_rem_sleep_time * non_rem_factor) / sleep_quantity
```

Where:
- `rem_factor`: 0.6 (REM sleep recovery weight)
- `non_rem_factor`: 0.4 (non-REM sleep recovery weight)

#### Sleep Debt Tracking
```python
sleep_debt_factor = max(0, sleep_debt - 2) / 6
```

Sleep debt increases homeostatic pressure during wakefulness.

#### Workload Integration
```python
def workload(t, Wt_prev, load_rating, asleep):
    if asleep:
        return Wt_prev + Wr  # Recovery during sleep
    else:
        return Wt_prev - Wd * (1 + load_rating)  # Accumulation during work
```

Where:
- `Wr`: Recovery rate (11)
- `Wd`: Depletion rate (1.14)

## Model Parameters

### Calibrated Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| K (homeostatic rate) | 0.5 | Sleep deprivation studies |
| as_factor | 0.235 | Asymptotic sleep pressure |
| tau1, tau2 | 1.0 | Recovery time constants |
| p (circadian peak) | 18 | Typical peak alertness |
| p' (secondary peak) | 3 | Secondary oscillation |
| β (circadian amplitude) | 0.5 | Secondary oscillation strength |
| Imax (max inertia) | 5 | Performance studies |
| i (inertia constant) | 0.04 | Empirical observation |
| Sc (critical pressure) | 2880 | Performance calibration |
| a1, a2 (circadian params) | 7, 5 | Performance modulation |

### Chronotype Adjustments

| Chronotype | Offset (hours) | Description |
|------------|----------------|-------------|
| Early Bird | -1.5 | Morning type |
| Intermediate | 0.0 | Standard type |
| Night Owl | +1.5 | Evening type |

## Validation and Limitations

### Scientific Validation

#### Strengths
1. **Theoretical Foundation**: Based on well-established Two-Process Model
2. **Physiological Realism**: Incorporates known sleep mechanisms
3. **Individual Differences**: Accounts for chronotype variations
4. **Workload Effects**: Models mental workload impact

#### Limitations
1. **Population Averages**: Parameters based on group data
2. **Environmental Factors**: No external stressor modeling
3. **Acute Sleep Loss**: Limited validation for extreme deprivation
4. **Subjective Inputs**: Workload and sleep quality are subjective

### Model Assumptions

1. **Linear Sleep Pressure**: Homeostatic process assumes linear accumulation
2. **Exponential Recovery**: Sleep recovery follows exponential decay
3. **Additive Effects**: Sleep inertia and workload effects are additive
4. **Time Invariance**: Parameters remain constant over time

## Performance Metrics

### Output Interpretation

#### Performance Zones
- **Green (80-100)**: Optimal performance
- **Yellow (60-80)**: Moderate performance
- **Red (0-60)**: Poor performance

#### Baseline Performance
- Reference line at 77.5 represents baseline performance
- Values above/below indicate relative performance

### Data Export Format

The system exports time series data with:
- **Time of Day**: Hour of day (0-23)
- **Predicted Cognitive Performance**: Performance score (0-100)

## Future Enhancements

### Potential Improvements

1. **Individual Calibration**: Personalized parameter estimation
2. **Environmental Factors**: Temperature, noise, light effects
3. **Acute Stressors**: Caffeine, exercise, medication effects
4. **Machine Learning**: Data-driven parameter optimization
5. **Real-time Adaptation**: Continuous parameter adjustment

### Research Applications

1. **Shift Work Optimization**: Schedule design for shift workers
2. **Aviation Safety**: Pilot fatigue management
3. **Healthcare**: Medical staff scheduling
4. **Transportation**: Driver fatigue prevention
5. **Military Operations**: Operational readiness assessment

## Code Quality and Maintenance

### Code Structure
- **Modular Design**: Separate functions for each process
- **Parameter Centralization**: Easy parameter modification
- **Error Handling**: Input validation and error messages
- **Documentation**: Comprehensive inline comments

### Testing Recommendations

1. **Unit Tests**: Individual function testing
2. **Integration Tests**: End-to-end simulation testing
3. **Validation Tests**: Comparison with empirical data
4. **Performance Tests**: Computational efficiency testing

### Maintenance Guidelines

1. **Parameter Updates**: Document parameter changes
2. **Validation Studies**: Regular model validation
3. **Literature Review**: Stay current with sleep research
4. **User Feedback**: Incorporate user experience improvements

## References and Further Reading

### Primary Literature
1. Borbély, A. A. (1982). A two process model of sleep regulation. *Human Neurobiology*, 1(3), 195-204.
2. Achermann, P. (2004). The two-process model of sleep regulation revisited. *Aviation, Space, and Environmental Medicine*, 75(3), A37-A43.

### Implementation References
1. Van Dongen, H. P., & Dinges, D. F. (2003). Sleep, circadian rhythms, and psychomotor vigilance. *Clinics in Sports Medicine*, 22(2), 253-265.
2. Åkerstedt, T., & Folkard, S. (1997). The three-process model of alertness. *Chronobiology International*, 14(2), 115-123.

### Related Models
1. **Three-Process Model**: Extends Two-Process Model with sleep inertia
2. **Circadian Performance Model**: Focuses on circadian rhythm effects
3. **Fatigue Risk Index**: Operational fatigue assessment tool
4. **Sleep-Wake Predictor**: Real-time performance prediction

## Conclusion

This cognitive fatigue prediction system provides a scientifically-grounded approach to modeling human performance based on sleep-wake patterns. While the model has limitations, it offers valuable insights for applications in safety-critical environments and research settings. Continued development should focus on individual calibration and environmental factor integration. 
# Cognitive Fatigue Prediction System

## Overview

This project implements a scientifically-grounded cognitive fatigue prediction system based on the **Two-Process Model of Sleep Regulation** (Borbély, 1982). The system predicts cognitive performance over time by modeling the interaction between homeostatic sleep pressure (Process S) and circadian rhythmicity (Process C), incorporating workload effects and individual chronotype differences.

## Scientific Foundation

### Two-Process Model of Sleep Regulation

The system is built upon the Two-Process Model, which describes sleep regulation through two independent but interacting processes:

1. **Process S (Homeostatic Process)**: Represents sleep pressure that builds up during wakefulness and dissipates during sleep
2. **Process C (Circadian Process)**: Represents the endogenous circadian rhythm that modulates alertness and performance

### Mathematical Framework

The cognitive performance prediction integrates several physiological processes:

#### Homeostatic Process (S)
```
S(t) = S(t-1) - K_adjusted * t  (during wakefulness)
S(t) = as_factor + recovery_factor * S(t-1) + sleep_recovery  (during sleep)
```

Where:
- `K_adjusted`: Sleep pressure accumulation rate (adjusted for sleep quantity)
- `as_factor`: Asymptotic level of sleep pressure
- `recovery_factor`: Sleep quality-dependent recovery rate
- `sleep_recovery`: REM/non-REM sleep weighted recovery

#### Circadian Process (C)
```
C(t) = cos(2π(t - p)/24) + β * cos(4π(t - p')/24)
```

Where:
- `p`: Peak circadian time (typically 18:00)
- `p'`: Secondary peak time (typically 03:00)
- `β`: Amplitude of secondary oscillation (0.5)

#### Sleep Inertia (I)
```
I(t) = Imax * exp(-t/i)  (for t < 2 hours after awakening)
I(t) = 0  (for t ≥ 2 hours)
```

#### Cognitive Performance (E)
```
E(t) = 100 * (S(t)/Sc) + (a1 + a2 * (Sc - S(t))/Sc) * C(t) + I(t)
```

Where:
- `Sc`: Critical sleep pressure threshold (2880)
- `a1, a2`: Circadian amplitude parameters (7, 5)

## Features

### Core Functionality
- **Multi-day prediction**: Simulates cognitive performance for extended periods
- **Chronotype support**: Accounts for individual differences in circadian timing
- **Workload integration**: Models the impact of mental workload on performance
- **Sleep architecture**: Incorporates REM/non-REM sleep effects
- **Sleep debt tracking**: Accounts for accumulated sleep deprivation

### Advanced Features
- **Visualization**: Generates performance plots with color-coded performance zones
- **Data export**: Exports predictions to Excel format
- **Flexible scheduling**: Supports variable sleep and work schedules

## Files Description

### `FatigueCalc3.py`
Basic implementation of the Two-Process Model with:
- Simplified homeostatic process
- Basic circadian rhythm modeling
- Sleep inertia effects
- Workload integration
- 48-hour prediction capability

### `FatigueCalcVerAlfa.py`
Advanced implementation with enhanced features:
- Detailed sleep architecture modeling (REM/non-REM)
- Chronotype adjustments
- Sleep debt tracking
- Multi-day sleep history
- Performance visualization
- Flexible prediction duration

## Installation and Dependencies

### Requirements
```bash
pip install pandas matplotlib numpy
```

### Python Version
- Python 3.6 or higher recommended

## Usage

### Basic Usage (FatigueCalc3.py)
```bash
python FatigueCalc3.py
```

The program will prompt for:
- Sleep schedule (start/end times)
- Sleep quality (0-1 scale)
- Sleep quantity (hours)
- Work schedule (start/end times)
- Workload rating (0-3 scale)

### Advanced Usage (FatigueCalcVerAlfa.py)
```bash
python FatigueCalcVerAlfa.py
```

Additional inputs include:
- Prediction duration (hours)
- Chronotype selection (early bird/intermediate/night owl)
- Multi-day sleep history
- REM/non-REM sleep times
- Sleep debt information

## Output

### Data Files
- `cognitive_performance_data.xlsx`: Time series of predicted cognitive performance

### Visualization (FatigueCalcVerAlfa.py)
- Performance plot with color-coded zones:
  - Red (0-60): Poor performance
  - Yellow (60-80): Moderate performance
  - Green (80-100): Optimal performance
- Reference line at 77.5 (baseline performance)

## Scientific Validation

### Model Parameters
The model parameters are based on empirical sleep research:

- **Homeostatic decay rate (K)**: 0.5 (derived from sleep deprivation studies)
- **Circadian peak time (p)**: 18:00 (typical peak alertness)
- **Sleep inertia duration**: 2 hours (empirical observation)
- **Critical sleep pressure (Sc)**: 2880 (calibrated from performance studies)

### Limitations
1. **Individual variability**: Model parameters are population averages
2. **Environmental factors**: Does not account for external stressors
3. **Acute sleep deprivation**: Limited validation for extreme sleep loss
4. **Workload quantification**: Subjective workload ratings

## References

1. Borbély, A. A. (1982). A two process model of sleep regulation. *Human Neurobiology*, 1(3), 195-204.

2. Achermann, P. (2004). The two-process model of sleep regulation revisited. *Aviation, Space, and Environmental Medicine*, 75(3), A37-A43.

3. Van Dongen, H. P., & Dinges, D. F. (2003). Sleep, circadian rhythms, and psychomotor vigilance. *Clinics in Sports Medicine*, 22(2), 253-265.

4. Åkerstedt, T., & Folkard, S. (1997). The three-process model of alertness and its extension to performance, sleep latency, and sleep length. *Chronobiology International*, 14(2), 115-123.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Author

**Diego Malpica**
- Created: March 25, 2023
- Implementation of Two-Process Model for cognitive fatigue prediction

## Contributing

Contributions are welcome! Please ensure any modifications maintain scientific accuracy and include appropriate validation.

## Disclaimer

This software is for research and educational purposes. Predictions should not be used as the sole basis for safety-critical decisions. Always consult with qualified professionals for medical or safety-related applications. 
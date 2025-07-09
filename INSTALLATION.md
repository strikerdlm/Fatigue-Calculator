# Installation Guide: Cognitive Fatigue Prediction System

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.6 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 100MB free space

### Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

#### macOS
1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```bash
   brew install python
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Installation Steps

### 1. Clone or Download the Repository

#### Option A: Git Clone
```bash
git clone <repository-url>
cd cognitive-fatigue-prediction
```

#### Option B: Download ZIP
1. Download the project ZIP file
2. Extract to your desired directory
3. Open terminal/command prompt in the project directory

### 2. Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv fatigue_env
fatigue_env\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv fatigue_env
source fatigue_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas>=1.3.0
pip install matplotlib>=3.5.0
pip install numpy>=1.21.0
pip install openpyxl>=3.0.0
```

### 4. Verify Installation

```bash
python -c "import pandas, matplotlib, numpy; print('All dependencies installed successfully!')"
```

## Quick Start

### Basic Usage (FatigueCalc3.py)

1. **Run the basic version**:
   ```bash
   python FatigueCalc3.py
   ```

2. **Follow the prompts**:
   ```
   Enter sleep start time (0-23): 22
   Enter sleep end time (0-23): 6
   Enter sleep quality (0-1): 0.8
   Enter sleep quantity (in hours): 8.0
   Enter work start time (0-23): 8
   Enter work end time (0-23): 17
   Enter workload rating (0-3): 2
   ```

3. **Check results**:
   - Look for `cognitive_performance_data.xlsx` in the project directory
   - Open the Excel file to view the predicted performance data

### Advanced Usage (FatigueCalcVerAlfa.py)

1. **Run the advanced version**:
   ```bash
   python FatigueCalcVerAlfa.py
   ```

2. **Follow the detailed prompts**:
   ```
   Enter the number of hours you want the prediction for: 72
   
   Enter your chronotype:
   1: Early bird (morning type)
   2: Intermediate type
   3: Night owl (evening type)
   Your choice (1-3): 2
   
   Enter sleep data for the 1-th sleep session:
   Start time (0-23): 22
   End time (0-23): 6
   Sleep quality (0-1): 0.8
   Sleep quantity (0-12): 8.0
   REM sleep time (hours): 2.0
   Non-REM sleep time (hours): 6.0
   sleep debt (hours): 0.0
   
   Enter work data for the 1-th work session:
   Work start time (0-23): 8
   Work end time (0-23): 17
   
   Enter workload rating for the 1-th work session (0-1): 2
   ```

3. **View results**:
   - Performance plot will be displayed
   - Excel file will be created with detailed data

## Configuration

### Environment Variables (Optional)

Create a `.env` file for custom configurations:

```bash
# .env
DEFAULT_SLEEP_QUALITY=0.8
DEFAULT_WORKLOAD_RATING=2
DEFAULT_CHRONOTYPE=2
PREDICTION_HOURS=48
```

### Custom Parameters

You can modify the model parameters in the source files:

```python
# In FatigueCalc3.py or FatigueCalcVerAlfa.py
K = 0.5  # Homeostatic rate
as_factor = 0.235  # Asymptotic sleep pressure
Imax = 5  # Maximum sleep inertia
```

## Troubleshooting

### Common Issues

#### 1. Python Not Found
**Error**: `python: command not found`

**Solution**:
- Windows: Add Python to PATH or use `py` instead of `python`
- macOS/Linux: Use `python3` instead of `python`

#### 2. Module Not Found
**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
pip install pandas matplotlib numpy openpyxl
```

#### 3. Matplotlib Display Issues
**Error**: Plot not showing or display errors

**Solution**:
```bash
# For headless systems (Linux servers)
export DISPLAY=:0
# Or use non-interactive backend
python -c "import matplotlib; matplotlib.use('Agg')"
```

#### 4. Excel File Permission Error
**Error**: Cannot write to Excel file

**Solution**:
- Check file permissions
- Close any open Excel files
- Run as administrator (Windows)

### Performance Issues

#### Slow Execution
- Reduce prediction hours
- Use basic version (FatigueCalc3.py) for simple simulations
- Close other applications to free memory

#### Memory Issues
- Reduce prediction duration
- Use smaller time steps
- Restart Python environment

## Development Setup

### For Contributors

1. **Fork the repository**

2. **Set up development environment**:
   ```bash
   git clone <your-fork-url>
   cd cognitive-fatigue-prediction
   python -m venv dev_env
   source dev_env/bin/activate  # Linux/macOS
   # or
   dev_env\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Install development dependencies**:
   ```bash
   pip install pytest black flake8
   ```

4. **Run tests** (if available):
   ```bash
   pytest tests/
   ```

### Code Style

The project follows PEP 8 style guidelines:
```bash
black *.py
flake8 *.py
```

## Platform-Specific Instructions

### Windows

#### Using Anaconda
```bash
conda create -n fatigue python=3.8
conda activate fatigue
pip install -r requirements.txt
```

#### Using PowerShell
```powershell
python -m venv fatigue_env
.\fatigue_env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS

#### Using Homebrew
```bash
brew install python@3.8
python3 -m venv fatigue_env
source fatigue_env/bin/activate
pip install -r requirements.txt
```

#### Using Anaconda
```bash
conda create -n fatigue python=3.8
conda activate fatigue
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

#### System Packages
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 -m venv fatigue_env
source fatigue_env/bin/activate
pip install -r requirements.txt
```

#### Using Anaconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda create -n fatigue python=3.8
conda activate fatigue
pip install -r requirements.txt
```

## Docker Setup (Optional)

### Dockerfile
```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "FatigueCalc3.py"]
```

### Docker Commands
```bash
# Build image
docker build -t fatigue-prediction .

# Run container
docker run -it fatigue-prediction

# Run with volume mount
docker run -it -v $(pwd):/app fatigue-prediction
```

## Verification

### Test Installation

Run this Python script to verify all components:

```python
# test_installation.py
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def test_imports():
    print("✓ All required modules imported successfully")
    
def test_basic_functionality():
    # Test basic mathematical operations
    import math
    result = math.cos(2 * math.pi * 18 / 24)
    print(f"✓ Basic math operations: {result:.3f}")
    
def test_pandas():
    # Test pandas functionality
    df = pd.DataFrame({'test': [1, 2, 3]})
    print(f"✓ Pandas DataFrame created: {len(df)} rows")
    
def test_matplotlib():
    # Test matplotlib (non-interactive)
    plt.ioff()
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 2])
    plt.close()
    print("✓ Matplotlib plotting works")

if __name__ == "__main__":
    print("Testing Cognitive Fatigue Prediction System Installation...")
    test_imports()
    test_basic_functionality()
    test_pandas()
    test_matplotlib()
    print("\n🎉 Installation verified successfully!")
```

Run the test:
```bash
python test_installation.py
```

## Support

### Getting Help

1. **Check the documentation**: README.md, TECHNICAL_DOCUMENTATION.md
2. **Review error messages**: Most errors include helpful information
3. **Check system requirements**: Ensure Python 3.6+ and sufficient memory
4. **Verify dependencies**: Ensure all required packages are installed

### Common Questions

**Q: Can I use this on a server without display?**
A: Yes, use the non-interactive matplotlib backend or run without visualization.

**Q: How accurate are the predictions?**
A: The model is based on scientific literature but should not be used for medical decisions.

**Q: Can I modify the model parameters?**
A: Yes, edit the constants in the source files, but validate changes with scientific literature.

**Q: What's the difference between the two versions?**
A: FatigueCalc3.py is basic, FatigueCalcVerAlfa.py includes advanced features like chronotype support and visualization.

## License

This software is licensed under the GNU General Public License v3.0. See LICENSE file for details. 
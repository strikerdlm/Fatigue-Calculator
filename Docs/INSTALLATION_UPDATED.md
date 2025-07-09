# Updated Installation Guide - Enhanced Fatigue Calculator 2024

## Requirements Update Summary

The requirements.txt file has been updated to use **accurate, tested versions** based on official documentation and compatibility testing. This resolves the previous TensorFlow installation issues.

### What Changed

1. **TensorFlow Version Issue Fixed**
   - **Problem**: `tensorflow>=2.12.0` was not available or compatible
   - **Solution**: Made TensorFlow optional and specified accurate version `tensorflow>=2.15.0`

2. **NumPy Compatibility**
   - **Problem**: NumPy 2.x caused compatibility issues with existing packages
   - **Solution**: Specified `numpy>=1.21.0,<2.0.0` for broad compatibility

3. **Modular Installation**
   - **Core functionality**: Works without deep learning libraries
   - **Optional deep learning**: Separate installation for future CogPSGFormer features

## Installation Options

### Option 1: Core Functionality Only (Recommended)

```bash
pip install -r requirements.txt
```

This installs all dependencies needed for the enhanced fatigue calculator including:
- Latest scientific research enhancements (2020-2024)
- Adenosine dynamics and glial modulation
- Updated sleep inertia model
- Individual differences framework
- Enhanced visualization capabilities

### Option 2: With Deep Learning Support (Optional)

```bash
# First install core requirements
pip install -r requirements.txt

# Then install deep learning dependencies
pip install -r requirements-deeplearning.txt
```

This adds TensorFlow, PyTorch, and other deep learning libraries for future CogPSGFormer integration.

### Option 3: Individual Deep Learning Components

```bash
# Install core requirements first
pip install -r requirements.txt

# Then choose your preferred deep learning framework:

# For TensorFlow (recommended for CogPSGFormer)
pip install tensorflow>=2.15.0

# OR for PyTorch
pip install torch>=2.0.0 torchvision>=0.15.0

# For Transformers (Hugging Face)
pip install transformers>=4.30.0
```

## Compatibility Information

### Python Version Support
- **Required**: Python 3.8-3.11
- **Tested**: Python 3.11.11 on Windows 10/11
- **Recommended**: Python 3.11.x for best compatibility

### TensorFlow Support
- **Version**: TensorFlow 2.15.0+ (if using deep learning features)
- **Platforms**: Windows, macOS, Linux
- **Documentation**: [TensorFlow Installation Guide](https://www.tensorflow.org/install)

### System Requirements
- **RAM**: 8GB+ recommended (16GB+ for deep learning)
- **Storage**: 2GB for core, 10GB+ for deep learning dependencies
- **GPU**: Optional, supported for TensorFlow operations

## Verification

After installation, verify the enhanced calculator is working:

```python
from fatigue_calculator.core import enhanced_simulate_cognitive_performance, calculate_individual_factors

# Test basic functionality
print("✅ Enhanced fatigue calculator is working!")

# Test individual factors calculation
factors = calculate_individual_factors(['DEC2', 'PER3'], 'female', 25)
print(f"Individual factors test: {factors}")
```

Expected output:
```
✅ Enhanced fatigue calculator is working!
Individual factors test: (0.96, 1.2)
```

## New Features Available

With the updated requirements, you now have access to:

1. **Enhanced Scientific Models** (2020-2024 research)
   - Adenosine dynamics and glial modulation
   - Updated sleep inertia (15-60 min duration)
   - Ultradian rhythms integration
   - Individual differences framework

2. **Advanced Visualization**
   - Plotly interactive charts
   - Bokeh dashboards
   - Seaborn statistical plots

3. **Statistical Analysis**
   - Statsmodels for regression analysis
   - Pingouin for statistical testing
   - Enhanced model validation

4. **Development Tools**
   - Jupyter notebooks for interactive analysis
   - Pytest for comprehensive testing
   - Enhanced debugging capabilities

## Troubleshooting

### Common Issues

1. **TensorFlow Installation Error**
   - Solution: TensorFlow is now optional - skip it for core functionality
   - If needed: `pip install tensorflow>=2.15.0`

2. **NumPy Compatibility Warning**
   - Solution: We now use `numpy<2.0.0` for better compatibility
   - If issues persist: `pip install "numpy<2" --force-reinstall`

3. **Dependency Conflicts**
   - Solution: Use a fresh virtual environment
   - Command: `python -m venv fatigue_env && fatigue_env\\Scripts\\activate`

### Getting Help

- **Issues**: Check the GitHub issues page
- **Documentation**: See `Docs/2024_RESEARCH_ENHANCEMENTS.md`
- **Citation**: All enhancements include proper scientific citations

## Next Steps

1. **Run the Enhanced Calculator**: Use `scripts/FatigueCalcEnhanced2024.py`
2. **Explore New Features**: Check the 2024 research enhancements
3. **Validate Results**: Use the built-in validation framework
4. **Future Integration**: Consider deep learning features for CogPSGFormer

The enhanced fatigue calculator is now ready for use with the latest scientific research and proper dependency management! 
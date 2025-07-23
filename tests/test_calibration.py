import numpy as np
from fatigue_calculator.calibration import optimise_ml_enhancement


def test_optimise_ml_enhancement_identity():
    # Synthetic data where best factor should be exactly 1.0
    rng = np.random.default_rng(42)
    y_true = rng.uniform(50, 100, size=100)
    best_factor, rmse = optimise_ml_enhancement(y_true, y_true)
    assert abs(best_factor - 1.0) < 1e-3, "Calibration should return factor ~1.0 for perfect predictions"
    assert rmse == 0.0
"""Test various helper functions."""
import numpy as np

from pyprep.utils import (
    _mat_round, _mat_quantile, _mat_iqr, _get_random_subset, _correlate_arrays
)


def test_mat_round():
    """Test the MATLAB-compatible rounding function."""
    # Test normal rounding behaviour
    assert _mat_round(1.5) == 2
    assert _mat_round(0.4) == 0
    assert _mat_round(0.6) == 1

    # Test MATLAB-specific rounding behaviour
    assert _mat_round(0.5) == 1


def test_mat_quantile_iqr():
    """Test MATLAB-compatible quantile and IQR functions.

    MATLAB code used to generate the comparison results:

    .. code-block:: matlab

       % Generate test data
       rng(435656);
       tst = rand(100, 3);

       % Calculate IQR and 0.98 quantile for test data
       quantile(tst, 0.98);
       iqr(tst);

    """
    # Generate test data
    np.random.seed(435656)
    tst = np.transpose(np.random.rand(3, 100))

    # Create arrays containing MATLAB results
    quantile_expected = np.asarray([0.9710, 0.9876, 0.9802])
    iqr_expected = np.asarray([0.4776, 0.5144, 0.4851])

    # Test quantile equivalence with MATLAB
    quantile_actual = _mat_quantile(tst, 0.98, axis=0)
    assert all(np.isclose(quantile_expected, quantile_actual, atol=0.001))

    # Test IQR equivalence with MATLAB
    iqr_actual = _mat_iqr(tst, axis=0)
    assert all(np.isclose(iqr_expected, iqr_actual, atol=0.001))


def test_get_random_subset():
    """Test the function for getting random channel subsets."""
    # Generate test data
    rng = np.random.RandomState(435656)
    chans = range(1, 61)

    # Compare random subset equivalence with MATLAB
    expected_picks = [6, 47, 55, 31, 29, 44, 36, 15]
    actual_picks = _get_random_subset(chans, size=8, rand_state=rng)
    assert all(np.equal(expected_picks, actual_picks))


def test_correlate_arrays():
    """Test MATLAB PREP-compatible array correlation function.

    MATLAB code used to generate the comparison results:

    .. code-block:: matlab

       % Generate test data
       rng(435656);
       a = rand(100, 3) - 0.5;
       b = rand(100, 3) - 0.5;

       % Calculate correlations
       correlations = sum(a.*b)./(sqrt(sum(a.^2)).*sqrt(sum(b.^2)));

    """
    # Generate test data
    np.random.seed(435656)
    a = np.random.rand(3, 100) - 0.5
    b = np.random.rand(3, 100) - 0.5

    # Test regular Pearson correlation
    corr_expected = np.asarray([-0.0898, 0.0340, -0.1068])
    corr_actual = _correlate_arrays(a, b)
    assert all(np.isclose(corr_expected, corr_actual, atol=0.001))

    # Test correlation equivalence with MATLAB PREP
    corr_expected = np.asarray([-0.0898, 0.0327, -0.1140])
    corr_actual = _correlate_arrays(a, b, matlab_strict=True)
    assert all(np.isclose(corr_expected, corr_actual, atol=0.001))

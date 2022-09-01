import numpy as np


def assert_almost_equal(a, b, rtol=1e-5, atol=1e-5):
    np.testing.assert_allclose(a, b, rtol=rtol, atol=atol)

import numpy as np
from glidergun._grid import grid


def test_grid_reclass():
    g = grid(np.array([[1, 2], [3, 4]]))
    result = g.reclass((1, 2, 10), (2, 3, 20), (3, 4, 30))
    expected = grid(np.array([[10, 20], [30, np.nan]]))
    assert np.array_equal(result.data, expected.data, equal_nan=True)


def test_grid_percentile():
    g = grid(np.array([[1, 2], [3, 4]]))
    result = g.percentile(50)
    expected = 2.5
    assert result == expected


def test_grid_slice():
    g = grid(np.array([[1, 2], [3, 4]]))
    result = g.slice(2)
    expected = grid(np.array([[1, 1], [2, 2]]))
    assert np.array_equal(result.data, expected.data)


def test_grid_replace():
    g = grid(np.array([[1, 2], [3, 4]]))
    result = g.replace(2, 20)
    expected = grid(np.array([[1, 20], [3, 4]]))
    assert np.array_equal(result.data, expected.data)


def test_grid_set_nan():
    g = grid(np.array([[1, 2], [3, 4]]))
    result = g.set_nan(2)
    expected = grid(np.array([[1, np.nan], [3, 4]]))
    assert np.array_equal(result.data, expected.data, equal_nan=True)


def test_grid_value():
    g = grid(np.array([[1, 2], [3, 4]]), extent=(0, 0, 2, 2))
    result = g.value(1, 1)
    expected = 4
    assert result == expected

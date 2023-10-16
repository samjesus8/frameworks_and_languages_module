from example import *
import pytest

def test_add():
    assert add(1, 2) == 3
    assert add(1, -2) == -1
    assert add(1000000000000000000, 2) == 1000000000000000002
    assert add(2, "random") == pytest.raises(ValueError)

def test_multiply():
    assert multiply(2, 2) == 4
    assert multiply(10, -10) == -100
    assert multiply(-6, -6) == 36

def test_divide():
    assert divide(2, 2) == 1
    assert divide(100, 2) == 50
    assert divide(1, 0) == pytest.raises(ZeroDivisionError)
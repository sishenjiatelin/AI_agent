import pytest
from FULLTEST.main import add1

def test_add1():
    assert add1(1, 2) == 3


def test_add2():

    assert add1(-1, 1) != 1


def test_add3():

    assert add1(0, 0) == 0.0

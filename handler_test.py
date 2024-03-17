import pytest

@pytest.mark.parametrize("num1,num2,expected", [(1, 2, 3), (4, 5, 9), (0, 1, 1)])
def test_addition(num1, num2, expected):
    assert num1 + num2 == expected
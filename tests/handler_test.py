from unittest.mock import patch

from handler import get_monthly_cost
from handler import get_report_string

mocked_value = [
    ("AWS Lambda", 100.0, 50.0),
    ("Amazon S3", 50.0, 25.0),
    ("Amazon EC2", 30.0, 15.0),
    ("Tax", 20.0, 10.0),
    ("Total", 200.0, 100.0),
]


@patch("handler.get_monthly_cost")
def test_get_monthly_cost(mock_get_monthly_cost):

    mock_get_monthly_cost.return_value = mocked_value

    monthly_cost = get_monthly_cost(2024, 3)
    assert isinstance(monthly_cost, list)
    assert len(monthly_cost) > 0

    head = monthly_cost[0]
    assert isinstance(head, tuple)
    assert len(head) == 3

    first = head[0]
    second = head[1]
    third = head[2]

    assert isinstance(first, str)
    assert isinstance(second, float)
    assert isinstance(third, float)


@patch("handler.get_monthly_cost")
def test_get_report_string(mock_get_monthly_cost):

    mock_get_monthly_cost.return_value = mocked_value

    monthly_cost = get_monthly_cost(2024, 3)
    report_string = get_report_string(monthly_cost)

    assert isinstance(report_string, str)
    lines = report_string.split("\n")
    assert len(lines) > 3

    last = lines[-1]
    assert last.startswith("Total:")

    last1 = lines[-2]
    assert last1.startswith("Tax:")

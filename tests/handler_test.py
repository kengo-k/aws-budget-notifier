from handler import get_monthly_cost
from handler import get_report_string

def test_get_monthly_cost():
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

def test_get_report_string():
    monthly_cost = get_monthly_cost(2024, 3)
    report_string = get_report_string(monthly_cost)

    assert isinstance(report_string, str)
    lines = report_string.split("\n")
    assert len(lines) > 3

    last = lines[-1]
    assert last.startswith("Total:")

    last1 = lines[-2]
    assert last1.startswith("Tax:")
    
import dpath

from handler import get_monthly_cost

def test_get_monthly_cost():
    monthly_cost = get_monthly_cost(2024, 3)
    assert isinstance(monthly_cost, dict)

    results = dpath.get(monthly_cost, 'ResultsByTime')
    assert isinstance(results, list)
    assert len(results) == 1

    total = dpath.get(results[0], 'Total/UnblendedCost/Amount')
    assert total is not None

from prometheus_client import (
    Gauge,
    Counter,
    Summary
)


test_gauge = Gauge(
    'observability_test_gauge',
    'Test Observability Gauge'
)

test_counter = Counter(
    'observability_test_counter',
    'Test Observability Counter'
)

test_summary = Summary(
    'observability_test_summary',
    'Test Observability Summary'
)

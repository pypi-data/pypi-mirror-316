import pytest
from unittest.mock import patch
from src.metrics.cpu import get_cpu_usage, get_per_core_usage

def test_get_cpu_usage():
    with patch('psutil.cpu_percent', return_value=55.5) as mock_cpu:
        usage = get_cpu_usage(interval=0.1)
        mock_cpu.assert_called_once_with(interval=0.1)
        assert isinstance(usage, float)
        assert 0.0 <= usage <= 100.0
        assert usage == 55.5

def test_get_per_core_usage():
    mock_usage = [30.0, 45.5, 60.0, 75.5]
    with patch('psutil.cpu_percent', return_value=mock_usage) as mock_cpu:
        usage = get_per_core_usage(interval=0.1)
        mock_cpu.assert_called_once_with(interval=0.1, percpu=True)
        assert isinstance(usage, list)
        assert all(isinstance(core, float) for core in usage)
        assert usage == mock_usage
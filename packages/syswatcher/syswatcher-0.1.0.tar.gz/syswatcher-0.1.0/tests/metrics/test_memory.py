from src.metrics.memory import get_memory_usage

def test_get_memory_usage():
    usage_percent, used_memory, total_memory = get_memory_usage()
    
    # Check if the percentage is a float between 0 and 100
    assert isinstance(usage_percent, float)
    assert 0 <= usage_percent <= 100
    
    # Check if used_memory and total_memory are strings in the expected format
    assert isinstance(used_memory, str)
    assert isinstance(total_memory, str)
    assert "GB" in used_memory or "MB" in used_memory
    assert "GB" in total_memory or "MB" in total_memory

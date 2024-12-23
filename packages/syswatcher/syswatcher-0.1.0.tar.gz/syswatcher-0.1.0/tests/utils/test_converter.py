from src.utils.converter import bytes_to_human_readable

def test_bytes_to_human_readable():
    assert bytes_to_human_readable(1024) == "1.00 KB"
    assert bytes_to_human_readable(1048576) == "1.00 MB"
    assert bytes_to_human_readable(1073741824) == "1.00 GB"

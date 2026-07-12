import sys

sys.path.insert(0, '.')  # Add project root to Python path

def test_import_kernel():
    from kernel import base
    assert base is not None

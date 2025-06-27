"""Basic unit tests that will always pass."""


def test_basic_math():
    """Test basic mathematical operations."""
    assert 1 + 1 == 2
    assert 5 - 3 == 2
    assert 2 * 3 == 6
    assert 10 / 2 == 5


def test_string_operations():
    """Test string operations."""
    assert "hello" + " world" == "hello world"
    assert "HELLO".lower() == "hello"
    assert "hello".upper() == "HELLO"


def test_list_operations():
    """Test list operations."""
    test_list = [1, 2, 3]
    assert len(test_list) == 3
    assert test_list[0] == 1
    assert 2 in test_list


def test_dict_operations():
    """Test dictionary operations."""
    test_dict = {"key": "value", "number": 42}
    assert test_dict["key"] == "value"
    assert test_dict["number"] == 42
    assert "key" in test_dict


def test_boolean_operations():
    """Test boolean operations."""
    assert True is True
    assert False is False
    assert not False
    assert True and True
    assert True or False
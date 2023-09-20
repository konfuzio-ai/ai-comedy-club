# Use pytest to test for the following test cases:
# 1. tell_joke() -> str
# 2. rate_joke() -> int[1-10]
import pytest
from joke_bot import Bot


def test_tell_joke_str():
    """Test Case 1: Does the function return a string"""
    jester = Bot()
    assert isinstance(jester.tell_joke(), str)

def test_rate_joke_float():
    """Test Case 2: Does the function return a float"""
    jester = Bot()
    assert isinstance(jester.rate_joke("What do you call a fish with no eyes? Fsh!"), float)

def test_rate_joke_range():
    """Test Case 3: Does the function return a float within a range of 1 to 10"""
    jester = Bot()
    assert 1.0 <= jester.rate_joke("What do you call a fish with no eyes? Fsh!") <= 10.0
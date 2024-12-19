from alicepackage.function import alice_add_positive, NonZeroOrNegativeNumber, NotListOfNumbers
import pytest

def test_alice_add_positive_happy_path(input_happy_path):
    results = alice_add_positive(input_happy_path)
    assert results == 6

def test_alice_add_positive_non_list(input_not_list):
    with pytest.raises(NotListOfNumbers) as e:
        alice_add_positive(input_not_list)
    assert str(e.value) == "Input must be a list of numbers."

def test_alice_add_positive_negative_number(input_negative):
    with pytest.raises(NonZeroOrNegativeNumber) as e:
        alice_add_positive(input_negative)
    assert str(e.value) == "All numbers must be positive."

def test_alice_add_positive_zero_number(input_zero):
    with pytest.raises(NonZeroOrNegativeNumber) as e:
        alice_add_positive(input_zero)
    assert str(e.value) == "All numbers must be positive."

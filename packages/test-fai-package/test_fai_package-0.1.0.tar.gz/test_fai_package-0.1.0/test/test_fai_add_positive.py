from testfaipackage.functions import fai_add_positive,NonZeroOrNegativeNumber,NotListofNumbers
import pytest

def test_fai_add_positive_happy_path(input_happy_path):
    results = fai_add_positive(input_happy_path)
    assert results == 6

def test_fai_add_positive_non_list(input_non_list):
    with pytest.raises(NotListofNumbers) as e:
        fai_add_positive(input_non_list)
    assert str(e.value) == "Input must be a list of number"

def test_fai_add_positive_negative_number(input_negative):
    with pytest.raises(NonZeroOrNegativeNumber) as e:
        fai_add_positive(input_negative)
    assert str(e.value) == "All numbers must be positive"

def test_fai_add_positive_zero(input_zero):
    with pytest.raises(NonZeroOrNegativeNumber) as e:
        fai_add_positive(input_zero)
    assert str(e.value) == "All numbers must be positive"
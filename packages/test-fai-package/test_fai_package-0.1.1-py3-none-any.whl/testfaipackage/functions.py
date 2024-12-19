from typing import List
import numpy as np

def fai_sum(numbers: List[float])->float:
    return sum(numbers) 

class NonZeroOrNegativeNumber(ValueError):
    pass

class NotListofNumbers(TypeError):
    pass

def fai_add_positive(numbers: List[float])->float:
    if not isinstance(numbers,list):
        raise NotListofNumbers("Input must be a list of number")
    if sum([1 for number in numbers if number<=0])>0:
        raise NonZeroOrNegativeNumber("All numbers must be positive")
    return sum(numbers)

def sub1(a:int)->int:
    # validate inputs
    return a

def sub2(b:int)->int:
    # validate inputs
    return b

def main(a:int,b:int)->int:
    # validate inputs
    return sub1(1) + sub2(2)
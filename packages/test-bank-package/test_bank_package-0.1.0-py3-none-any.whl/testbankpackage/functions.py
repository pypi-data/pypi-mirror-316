from typing import List
# import numpy as np

def bank_sum(numbers: List[float])->float:
    return sum(numbers)

class NonZeroOrNegativeNumber(ValueError):
    pass

class NotListOfNumbers(TypeError):
    pass

def bank_add_positive(numbers: List[float])->float:
    if not isinstance(numbers, list):
        raise NotListOfNumbers("Input must be a list of numbers.")
    if sum([1 for number in numbers if number<=0])>0:
        raise NonZeroOrNegativeNumber("All numbers must be positive.")
    return sum(numbers)

def sub1(a:int)->int:
    # validate input
    return a

def sub2(b:int)->int:
    # validate input
    return b

def main(a:int, b:int)->int:
    # validate inputs
    return sub1(a) + sub2(b)
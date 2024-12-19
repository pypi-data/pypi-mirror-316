from typing import List

def ter_sum(numbers: List[float])->float:
    return sum(numbers)

class NonZeroOrNegativeNumber(ValueError):
    pass

class NotListOfNumbers(TypeError):
    pass

def ter_add_positive(numbers: List[float])->float:
    if not isinstance(numbers, list):
        raise NotListOfNumbers("Input must be a list of numbers.")
    if sum([1 for number in numbers if number<=0])>0:
        raise NonZeroOrNegativeNumber("All numbers must be positive.")
    return sum(numbers)